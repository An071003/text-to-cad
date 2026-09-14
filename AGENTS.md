# Dự Án Đồng Hồ Cơ (Text-to-CAD Watch Project) - Quy Tắc Tác Vụ Agent

## Quy Tắc Điều Phối: Sử Dụng CI/CD Sandbox Thay Vì Mở Terminal Tự Do

### Chỉ thị bắt buộc (Mandatory Directive)
Mỗi khi cần kiểm tra cú pháp, biên dịch mô hình CAD, thẩm định hình học OpenCASCADE, hoặc kiểm tra tính toàn vẹn hệ thống:
- **KHÔNG** chạy các câu lệnh terminal phân mảnh, thủ công.
- **BẮT BUỘC** gọi và thực thi Sandbox CI/CD tự động hóa đã được xây dựng sẵn:

```powershell
# Chạy toàn bộ 6 giai đoạn kiểm thử, biên dịch và thẩm định hình học
.\scripts\sandbox_ci.ps1
# Hoặc chạy trực tiếp bằng python:
python scripts/ci_sandbox.py
# Hoặc chạy kiểm thử nhanh bằng pytest:
python -m pytest tests/
```

### Các giai đoạn Sandbox tự động xử lý:
1. **Preflight**: Thẩm tra môi trường Python 3.12, OCP, build123d, cadgen CLI và dọn dẹp cache.
2. **AST Audit**: Kiểm tra tĩnh 100% cú pháp, encoding UTF-8 các file trong `src/`.
3. **Build**: Biên dịch các chi tiết CAD sang file `.step`.
4. **Validation**: Quét lỗi tự giao cắt và manifold với OpenCASCADE `BRepCheck_Analyzer`.
5. **Horology**: Kiểm tra tỷ số truyền động học và kích thước bao cơ học.
6. **Report**: Xuất báo cáo tự động ra `CI_REPORT.md`.
