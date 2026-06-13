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

class AutomationOfInnovationSection4a(Scene):
    def construct(self):
        # 1. AUDIO 1: Intro (6s)
        title = Text("Bài toán Cap Set", font_size=48, color=BLUE)
        self.play(Write(title), run_time=3)
        self.wait(3) # Tổng 6s
        self.play(FadeOut(title))

        # 2. AUDIO 2: Quy luật a+c=2b (18s)
        rule_formula = MathTex(r"a + c \equiv 2b \pmod 3", font_size=60, color=GREEN).shift(UP * 3)
        
        # SỬA LẠI ĐOẠN NÀY: Dùng Paragraph kết hợp MathTex, ép căn dọc chính xác 
        # để tránh lỗi nhảy chữ tiếng Việt khi đi kèm ký tự toán học
        desc_line1 = Paragraph("Điều kiện: Không 3 điểm thẳng hàng, mọi điểm", font_size=25, alignment="center")
        desc_line2 = MathTex(r"x=(a_1,a_2,\ldots,a_n),\ a_i\in\{0,1,2\}", font_size=28)
        
        desc = VGroup(desc_line1, desc_line2).arrange(DOWN, buff=0.15, aligned_edge=ORIGIN)
        desc.next_to(rule_formula, DOWN, buff=0.2)
        
        self.play(Write(rule_formula), Write(desc), run_time=4)
        
        # Grid n=2 (giữ nguyên đến hết cảnh này)
        grid_n2 = self.create_grid_n2().scale(0.8).shift(DOWN * 0.8)
        self.play(Create(grid_n2), run_time=4)
        self.wait(10) # Tổng 18s

        # 3. AUDIO 3: Mô phỏng n=2 (16s)
        line = Line(grid_n2[0][0].get_center(), grid_n2[8][0].get_center(), color=RED, stroke_width=6)
        self.play(Create(line), run_time=3)
        self.play(
            grid_n2[0][0].animate.set_color(RED), 
            grid_n2[4][0].animate.set_color(RED), 
            grid_n2[8][0].animate.set_color(RED), 
            run_time=3
        )
        self.wait(4)
        self.play(FadeOut(line))
        
        # Hiện tập 4 điểm hình học (Tập thoả mãn Cap Set trong không gian 2D)
        for i in [0, 1, 3, 4]: 
            grid_n2[i][0].set_color(GREEN)
        self.wait(6) # Tổng 16s

        # 4. AUDIO 4: Bùng nổ 3^n (18s)
        self.play(FadeOut(grid_n2), FadeOut(rule_formula), FadeOut(desc), run_time=2)
        
        # Đồng bộ cụm text tính toán số mũ bùng nổ chiều
        n_math = MathTex(r"n=8 \implies 3^8 = 6561", font_size=40)
        n_lbl = Text("điểm", font_size=32)
        n_text = VGroup(n_math, n_lbl).arrange(RIGHT, buff=0.2, aligned_edge=ORIGIN)
        n_text.set_color(GOLD) 
        
        self.play(Write(n_text), run_time=4)
        self.wait(12) # Tổng 18s
        self.play(FadeOut(n_text))

        # 5. AUDIO 5: Kỷ lục con người (17s)
        human_res = Paragraph("Kỷ lục con người (n=8): 496 điểm", font_size=36, color=BLUE, alignment="center")
        self.play(Write(human_res), run_time=5)
        self.wait(12) # Tổng 17s
        self.play(FadeOut(human_res))

        # 6. AUDIO 6: FunSearch (16s)
        ai_txt = Paragraph("FunSearch: Chiến lược tiến hóa", font_size=40, color=TEAL, alignment="center")
        self.play(Write(ai_txt), run_time=4)
        self.wait(12) # Tổng 16s
        self.play(FadeOut(ai_txt))

        # 7. AUDIO 7: Kết quả 512 > 496 (14s)
        res_line1 = Paragraph("Con người: 496 điểm", color=BLUE, font_size=32, alignment="center")
        res_line2 = Paragraph("FunSearch: 512 điểm (Đột phá mới)", color=GREEN, font_size=36, alignment="center")
        
        res_group = VGroup(res_line1, res_line2).arrange(DOWN, buff=0.8, aligned_edge=ORIGIN)
        self.play(FadeIn(res_group, shift=UP), run_time=4)
        self.wait(10) # Tổng 14s
        self.play(FadeOut(res_group))

        # 8. AUDIO 8: Outro (8s)
        outro = Paragraph("Kỷ nguyên mới của khám phá khoa học", font_size=36, color=BLUE, alignment="center")
        self.play(Write(outro), run_time=4)
        self.wait(4) # Tổng 8s

    def create_grid_n2(self):
        grid = VGroup()
        for x in range(3):
            for y in range(3):
                p = RIGHT * (x - 1) * 2.2 + UP * (y - 1) * 2.2
                d = Dot(p, radius=0.18)
                l = MathTex(f"({x},{y})", font_size=24).next_to(d, DOWN, buff=0.15)
                grid.add(VGroup(d, l))
        return grid