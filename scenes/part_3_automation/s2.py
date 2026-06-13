from manim import *

# Định nghĩa hàm tự động co giãn và căn giữa hoàn hảo vào tâm hộp
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

class AutomationOfInnovationSection2(Scene):
    def construct(self):
        # Thiết lập tiêu đề góc trên màn hình
        main_title = Text("Automated Innovation Loop Architecture", font_size=30, color=BLUE).to_edge(UP)
        self.play(Write(main_title), run_time=1.5)

        # =========================================================================
        # ĐOẠN 1 (`s2_1.wav`): Ước lượng ~11.5 giây
        # Giới thiệu tổng quan vòng lặp 4 thành phần và Latent Space trung tâm
        # =========================================================================
        
        # Tạo vùng trung tâm Latent Space (Không gian ẩn) bằng nét đứt chuẩn Manim
        latent_center = DashedVMobject(Circle(radius=1.3, color=PURPLE, stroke_width=2))
        
        # Dùng Paragraph căn giữa trục đứng cho văn bản vùng trung tâm
        latent_text = Paragraph("Latent Space\n(Không gian ẩn)", font_size=25, color=PURPLE, alignment="center")
        fit_in_box(latent_text, latent_center, padding=0.1)
        
        self.play(Create(latent_center), Write(latent_text), run_time=2.5)

        # Định vị tọa độ cho 4 nút xung quanh theo cấu trúc vòng lặp vuông
        n1_pos = LEFT * 4.5 + UP * 1.7
        n2_pos = RIGHT * 4.5 + UP * 1.7
        n3_pos = RIGHT * 4.5 + DOWN * 1.8
        n4_pos = LEFT * 4.5 + DOWN * 1.8

        # Khởi tạo 4 khối hộp rỗng (chưa kích hoạt - mờ nhạt)
        box_width, box_height = 4.5, 1.4
        b1 = Rectangle(width=box_width, height=box_height, color=GRAY, fill_opacity=0.05).move_to(n1_pos)
        b2 = Rectangle(width=box_width, height=box_height, color=GRAY, fill_opacity=0.05).move_to(n2_pos)
        b3 = Rectangle(width=box_width, height=box_height, color=GRAY, fill_opacity=0.05).move_to(n3_pos)
        b4 = Rectangle(width=box_width, height=box_height, color=GRAY, fill_opacity=0.05).move_to(n4_pos)

        # Chuyển đổi sang Paragraph + alignment="center" và dùng fit_in_box để ép chữ nằm chính giữa hộp rỗng
        t1 = Paragraph("1. Hypothesis Gen\n(Khối sinh giả thuyết)", font_size=25, color=GRAY, alignment="center")
        fit_in_box(t1, b1, padding=0.15)
        
        t2 = Paragraph("2. Virtual Sandbox\n(Môi trường ảo)", font_size=25, color=GRAY, alignment="center")
        fit_in_box(t2, b2, padding=0.15)
        
        t3 = Paragraph("3. Falsification\n(Bộ lọc bác bỏ)", font_size=25, color=GRAY, alignment="center")
        fit_in_box(t3, b3, padding=0.15)
        
        t4 = Paragraph("4. Evo Update\n(Cập nhật tiến hóa)", font_size=25, color=GRAY, alignment="center")
        fit_in_box(t4, b4, padding=0.15)

        # Vẽ các đường mũi tên kết nối vòng lặp khép kín giữa các khối
        a1_2 = Arrow(b1.get_right(), b2.get_left(), color=GRAY, buff=0.1)
        a2_3 = Arrow(b2.get_bottom(), b3.get_top(), color=GRAY, buff=0.1)
        a3_4 = Arrow(b3.get_left(), b4.get_right(), color=GRAY, buff=0.1)
        a4_1 = Arrow(b4.get_top(), b1.get_bottom(), color=GRAY, buff=0.1)

        self.play(
            FadeIn(VGroup(b1, t1, b2, t2, b3, t3, b4, t4)),
            Create(VGroup(a1_2, a2_3, a3_4, a4_1)),
            run_time=4.0
        )
        
        # Chờ khớp hết âm thanh đoạn 1
        self.wait(3.5)

        # =========================================================================
        # ĐOẠN 2 (`s2_2.wav`): Ước lượng ~14.5 giây
        # Kích hoạt Khối 1: Hypothesis Generator
        # =========================================================================
        
        b1_active = Rectangle(width=box_width, height=box_height, color=BLUE, fill_color=BLUE, fill_opacity=0.2).move_to(n1_pos)
        
        # Tạo chữ active mới, ép vào tâm hình học của b1_active
        t1_active = Paragraph("1. Hypothesis Gen\n(Khối sinh giả thuyết)", font_size=25, color=BLUE, alignment="center")
        fit_in_box(t1_active, b1_active, padding=0.15)
        
        self.play(Transform(b1, b1_active), Transform(t1, t1_active), run_time=2.0)

        detail_1a = Text("• LLM / VLA Models", font_size=20, color=WHITE).next_to(b1, UP, aligned_edge=LEFT, buff=0.15)
        detail_1b = Text("• Symbolic Mutation (Đột biến mã)", font_size=20, color=WHITE).next_to(detail_1a, UP, aligned_edge=LEFT, buff=0.1)
        
        self.play(Write(detail_1a), run_time=2.0)
        self.play(Write(detail_1b), run_time=2.5)

        self.wait(12.0)

        # =========================================================================
        # ĐOẠN 3 (`s2_3.wav`): Ước lượng ~13.5 giây
        # Kích hoạt Khối 2: Virtual Sandbox
        # =========================================================================
        
        data_packet = Dot(color=YELLOW, radius=0.1).move_to(b1.get_right())
        a1_2_active = Arrow(b1.get_right(), b2.get_left(), color=BLUE, buff=0.1)
        
        self.play(Create(a1_2_active), run_time=1.0)
        self.play(data_packet.animate.move_to(b2.get_left()), run_time=2.0)
        self.play(FadeOut(data_packet))

        b2_active = Rectangle(width=box_width, height=box_height, color=TEAL, fill_color=TEAL, fill_opacity=0.2).move_to(n2_pos)
        
        # Tạo chữ active mới, ép vào tâm hình học của b2_active
        t2_active = Paragraph("2. Virtual Sandbox\n(Môi trường ảo)", font_size=25, color=TEAL, alignment="center")
        fit_in_box(t2_active, b2_active, padding=0.15)
        
        self.play(Transform(b2, b2_active), Transform(t2, t2_active), run_time=1.5)

        detail_2a = Text("• Driven by World Model", font_size=20, color=WHITE).next_to(b2, UP, aligned_edge=LEFT, buff=0.15)
        detail_2b = Text("• Dynamics Simulation", font_size=20, color=WHITE).next_to(detail_2a, UP, aligned_edge=LEFT, buff=0.1)
        
        self.play(Write(detail_2a), run_time=2.0)
        self.play(Write(detail_2b), run_time=2.0)

        self.wait(7.5)

        # =========================================================================
        # ĐOẠN 4 (`s2_4.wav`): Ước lượng ~13.5 giây
        # Kích hoạt Khối 3: Falsification Filter
        # =========================================================================
        
        data_packet2 = Dot(color=YELLOW, radius=0.1).move_to(b2.get_bottom())
        a2_3_active = Arrow(b2.get_bottom(), b3.get_top(), color=TEAL, buff=0.1)
        
        self.play(Create(a2_3_active), run_time=1.0)
        self.play(data_packet2.animate.move_to(b3.get_top()), run_time=1.5)
        self.play(FadeOut(data_packet2))

        b3_active = Rectangle(width=box_width, height=box_height, color=ORANGE, fill_color=ORANGE, fill_opacity=0.2).move_to(n3_pos)
        
        # Tạo chữ active mới, ép vào tâm hình học của b3_active
        t3_active = Paragraph("3. Falsification\n(Bộ lọc bác bỏ)", font_size=25, color=ORANGE, alignment="center")
        fit_in_box(t3_active, b3_active, padding=0.15)
        
        self.play(Transform(b3, b3_active), Transform(t3, t3_active), run_time=1.5)

        detail_3a = Text("• Physical Law Check", font_size=20, color=WHITE).next_to(b3, DOWN, aligned_edge=LEFT, buff=0.15)
        detail_3b = Text("• Discard Inconsistencies", font_size=20, color=WHITE).next_to(detail_3a, DOWN, aligned_edge=LEFT, buff=0.1)
        
        self.play(Write(detail_3a), run_time=2.0)
        self.play(Write(detail_3b), run_time=2.0)

        cross_mark = Cross(b3, stroke_color=RED, stroke_width=5, scale_factor=0.6)
        self.play(Create(cross_mark), run_time=1.0)
        self.play(FadeOut(cross_mark), run_time=1.0)

        self.wait(6)

        # =========================================================================
        # ĐOẠN 5 (`s2_5.wav`): Ước lượng ~15.5 giây
        # Kích hoạt Khối 4: Evolutionary Update
        # =========================================================================
        
        data_packet3 = Dot(color=GOLD, radius=0.1).move_to(b3.get_left())
        a3_4_active = Arrow(b3.get_left(), b4.get_right(), color=ORANGE, buff=0.1)
        
        self.play(Create(a3_4_active), run_time=1.0)
        self.play(data_packet3.animate.move_to(b4.get_right()), run_time=1.5)
        self.play(FadeOut(data_packet3))

        b4_active = Rectangle(width=box_width, height=box_height, color=GOLD, fill_color=GOLD, fill_opacity=0.2).move_to(n4_pos)
        
        # Tạo chữ active mới, ép vào tâm hình học của b4_active
        t4_active = Paragraph("4. Evo Update\n(Cập nhật tiến hóa)", font_size=25, color=GOLD, alignment="center")
        fit_in_box(t4_active, b4_active, padding=0.15)
        
        self.play(Transform(b4, b4_active), Transform(t4, t4_active), run_time=1.5)

        detail_4a = Text("• Fine-tune via Gradients", font_size=20, color=WHITE).next_to(b4, DOWN, aligned_edge=LEFT, buff=0.15)
        detail_4b = Text("• Update Gen & World Model", font_size=20, color=WHITE).next_to(detail_4a, DOWN, aligned_edge=LEFT, buff=0.1)
        
        self.play(Write(detail_4a), run_time=1.5)
        self.play(Write(detail_4b), run_time=1.5)

        a4_1_active = Arrow(b4.get_top(), b1.get_bottom(), color=GOLD, stroke_width=5, buff=0.1)
        gradient_sym = MathTex(r"\nabla W, \nabla G", color=GOLD, font_size=24).next_to(a4_1_active, LEFT, buff=0.1)
        
        self.play(
            Create(a4_1_active),
            FadeIn(gradient_sym, shift=RIGHT),
            latent_center.animate.scale(1.2).set_color(GOLD), 
            run_time=2.5
        )

        self.wait(8)

        # Dọn dẹp màn hình mượt mà
        all_elements = VGroup(
            main_title, latent_center, latent_text,
            b1, t1, b2, t2, b3, t3, b4, t4, a1_2, a2_3, a3_4, a4_1,
            a1_2_active, a2_3_active, a3_4_active, a4_1_active,
            detail_1a, detail_1b, detail_2a, detail_2b, detail_3a, detail_3b, detail_4a, detail_4b,
            gradient_sym
        )
        self.play(FadeOut(all_elements), run_time=1)