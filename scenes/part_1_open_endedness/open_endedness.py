from manim import *
import numpy as np
import os

# =========================================================================
# I. FOUNDATION CONFIG & UTILITY FUNCTIONS
# =========================================================================

# Cấu hình XeLaTeX làm bộ dịch mặc định cho LaTeX để hỗ trợ tiếng Việt
my_template = TexTemplate(tex_compiler="xelatex", output_format=".xdv")
my_template.add_to_preamble(r"\usepackage{xcolor}")
my_template.add_to_preamble(r"\usepackage{amsmath}")
config.tex_template = my_template


class VietnameseScene(Scene):
    def setup(self):
        config.tex_template = my_template
        super().setup()


class VietnameseMovingCameraScene(MovingCameraScene):
    def setup(self):
        config.tex_template = my_template
        super().setup()



def fit_in_box(mobject, box, padding=0.15):
    """
    Fits any mobject nicely inside a container box, scaling it down if necessary
    and centering it, to prevent screen overflow.
    """
    max_w = box.width - 2 * padding
    max_h = box.height - 2 * padding
    curr_w = mobject.width
    curr_h = mobject.height
    if curr_w > 0 and curr_h > 0:
        factor = min(1.0, max_w / curr_w, max_h / curr_h)
        mobject.scale(factor)
    mobject.move_to(box.get_center())
    return mobject


def load_safe_sound(scene, filename):
    """
    Safely adds a sound file if it exists, warning instead of crashing if missing.
    """
    audio_path = os.path.join(os.path.dirname(__file__), "assets", filename)
    if os.path.exists(audio_path):
        scene.add_sound(audio_path)
    else:
        print(f"[WARNING] Audio file not found at {audio_path}. Continuing without sound.")


# =========================================================================
# II. SCENE IMPLEMENTATIONS
# =========================================================================

