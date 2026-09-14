# Đồng Hồ Cơ Cổ Điển 42 mm (Classical Mechanical Dress Wristwatch)

Mô hình CAD tham chiếu Caliber **ETA 6497 / 6498** (18,000 vph / 2.5 Hz) được thiết kế tham số hoàn chỉnh bằng **Python build123d** và **cadgen**.

---

## 1. Thông Số Thiết Kế Tổng Thể

- **Kích thước vỏ**: Đường kính Ø 42.00 mm, lug-to-lug ~49.80 mm, độ dày tổng cộng <= 12.50 mm.
- **Kích thước Caliber**: Đường kính Ø 36.60 mm (ETA 6497-1), khoang chứa vỏ Ø 37.40 mm (khe hở an toàn >= 0.40 mm).
- **Tần số dao động**: 18,000 vph (2.5 Hz), chu kỳ dao động 0.4s, 5 nhịp/giây.
- **Bố cục mặt số & Kim**:
  - Kim giờ (`hour_hand`): Dáng feuille/dauphine cổ điển, chiều dài 10.20 mm, thép tôi xanh bóng (**Polished Blue Steel** `#204080`, metalness 0.92, roughness 0.10).
  - Kim phút (`minute_hand`): Dáng feuille thanh mảnh, chiều dài 14.80 mm chạm vạch phút, thép tôi xanh cobalt sáng nhẹ (**Cobalt Blue Steel** `#2A52BE`, metalness 0.88, roughness 0.14).
  - Kim giây rốn (`seconds_hand`): Kim hình kim có đối trọng giọt lệ, chiều dài 3.60 mm, đặt đồng trục tại Fourth Wheel Pivot `(-9.0000, 0.0000)`, sơn đỏ thẫm (**Crimson Red** `#D02020`, roughness 0.22, metalness 0.65).
  - Kính sapphire trước và sau: Tách rời thành occurrence/solid riêng biệt với độ trong suốt quang học (**Optical Sapphire** `#D8E8F8`, opacity 0.15).

---

## 2. Hướng Dẫn Tương Tác Trong CAD Viewer

Mô hình hỗ trợ hoàn toàn các công cụ native trong **cadgen CAD Viewer** (không cần cài đặt phần mềm bên thứ ba hay tạo trang web riêng):

### Bước 1: Khởi động và Mở Mô hình
1. Khởi động CAD Viewer server bằng lệnh:
   ```bash
   cadgen viewer
   ```
2. Truy cập trình duyệt tại địa chỉ: `http://127.0.0.1:3245/?file=STEP/watch_caliber_assembly.step`

### Bước 2: Xem Animation Chuyển Động Cơ Học
1. Chuyển sang tab **Animation** ở thanh công cụ bên phải.
2. Chọn clip **`running_x60`** (Presentation Speed) và bấm **Play**:
   - Kim giây hoàn thành 1 vòng tròn mỗi giây (tốc độ trình diễn 60x, quay đúng chiều kim đồng hồ từ góc nhìn mặt số).
   - Kim phút quét 6° mỗi giây.
   - Kim giờ quét 0.5° mỗi giây (tỷ số 12:1 chính xác tuyệt đối).
   - Bánh xe gai (escape wheel), ngựa (pallet fork) và vành tóc (balance wheel) dao động nhịp nhàng theo chu kỳ escapement.
3. Có thể chuyển sang các clip khác:
   - **`running_real_time`**: Tốc độ thời gian thực 1:1 (chu kỳ 60 giây).
   - **`wind_crown`**: Mô phỏng lên dây cót qua núm vặn, bánh cót (crown wheel) và bánh cóc (ratchet wheel).
   - **`time_setting`**: Rút núm chỉnh giờ, kim phút và kim giờ quét nhanh trong khi kim giây dừng.
   - **`inspection_exploded`**: Clip tự động bung mở vỏ đồng hồ trong 5 giây để quan sát cỗ máy bên trong.

### Bước 3: Chế Độ Inspection / Exploded View Bằng Sliders
1. Chuyển sang tab **Kinematics** trong CAD Viewer.
2. Người dùng có thể kéo trực tiếp 3 slider độc lập:
   - **`front_cover_open`** (0.0 – 8.0 mm): Dịch niềng bezel và kính sapphire trước về phía mặt số (Z âm) để quan sát mặt số, các kim và cầu motion work.
   - **`rear_cover_open`** (0.0 – 8.0 mm): Dịch nắp đáy sapphire về phía Z dương để quan sát toàn bộ bridge side, bánh xe cân bằng và hệ thống bánh răng.
   - **`caseband_inspection_shift`** (0.0 – 10.0 mm): Dịch thân vỏ (caseband) sang phương X dương để lộ toàn bộ caliber mà không bị che khuất.
3. Hoặc chọn pose định sẵn **`inspection_open`** để mở đồng thời cả 3 bộ phận về vị trí tối đa, hoặc pose **`rest`** để đóng hoàn toàn về trạng thái đeo tay.

### Bước 4: Chế Độ Tách Tự Động (CAD Viewer Exploded View)
- Vào tab **Display** → Bật tùy chọn **Exploded** → Kéo thanh trượt **Amount** để tự động phân rã mọi chi tiết máy theo các hướng hướng tâm.

### Bước 5: Chế Độ X-Ray và Ẩn Chi Tiết
- Trong cây phân cấp (Outliner / Scene Graph), bấm biểu tượng con mắt để ẩn/hiện nhanh các chi tiết:
  - Ẩn `bezel_and_crystal`, `caseband`, `exhibition_caseback` để xem riêng cỗ máy caliber.
  - Bật chế độ **X-Ray / Ghosting** trong tab Display để nhìn xuyên thấu qua thân vỏ thép.

---

## 3. Quy Trình Kiểm Thử và Thẩm Định CI/CD

Dự án áp dụng quy tắc thực thi qua **Sandbox CI/CD** tự động hóa:

```powershell
Start-Process `
  -FilePath "powershell.exe" `
  -ArgumentList @(
    "-NoProfile",
    "-NonInteractive",
    "-ExecutionPolicy", "Bypass",
    "-File", "C:\Users\ADMIN\Downloads\TEST\CLOCK\scripts\sandbox_ci.ps1"
  ) `
  -WindowStyle Hidden `
  -Wait
```

Sandbox tự động thực hiện 6 giai đoạn:
1. **Preflight**: Kiểm tra Python 3.11+, build123d, cadgen, OpenCASCADE.
2. **AST Audit**: Kiểm tra tĩnh 100% cú pháp Python.
3. **Build**: Biên dịch toàn bộ 28 model STEP.
4. **Validation**: Kiểm tra OpenCASCADE BRepCheck topology (0 lỗi self-intersection/manifold).
5. **Horology Tolerances**: Kiểm định kích thước bao 42 mm, khe hở Z các kim, độ đồng trục các pivot.
6. **Snapshots & Motion**: Kết xuất 17 ảnh PNG và xác minh sự thay đổi pixel/hash giữa các frame animation ($t_0 \ne t_{0.2} \ne t_{1.0}$).

---

## 4. Lưu Ý Kỹ Thuật (Disclaimer)

Mô hình này là sản phẩm trình diễn kỹ thuật cơ khí đồng hồ (Horological Presentation & Inspection CAD Model) phục vụ học tập, mô phỏng chuyển động động học và trực quan hóa 3D. Các chi tiết chưa bao gồm dung sai chế tạo micron chuyên dụng hoặc quy trình nhiệt luyện chế tác đồng hồ thương mại thực tế.
