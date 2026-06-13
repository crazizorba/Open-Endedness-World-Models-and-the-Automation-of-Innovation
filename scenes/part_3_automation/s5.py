from manim import *

# Định nghĩa hàm tự động co giãn và căn giữa hoàn hảo vào tâm hộp đối tượng
def fit_in_box(mobject, box, padding=0.15):
    max_w = box.width - 2 * padding
    max_h = box.height - 2 * padding
    curr_w = mobject.width
    curr_h = mobject.height
    if curr_w > 0 and curr_h > 0:
        factor = min(1.0, max_w / curr_w, max_h / curr_h)
        mobject.scale(factor)
    mobject.move_to(box.get_center())
    return mobject

class AutomationOfInnovationSection5(Scene):
    def construct(self):
        # Tiêu đề tổng quan
        scene_title = Text("The AI Scientist: Trợ Lý Nghiên Cứu Toàn Diện", font_size=30, color=BLUE).to_edge(UP)
        self.play(Write(scene_title), run_time=1.5)

        # =========================================================================
        # ĐOẠN 1 (Tương ứng `s5_1.wav`): Ước lượng ~14.0 giây
        # Giới thiệu kiến trúc The AI Scientist bao quát
        # =========================================================================
        
        # Khung tổng thể đại diện cho hệ thống
        ai_scientist_box = RoundedRectangle(width=6.5, height=3.5, color=PURPLE, fill_opacity=0.08).shift(DOWN * 0.2)
        ai_label = Paragraph("Toàn bộ quy trình nghiên cứu khép kín", font_size=30, color=PURPLE, alignment="center").next_to(ai_scientist_box, UP * 2, buff=0.2)
        
        core_text = Paragraph("The AI Scientist Architecture", font_size=25, color=WHITE, alignment="center")
        fit_in_box(core_text, ai_scientist_box, padding=0.2)
        
        self.play(Create(ai_scientist_box), Write(ai_label), run_time=2.5)
        self.play(Write(core_text), run_time=2.0)
        
        # Chờ khớp thời lượng đoạn 1
        self.wait(8.0)

        # =========================================================================
        # ĐOẠN 2 (Tương ứng `s5_2.wav`): Ước lượng ~18.0 giây
        # Đọc tài liệu arXiv & Chạy thực nghiệm Deep Learning
        # =========================================================================
        
        # Thu nhỏ khung tổng thể sang bên trái để nhường chỗ cho các bước chi tiết
        self.play(
            ai_scientist_box.animate.scale(0.55).to_edge(LEFT, buff=0.4).shift(DOWN * 0.5),
            ai_label.animate.scale(0.75).next_to(ai_scientist_box, UP, buff=0.5),
            FadeOut(core_text),
            run_time=2.0
        )
        
        # Bước 1: Đọc tài liệu
        step1_box = Rectangle(width=5, height=1.2, color=TEAL, fill_opacity=0.15).move_to(RIGHT * 0.5 + UP * 1)
        step1_txt = Paragraph("1. Data & Literature\n(Đọc arXiv & Tìm ý tưởng)", font_size=25, color=TEAL, alignment="center")
        fit_in_box(step1_txt, step1_box, padding=0.15)
        
        self.play(Create(step1_box), Write(step1_txt), run_time=2.5)
        self.wait(4)
        
        # Bước 2: Viết code và chạy thí nghiệm
        step2_box = Rectangle(width=5, height=1.2, color=YELLOW, fill_opacity=0.15).move_to(RIGHT * 0.5 + UP * -1)
        step2_txt = Paragraph("2. Deep Learning Exp.\n(Viết Code & Thu thập Data)", font_size=25, color=YELLOW, alignment="center")
        fit_in_box(step2_txt, step2_box, padding=0.15)
        
        arr1_2 = Arrow(step1_box.get_bottom(), step2_box.get_top(), color=GRAY, buff=0.1)
        
        self.play(Create(arr1_2), Create(step2_box), Write(step2_txt), run_time=3.0)
        
        # Hiệu ứng mô phỏng đồ thị kết quả hiện ra nhỏ bên cạnh
        # Tạo một trục tọa độ nhỏ và vẽ một đường cong logarit
        chart_axes = Axes(x_range=[0, 3, 1], y_range=[0, 2, 1], x_length=1.5, y_length=1.0).next_to(step2_box, LEFT, buff=0.2)
        chart_line = chart_axes.plot(lambda x: np.log(x + 1), color=YELLOW)
        chart_icon = VGroup(chart_axes, chart_line)
        
        self.play(Create(chart_icon), run_time=1.5)
        
        # Chờ khớp thời lượng đoạn 2
        self.wait(5.0)

        # =========================================================================
        # ĐOẠN 3 (Tương ứng `s5_3.wav`): Ước lượng ~16.0 giây
        # Biên dịch LaTeX và viết bài báo khoa học
        # =========================================================================
        
        # Bước 3: LaTeX Compilation
        step3_box = Rectangle(width=5, height=1.2, color=GREEN, fill_opacity=0.15).move_to(RIGHT * 0.5 + DOWN * 3)
        step3_txt = Paragraph("3. LaTeX Compilation\n(Viết bài báo hoàn chỉnh)", font_size=25, color=GREEN, alignment="center")
        fit_in_box(step3_txt, step3_box, padding=0.15)
        
        arr2_3 = Arrow(step2_box.get_bottom(), step3_box.get_top(), color=GRAY, buff=0.1)
        
        self.play(Create(arr2_3), Create(step3_box), Write(step3_txt), run_time=2.5)
        
        # Các thành phần của bài báo xuất hiện
        paper_details = Paragraph("Abstract → Methods → Results", font_size=20, color=WHITE, alignment="center").next_to(step3_box, DOWN, buff=0.15)
        self.play(Write(paper_details), run_time=2.0)
        
        # Chờ khớp thời lượng đoạn 3
        self.wait(11.5)

        # =========================================================================
        # ĐOẠN 4 (Tương ứng `s5_4.wav`): Ước lượng ~18.0 giây
        # AI Reviewer đánh giá theo chuẩn NeurIPS/ICML
        # =========================================================================
        
        # Chuyển đổi khung AI Scientist bên trái thành AI Reviewer
        reviewer_box = RoundedRectangle(width=4.5, height=1.8, color=RED, fill_color=RED, fill_opacity=0.15).move_to(LEFT * 5 + DOWN * 0.5)
        reviewer_txt = Paragraph("Independent AI Reviewer\n(Đánh giá tự động)", font_size=25, color=RED, alignment="center")
        fit_in_box(reviewer_txt, reviewer_box, padding=0.15)
        
        conf_standard = Paragraph("Tiêu chuẩn: NeurIPS, ICML", font_size=20, color=GOLD, alignment="center").next_to(reviewer_box, DOWN, buff=0.2)
        
        self.play(
            FadeOut(ai_scientist_box), FadeOut(ai_label), FadeOut(chart_icon), # Dọn dẹp đồ thị và khung cũ
            Create(reviewer_box), Write(reviewer_txt),
            run_time=2.5
        )
        
        # Gửi bài báo từ bước 3 sang khối Reviewer
        arr_submit = Arrow(step3_box.get_left(), reviewer_box.get_right(), color=GREEN, buff=0.2)
        self.play(Create(arr_submit), run_time=1.5)
        
        self.play(Write(conf_standard), run_time=2.0)
        
        # Vòng lặp phản hồi: Trả kết quả Review ngược lại Bước 1 để tinh chỉnh
        arr_feedback = CurvedArrow(reviewer_box.get_top(), step1_box.get_left(), color=ORANGE, angle=-TAU / 4)
        feedback_txt = Paragraph("Feedback Loop", font_size=20, color=ORANGE, alignment="center").next_to(arr_feedback, UP, buff=0.1)
        
        self.play(Create(arr_feedback), Write(feedback_txt), run_time=2.5)
        
        # Chờ khớp đoạn kết âm thanh
        self.wait(8.5)
        
        # Dọn dẹp sạch sẽ toàn bộ màn hình để kết thúc Cảnh 5 mượt mà
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)