class Phase1PetriDishVsClosedSystem(VietnameseScene):
    def construct(self):
        # 1. Load Safe Sound (Voiceover audio sync - 132.28 seconds)
        load_safe_sound(self, "Phase1_PetriDish_ClosedSystem.wav")

        # =====================================================================
        # PART 0: CINEMATIC INTRO SEQUENCE (00.00s - 28.00s)
        # =====================================================================
        # Technical dark background grid
        grid = NumberPlane(
            background_line_style={
                "stroke_color": GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.08
            }
        )

        intro_sub = Text(
            "KỶ NGUYÊN MỚI CỦA TRÍ TUỆ NHÂN TẠO",
            color=GOLD,
            font_size=18,
            weight=BOLD
        ).to_edge(UP, buff=1.8)

        intro_title = Text(
            "OPEN-ENDEDNESS",
            color=WHITE,
            font_size=46,
            weight=BOLD
        ).move_to(ORIGIN)

        intro_desc = Text(
            "Hành trình vượt ra ngoài giới hạn bế tắc của các Hệ thống Đóng",
            color=GRAY_A,
            font_size=16
        ).next_to(intro_title, DOWN, buff=0.5)

        # Draw intro elements
        self.play(Create(grid), run_time=1.5)
        self.play(FadeIn(intro_sub, shift=UP), run_time=1.5)
        self.play(Write(intro_title), run_time=2.0)
        self.play(FadeIn(intro_desc, shift=DOWN), run_time=1.5)
        self.wait(19.0) # Matches first 3 segments ending at 27.26s

        # Clean intro sequence
        self.play(
            FadeOut(grid),
            FadeOut(intro_sub),
            FadeOut(intro_title),
            FadeOut(intro_desc),
            run_time=2.0
        )
        self.wait(0.5)

        # =====================================================================
        # PART 1: LISA SIMPSON'S PETRI DISH (28.00s - 68.00s [Duration: 40s])
        # =====================================================================
        title_lisa = Text(
            "Đĩa Petri của Lisa Simpson (The Genesis Tub)", 
            color=BLUE_B,
            weight=BOLD
        ).scale(0.7).to_edge(UP, buff=0.8)

        # Draw a large Petri dish (Circle)
        circle = Circle(radius=2.5, color=BLUE, stroke_width=3)
        circle.set_fill(BLUE_E, opacity=0.05)

        # Dynamic Brownian micro-movement physics for living cells
        def make_vibrating_dot(pos, color, radius=0.08, keep_inside=True):
            dot = Dot(point=pos, color=color, radius=radius)
            def jitter(mob, dt):
                center = circle.get_center()
                # Random Brownian displacement
                mob.shift(np.array([
                    np.random.normal(0, 0.007),
                    np.random.normal(0, 0.007),
                    0
                ]))
                # Keep inside circle boundary dynamically if constraint is enabled
                if keep_inside:
                    curr_radius = circle.width / 2
                    dist = np.linalg.norm(mob.get_center() - center)
                    if dist > curr_radius - 0.12:
                        direction = (mob.get_center() - center) / dist
                        mob.move_to(center + direction * (curr_radius - 0.18))
            dot.add_updater(jitter)
            return dot

        # Dynamic link tracker that follows cells in real time
        def make_updating_line(dot_a, dot_b, color, opacity):
            line = Line(start=dot_a.get_center(), end=dot_b.get_center(), color=color, stroke_width=1.5).set_opacity(opacity)
            def update_line(mob):
                mob.put_start_and_end_on(dot_a.get_center(), dot_b.get_center())
            line.add_updater(update_line)
            return line

        # 28s - 40s: Render Petri dish and initial 4 cells (Segment 4 & 5)
        dots = VGroup()
        initial_positions = [
            np.array([0.4, 0.3, 0]),
            np.array([-0.5, -0.4, 0]),
            np.array([-0.2, 0.6, 0]),
            np.array([0.6, -0.5, 0])
        ]
        for pos in initial_positions:
            dots.add(make_vibrating_dot(pos, BLUE_B))

        self.play(Write(title_lisa), run_time=1.2)
        self.play(Create(circle), run_time=1.8)
        self.play(FadeIn(dots, scale=0.5), run_time=1.5)
        self.wait(7.5) # Reaches 40.00s

        # 40s - 48s: First cell division (Sprout new dots & connect with tracking lines)
        gen2_positions = [
            np.array([1.1, 0.7, 0]),
            np.array([-1.2, -0.8, 0]),
            np.array([-0.9, 1.1, 0]),
            np.array([1.3, -1.0, 0]),
            # Outer points (escaping the boundary)
            np.array([2.7, 1.0, 0]),
            np.array([-2.7, -1.2, 0]),
            np.array([1.6, 2.2, 0]),
            np.array([-1.0, -2.4, 0])
        ]
        
        gen2_dots = VGroup()
        gen2_lines = VGroup()
        for i, pos in enumerate(gen2_positions[:4]):
            parent_dot = dots[i]
            dot = make_vibrating_dot(pos, BLUE_A)
            line = make_updating_line(parent_dot, dot, BLUE_D, 0.45)
            gen2_dots.add(dot)
            gen2_lines.add(line)

        self.play(
            LaggedStart(*[Create(l) for l in gen2_lines], lag_ratio=0.15),
            LaggedStart(*[FadeIn(d, scale=0.3) for d in gen2_dots], lag_ratio=0.15),
            run_time=2.5
        )
        self.wait(5.5) # Reaches 48.00s

        # 48s - 62s: Second cell division & escaping boundary constraints
        gen3_dots = VGroup()
        gen3_lines = VGroup()
        for i, pos in enumerate(gen2_positions[4:]):
            parent_dot = gen2_dots[i % len(gen2_dots)]
            # Set keep_inside=False for outer cells to visual escape closed loops
            dot = make_vibrating_dot(pos, BLUE_A, keep_inside=False)
            line = make_updating_line(parent_dot, dot, BLUE_D, 0.45)
            gen3_dots.add(dot)
            gen3_lines.add(line)

        cross_lines = VGroup()
        cross_pairs = [(dots[0], gen2_dots[1]), (dots[1], gen2_dots[2]), (gen2_dots[0], gen2_dots[3])]
        for d1, d2 in cross_pairs:
            line = make_updating_line(d1, d2, BLUE_E, 0.35)
            cross_lines.add(line)

        self.play(
            LaggedStart(*[Create(l) for l in gen3_lines], lag_ratio=0.15),
            LaggedStart(*[FadeIn(d, scale=0.3) for d in gen3_dots], lag_ratio=0.15),
            Create(cross_lines),
            run_time=3.0
        )
        self.wait(11.0) # Reaches 62.00s

        # 62s - 68s: Move the living network to the left
        petri_group = VGroup(circle, title_lisa, dots, gen2_dots, gen2_lines, gen3_dots, gen3_lines, cross_lines)
        self.play(
            petri_group.animate.scale(0.55).shift(LEFT * 3.5 + DOWN * 0.5),
            run_time=2.5
        )
        self.wait(3.5) # Reaches 68.00s

        # =====================================================================
        # PART 2: SPLIT SCREEN & CLOSED SYSTEM LOSS SATURATION (68.00s - 104.00s [Duration: 36s])
        # =====================================================================
        # Closed System Plot on the right
        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 5, 1],
            x_length=5,
            y_length=3.5,
            axis_config={"include_tip": True, "color": GRAY}
        ).shift(RIGHT * 3.5 + DOWN * 0.5)

        x_lbl = MathTex("t", color=WHITE).scale(0.7).next_to(axes.x_axis.get_end(), DOWN, buff=0.1)
        y_lbl = MathTex(r"\text{Loss}", color=WHITE).scale(0.7).next_to(axes.y_axis.get_end(), LEFT, buff=0.1)
        
        title_closed = Text(
            "Hệ thống Đóng (Closed System)", 
            color=RED,
            weight=BOLD
        ).scale(0.52).next_to(axes, UP, buff=0.4)

        loss_curve = axes.plot(
            lambda x: 3.5 * np.exp(-0.8 * x) + 0.5,
            color=RED,
            x_range=[0, 7.5]
        )

        self.play(
            Create(axes),
            Write(x_lbl), Write(y_lbl),
            Write(title_closed),
            run_time=2.0
        )
        self.wait(6.0) # Reaches 76.00s (Segment 9)
        
        self.play(
            Create(loss_curve),
            run_time=4.0
        )
        self.wait(8.0) # Reaches 88.00s (Segment 10)
        
        # Blinking highlight at flatline saturation point
        flat_dot = Dot(point=axes.c2p(7.0, 0.5), color=YELLOW, radius=0.08)
        self.play(FadeIn(flat_dot), run_time=0.5)
        self.play(Flash(flat_dot, color=YELLOW, line_length=0.2, num_lines=12), run_time=1.5)

        # Draw red transparent "FREEZE" overlay representing AI model lock
        freeze_rect = SurroundingRectangle(loss_curve, color=RED, fill_color=RED, fill_opacity=0.2, stroke_width=2.5)
        freeze_label = Text(
            "FREEZE / ĐÓNG BĂNG MÔ HÌNH", 
            color=RED_A,
            weight=BOLD
        ).scale(0.55).move_to(freeze_rect.get_center())

        self.play(
            Create(freeze_rect),
            Write(freeze_label),
            run_time=2.0
        )
        self.wait(10.0) # Reaches 102.00s (Segment 11 & 12)

        # Clean the stage
        self.play(
            FadeOut(petri_group),
            FadeOut(axes), FadeOut(x_lbl), FadeOut(y_lbl), FadeOut(title_closed),
            FadeOut(loss_curve), FadeOut(freeze_rect), FadeOut(freeze_label), FadeOut(flat_dot),
            run_time=1.5
        )
        self.wait(0.5) # Reaches 104.00s

        # =====================================================================
        # PART 3: COMPARISON TABLE (104.00s - 132.28s [Duration: 28.28s])
        # =====================================================================
        # Comparison Table Title
        title_table = Text(
            "So sánh Đặc tính Bản chất của Hai Hệ thống", 
            color=GOLD,
            weight=BOLD
        ).to_edge(UP, buff=0.5).scale(0.7)

        # Table cell utility
        def make_cell(text, x, y, w, h, color=WHITE, font_size=20, is_bold=False):
            box = RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=GRAY_E, fill_color=GRAY_D, fill_opacity=0.05).move_to([x, y, 0])
            if is_bold:
                lbl = Text(text, color=color, font_size=font_size, weight=BOLD)
            else:
                lbl = Text(text, color=color, font_size=font_size)
            fit_in_box(lbl, box, padding=0.1)
            return VGroup(box, lbl)

        col_x = [-4.5, -1.0, 3.5]
        
        # Header Row
        h1 = make_cell("Đặc tính", col_x[0], 1.5, 2.3, 0.7, color=GOLD, is_bold=True)
        h2 = make_cell("Hệ thống Đóng (Closed)", col_x[1], 1.5, 4.3, 0.7, color=RED, is_bold=True)
        h3 = make_cell("Hệ thống Mở (Open-Ended)", col_x[2], 1.5, 4.3, 0.7, color=GREEN, is_bold=True)
        
        # Row 1: Data Space
        r1_1 = make_cell("Không gian dữ liệu", col_x[0], 0.5, 2.3, 0.9, color=WHITE, is_bold=True)
        r1_2 = make_cell("Tĩnh, cố định và giới hạn (In-Distribution)", col_x[1], 0.5, 4.3, 0.9, color=GRAY_A)
        r1_3 = make_cell("Động, liên tục mở rộng và tự sản sinh vô tận", col_x[2], 0.5, 4.3, 0.9, color=GREEN_B)

        # Row 2: Optimization Goal
        r2_1 = make_cell("Mục tiêu tối ưu", col_x[0], -0.5, 2.3, 0.9, color=WHITE, is_bold=True)
        r2_2 = make_cell("Hàm mục tiêu cố định do con người định nghĩa", col_x[1], -0.5, 4.3, 0.9, color=GRAY_A)
        r2_3 = make_cell("Mục tiêu động, tự sinh thử thách tăng dần", col_x[2], -0.5, 4.3, 0.9, color=GREEN_B)

        # Row 3: Evolution Ability
        r3_1 = make_cell("Khả năng tiến hóa", col_x[0], -1.5, 2.3, 0.9, color=WHITE, is_bold=True)
        r3_2 = make_cell("Giới hạn sau hội tụ; cần kỹ sư nâng cấp thủ công", col_x[1], -1.5, 4.3, 0.9, color=GRAY_A)
        r3_3 = make_cell("Tự vận hành, liên tục kiến tạo tạo tác phức tạp", col_x[2], -1.5, 4.3, 0.9, color=GREEN_B)

        # Golden-Green Highlight on Open-Ended Column
        open_column_highlight = RoundedRectangle(
            width=4.5, height=3.8, corner_radius=0.1, 
            color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.06
        ).move_to([col_x[2], -0.05, 0])

        # Perfectly timed row fade-ins matching the detailed Vietnamese speech segments
        self.play(Write(title_table), run_time=1.5)
        self.wait(1.5) # Reaches 107.00s

        # Header
        self.play(Create(h1[0]), Write(h1[1]), Create(h2[0]), Write(h2[1]), Create(h3[0]), Write(h3[1]), run_time=2.0)
        self.wait(1.0) # Reaches 110.00s

        # Row 1
        self.play(Create(r1_1[0]), Write(r1_1[1]), Create(r1_2[0]), Write(r1_2[1]), Create(r1_3[0]), Write(r1_3[1]), run_time=2.0)
        self.wait(1.0) # Reaches 113.00s

        # Row 2
        self.play(Create(r2_1[0]), Write(r2_1[1]), Create(r2_2[0]), Write(r2_2[1]), Create(r2_3[0]), Write(r2_3[1]), run_time=2.0)
        self.wait(1.0) # Reaches 116.00s

        # Row 3
        self.play(Create(r3_1[0]), Write(r3_1[1]), Create(r3_2[0]), Write(r3_2[1]), Create(r3_3[0]), Write(r3_3[1]), run_time=2.0)
        self.wait(2.0) # Reaches 120.00s

        # Highlight Open Column
        self.play(Create(open_column_highlight), run_time=2.0)
        self.wait(8.0) # Reaches 130.00s

        # End of Phase 1
        self.play(
            FadeOut(title_table),
            FadeOut(h1), FadeOut(h2), FadeOut(h3),
            FadeOut(r1_1), FadeOut(r1_2), FadeOut(r1_3),
            FadeOut(r2_1), FadeOut(r2_2), FadeOut(r2_3),
            FadeOut(r3_1), FadeOut(r3_2), FadeOut(r3_3),
            FadeOut(open_column_highlight),
            run_time=2.0
        )
        self.wait(0.28) # Exact 132.28 seconds match!


