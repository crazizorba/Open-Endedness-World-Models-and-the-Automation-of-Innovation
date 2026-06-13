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

class AutomationOfInnovationSection6(Scene):
    def construct(self):
        # 1. AUDIO 1: Tổng kết tác động (17s)
        title = Text("Tác động của AI trong Khoa học", font_size=40, color=BLUE).to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        
        # Chuyển đổi sang Paragraph, giữ nguyên lề trái để tạo khối danh sách đẹp mắt
        impact_list = VGroup(
            Paragraph("• Tự động hóa khám phá", font_size=32),
            Paragraph("• Vượt giới hạn con người", font_size=32),
            Paragraph("• Khả năng mở rộng quy mô", font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.8).shift(LEFT * 0.5)
        
        self.play(FadeIn(impact_list, shift=RIGHT), run_time=5)
        self.wait(10) 
        self.play(FadeOut(title), FadeOut(impact_list))

        # 2. AUDIO 2: Vai trò con người (13s)
        human_role = Paragraph("Vai trò của con người là gì?", font_size=40, color=YELLOW, alignment="center").shift(UP * 1)
        
        # Dùng Paragraph căn giữa để thay thế text xuống dòng chứa ký tự \n gốc
        role_desc = Paragraph(
            "Con người là người đặt câu hỏi,\nkiểm chứng và định hướng AI.", 
            font_size=32, alignment="center"
        ).next_to(human_role, DOWN, buff=0.5)
        
        self.play(Write(human_role), run_time=3)
        self.play(FadeIn(role_desc), run_time=3)
        self.wait(7)
        self.play(FadeOut(human_role), FadeOut(role_desc))

        # 3. AUDIO 3: Tương lai & Kêu gọi (22s)
        future_title = Paragraph("Kỷ nguyên đồng sáng tạo", font_size=42, color=GOLD, alignment="center")
        self.play(GrowFromCenter(future_title), run_time=3)
        self.play(FadeOut(future_title), run_time=1.5)
        
        # Cấu trúc lại nhóm liên kết công thức đồng sáng tạo 
        ai_part = Paragraph("AI (Tốc độ & Dữ liệu)", color=GREEN, font_size=28, alignment="center")
        plus_sign = Paragraph("+", font_size=55, alignment="center")
        human_part = Paragraph("Con người (Sáng tạo & Đạo đức)", color=BLUE, font_size=28, alignment="center")
        
        connection = VGroup(ai_part, plus_sign, human_part).arrange(DOWN, buff=0.4, aligned_edge=ORIGIN).shift(DOWN * 0.2)
        
        self.play(FadeIn(connection), run_time=5)
        self.wait(13)
        
        self.wait(2)