Dựa trên voice-over script đã được phê duyệt.

Hãy tạo Animation Production Plan cho Manim.

Thông tin project:

scenes/
└── part_1_open_endedness/
└── open_endedness.py

Yêu cầu:

Mỗi Scene phải bao gồm:

1. Scene Name
2. Corresponding Manim Class Name
3. Estimated Duration
4. Animation Timeline

Timeline phải có dạng:

00:00 - 00:08
Animation ...

00:08 - 00:15
Animation ...

00:15 - 00:22
Animation ...

Đối với từng animation:

* Mô tả đối tượng xuất hiện.
* Mô tả chuyển động.
* Mô tả transform.
* Mục đích sư phạm.

Ngoài ra hãy liệt kê:

* Text objects
* MathTex objects
* Shapes
* Graphs
* Icons
* Images
* Sound effects
* Camera movements

sẽ cần dùng trong từng Scene.

Mục tiêu:

Sau khi đọc tài liệu này, một lập trình viên Manim có thể bắt đầu code mà không cần phải tự thiết kế lại animation.

Không viết code Manim.

Dựa vào file tham khảo Genie.py tôi đã cung cấp:

Khi xây dựng Animation Production Plan:

* Ưu tiên tái sử dụng các helper functions tương tự nếu phù hợp.
* Giữ phong cách camera nhất quán.
* Giữ cách tổ chức animation nhất quán.
* Giữ cách đặt tên Scene nhất quán.
* Giữ mức độ phức tạp animation tương đương.

Mục tiêu là để open_endedness.py và Genie.py trông như cùng một dự án được thực hiện bởi một tác giả.
