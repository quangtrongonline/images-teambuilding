# Bộ 14 ảnh team-building đã ghép logo

- `index.html`: xem ảnh, đối chiếu trước/sau, tải từng PNG hoặc SVG.
- `png/`: 14 ảnh hoàn thiện, giữ nguyên kích thước demo gốc.
- `svg/`: 14 bản ghép có ảnh nền và từng logo nhúng riêng; có thể chỉnh vị trí trong phần mềm hỗ trợ SVG. Đây là SVG bố cục chứa ảnh bitmap, không phải toàn bộ thiết kế vector.
- `vi-tri-logo.json`: tọa độ các logo, vùng panel và SHA-256 ảnh gốc.
- `ghep_logo.py`: mã ghép dùng Pillow; chạy từ dự án gốc để xuất lại. Cần thư mục logo đã tải tại `output/logo-mau-vnpay-pos365/png` và 14 ảnh nguồn trong `team-building`.
- `tong-quan.jpg`, `xem-truoc/`: ảnh xem nhanh, không thay thế PNG đầy đủ.

## Bố trí

10 ảnh gala/check-in: logo QR, SmartPOS, PhonePOS tại Thanh toán số; POS365 tại Quản lý bán hàng; VNPAY-Invoice tại Hóa đơn điện tử; VNPAY-CA tại Chữ ký số; VNPAY-eKYC tại Ngân hàng số; VNPAY-App, Taxi, VnShop tại Tiện ích số. Các logo đặt trong panel trắng phủ khu vực biểu tượng cũ, giữ nguyên tên nhóm và mô tả bên dưới. eKYC đại diện phần eKYC của nhóm ngân hàng; không phải logo cho toàn bộ Mobile Banking.

4 ảnh team building: cặp logo POS365 × VNPAY phía trên, không chạm tiêu đề, slogan hoặc chủ thể.

## Phương pháp và kiểm tra

Bản cuối được ghép trực tiếp bằng mã theo lựa chọn của người dùng. Không dùng ảnh AI thử nghiệm làm nền đầu ra. Logo được lấy từ file tải ở bước trước, chỉ cắt khoảng alpha trống, đổi kích thước đúng tỷ lệ và đặt vào bố cục; không vẽ lại, đổi chữ hay đổi màu. Nguồn logo chi tiết nằm trong `output/logo-mau-vnpay-pos365/nguon-logo.json` của dự án.

Đã kiểm tra cả 14 file: kích thước đầu ra bằng ảnh gốc, checksum ảnh nguồn không đổi, mọi pixel ngoài vùng panel đều trùng ảnh gốc. Bản PNG là bản xem chuẩn; bản SVG có thể hiển thị khử răng cưa hơi khác tùy phần mềm.

Ảnh vẫn ở độ phân giải demo gốc, chưa nâng độ phân giải cho in backdrop khổ lớn.
