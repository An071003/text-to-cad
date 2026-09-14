# Rule: Sử Dụng CI/CD Sandbox Thay Vì Mở Terminal Thủ Công (Use CI/CD Sandbox Runner)

## Bối Cảnh & Mục Đích (Context & Purpose)
Dự án đồng hồ cơ **text-to-cad** có cấu trúc gồm nhiều phân hệ CAD (21+ subsystems), các thư viện dùng chung, và kiểm định hình học chuyên sâu qua nhân OpenCASCADE (`BRepCheck_Analyzer`). Việc mở terminal chạy các lệnh nhỏ lẻ thủ công (ad-hoc commands) dễ gây lỗi mã hóa console (cp1252 vs UTF-8), tốn thời gian và thiếu tính toàn diện.

Do đó, toàn bộ quy trình kiểm tra, biên dịch, thẩm định và báo cáo phải được điều phối thông qua **CI/CD Sandbox Runner** đã được chuẩn hóa.

---

## Quy Tắc Bắt Buộc (Mandatory Guidelines)

### 1. Bắt Buộc Dùng Sandbox Thay Vì Chạy Lệnh Rời Rạc
- **KHÔNG** chạy thủ công từng lệnh biên dịch riêng lẻ nếu không cần cô lập lỗi.
- **BẮT BUỘC** sử dụng bộ Sandbox Runner hoặc bộ kiểm thử `pytest` tập trung:
  - **PowerShell**:
    ```powershell
    .\scripts\sandbox_ci.ps1
    ```
  - **Windows CMD**:
    ```cmd
    scripts\sandbox_ci.bat
    ```
  - **Linux / macOS (Bash)**:
    ```bash
    ./scripts/sandbox_ci.sh
    ```
  - **Python runner trực tiếp**:
    ```bash
    python scripts/ci_sandbox.py
    ```
  - **Bộ kiểm thử tự động pytest**:
    ```bash
    python -m pytest tests/
    ```

---

### 2. Các Giai Đoạn Sandbox Tự Động Thực Hiện
Khi chạy sandbox runner, hệ thống tự động hoàn thành 6 giai đoạn nghiêm ngặt:
1. **Stage 1 (Preflight)**: Kiểm tra môi trường Python 3.12, OpenCASCADE (OCP), build123d, cadgen CLI, dọn dẹp cache `tmp/`.
2. **Stage 2 (Syntax Audit)**: Quét AST cú pháp, encoding UTF-8 trên toàn bộ thư mục `src/`.
3. **Stage 3 (CAD Compilations)**: Biên dịch đồng bộ các mô hình và cụm lắp ráp sang file `.step`.
4. **Stage 4 (Geometric Validation)**: Kiểm định 0 lỗi tự giao cắt (self-intersection) qua OpenCASCADE.
5. **Stage 5 (Horological Constraints)**: Kiểm tra tần số dao động (18,000 vph hoặc 28,800 vph), tỷ số truyền bánh răng và kích thước caliber $\varnothing 36.60\text{ mm}$ / vỏ $\varnothing 40.0\text{ mm}$.
6. **Stage 6 (Reporting)**: Xuất báo cáo tự động ra `CI_REPORT.md` và `tmp/ci_report.json`.

---

### 3. Quy Trình Làm Việc Khi Thay Đổi Mã Nguồn
1. Thực hiện chỉnh sửa mã nguồn trong `src/` hoặc `tests/`.
2. Kích hoạt sandbox runner:
   `python scripts/ci_sandbox.py` (hoặc `.\scripts\sandbox_ci.ps1`).
3. Đọc kết quả trong terminal hoặc xem báo cáo tại [CI_REPORT.md](file:///c:/Users/ADMIN/Downloads/TEST/CLOCK/CI_REPORT.md).
4. Chỉ commit và đẩy lên git khi sandbox trả về mã trạng thái thành công: `[SUCCESS] CI/CD SANDBOX PIPELINE PASSED!`.
