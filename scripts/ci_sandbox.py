#!/usr/bin/env python3
"""CAD CI/CD Local Sandbox Simulation Runner for Complete Mechanical Wristwatch.

Simulates the complete CI/CD testing and validation pipeline locally for the text-to-cad project:
1. Environment & Dependency Preflight
2. Syntax & AST Quality Audits
3. Parametric Model Building & Compilation (28 models: 22 movement + 6 exterior)
4. Geometric Integrity & Self-Intersection Validation (cadgen inspect validate)
5. Horological & Watch Case Dimensional Tolerances
6. Snapshot Visual Rendering Verification
7. Structured Artifact & Summary Report Generation
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

# Force UTF-8 on Windows stdout/stderr
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
STEP_DIR = PROJECT_ROOT / "STEP"
TMP_DIR = PROJECT_ROOT / "tmp"
REPORT_JSON = TMP_DIR / "ci_report.json"
REPORT_MD = PROJECT_ROOT / "CI_REPORT.md"

# ANSI Colors for Terminal
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Silent subprocess execution on Windows to suppress console/terminal popups
WIN32_FLAGS = {"creationflags": subprocess.CREATE_NO_WINDOW} if sys.platform == "win32" else {}

# Disable cadgen daemon to prevent it from spawning background warm workers that open console windows
os.environ["CADGEN_DAEMON"] = "0"


class SandboxPipeline:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "stages": {},
            "summary": {"total_tests": 0, "passed": 0, "failed": 0, "duration_seconds": 0.0},
        }
        self.start_time = time.time()
        TMP_DIR.mkdir(parents=True, exist_ok=True)
        STEP_DIR.mkdir(parents=True, exist_ok=True)

    def log(self, stage: str, message: str, status: str = "INFO"):
        prefix = {
            "INFO": f"{CYAN}[INFO]{RESET}",
            "PASS": f"{GREEN}[PASS]{RESET}",
            "FAIL": f"{RED}[FAIL]{RESET}",
            "WARN": f"{YELLOW}[WARN]{RESET}",
        }.get(status, f"[{status}]")
        print(f"{prefix} {BOLD}{stage}:{RESET} {message}")

    def run_stage_1_environment(self) -> bool:
        """Verify Python, build123d, cadgen, and OpenCASCADE dependencies."""
        print(f"\n{BOLD}=== STAGE 1: Environment & Dependency Preflight ==={RESET}")
        stage_data = {"checks": [], "passed": True}
        self.results["stages"]["environment"] = stage_data

        # 1. Python Version
        py_ver = sys.version_info
        py_ok = py_ver >= (3, 11)
        stage_data["checks"].append({
            "name": "Python Version >= 3.11",
            "passed": py_ok,
            "details": f"{py_ver.major}.{py_ver.minor}.{py_ver.micro}",
        })
        self.log("Python", f"Version {py_ver.major}.{py_ver.minor}.{py_ver.micro}", "PASS" if py_ok else "FAIL")

        # 2. build123d Import
        try:
            import build123d
            b123d_ver = getattr(build123d, "__version__", "installed")
            stage_data["checks"].append({"name": "build123d", "passed": True, "details": b123d_ver})
            self.log("build123d", f"Available ({b123d_ver})", "PASS")
        except Exception as e:
            stage_data["checks"].append({"name": "build123d", "passed": False, "details": str(e)})
            self.log("build123d", f"Failed: {e}", "FAIL")
            stage_data["passed"] = False

        # 3. cadgen CLI Tool
        try:
            res = subprocess.run(["cadgen", "--version"], capture_output=True, text=True, check=True, **WIN32_FLAGS)
            cadgen_ver = res.stdout.strip()
            stage_data["checks"].append({"name": "cadgen CLI", "passed": True, "details": cadgen_ver})
            self.log("cadgen CLI", f"Available ({cadgen_ver})", "PASS")
        except Exception as e:
            stage_data["checks"].append({"name": "cadgen CLI", "passed": False, "details": str(e)})
            self.log("cadgen CLI", f"Failed: {e}", "FAIL")
            stage_data["passed"] = False

        # 4. Playwright Headless Browser
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                browser.close()
            stage_data["checks"].append({"name": "Playwright Chromium", "passed": True, "details": "Launch successful"})
            self.log("Playwright", "Chromium Headless launch OK", "PASS")
        except Exception as e:
            stage_data["checks"].append({"name": "Playwright Chromium", "passed": False, "details": str(e)})
            self.log("Playwright", f"Browser test failed (snapshots may be limited): {e}", "WARN")

        return stage_data["passed"]

    def run_stage_2_ast_audit(self) -> bool:
        """Audit Python syntax across all src/ and tests/ modules."""
        print(f"\n{BOLD}=== STAGE 2: Static AST Code & Syntax Audit ==={RESET}")
        import ast

        stage_data = {"audited_files": 0, "errors": [], "passed": True}
        self.results["stages"]["ast_audit"] = stage_data

        py_files = list(SRC_DIR.glob("**/*.py")) + list((PROJECT_ROOT / "tests").glob("**/*.py"))
        has_error = False

        for py_file in py_files:
            rel = py_file.relative_to(PROJECT_ROOT)
            try:
                content = py_file.read_text(encoding="utf-8")
                ast.parse(content, filename=str(rel))
            except Exception as e:
                has_error = True
                stage_data["errors"].append({"file": str(rel), "error": str(e)})
                self.log("AST", f"{rel}: Syntax Error -> {e}", "FAIL")

        stage_data["audited_files"] = len(py_files)
        stage_data["passed"] = not has_error
        if not has_error:
            self.log("AST", f"Successfully audited {len(py_files)} Python source files (0 errors)", "PASS")
        return not has_error

    def run_stage_3_build_models(self) -> bool:
        """Execute and compile all 28 parametric CAD models into STEP files."""
        print(f"\n{BOLD}=== STAGE 3: Parametric CAD Compilation (28 Models) ==={RESET}")
        stage_data = {"models": [], "passed": True}
        self.results["stages"]["build"] = stage_data

        model_scripts = [
            # 1. Mainplate & Bridges
            SRC_DIR / "mainplate_and_bridges" / "mainplate.py",
            SRC_DIR / "mainplate_and_bridges" / "barrel_bridge.py",
            SRC_DIR / "mainplate_and_bridges" / "train_bridge.py",
            SRC_DIR / "mainplate_and_bridges" / "pallet_cock.py",
            SRC_DIR / "mainplate_and_bridges" / "balance_cock.py",
            # 2. Gear Train
            SRC_DIR / "gear_train" / "center_wheel.py",
            SRC_DIR / "gear_train" / "third_wheel.py",
            SRC_DIR / "gear_train" / "fourth_wheel.py",
            # 3. Escapement & Regulating Organ
            SRC_DIR / "escapement" / "escape_wheel.py",
            SRC_DIR / "escapement" / "pallet_fork.py",
            SRC_DIR / "escapement" / "pallet_jewels.py",
            SRC_DIR / "balance" / "balance_wheel.py",
            SRC_DIR / "balance" / "hairspring.py",
            SRC_DIR / "balance" / "roller_table.py",
            # 4. Power & Keyless Works
            SRC_DIR / "winding_and_barrel" / "mainspring_barrel.py",
            SRC_DIR / "winding_and_barrel" / "ratchet_and_crown.py",
            SRC_DIR / "winding_and_barrel" / "winding_mechanism.py",
            SRC_DIR / "winding_and_barrel" / "motion_work.py",
            # 5. Fasteners & Jewels
            SRC_DIR / "fasteners" / "screws.py",
            SRC_DIR / "fasteners" / "jewels.py",
            SRC_DIR / "fasteners" / "steady_pins.py",
            # 6. Watch Exterior Components
            SRC_DIR / "watch_exterior" / "caseband.py",
            SRC_DIR / "watch_exterior" / "bezel.py",
            SRC_DIR / "watch_exterior" / "dial.py",
            SRC_DIR / "watch_exterior" / "hands.py",
            SRC_DIR / "watch_exterior" / "crown.py",
            SRC_DIR / "watch_exterior" / "caseback.py",
            # 7. Complete Top-Level Assembly
            SRC_DIR / "assembly.py",
        ]

        all_ok = True
        for ms in model_scripts:
            rel = ms.relative_to(PROJECT_ROOT)
            t0 = time.time()
            res = subprocess.run([sys.executable, str(ms)], cwd=str(PROJECT_ROOT), capture_output=True, text=True, **WIN32_FLAGS)
            elapsed = time.time() - t0

            if res.returncode == 0:
                stage_data["models"].append({"script": str(rel), "status": "SUCCESS", "elapsed_s": round(elapsed, 2)})
                self.log("Build", f"{ms.stem:<24} in {elapsed:.2f}s", "PASS")
            else:
                all_ok = False
                stage_data["models"].append({
                    "script": str(rel),
                    "status": "FAILED",
                    "elapsed_s": round(elapsed, 2),
                    "error": res.stderr.strip() or res.stdout.strip(),
                })
                self.log("Build", f"{ms.stem:<24} FAILED ({res.stderr[:80]}...)", "FAIL")

        stage_data["passed"] = all_ok
        return all_ok

    def run_stage_4_geometric_validation(self) -> bool:
        """Run cadgen step inspect validate against all generated STEP documents."""
        print(f"\n{BOLD}=== STAGE 4: Geometric Soundness & Self-Intersection Validation ==={RESET}")
        stage_data = {"files": [], "passed": True}
        self.results["stages"]["geometric_validation"] = stage_data

        step_files = sorted(list(STEP_DIR.glob("*.step")))
        all_ok = True

        for sf in step_files:
            rel = sf.relative_to(PROJECT_ROOT)
            cmd = ["cadgen", "step", "inspect", "validate", str(rel)]
            res = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True, **WIN32_FLAGS)

            is_valid = False
            details = {}
            if res.returncode == 0:
                try:
                    data = json.loads(res.stdout)
                    if data.get("ok") is True and data.get("failureCount", 0) == 0:
                        is_valid = True
                        details = data
                except Exception:
                    pass

            if is_valid:
                stage_data["files"].append({
                    "file": sf.name,
                    "valid": True,
                    "occurrences": details.get("occurrenceCount", 1),
                })
                self.log("Validate", f"{sf.name:<28} (0 errors, sound solid)", "PASS")
            else:
                all_ok = False
                stage_data["files"].append({
                    "file": sf.name,
                    "valid": False,
                    "error": res.stderr or res.stdout,
                })
                self.log("Validate", f"{sf.name:<28} FAILED validation", "FAIL")

        stage_data["passed"] = all_ok
        return all_ok

    def run_stage_5_caliber_tolerance(self) -> bool:
        """Check assembly bounding box against ETA 6497 and 42 mm watch specifications."""
        print(f"\n{BOLD}=== STAGE 5: Watch Caliber & Case Dimensional Tolerances ==={RESET}")
        stage_data = {"metrics": {}, "passed": True}
        self.results["stages"]["tolerances"] = stage_data

        assembly_step = STEP_DIR / "watch_caliber_assembly.step"
        if not assembly_step.exists():
            self.log("Tolerance", "Assembly STEP file not found", "FAIL")
            stage_data["passed"] = False
            return False

        cmd = ["cadgen", "step", "inspect", "refs", "STEP/watch_caliber_assembly.step", "--facts"]
        res = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True, **WIN32_FLAGS)

        try:
            data = json.loads(res.stdout)
            token = data["tokens"][0]
            summary = token["summary"]
            facts = token["entryFacts"]

            size_x, size_y, size_z = facts["size"]
            face_count = summary["faceCount"]
            edge_count = summary["edgeCount"]
            occurrences = summary["occurrenceCount"]

            # Tolerance rules:
            # Lug-to-lug span along Y axis is ~49.8 mm (allowed between 46.0 and 52.0 mm)
            # Total watch thickness along Z should not exceed 12.50 mm
            # Watch assembly must contain at least 25 components
            lug_to_lug_ok = 46.0 <= size_y <= 52.0
            height_ok = size_z <= 12.50
            parts_ok = occurrences >= 25

            all_ok = lug_to_lug_ok and height_ok and parts_ok

            stage_data["metrics"] = {
                "size": [round(size_x, 2), round(size_y, 2), round(size_z, 2)],
                "faces": face_count,
                "edges": edge_count,
                "components": occurrences,
                "lug_to_lug_check": lug_to_lug_ok,
                "height_check": height_ok,
                "parts_count_check": parts_ok,
            }
            stage_data["passed"] = all_ok

            self.log("Dimensions", f"Watch Size: {size_x:.1f} x {size_y:.1f} x {size_z:.1f} mm", "PASS" if all_ok else "FAIL")
            self.log("Complexity", f"Faces: {face_count:,} | Edges: {edge_count:,} | Components: {occurrences}", "INFO")
            return all_ok
        except Exception as e:
            self.log("Tolerance", f"Failed to parse facts: {e}", "FAIL")
            stage_data["passed"] = False
            return False

    def run_stage_6_snapshots(self) -> bool:
        """Generate verification snapshots using headless browser."""
        print(f"\n{BOLD}=== STAGE 6: Visual Rendering & Snapshot Tests ==={RESET}")
        stage_data = {"renders": [], "passed": True}
        self.results["stages"]["snapshots"] = stage_data

        snapshot_targets = [
            ("STEP/watch_caliber_assembly.step", "tmp/watch_isometric.png", ["--camera", "45:35"]),
            ("STEP/watch_caliber_assembly.step", "tmp/watch_front_dial.png", ["--camera", "0:-89"]),
            ("STEP/watch_caliber_assembly.step", "tmp/watch_back_sapphire.png", ["--camera", "0:89"]),
            ("STEP/dial.step", "tmp/watch_dial_detail.png", []),
            ("STEP/caseband.step", "tmp/watch_caseband_detail.png", ["--camera", "45:35"]),
            ("STEP/watch_caliber_assembly.step", "tmp/watch_running_t0.png", ["--animation", "running_real_time", "--time", "0.0"]),
            ("STEP/watch_caliber_assembly.step", "tmp/watch_running_t02.png", ["--animation", "running_real_time", "--time", "0.2"]),
            ("STEP/watch_caliber_assembly.step", "tmp/watch_running_t2.png", ["--animation", "running_real_time", "--time", "2.0"]),
        ]

        all_ok = True
        for target, out, extra_args in snapshot_targets:
            cmd = ["cadgen", "step", "snapshot", target, out] + extra_args

            t0 = time.time()
            res = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True, **WIN32_FLAGS)
            elapsed = time.time() - t0
            out_file = PROJECT_ROOT / out

            if res.returncode == 0 and out_file.exists():
                size_kb = out_file.stat().st_size / 1024.0
                stage_data["renders"].append({"target": target, "output": out, "size_kb": round(size_kb, 1), "elapsed_s": round(elapsed, 2)})
                self.log("Snapshot", f"{out} ({size_kb:.1f} KB in {elapsed:.2f}s)", "PASS")
            else:
                all_ok = False
                stage_data["renders"].append({"target": target, "output": out, "error": res.stderr})
                self.log("Snapshot", f"{out} failed", "FAIL")

        stage_data["passed"] = all_ok
        return all_ok

    def generate_report(self):
        """Generate both JSON and Markdown CI reports."""
        duration = round(time.time() - self.start_time, 2)
        self.results["summary"]["duration_seconds"] = duration

        # Count passes/fails
        total = 0
        passed = 0
        for st_name, st_data in self.results["stages"].items():
            total += 1
            if st_data.get("passed", False):
                passed += 1

        self.results["summary"]["total_stages"] = total
        self.results["summary"]["passed_stages"] = passed
        self.results["summary"]["failed_stages"] = total - passed

        # Save JSON
        with open(REPORT_JSON, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2)

        # Save Markdown Report
        md = []
        md.append("# CAD CI/CD Sandbox Simulation Report")
        md.append(f"\n**Timestamp**: `{self.results['timestamp']}`  ")
        md.append(f"**Total Duration**: `{duration}s`  ")
        status_badge = "PASSED" if (total == passed) else "FAILED"
        md.append(f"**Overall Status**: `{status_badge}` ({passed}/{total} stages passed)\n")

        md.append("## 1. Pipeline Execution Stages\n")
        md.append("| Stage | Description | Status |")
        md.append("| :--- | :--- | :--- |")
        descriptions = {
            "environment": "Preflight Environment & Dependencies",
            "ast_audit": "Static AST Syntax Check",
            "build": "Parametric Model Compilation (28 models)",
            "geometric_validation": "OpenCASCADE BRepCheck Integrity",
            "tolerances": "42 mm Watch Case & Caliber Bounding Box Checks",
            "snapshots": "Visual Rendering & Animation Snapshots",
        }
        for st_name, st_data in self.results["stages"].items():
            desc = descriptions.get(st_name, st_name)
            st_str = "PASS" if st_data.get("passed") else "FAIL"
            md.append(f"| `{st_name}` | {desc} | **{st_str}** |")

        md.append("\n## 2. Watch Caliber & Case Specifications\n")
        m = self.results["stages"].get("tolerances", {}).get("metrics", {})
        if m:
            md.append(f"- **Dimensions**: `{m.get('size', [])}` mm (X x Y x Z)")
            md.append(f"- **Topology Complexity**: `{m.get('faces', 0):,}` faces, `{m.get('edges', 0):,}` edges")
            md.append(f"- **Total Components**: `{m.get('components', 0)}` occurrences in assembly")
            md.append(f"- **Lug-to-Lug Check**: `{'PASSED' if m.get('lug_to_lug_check') else 'FAILED'}`")
            md.append(f"- **Thickness Check (<= 12.5mm)**: `{'PASSED' if m.get('height_check') else 'FAILED'}`")

        with open(REPORT_MD, "w", encoding="utf-8") as f:
            f.write("\n".join(md) + "\n")

        print(f"\n{BOLD}=== CI/CD Report Generated ==={RESET}")
        self.log("Report", f"Markdown saved to {REPORT_MD.relative_to(PROJECT_ROOT)}", "PASS")
        self.log("Report", f"JSON data saved to {REPORT_JSON.relative_to(PROJECT_ROOT)}", "PASS")


def main():
    parser = argparse.ArgumentParser(description="Run local CAD CI/CD Sandbox Simulation.")
    parser.add_argument("--all", action="store_true", help="Run all pipeline stages.")
    parser.add_argument("--stage", type=int, choices=[1, 2, 3, 4, 5, 6], help="Run a specific stage.")
    args = parser.parse_args()

    pipeline = SandboxPipeline()
    success = True

    if args.all or args.stage is None:
        stages = [
            pipeline.run_stage_1_environment,
            pipeline.run_stage_2_ast_audit,
            pipeline.run_stage_3_build_models,
            pipeline.run_stage_4_geometric_validation,
            pipeline.run_stage_5_caliber_tolerance,
            pipeline.run_stage_6_snapshots,
        ]
        for stage_fn in stages:
            ok = stage_fn()
            if not ok:
                success = False
                break
    else:
        stage_map = {
            1: pipeline.run_stage_1_environment,
            2: pipeline.run_stage_2_ast_audit,
            3: pipeline.run_stage_3_build_models,
            4: pipeline.run_stage_4_geometric_validation,
            5: pipeline.run_stage_5_caliber_tolerance,
            6: pipeline.run_stage_6_snapshots,
        }
        success = stage_map[args.stage]()

    pipeline.generate_report()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
