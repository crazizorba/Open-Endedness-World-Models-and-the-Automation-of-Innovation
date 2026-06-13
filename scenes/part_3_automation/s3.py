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

class AutomationOfInnovationSection3(Scene):
    def construct(self):
        # Thiết lập tiêu đề tổng quan cho Cảnh 3
        scene_title = Text("Khối Sinh Giả Thuyết — Cơ Chế Vận Hành", font_size=30, color=BLUE).to_edge(UP)
        self.play(Write(scene_title), run_time=6)

        # =========================================================================
        # ĐOẠN 1 (Tương ứng `s3_1.wav`): ~15.0 giây
        # Phân tích Symbolic Space & Phủ định bẫy ảo giác văn bản tự do
        # =========================================================================
        
        # Tạo khung Không gian ký hiệu ở chính giữa
        symbolic_space = RoundedRectangle(width=5.5, height=3.2, color=PURPLE, fill_opacity=0.08).shift(UP * 0.2)
        ss_text = Text("Symbolic Space (Không gian ký hiệu)", font_size=35, color=PURPLE).next_to(symbolic_space, UP, buff=0.15)
        
        self.play(Create(symbolic_space), Write(ss_text), run_time=1)

        # Hiển thị text Ảo giác vô nghĩa và thực hiện đánh dấu X (bác bỏ)
        hallucination_text = Paragraph("Free Text & Hallucination\n(Văn bản tự do & Ảo giác)", font_size=25, color=RED, alignment="center")
        fit_in_box(hallucination_text, symbolic_space, padding=0.2)
        
        cross_mark = Cross(hallucination_text, stroke_color=RED, stroke_width=4, scale_factor=0.8)
        
        self.play(Write(hallucination_text), run_time=1)
        self.play(Create(cross_mark), run_time=1)
        # Biến mất vùng ảo giác để nhường chỗ cho các ký hiệu toán học thực tế
        self.play(FadeOut(hallucination_text), FadeOut(cross_mark), run_time=1.0)
        
        # Xuất hiện các nút ký hiệu/thuật toán biểu diễn tượng trưng bên trong không gian
        symbolic_nodes = VGroup(
            MathTex(r"f(x) \rightarrow y", color=WHITE, font_size=30),
            MathTex(r"\mathcal{A}_{mutated}", color=YELLOW, font_size=30),
            MathTex(r"\pi_{\phi}(s)", color=TEAL, font_size=30)
        ).arrange(RIGHT, buff=0.6).move_to(symbolic_space.get_center())
        
        self.play(FadeIn(symbolic_nodes, shift=UP), run_time=2.0)
        
        # Chờ khớp thời lượng đoạn 1
        self.wait(1)

        # =========================================================================
        # ĐOẠN 2 (Tương ứng `s3_2.wav`): ~22.0 giây
        # Mô hình LLM đóng vai trò toán tử đột biến mã nguồn (Evolutionary Mutation)
        # =========================================================================
        
        # Thu nhỏ thu gọn vùng Symbolic Space sang góc trái để lấy không gian cho LLM
        self.play(
            symbolic_space.animate.scale(0.55).to_edge(LEFT, buff=0.4).shift(DOWN * 0.5),
            ss_text.animate.scale(0.75).next_to(symbolic_space, UP, buff=0.1),
            FadeOut(symbolic_nodes),
            run_time=2.0
        )

        # Khởi tạo khối hộp chức năng LLM Mutation Operator ở bên phải
        llm_box = Rectangle(width=4.2, height=1.6, color=BLUE, fill_color=BLUE, fill_opacity=0.15).move_to(RIGHT * 0 + UP * -0.4)
        
        llm_text = Paragraph("LLM / VLA Model\n(Evolutionary Mutation)", font_size=25, color=BLUE, alignment="center")
        fit_in_box(llm_text, llm_box, padding=0.15)
        
        # Đầu vào: Mã nguồn thuật toán hiện tại
        code_in = Paragraph("Current Algorithm Code\n(Mã thuật toán hiện tại)", font_size=25, color=GRAY, alignment="center").next_to(llm_box, UP, buff=0.5)
        arrow_in = Arrow(code_in.get_bottom(), llm_box.get_top(), color=GRAY, buff=0.1)
        
        self.play(Create(llm_box), Write(llm_text), FadeIn(code_in), Create(arrow_in), run_time=3.0)
        
        # Kỹ thuật tác động: Prompt nâng cao & Tinh chỉnh Temperature
        param_text = Paragraph("Advanced Prompting\n Temp Adjustment", font_size=25, color=YELLOW, alignment="center").next_to(llm_box, RIGHT, buff=0.2).scale(0.9)
        self.play(Write(param_text), run_time=2.5)
        
        # Đầu ra: Các biến thể mã nguồn đột biến mới
        code_out = Paragraph("New Source Code Variants\n(Biến thể mã nguồn mới)", font_size=25, color=GREEN, alignment="center").next_to(llm_box, DOWN, buff=0.6)
        arrow_out = Arrow(llm_box.get_bottom(), code_out.get_top(), color=GREEN, buff=0.1)
        
        self.play(Create(arrow_out), FadeIn(code_out, shift=DOWN), run_time=2.5)
        
        # Chờ khớp thời lượng đoạn 2
        self.wait(10.5)

        # =========================================================================
        # ĐOẠN 3 (Tương ứng `s3_3.wav`): ~17.5 giây
        # Ứng dụng điều khiển Robot thực tế thông qua cấu trúc VLA
        # =========================================================================
        
        # Dọn sạch các chi tiết đột biến code để chuyển đổi ngữ cảnh sang Robot điều khiển
        self.play(
            FadeOut(VGroup(symbolic_space, ss_text, llm_box, llm_text, code_in, arrow_in, param_text, code_out, arrow_out)),
            run_time=1.5
        )
        
        # Đặt lại khối VLA trung tâm
        vla_box = Rectangle(width=4.2, height=1.6, color=TEAL, fill_color=TEAL, fill_opacity=0.2).move_to(LEFT * 3.1)
        
        vla_text = Paragraph("Vision-Language-Action\n(Mô hình VLA)", font_size=25, color=TEAL, alignment="center")
        fit_in_box(vla_text, vla_box, padding=0.15)
        
        abstract_hyp = Paragraph("Abstract Hypotheses\n(Giả thuyết trừu tượng)", font_size=25, color=WHITE, alignment="center").next_to(vla_box, UP, buff=0.6)
        arrow_vla_in = Arrow(abstract_hyp.get_bottom(), vla_box.get_top(), color=PURPLE, buff=0.1)
        
        self.play(Create(vla_box), Write(vla_text), FadeIn(abstract_hyp), Create(arrow_vla_in), run_time=2.5)
        
        # Khởi tạo một lưới hệ tọa độ tượng trưng cho không gian vật lý điều khiển robot
        robot_grid = NumberPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1], background_line_style={"stroke_opacity": 0.2}).scale(0.6).move_to(RIGHT * 2.9)
        robot_label = Paragraph("Physical Action Space\n(Không gian hành động)", font_size=25, color=WHITE, alignment="center").next_to(robot_grid, UP, buff=0.2)
        
        self.play(Create(robot_grid), Write(robot_label), run_time=2.5)
        
        # Vẽ mũi tên truyền đổi từ VLA sang lưới hành động
        arrow_vla_out = Arrow(vla_box.get_right(), robot_grid.get_left(), color=TEAL, buff=0.15)
        self.play(Create(arrow_vla_out), run_time=1.0)
        
        # Vẽ các vector chuỗi quỹ đạo động lực liên tiếp (hành động cụ thể của robot)
        traj1 = Line(robot_grid.get_center(), robot_grid.get_center() + RIGHT * 0.7 + UP * 0.5, color=YELLOW, stroke_width=3).add_tip()
        traj2 = Line(traj1.get_end(), traj1.get_end() + DOWN * 0.7 + RIGHT * 0.6, color=ORANGE, stroke_width=3).add_tip()
        
        self.play(Create(traj1), run_time=1.5)
        self.play(Create(traj2), run_time=1.5)
        
        # Chờ khớp thời lượng đoạn 3
        self.wait(7.0)

        # =========================================================================
        # ĐOẠN 4 (Tương ứng `s3_4.wav`): ~24.0 giây
        # Cơ chế Novelty Search để tối ưu hóa tính đa dạng sinh giải thuyết
        # =========================================================================
        
        # Dọn dẹp giao diện Robot để sang phần thuật toán Novelty Search
        self.play(
            FadeOut(VGroup(vla_box, vla_text, abstract_hyp, arrow_vla_in, robot_grid, robot_label, arrow_vla_out, traj1, traj2)),
            run_time=1.5
        )
        
        # Tiêu đề cơ chế Novelty Search
        ns_title = Text("Diversity via Novelty Search Mechanism", font_size=25, color=GOLD).to_edge(UP, buff=1.5)
        self.play(Write(ns_title), run_time=1.5)
        
        # Hộp phần thưởng truyền thống (Bị loại bỏ / gạch chéo)
        box_trad = Rectangle(width=5.5, height=1.6, color=GRAY, fill_opacity=0.05).move_to(LEFT * 3 + UP * 0.4)
        
        text_trad = Paragraph("Standard Reward\n(Đúng / Sai cục bộ)", font_size=25, color=GRAY, alignment="center")
        fit_in_box(text_trad, box_trad, padding=0.15)
        
        cross_trad = Cross(box_trad, stroke_color=RED, stroke_width=3, scale_factor=0.75)
        
        # Hộp phần thưởng tính mới Novelty (Được tập trung)
        box_novel = Rectangle(width=3.5, height=1.6, color=GOLD, fill_color=GOLD, fill_opacity=0.15).move_to(RIGHT * 3 + UP * 0.4)
        
        text_novel = Paragraph("Novelty Reward\n(Độ mới cấu trúc)", font_size=25, color=GOLD, alignment="center")
        fit_in_box(text_novel, box_novel, padding=0.15)
        
        self.play(
            Create(box_trad), Write(text_trad),
            Create(box_novel), Write(text_novel),
            run_time=3.0
        )
        self.play(Create(cross_trad), run_time=1.5)
        
        # Tạo khối kho dữ liệu lưu trữ lịch sử ở phía dưới để tính khoảng cách độ lệch
        archive_box = RoundedRectangle(width=9.0, height=1.0, color=BLUE, fill_opacity=0.1).move_to(DOWN * 1.5)
        
        archive_text = Paragraph("Historical Algorithm Archive (Kho mẫu lịch sử)", font_size=25, color=BLUE, alignment="center")
        fit_in_box(archive_text, archive_box, padding=0.1)
        
        self.play(Create(archive_box), Write(archive_text), run_time=2.5)
        
        # Vẽ mũi tên kép đo lường khoảng cách cấu trúc thuật toán so với quá khứ
        dist_arrow = DoubleArrow(box_novel.get_bottom(), archive_box.get_top() + RIGHT * 1.5, color=YELLOW, buff=0.1)
        dist_label = MathTex(r"\text{Distance } \Delta \mathcal{A}", color=YELLOW, font_size=25).next_to(dist_arrow, RIGHT, buff=0.1)
        
        self.play(Create(dist_arrow), FadeIn(dist_label), run_time=2.0)
        
        # Chờ khớp nốt đoạn âm thanh cuối
        self.wait(3.5)
        
        # Dọn dẹp toàn bộ màn hình để kết thúc Cảnh 3 mượt mà
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)