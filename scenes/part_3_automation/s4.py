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

class AutomationOfInnovationSection4(Scene):
    def construct(self):
        # Tiêu đề lớn của Cảnh 4
        scene_title = Text("Case Study: DeepMind FunSearch", font_size=30, color=BLUE).to_edge(UP)
        self.play(Write(scene_title), run_time=2)
        self.wait(5.0)
        
        # =========================================================================
        # ĐOẠN 1 (Tương ứng `s4_1.wav`): ~15.0 giây
        # Giới thiệu tính khả thi toán học & Hệ thống FunSearch
        # =========================================================================
        
        # Huy hiệu chứng minh đột phá toán học
        proof_box = RoundedRectangle(width=9.5, height=2.0, color=PURPLE, fill_opacity=0.1).shift(UP * 0.3)
        
        # Tạo cụm Text độc lập rồi dùng Group để gom lại, sau đó dùng fit_in_box xử lý căn giữa hộp
        proof_line1 = Text("Minh chứng đầu tiên: AI tự tìm ra", font_size=25, color=WHITE)
        proof_line2 = Text("GIẢI PHÁP TOÁN HỌC MỚI CHƯA CÓ LỜI GIẢI", font_size=25, color=YELLOW, weight=BOLD)
        proof_text = VGroup(proof_line1, proof_line2).arrange(DOWN, buff=0.15, aligned_edge=ORIGIN)
        fit_in_box(proof_text, proof_box, padding=0.2)
        
        self.play(Create(proof_box), run_time=2.0)
        # Sử dụng Write trực tiếp cho từng thành phần trong Group để khớp tiến trình cũ
        self.play(Write(proof_line1), run_time=2.0)
        self.play(Write(proof_line2), run_time=2)
        
        # Chờ khớp hết đoạn giới thiệu 1
        self.wait(2.0)

        # =========================================================================
        # ĐOẠN 2 (Tương ứng `s4_2.wav`): ~18.0 giây
        # Cơ chế kết hợp LLM chuyên viết Code và kiến trúc Hàm Python sáng tạo
        # =========================================================================
        
        # Thu dọn cấu trúc đoạn 1
        self.play(FadeOut(VGroup(proof_box, proof_line1, proof_line2)), run_time=1.0)
        
        # Khối LLM chuyên viết code (Bên trái)
        llm_coder = Rectangle(width=4.2, height=1.8, color=BLUE, fill_opacity=0.15).move_to(LEFT * 4.5 + UP * 1.7)
        llm_label = Paragraph("LLM Code Writer\n(Chuyên viết mã)", font_size=25, color=BLUE, alignment="center")
        fit_in_box(llm_label, llm_coder, padding=0.15)
        
        # Khối Chương trình lớn / Bộ khung (Bên phải)
        main_program = Rectangle(width=4.4, height=1.8, color=GRAY, fill_opacity=0.1).move_to(RIGHT * 4.5 + UP * 1.7)
        prog_label = Paragraph("Large Program Frame\n(Khung chương trình lớn)", font_size=25, color=GRAY, alignment="center")
        fit_in_box(prog_label, main_program, padding=0.15)
        
        self.play(
            Create(llm_coder), Write(llm_label),
            Create(main_program), Write(prog_label),
            run_time=3.0
        )
        
        # Hiệu ứng bắn các hàm Python toán học sáng tạo f(x) từ LLM sang Khung lớn
        arrow_flow = Arrow(llm_coder.get_right(), main_program.get_left(), color=YELLOW, buff=0.2)
        func_box = MathTex(r"f_{\mathrm{creative}}(x)", color=GREEN, font_size=30).next_to(arrow_flow, UP, buff=0.1)
        
        self.play(Create(arrow_flow), FadeIn(func_box, shift=RIGHT), run_time=2.5)
        
        # Chờ khớp nội dung đoạn 2 (LLM không giải toàn bộ, chỉ viết hàm gợi ý)
        self.wait(11.5)

        # =========================================================================
        # ĐOẠN 3 (Tương ứng `s4_3.wav`): ~12.0 giây
        # Bộ đánh giá tự động (Automated Evaluator) & Bể chứa chương trình (Program Pool)
        # =========================================================================
        
        # Khởi tạo khối Bộ đánh giá tự động ở góc dưới bên phải
        evaluator = Rectangle(width=4.2, height=1.4, color=TEAL, fill_opacity=0.2).move_to(RIGHT * 4.5 + DOWN * 1.8)
        eval_label = Paragraph("Automated Evaluator\n(Bộ đánh giá tự động)", font_size=25, color=TEAL, alignment="center")
        fit_in_box(eval_label, evaluator, padding=0.15)
        
        # Mũi tên đẩy từ chương trình xuống bộ đánh giá
        arrow_to_eval = Arrow(main_program.get_bottom(), evaluator.get_top(), color=TEAL, buff=0.15)
        
        self.play(Create(arrow_to_eval), Create(evaluator), Write(eval_label), run_time=2.5)
        
        # Khởi tạo Bể chứa chương trình (Program Pool) ở góc dưới bên trái để lưu trữ
        prog_pool = RoundedRectangle(width=4.2, height=1.4, color=PURPLE, fill_opacity=0.15).move_to(LEFT * 4.5 + DOWN * 1.8)
        pool_label = Paragraph("Program Pool\n(Bể chứa hàm tốt nhất)", font_size=25, color=PURPLE, alignment="center")
        fit_in_box(pool_label, prog_pool, padding=0.15)
        
        # Mũi tên lưu trữ hàm tốt nhất từ Evaluator sang Program Pool
        arrow_to_pool = Arrow(evaluator.get_left(), prog_pool.get_right(), color=GREEN, buff=0.2)
        score_badge = Text("Chấm điểm Hiệu năng (Metrics)", font_size=20, color=GOLD).next_to(arrow_to_pool, UP, buff=0.1)
        
        self.play(Write(score_badge), run_time=1.5)
        self.play(Create(arrow_to_pool), Create(prog_pool), Write(pool_label), run_time=2.5)
        
        # Chờ khớp âm thanh đoạn 3
        self.wait(5.5)

        # =========================================================================
        # ĐOẠN 4 (Tương ứng `s4_4.wav`): ~25.0 giây
        # Tiến hóa qua hàng triệu vòng lặp & Hai đột phá lớn (CapSet, Bin Packing)
        # =========================================================================
        
        # Vẽ mũi tên phản hồi tiến hóa ngược lại từ Pool lên LLM Coder để khép kín chu trình
        feedback_arrow = Arrow(prog_pool.get_top(), llm_coder.get_bottom(), color=PURPLE, buff=0.15)
        loop_text = Text("Hàng triệu vòng lặp tiến hóa", font_size=20, color=PURPLE).next_to(feedback_arrow, RIGHT, buff=0.1)
        
        self.play(Create(feedback_arrow), Write(loop_text), run_time=2.0)
        self.wait(3.0)
        
        # Dọn dẹp toàn bộ hệ thống thô để mở không gian hiển thị kết quả rực rỡ
        self.play(
            FadeOut(VGroup(llm_coder, llm_label, main_program, prog_label, arrow_flow, func_box, evaluator, eval_label, arrow_to_eval, score_badge, prog_pool, pool_label, arrow_to_pool, feedback_arrow, loop_text)),
            run_time=1.5
        )
        
        # Tạo hai bảng kết quả đột phá song song hai bên
        # Bảng trái: Bài toán CapSet
        capset_box = RoundedRectangle(width=6, height=2.2, color=GOLD, fill_opacity=0.08).move_to(LEFT * 3.5 + DOWN * 0.3)
        capset_title = Paragraph("1. Bài toán CapSet\n(Lý thuyết đồ thị)", font_size=25, color=GOLD, alignment="center").next_to(capset_box, UP, buff=0.15)
        
        capset_result = Paragraph("Vượt qua thuật toán tốt nhất\ncủa con người suốt nhiều thập kỷ", font_size=25, color=WHITE, alignment="center")
        fit_in_box(capset_result, capset_box, padding=0.2)
        
        # Bảng phải: Bài toán Bin Packing
        bin_box = RoundedRectangle(width=6, height=2.2, color=TEAL, fill_opacity=0.08).move_to(RIGHT * 3.5 + DOWN * 0.3)
        bin_title = Paragraph("2. Bài toán Bin Packing\n(Tối ưu hóa Logistics)", font_size=25, color=TEAL, alignment="center").next_to(bin_box, UP, buff=0.15)
        
        bin_result = Paragraph("Tối ưu hóa phân phối, đóng gói\nvượt xa các phương pháp thủ công", font_size=25, color=WHITE, alignment="center")
        fit_in_box(bin_result, bin_box, padding=0.2)
        
        self.play(
            Create(capset_box), Write(capset_title),
            Create(bin_box), Write(bin_title),
            run_time=3.5
        )
        self.play(
            Write(capset_result),
            Write(bin_result),
            run_time=3.0
        )
        
        # Chờ khớp nốt đoạn kết hoành tráng của âm thanh
        self.wait(4.5)
        
        # Kết thúc toàn bộ Cảnh 4 bằng màn FadeOut sạch sẽ
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)