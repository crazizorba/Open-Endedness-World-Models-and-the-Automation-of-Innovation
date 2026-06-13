from manim import *
import numpy as np

# Định nghĩa hàm fit_in_box ở đầu file để tái sử dụng toàn bộ project
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

class AutomationOfInnovationSection1(Scene):
    def construct(self):
        # =========================================================================
        # ĐOẠN 1 (`s1_1.wav`): ĐÚNG 17.76 GIÂY
        # Giới thiệu tiêu đề và câu hỏi nghiên cứu nền tảng
        # =========================================================================
        
        # 1. Hiển thị tiêu đề chính (0.0s -> 3.5s)
        title = Title(r"The Automation of Innovation", color=BLUE_B)
        subtitle = Text("Tự Động Hóa Phát Minh Khoa Học", font_size=30, color=GRAY_A).next_to(title, DOWN)
        
        self.play(
            Write(title),
            FadeIn(subtitle, shift=UP),
            run_time=3.5
        )

        self.wait(9.5)
        
        # 2. Xuất hiện câu hỏi nghiên cứu cốt lõi (3.5s -> 8.0s)
        question_box = Rectangle(width=11, height=2, color=YELLOW_D).shift(DOWN * 0.5)
        
        # Đổi sang dùng Paragraph kết hợp alignment="center" để các dòng văn bản tự căn đều trục dọc
        question_text = Paragraph(
            "Liệu AI có thể tự mình tìm ra tri thức mới\nthay vì chỉ giải các bài toán có sẵn?", 
            font_size=25, color=WHITE, line_spacing=1.2,
            alignment="center"
        )
        # Sử dụng hàm fit_in_box để tự động ép chữ chui vào chính giữa tâm hình học của question_box
        fit_in_box(question_text, question_box, padding=0.3)
        
        #13
        self.play(
            Create(question_box),
            Write(question_text),
            run_time=8
        )
        #21
        # 3. Chờ khớp nốt thời lượng âm thanh s1_1 (8.0s -> 16.76s = 8.76s)
        #self.wait(8.5)
        
        # Dọn dẹp màn hình chuyển cảnh (16.76s -> 17.76s = 1.0s)
        self.play(
            FadeOut(title), FadeOut(subtitle), 
            FadeOut(question_box), FadeOut(question_text), 
            run_time=1.0
        )

        # =========================================================================
        # ĐOẠN 2 (`s1_2.wav`): ĐÚNG 18.04 GIÂY
        # Nhận thức luận Karl Popper (Vòng lặp Giả thuyết & Bác bỏ)
        # =========================================================================
        
        # 1. Hiển thị tên lý thuyết nền tảng (0.0s -> 3.0s)
        self.wait(1)
        #23

        theory_title = Text("Popperian Epistemology (Nhận Thức Luận Popper)", font_size=30, color=RED_B).to_edge(UP)
        self.play(Write(theory_title), run_time=7.0)
        
        # 2. Xây dựng đồ thị vòng lặp: Giả thuyết <-> Bác bỏ (3.0s -> 9.0s)
        #30
        hypothesis_node = Circle(radius=1.2, color=GREEN, fill_opacity=0.2).shift(LEFT * 2.5 + DOWN * 0.5)
        
        hypo_text = Paragraph("Hypothesis\n(Giả thuyết)", font_size=25, alignment="center")
        fit_in_box(hypo_text, hypothesis_node, padding=0.15)
        
        falsification_node = Circle(radius=1.2, color=ORANGE, fill_opacity=0.2).shift(RIGHT * 2.5 + DOWN * 0.5)
        
        fals_line1 = Text("Falsification", font_size=25)
        fals_line2 = Text("(Bác bỏ)", font_size=25)
        
        # Gom 2 dòng lại, xếp thẳng đứng (DOWN) và ép căn giữa trục dọc (aligned_edge=ORIGIN)
        fals_text = VGroup(fals_line1, fals_line2).arrange(DOWN, buff=0.1, aligned_edge=ORIGIN)
        
        # Sau đó mới ném cả cụm này vào hàm fit_in_box để căn giữa vòng tròn
        fit_in_box(fals_text, falsification_node, padding=0.15)
        
        arrow_top = CurvedArrow(hypothesis_node.get_top(), falsification_node.get_top(), radius=-4)
        arrow_bottom = CurvedArrow(falsification_node.get_bottom(), hypothesis_node.get_bottom(), radius=-4)
        
        self.play(
            FadeIn(hypothesis_node), Write(hypo_text),
            FadeIn(falsification_node), Write(fals_text),
            run_time=3.5
        )
        self.play(Create(arrow_top), Create(arrow_bottom), run_time=2.5)
        
        #36
        # 3. Chờ khớp nốt thời lượng âm thanh s1_2 (9.0s -> 16.54s = 7.54s)
        self.wait(4.54)
        
        # Thu nhỏ vòng lặp làm nền chuyển tiếp (16.54s -> 18.04s = 1.5s)
        popper_group = VGroup(theory_title, hypothesis_node, hypo_text, falsification_node, fals_text, arrow_top, arrow_bottom)
        self.play(popper_group.animate.scale(0.5).to_edge(UL), run_time=1.5)

        # =========================================================================
        # ĐOẠN 3 (`s1_3.wav`): ĐÚNG 17.40 GIÂY
        # AI Scientist - Tự sinh không gian và Phá vỡ giới hạn
        # =========================================================================
        
        # 1. Tạo khối thực thể AI Nghiên cứu độc lập (0.0s -> 3.5s)
        ai_box = Rectangle(width=6, height=3, color=BLUE_D, fill_opacity=0.1).shift(RIGHT * 3 + DOWN * 0.5)
        ai_title = Text("Autonomous AI Scientist", font_size=30, color=BLUE_A).next_to(ai_box, UP, buff=0.2)
        
        self.play(Create(ai_box), Write(ai_title), run_time=3.5)
        
        # 2. Xuất hiện các tác vụ phát kiến khoa học (3.5s -> 9.5s)
        task_1 = Text("• Tự sinh không gian tìm kiếm", font_size=25, color=WHITE).move_to(ai_box).shift(UP * 0.5)
        task_2 = Text("• Tự thiết kế bài toán mới", font_size=25, color=WHITE).next_to(task_1, DOWN, aligned_edge=LEFT)
        task_3 = Text("• Phá vỡ giới hạn tri thức", font_size=25, color=YELLOW).next_to(task_2, DOWN, aligned_edge=LEFT)
        
        self.play(Write(task_1), run_time=2.0)
        self.play(Write(task_2), run_time=2.0)
        self.play(Write(task_3), run_time=2.0)
        
        # 3. Chờ khớp nốt thời lượng âm thanh s1_3 (9.5s -> 16.40s = 6.90s)
        self.wait(6.90)
        
        # Dọn dẹp sân khấu chuẩn bị biểu đồ toán học đoạn 4 (16.40s -> 17.40s = 1.0s)
        self.play(
            FadeOut(popper_group), FadeOut(ai_box), FadeOut(ai_title), 
            FadeOut(task_1), FadeOut(task_2), FadeOut(task_3), 
            run_time=1.0
        )

        # =========================================================================
        # ĐOẠN 4 (`s1_4.wav`): ĐÚNG 16.20 GIÂY
        # Sự chuyển dịch: Interpolation (Nội suy) -> Extrapolation (Ngoại suy - OOD)
        # =========================================================================
        
        # 1. Vẽ hệ trục tọa độ không gian tri thức (0.0s -> 3.0s)
        axes = Axes(x_range=[-1, 6, 1], y_range=[-1, 5, 1], axis_config={"include_tip": True}, x_length=6, y_length=4).shift(LEFT * 2)
        axes_label = Text("Không gian Tri thức / Dữ liệu", font_size=30, color=GRAY_B).next_to(axes, UP)
        self.play(Create(axes), Write(axes_label), run_time=3.0)
        
        # 2. Vẽ vùng phân phối dữ liệu huấn luyện (Interpolation) (3.0s -> 6.5s)
        known_domain = Circle(radius=1.2, color=GRAY_C, fill_opacity=0.15).move_to(axes.c2p(2, 2))
        
        known_label = Paragraph("Dữ liệu đã biết\n(Interpolation)", font_size=25, color=GRAY_C, alignment="center").next_to(known_domain, UP, buff=0.1)
        
        # Tạo ngẫu nhiên tập hợp các điểm dữ liệu phân phối tĩnh
        np.random.seed(42)  # Đóng băng seed tránh biến đổi bất ngờ khi render lại
        dots = VGroup(*[Dot(axes.c2p(2 + np.random.uniform(-0.6, 0.6), 2 + np.random.uniform(-0.6, 0.6)), color=BLUE_C, radius=0.04) for _ in range(12)])
        
        self.play(Create(known_domain), Write(known_label), FadeIn(dots), run_time=3.5)
        
        # 3. Hiện mũi tên bứt phá sang vùng Ngoại suy Out-of-Distribution (6.5s -> 11.0s)
        ood_dot = Dot(axes.c2p(5, 4), color=RED, radius=0.08)
        
        ood_label = Paragraph("TRI THỨC MỚI\n(Extrapolation - OOD)", font_size=25, color=RED, alignment="center").next_to(ood_dot, UR, buff=0.2)
        
        breakthrough_arrow = DoubleArrow(
            axes.c2p(2, 2), axes.c2p(5, 4), 
            stroke_width=4, color=YELLOW, buff=0.1
        )
        
        self.play(
            Create(breakthrough_arrow),
            Flash(ood_dot, color=YELLOW, flash_radius=0.3),
            Create(ood_dot),
            Write(ood_label),
            run_time=4.5
        )
        
        # 4. Chờ khớp nốt thời lượng âm thanh s1_4 (11.0s -> 15.20s = 4.20s)
        self.wait(0.5)
        
        # Kết thúc phân đoạn 1 bằng hiệu ứng tắt màn hình mượt mà (15.20s -> 16.20s = 1.0s)
        self.play(
            FadeOut(axes), FadeOut(axes_label), FadeOut(known_domain), 
            FadeOut(known_label), FadeOut(dots), FadeOut(breakthrough_arrow), 
            FadeOut(ood_dot), FadeOut(ood_label), 
            run_time=1.0
        )