# =========================================================================
# III. SCAFFOLDS FOR REMAINDER SCENES (PHASES 2 TO 7)
# =========================================================================

class Phase2NethackAGI(VietnameseMovingCameraScene):
    def construct(self):
        title = Text("Phase 2: Điểm mù 1.7% tại NetHack & Bản chất AGI", color=GOLD, weight=BOLD).scale(0.7)
        self.play(Write(title))
        self.wait(2.0)
        self.play(FadeOut(title))


class Phase3MathOpenEndedness(VietnameseScene):
    def construct(self):
        title = Text("Phase 3: Khung toán học chặt chẽ của tính mở (ICML 2024)", color=GOLD, weight=BOLD).scale(0.7)
        self.play(Write(title))
        self.wait(2.0)
        self.play(FadeOut(title))


class Phase4ObjectiveSteppingStones(VietnameseScene):
    def construct(self):
        title = Text("Phase 4: Nghịch lý mục tiêu & Lý thuyết Bước đệm", color=GOLD, weight=BOLD).scale(0.7)
        self.play(Write(title))
        self.wait(2.0)
        self.play(FadeOut(title))


class Phase5XLandGoldilocks(VietnameseScene):
    def construct(self):
        title = Text("Phase 5: Dự án XLand 2.0 & Vùng Goldilocks", color=GOLD, weight=BOLD).scale(0.7)
        self.play(Write(title))
        self.wait(2.0)
        self.play(FadeOut(title))


class Phase6FoundationEvolution(VietnameseScene):
    def construct(self):
        title = Text("Phase 6: FM làm động cơ tiến hóa mở", color=GOLD, weight=BOLD).scale(0.7)
        self.play(Write(title))
        self.wait(2.0)
        self.play(FadeOut(title))


class Phase7FoundationWorldModels(VietnameseMovingCameraScene):
    def construct(self):
        title = Text("Phase 7: Dịch chuyển sang Foundation World Models", color=GOLD, weight=BOLD).scale(0.7)
        self.play(Write(title))
        self.wait(2.0)
        self.play(FadeOut(title))
