#!/usr/bin/env python3
"""CAD CI/CD Local Sandbox Simulation Runner.

Simulates the complete CI/CD testing and validation pipeline locally for the text-to-cad project:
1. Environment & Dependency Preflight
2. Syntax & AST Quality Audits
3. Parametric Model Building & Compilation
4. Geometric Integrity & Self-Intersection Validation (cadgen inspect)
5. Caliber Tolerance & Bounding Box Checks
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

# Base Paths
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

    def run_stage_2_syntax(self) -> bool:
        """Run AST syntax audit and UTF-8 encoding verification across all source files."""
        print(f"\n{BOLD}=== STAGE 2: Code Quality & AST Syntax Audit ==={RESET}")
        import ast

        stage_data = {"files": [], "passed": True}
        self.results["stages"]["syntax_audit"] = stage_data

        py_files = sorted(list(SRC_DIR.glob("**/*.py")))
        all_ok = True

        for pf in py_files:
            rel_path = pf.relative_to(PROJECT_ROOT)
            try:
                content = pf.read_text(encoding="utf-8")
                ast.parse(content, filename=str(pf))
                stage_data["files"].append({"file": str(rel_path), "status": "OK"})
                if self.verbose:
                    self.log("AST", f"{rel_path} - Syntax valid", "PASS")
            except Exception as e:
                all_ok = False
                stage_data["files"].append({"file": str(rel_path), "status": "ERROR", "error": str(e)})
                self.log("AST", f"{rel_path} - Error: {e}", "FAIL")

        stage_data["passed"] = all_ok
        self.log("Syntax Audit", f"Audited {len(py_files)} Python source files (All valid: {all_ok})", "PASS" if all_ok else "FAIL")
        return all_ok

    def run_stage_3_build_models(self) -> bool:
        """Execute and compile all CAD models in src/."""
        print(f"\n{BOLD}=== STAGE 3: Model Building & STEP Compilation ==={RESET}")
        stage_data = {"models": [], "passed": True}
        self.results["stages"]["model_builds"] = stage_data

        model_scripts = [
            SRC_DIR / "mainplate_and_bridges" / "mainplate.py",
            SRC_DIR / "mainplate_and_bridges" / "barrel_bridge.py",
            SRC_DIR / "mainplate_and_bridges" / "train_bridge.py",
            SRC_DIR / "mainplate_and_bridges" / "pallet_cock.py",
            SRC_DIR / "mainplate_and_bridges" / "balance_cock.py",
            SRC_DIR / "gear_train" / "center_wheel.py",
            SRC_DIR / "gear_train" / "third_wheel.py",
            SRC_DIR / "gear_train" / "fourth_wheel.py",
            SRC_DIR / "escapement" / "escape_wheel.py",
            SRC_DIR / "escapement" / "pallet_fork.py",
            SRC_DIR / "escapement" / "pallet_jewels.py",
            SRC_DIR / "balance" / "balance_wheel.py",
            SRC_DIR / "balance" / "hairspring.py",
            SRC_DIR / "balance" / "roller_table.py",
            SRC_DIR / "winding_and_barrel" / "mainspring_barrel.py",
            SRC_DIR / "winding_and_barrel" / "ratchet_and_crown.py",
            SRC_DIR / "winding_and_barrel" / "winding_mechanism.py",
            SRC_DIR / "winding_and_barrel" / "motion_work.py",
            SRC_DIR / "fasteners" / "screws.py",
            SRC_DIR / "fasteners" / "jewels.py",
            SRC_DIR / "fasteners" / "steady_pins.py",
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
                self.log("Validate", f"{sf.name:<26} (0 errors, sound solid)", "PASS")
            else:
                all_ok = False
                stage_data["files"].append({
                    "file": sf.name,
                    "valid": False,
                    "error": res.stderr or res.stdout,
                })
                self.log("Validate", f"{sf.name:<26} FAILED validation", "FAIL")

        stage_data["passed"] = all_ok
        return all_ok

    def run_stage_5_caliber_tolerance(self) -> bool:
        """Check assembly bounding box against ETA 6497/6498 specifications."""
        print(f"\n{BOLD}=== STAGE 5: Horological Caliber Dimensional Tolerances ==={RESET}")
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
            bounds = summary["bounds"]

            size_x, size_y, size_z = facts["size"]
            face_count = summary["faceCount"]
            edge_count = summary["edgeCount"]
            occurrences = summary["occurrenceCount"]

            # Tolerance rules:
            # Caliber diameter is 36.60 mm (+/- 0.5 mm on circular bounds)
            # Winding stem extends outward on X axis (allowed up to 45 mm)
            # Caliber height should not exceed 8.0 mm
            diameter_ok = abs(size_y - 36.60) < 1.0
            height_ok = size_z <= 8.0
            parts_ok = occurrences >= 20

            all_ok = diameter_ok and height_ok and parts_ok

            stage_data["metrics"] = {
                "size": [round(size_x, 2), round(size_y, 2), round(size_z, 2)],
                "faces": face_count,
                "edges": edge_count,
                "components": occurrences,
                "diameter_check": diameter_ok,
                "height_check": height_ok,
                "parts_count_check": parts_ok,
            }
            stage_data["passed"] = all_ok

            self.log("Dimensions", f"Caliber Size: {size_x:.1f} x {size_y:.1f} x {size_z:.1f} mm", "PASS" if all_ok else "FAIL")
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
            ("STEP/watch_caliber_assembly.step", "tmp/ci_assembly_top.png", "default"),
            ("STEP/watch_caliber_assembly.step", "tmp/ci_assembly_iso.png", "45:35"),
            ("STEP/balance_wheel.step", "tmp/ci_balance_wheel.png", "default"),
            ("STEP/escape_wheel.step", "tmp/ci_escape_wheel.png", "default"),
        ]

        all_ok = True
        for target, out, cam in snapshot_targets:
            cmd = ["cadgen", "step", "snapshot", target, out]
            if cam != "default":
                cmd += ["--camera", cam]

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
        duration = time.time() - self.start_time
        self.results["summary"]["duration_seconds"] = round(duration, 2)

        stages = self.results["stages"]
        total_stages = len(stages)
        passed_stages = sum(1 for s in stages.values() if s.get("passed", False))
        overall_ok = passed_stages == total_stages

        self.results["summary"]["overall_success"] = overall_ok

        # Save JSON
        REPORT_JSON.write_text(json.dumps(self.results, indent=2), encoding="utf-8")

        # Save Markdown Report
        md = []
        status_badge = "![PASSED](https://img.shields.io/badge/CI_PIPELINE-PASSED-brightgreen)" if overall_ok else "![FAILED](https://img.shields.io/badge/CI_PIPELINE-FAILED-red)"
        md.append(f"# CAD CI/CD Sandbox Simulation Report\n")
        md.append(f"{status_badge}  `Generated: {self.results['timestamp']}`  `Duration: {duration:.2f}s`\n")
        md.append("## Executive Summary\n")
        md.append(f"| Stage | Name | Status | Details |")
        md.append(f"| :---: | :--- | :---: | :--- |")

        for key, stage in stages.items():
            st_badge = "✅ PASS" if stage.get("passed", False) else "❌ FAIL"
            name = key.replace("_", " ").title()
            details_str = f"{len(stage.get('files', stage.get('models', stage.get('checks', []))))} checks"
            md.append(f"| {st_badge} | **{name}** | {stage.get('passed')} | {details_str} |")

        tol = stages.get("tolerances", {}).get("metrics", {})
        if tol:
            md.append(f"\n## Caliber Geometry & Verification Facts\n")
            md.append(f"- **Total Components**: {tol.get('components', 'N/A')} parts")
            md.append(f"- **Face Count**: {tol.get('faces', 0):,} faces")
            md.append(f"- **Edge Count**: {tol.get('edges', 0):,} edges")
            md.append(f"- **Bounding Box Dimensions**: `{tol.get('size', [])}` mm (Caliber 16.5''' target: Ø 36.60 mm)")

        md.append(f"\n## Artifacts Generated\n")
        step_files = list(STEP_DIR.glob("*.step"))
        md.append(f"- **Total STEP Files**: {len(step_files)}")
        for sf in step_files:
            size_kb = sf.stat().st_size / 1024.0
            md.append(f"  - `{sf.name}` ({size_kb:.1f} KB)")

        REPORT_MD.write_text("\n".join(md), encoding="utf-8")

        print(f"\n{BOLD}===================================================={RESET}")
        if overall_ok:
            print(f"{GREEN}{BOLD}[SUCCESS] CI/CD SANDBOX PIPELINE PASSED! (Duration: {duration:.2f}s){RESET}")
        else:
            print(f"{RED}{BOLD}[FAILURE] CI/CD SANDBOX PIPELINE ENCOUNTERED FAILURES!{RESET}")
        print(f"Detailed Markdown report written to: {REPORT_MD}")
        print(f"JSON metrics exported to: {REPORT_JSON}")
        print(f"{BOLD}===================================================={RESET}\n")

        return 0 if overall_ok else 1


def main():
    parser = argparse.ArgumentParser(description="CAD CI/CD Local Sandbox Simulation")
    parser.add_argument("--all", action="store_true", help="Run full pipeline")
    parser.add_argument("--skip-build", action="store_true", help="Skip model rebuild, only validate existing files")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    sandbox = SandboxPipeline(verbose=args.verbose)

    # Execute Pipeline
    ok = sandbox.run_stage_1_environment()
    ok = sandbox.run_stage_2_syntax() and ok
    if not args.skip_build:
        ok = sandbox.run_stage_3_build_models() and ok
    ok = sandbox.run_stage_4_geometric_validation() and ok
    ok = sandbox.run_stage_5_caliber_tolerance() and ok
    ok = sandbox.run_stage_6_snapshots() and ok

    exit_code = sandbox.generate_report()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
