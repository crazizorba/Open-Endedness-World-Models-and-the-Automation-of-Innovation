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

class AutomationOfInnovationSection5a(Scene):
    def construct(self):
        # Tiêu đề Cảnh 5A (Thời gian: 1.5s)
        scene_title = Text("Case Study: Bài Báo Đầu Tiên Của The AI Scientist", font_size=30, color=BLUE).to_edge(UP, buff=0.4)
        self.play(Write(scene_title), run_time=1.5)

        # =========================================================================
        # ĐOẠN 1 (`s5a_1.wav`): TỔNG CHÍNH XÁC 18.0 GIÂY
        # Giới thiệu Sakana AI và hiển thị bìa bài báo thực tế
        # =========================================================================
        
        # Gọi file ảnh bìa bài báo (Cần đảm bảo file paper.jpg nằm trong thư mục assets)
        paper_img = ImageMobject("assets/paper.jpg")
        paper_img.scale_to_fit_height(4.2)  
        paper_img.move_to(UP * 0.2)
        
        # Viền nhấn mạnh bao quanh bài báo
        paper_border = SurroundingRectangle(paper_img, color=GOLD, stroke_width=2, buff=0.02)
        
        # Hiệu ứng hiện ảnh (Thời gian: 2.5s)
        self.play(FadeIn(paper_img, shift=UP), Create(paper_border), run_time=2.5)
        
        # Bù giờ để ĐOẠN 1 tròn 18s (18.0 - 1.5 - 2.5 = 14.0s)
        self.wait(14.0)

        # =========================================================================
        # ĐOẠN 2 (`s5a_2.wav`): TỔNG CHÍNH XÁC 20.0 GIÂY
        # Tóm tắt nội dung Abstract và tiến trình tự biên soạn
        # =========================================================================
        
        # Hiệu ứng quét đọc mô phỏng AI phân tích (Thời gian: 0.5 + 3.5 + 0.5 = 4.5s)
        scan_line = Line(paper_border.get_left(), paper_border.get_right(), color=YELLOW, stroke_width=4)
        scan_line.move_to(paper_border.get_top())
        
        self.play(FadeIn(scan_line), run_time=0.5)
        self.play(scan_line.animate.move_to(paper_border.get_bottom()), run_time=3.5)
        self.play(FadeOut(scan_line), run_time=0.5)
        
        # Hiển thị chú thích (Thời gian: 2.5 + 2.0 = 4.5s)
        # SỬA LỖI TẠI ĐÂY: Bỏ max_width, chủ động dùng \n ngắt dòng để chữ không tràn biên màn hình
        content_note_1 = Paragraph(
            "Phát hiện: Ép buộc cấu trúc mạng (Regularization)\nkhông đảm bảo Generalization.", 
            font_size=22, color=WHITE, alignment="center"
        ).next_to(paper_border, DOWN, buff=0.2)
        
        content_note_2 = Paragraph(
            "→ 100% Code, Biểu đồ & Văn bản do AI tự biên soạn", 
            font_size=22, color=LIGHT_GRAY, alignment="center"
        ).next_to(content_note_1, DOWN, buff=0.15)
        
        self.play(Write(content_note_1), run_time=2.5)
        self.play(Write(content_note_2), run_time=2.0)
        
        # Bù giờ để ĐOẠN 2 tròn 20s (20.0 - 4.5 - 4.5 = 11.0s)
        self.wait(11.0)

        # =========================================================================
        # ĐOẠN 3 (`s5a_3.wav`): TỔNG CHÍNH XÁC 35.0 GIÂY
        # Kết quả phản biện Review: 6.33/10 (Top 45% ICLR) - Mở ra kỷ nguyên mới
        # =========================================================================
        
        # Thu nhỏ cụm bài báo đẩy sang góc trái (Thời gian: 2.0s)
        paper_cluster = Group(paper_img, paper_border, content_note_1, content_note_2)
        self.play(
            paper_cluster.animate.scale(0.65).to_edge(LEFT, buff=0.4).shift(DOWN * 0.1),
            run_time=2.0
        )
        
        # Bảng Reviewer độc lập bên phải (Thời gian: 2.0s)
        reviewer_box = RoundedRectangle(width=5.8, height=3.2, color=RED, fill_color=RED, fill_opacity=0.12).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)
        reviewer_title = Paragraph("Hội Nghị ICLR 2025 Review", font_size=25, color=RED, alignment="center").next_to(reviewer_box, UP, buff=0.15)
        self.play(Create(reviewer_box), Write(reviewer_title), run_time=2.0)
        
        # Gửi mũi tên nộp bài / Chờ đọc thoại (Thời gian: 1.5s)
        self.wait(1.5)
        
        # Hiển thị Điểm số ấn tượng (Thời gian: 2.0 + 2.0 + 2.0 = 6.0s)
        score_val = Paragraph("Điểm trung bình: 6.33 / 10", font_size=22, color=WHITE, alignment="center")
        ranking_val = Paragraph("Xếp hạng: Top ~45% bài nộp", font_size=22, color=GOLD, alignment="center")
        status_val = Paragraph("Vượt ngưỡng chấp nhận trung bình", font_size=22, color=GREEN, alignment="center")
        
        # Gộp cụm kết quả chấm điểm lại để dùng fit_in_box căn giữa hộp đỏ một cách tự động
        score_group = VGroup(score_val, ranking_val, status_val).arrange(DOWN, buff=0.25, aligned_edge=ORIGIN)
        fit_in_box(score_group, reviewer_box, padding=0.2)
        
        self.play(Write(score_val), run_time=2.0)
        self.play(Write(ranking_val), run_time=2.0)
        self.play(Write(status_val), run_time=2.0)
        
        # Bù giờ để ĐOẠN 3 tròn 35s (35.0 - 2.0 - 2.0 - 1.5 - 6.0 = 23.5s)
        self.wait(23.5)
        
        # Kết thúc scene (Thời gian dư này là quá trình chuyển cảnh, không tính vào mốc s5a_3)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)