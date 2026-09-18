# Bộ ảnh mới — logo nhỏ, không khung

Theo điều chỉnh cuối của người dùng: sử dụng trực tiếp 14 ảnh demo gốc; giữ nguyên mọi thiết kế, chữ và icon. Chỉ bổ sung cặp POS365 × VNPAY nhỏ, có khoảng thở và không có ô trắng.

- `png/`: 14 ảnh hoàn thiện, kích thước bằng nguồn.
- `svg/`: 14 bố cục có nền và logo nhúng riêng, chỉnh vị trí được; không phải vector hóa ảnh nền.
- `index.html`: xem trước, so với nguồn và tải từng ảnh.
- `assets/`: logo dùng trong bộ mới. POS365 màu/trắng lấy từ tài nguyên dự án. VNPAY bản màu gốc; bản chữ trắng giữ nguyên biểu tượng màu và hình dạng chữ, điều chỉnh chữ trắng cho nền tối.
- `danh-sach.json`: vị trí logo và kết quả kiểm tra.
- `tao_bo_moi.py`: mã ghép trực tiếp bằng Pillow; chạy trong dự án gốc.

Không dùng các ảnh dọn nền bằng AI trong bộ giao này. Không có logo sản phẩm ghép thêm hoặc hộp nền trắng. Đã kiểm tra ảnh đầu ra đủ 14, cùng kích thước nguồn; tất cả pixel ngoài vùng logo nhỏ và bóng nhẹ đều không đổi. File nguồn được giữ nguyên.

Ảnh ở độ phân giải demo gốc, chưa nâng độ phân giải in khổ lớn.
