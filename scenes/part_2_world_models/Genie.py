from manim import *
import numpy as np
import os


# Set default TexTemplate to support Vietnamese using XeLaTeX
my_template = TexTemplate(tex_compiler="xelatex", output_format=".xdv")
my_template.add_to_preamble(r"\usepackage{xcolor}")
my_template.add_to_preamble(r"\usepackage{amsmath}")
config.tex_template = my_template

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

class Section1IntroductionPart1(Scene):
    def construct(self):
        # Add audio
        self.add_sound(os.path.join(os.path.dirname(__file__), "assets", "Genie_Intro_Part1.wav"))

        # =========================================================================
        # PHASE 0: OPEN-ENDEDNESS PRE-INTRO QUESTION (0s - 11s)
        # =========================================================================
        question = Tex(
            r"\text{Làm sao để hiện thực hóa \textbf{Open-Endedness} mà Tim vừa đề cập?}",
            color=WHITE
        ).scale(0.85).to_edge(UP, buff=1.0)

        agent_box = RoundedRectangle(width=5.2, height=1.6, color=GRAY_C, fill_color=GRAY_D, fill_opacity=0.1).shift(LEFT * 3.2 + DOWN * 0.5)
        agent_label = Tex(
            r"\text{Nâng cấp thuật toán của Agent}",
            color=GRAY_A
        ).scale(0.7)
        fit_in_box(agent_label, agent_box)
        agent_cross = Cross(agent_box, stroke_color=RED, stroke_width=6)

        env_box = RoundedRectangle(width=5.2, height=1.6, color=GREEN_C, fill_color=GREEN_E, fill_opacity=0.15).shift(RIGHT * 3.2 + DOWN * 0.5)
        env_label = Tex(
            r"\text{\textbf{Tái định nghĩa Môi trường}}",
            color=GREEN_C
        ).scale(0.75)
        fit_in_box(env_label, env_box)

        # 0.5s: Write question
        self.wait(0.5)
        self.play(Write(question), run_time=1.5)
        
        # Wait until 3.0s (already elapsed: 2.0s -> wait 1.0s)
        self.wait(1.0)
        
        # 3.0s: Show Agent Option
        self.play(Create(agent_box), Write(agent_label), run_time=1.0)
        
        # 4.0s: Draw Red Cross over Agent Option
        self.play(Create(agent_cross), run_time=0.8)
        
        # Wait until 6.0s (already elapsed: 4.8s -> wait 1.2s)
        self.wait(1.2)
        
        # 6.0s: Show Environment Option
        self.play(Create(env_box), Write(env_label), run_time=1.0)
        
        # 7.0s: Highlight Environment Option by animating stroke color and width
        self.play(env_box.animate.set_stroke(color=GREEN, width=6), run_time=1.0)
        
        # Wait until 9.5s (already elapsed: 8.0s -> wait 1.5s)
        self.wait(1.5)
        
        # 9.5s: Fade out all intro elements to clear screen (finishes at 10.5s)
        self.play(
            FadeOut(question),
            FadeOut(agent_box), FadeOut(agent_label), FadeOut(agent_cross),
            FadeOut(env_box), FadeOut(env_label),
            run_time=1.0
        )
        
        # Wait until 11.0s (already elapsed: 10.5s -> wait 0.5s)
        self.wait(0.5)

        # =========================================================================
        # PHASE 1: ALAN WATTS QUOTE (1972)
        # =========================================================================
        # Title Alan Watts
        title_watts = Tex(r"\text{\textbf{Alan Watts (1972)}}", color=GOLD).to_edge(UP, buff=1.0).scale(1.1)
        
        quote_watts = Tex(
            r"``The relationship between the organism and the environment is transactional --\\",
            r"the environment grows the organism, and the organism creates the environment.''",
            tex_to_color_map={
                "organism": BLUE_C,
                "environment": GREEN_C,
                "grows": GOLD,
                "creates": GOLD
            }
        ).scale(0.7).arrange(DOWN, buff=0.15).next_to(title_watts, DOWN, buff=0.7)

        organism_box = RoundedRectangle(width=3.2, height=1.2, color=BLUE_C).shift(LEFT * 3.5 + DOWN * 1.5)
        organism_label = Tex(r"\text{\textbf{Sinh vật}}", color=BLUE_C).move_to(organism_box.get_center()).scale(0.75)
        fit_in_box(organism_label, organism_box)

        environment_box = RoundedRectangle(width=3.8, height=1.2, color=GREEN_C).shift(RIGHT * 3.5 + DOWN * 1.5)
        environment_label = Tex(r"\text{\textbf{Môi trường}}", color=GREEN_C).move_to(environment_box.get_center()).scale(0.75)
        fit_in_box(environment_label, environment_box)

        arrow_creates = ArcBetweenPoints(
            start=organism_box.get_edge_center(UP) + RIGHT * 0.2,
            end=environment_box.get_edge_center(UP) + LEFT * 0.2,
            angle=-TAU/6,  
            color=GOLD
        ).add_tip(tip_length=0.2)
        creates_label = Tex(r"\text{Tạo ra}", color=GOLD).next_to(arrow_creates, UP, buff=0.1).scale(0.7)

        arrow_grows = ArcBetweenPoints(
            start=environment_box.get_edge_center(DOWN) + LEFT * 0.2,
            end=organism_box.get_edge_center(DOWN) + RIGHT * 0.2,
            angle=-TAU/6,  
            color=GOLD
        ).add_tip(tip_length=0.2)
        grows_label = Tex(r"\text{Nuôi dưỡng}", color=GOLD).next_to(arrow_grows, DOWN, buff=0.1).scale(0.7)
        
        # Timeline: 11s - Alan Watts Title
        self.play(Write(title_watts))
        
        # Timeline: 19s - Alan Watts Quote & Boxes
        self.wait(7.0)
        self.play(
            FadeIn(quote_watts),
            Create(organism_box), Write(organism_label),
            Create(environment_box), Write(environment_label)
        )
        
        # Timeline: 24s - Environment -> Organism arrow (arrow_grows)
        self.wait(3.5)
        self.play(Create(arrow_grows), Write(grows_label))
        
        # Timeline: 26s - Organism -> Environment arrow (arrow_creates)
        self.wait(1.0)
        self.play(Create(arrow_creates), Write(creates_label))

        # =========================================================================
        # PHASE 2: JEFF CLUNE QUOTE (2019)
        # =========================================================================
        # Timeline: 40s - Jeff Clune Title (Fade out Watts elements at 39s)
        self.wait(12.0)
        self.play(
            FadeOut(title_watts), FadeOut(quote_watts),
            FadeOut(organism_box), FadeOut(organism_label),
            FadeOut(environment_box), FadeOut(environment_label),
            FadeOut(arrow_creates), FadeOut(creates_label),
            FadeOut(arrow_grows), FadeOut(grows_label)
        )
        
        title_clune = Tex(r"\text{\textbf{Jeff Clune (2019)}}", color=GOLD).to_edge(UP, buff=1.0).scale(1.1)
        
        quote_clune = Tex(
            r"``\textbf{Open-Ended Darwin-Complete Search Spaces}: spaces in which}\\",
            r"any \textbf{computable environment} can be \textbf{simulated}, allowing for\\",
            r"the \textbf{emergence} of a diverse range of \textbf{intelligent behaviors.}''",
            tex_to_color_map={
                "Open-Ended Darwin-Complete Search Spaces": ORANGE, 
                "computable environment": GREEN_C,                  
                "simulated": GOLD,                                 
                "emergence": BLUE_C,                                
                "intelligent behaviors.": ORANGE                    
            }
        ).scale(0.7).arrange(DOWN, buff=0.15).shift(UP * 0.5)

        explanation_clune = Tex(r"\text{Không gian tìm kiếm vô hạn, nơi mọi môi trường có thể lập trình đều được mô phỏng}", color=GRAY_A).scale(0.75).shift(DOWN * 1.5)

        self.play(Write(title_clune))
        
        # Timeline: 49s - Quote & Explanation
        self.wait(8.0)
        self.play(FadeIn(quote_clune, shift=UP * 0.5), Write(explanation_clune))

        # =========================================================================
        # PHASE 3: FOUNDATION WORLD MODELS INTRODUCTION
        # =========================================================================
        # Timeline: 1:05s (65s) - Foundation World Model Title (Fade out Clune at 64s)
        self.wait(13.5)
        self.play(
            FadeOut(title_clune), FadeOut(quote_clune), FadeOut(explanation_clune)
        )
        
        title_fwm = Tex(r"\text{\textbf{02. Foundation World Models}}", color=GOLD).to_edge(UP, buff=1.0).scale(1.1)
        
        intro_text = Tex(
            r"``Tương tự như cách LLM hiểu ngôn ngữ, một Foundation World Model\\",
            r"học cách xây dựng một bộ mô phỏng về quy luật vật lý và hành vi của thế giới.''",
            tex_to_color_map={
                "Foundation World Model": GOLD 
            }
        ).scale(0.68).arrange(DOWN, buff=0.15).shift(UP * 1.5)

        # Define the components of the formula separately for correct color and target properties
        f_part = MathTex(r"f:", font_size=42)
        state_part = MathTex(r"\text{State}", color=BLUE_C, font_size=42)
        times_part = MathTex(r"\times", font_size=42)
        action_part = MathTex(r"\text{Action}", color=ORANGE, font_size=42)
        arrow_part = MathTex(r"\rightarrow", font_size=42)
        dist_part = MathTex(r"\text{State Distribution}", color=GREEN_C, font_size=42)

        # Group and arrange them horizontally
        formula_fwm = VGroup(f_part, state_part, times_part, action_part, arrow_part, dist_part).arrange(RIGHT, buff=0.15).shift(DOWN * 0.2)

        # Surrounding boxes targeting the individual components
        state_box = SurroundingRectangle(state_part, color=BLUE, buff=0.1, corner_radius=0.1)
        action_box = SurroundingRectangle(action_part, color=ORANGE, buff=0.1, corner_radius=0.1)
        output_box = SurroundingRectangle(dist_part, color=GREEN, buff=0.1, corner_radius=0.1)
        
        intervention_label = Tex(r"\text{Interventions (Can thiệp chủ động)}", color=ORANGE).shift(DOWN * 2.0 + LEFT * 1.2).scale(0.75)
        
        intervention_arrow = ArcBetweenPoints(
            start=intervention_label.get_top() + RIGHT * 0.3,
            end=action_box.get_bottom() + DOWN * 0.05,
            angle=-TAU/10,
            color=ORANGE
        ).add_tip(tip_length=0.18)

        explanation_fwm = Tex(
            r"\text{Mô hình dự đoán phân phối trạng thái tiếp theo dựa trên trạng thái hiện tại và hành động}", 
            color=GRAY_A
        ).scale(0.7).next_to(formula_fwm, DOWN, buff=2.5)

        self.play(Write(title_fwm))
        
        # Timeline: 1:10s (70s) - Text "Tương tự..."
        self.wait(4.0)
        self.play(FadeIn(intro_text, shift=UP * 0.2))
        
        # Timeline: 1:20s (80s) - Formula f:...
        self.wait(9.0)
        self.play(Write(formula_fwm), run_time=1.5)
        self.play(Create(state_box), Create(action_box), Create(output_box))
        
        # Timeline: 1:28s (88s) - Interventions arrow
        self.wait(5.5)
        self.play(FadeIn(intervention_label, shift=UP * 0.2), Create(intervention_arrow))
        self.play(action_box.animate.set_stroke(width=4), run_time=0.5) 
        self.play(Write(explanation_fwm))
        
        # Wait until the audio ends (95.2s)
        self.wait(4.2)


class Section1IntroductionPart2(Scene):
    def construct(self):
        # Add audio
        self.add_sound(os.path.join(os.path.dirname(__file__), "assets", "Genie_Intro_Part2.wav"))

        # =========================================================================
        # PHASE 4: MODEL COMPARISON TABLE
        # =========================================================================
        title_table = Tex(r"\text{\textbf{So sánh các Model Class hiện nay}}", color=WHITE).to_edge(UP, buff=1.0).scale(1.1)

        col_x = [-4.0, -0.8, 2.5, 5.5]
        row_y = [1.8, 0.6, -0.6, -1.8]

        headers = [
            Tex(r"\text{\textbf{Model Class}}", color=GOLD).scale(0.85).move_to([col_x[0], row_y[0], 0]),
            Tex(r"\text{\textbf{Training Data}}", color=GOLD).scale(0.85).move_to([col_x[1], row_y[0], 0]),
            Tex(r"\text{\textbf{Controllability}}", color=GOLD).scale(0.85).move_to([col_x[2], row_y[0], 0])
        ]

        r1_class = Tex(r"\text{World Models}", color=WHITE).scale(0.8).move_to([col_x[0], row_y[1], 0])
        r1_data = Tex(r"\text{Video + Actions}", color=WHITE).scale(0.8).move_to([col_x[1], row_y[1], 0])
        r1_control = Tex(r"\text{Frame-level}", color=WHITE).scale(0.8).move_to([col_x[2], row_y[1], 0])
        r1_ex = Tex(r"\text{e.g. GAIA-2}", color=GRAY).scale(0.75).move_to([col_x[3], row_y[1], 0])

        r1_drawback_box = Rectangle(width=3, height=0.5, color=RED).move_to(r1_data.get_center())
        r1_drawback_lbl = Tex(r"\text{Cần nhãn hành động (Costly)}", color=RED).scale(0.55).next_to(r1_drawback_box, DOWN, buff=0.1)

        r2_class = Tex(r"\text{Video Models}", color=WHITE).scale(0.8).move_to([col_x[0], row_y[2], 0])
        r2_data = Tex(r"\text{Video + Text}", color=WHITE).scale(0.8).move_to([col_x[1], row_y[2], 0])
        r2_control = Tex(r"\text{Video-level}", color=WHITE).scale(0.8).move_to([col_x[2], row_y[2], 0])
        r2_ex = Tex(r"\text{e.g. Veo 2}", color=GRAY).scale(0.75).move_to([col_x[3], row_y[2], 0])

        r2_drawback_box = Rectangle(width=2.4, height=0.5, color=RED).move_to(r2_control.get_center())
        r2_drawback_lbl = Tex(r"\text{Không có frame-level control}", color=RED).scale(0.55).next_to(r2_drawback_box, DOWN, buff=0.1)

        r3_class = Tex(r"\text{\textbf{Genie}}", color=GOLD).scale(0.85).move_to([col_x[0], row_y[3], 0])
        r3_data = Tex(r"\text{Video}", color=GOLD).scale(0.85).move_to([col_x[1], row_y[3], 0])
        r3_control = Tex(r"\text{Frame-level}", color=GOLD).scale(0.85).move_to([col_x[2], row_y[3], 0])

        genie_highlight = Rectangle(width=12.2, height=0.65, color=GOLD_E, fill_color=GOLD_E, fill_opacity=0.25).move_to([0.0, row_y[3], 0]).set_stroke(GOLD, width=1.5)
        genie_label_desc = Tex(r"\text{\textbf{Tối ưu: Chỉ cần Video \& Đạt được Frame-level control}}", color=GOLD).scale(0.75).move_to([0.0, -2.9, 0])

        line_header_top = Line(start=[-5.5, 2.2, 0], end=[6.5, 2.2, 0], color=GRAY)
        line_top = Line(start=[-5.5, 1.2, 0], end=[6.5, 1.2, 0], color=GRAY)
        line_bottom = Line(start=[-5.5, -2.4, 0], end=[6.5, -2.4, 0], color=GRAY)

        # Timeline: 0s - Title
        self.play(Write(title_table))
        self.play(
            Create(line_header_top), 
            Create(line_top), 
            Create(line_bottom),
            run_time=1.0
        )
        self.play(*[Write(h) for h in headers], run_time=1.0)

        # -----------------------------------------------------------------
        # HÀNG 1: World Models (e.g. GAIA-2)
        # -----------------------------------------------------------------
        # Timeline: 12s - Row 1 class + ex
        self.wait(9.0)
        self.play(Write(r1_class), Write(r1_ex), run_time=1.0)
        
        # Timeline: 16s - Row 1 Frame-level control
        self.wait(3.0)
        self.play(Write(r1_control), run_time=1.0)

        # Timeline: 21s - Row 1 Video-Action + box đỏ + drawback
        self.wait(4.0)
        self.play(
            Write(r1_data), 
            Create(r1_drawback_box), 
            Write(r1_drawback_lbl),
            run_time=1.5
        )

        # -----------------------------------------------------------------
        # HÀNG 2: Video Models (e.g. Veo 2)
        # -----------------------------------------------------------------
        # Timeline: 30s - Row 2 class + ex
        self.wait(7.5)
        self.play(Write(r2_class), Write(r2_ex), run_time=1.0)
        
        # Timeline: 36s - Row 2 Video + Text
        self.wait(5.0)
        self.play(Write(r2_data), run_time=1.0)

        # Timeline: 41s - Row 2 Video-level + box đỏ + drawback
        self.wait(4.0)
        self.play(
            Write(r2_control), 
            Create(r2_drawback_box), 
            Write(r2_drawback_lbl),
            run_time=1.5
        )

        # -----------------------------------------------------------------
        # HÀNG 3: GENIE
        # -----------------------------------------------------------------    
        # Timeline: 51s - Row 3 highlight + Genie class text
        self.wait(8.5)
        self.play(FadeIn(genie_highlight, scale=0.9), Write(r3_class), run_time=1.0)
        
        # Timeline: 58s - Row 3 Video data text
        self.wait(6.0)
        self.play(Write(r3_data), run_time=1.0)
        
        # Timeline: 1:04s (64s) - Row 3 control + summary description
        self.wait(5.0)
        self.play(Write(r3_control), Write(genie_label_desc), run_time=1.5)

        # =========================================================================
        # PHASE 5: GENIE GOAL DIAGRAM
        # =========================================================================
        # Timeline: 1:08s (68s) - Title Goal (FadeOut comparison table at 67s)
        self.wait(1.5)
        self.play(
            FadeOut(title_table), FadeOut(line_header_top), FadeOut(line_top), FadeOut(line_bottom),
            FadeOut(genie_highlight), FadeOut(genie_label_desc),
            *[FadeOut(h) for h in headers],
            FadeOut(r1_class), FadeOut(r1_data), FadeOut(r1_control), FadeOut(r1_ex), FadeOut(r1_drawback_box), FadeOut(r1_drawback_lbl),
            FadeOut(r2_class), FadeOut(r2_data), FadeOut(r2_control), FadeOut(r2_ex), FadeOut(r2_drawback_box), FadeOut(r2_drawback_lbl),
            FadeOut(r3_class), FadeOut(r3_data), FadeOut(r3_control),
            run_time=1.0
        )

        title_goal = Tex(r"\text{\textbf{Mục tiêu của Genie}}", color=GOLD).to_edge(UP, buff=1.0).scale(1.1)

        # Split desc_goal into word-by-word groups for sequential text-diagram sync
        part1_specs = [
            ("``Huấn", WHITE, False),
            ("luyện", WHITE, False),
            ("một", WHITE, False),
            ("generative", GOLD, True),
            ("world", GOLD, True),
            ("model", GOLD, True),
            ("từ", WHITE, False),
            ("internet", ORANGE, True),
            ("videos,", ORANGE, True)
        ]
        desc_part1 = VGroup(*[
            Tex(rf"\text{{\textbf{{{text}}}}}" if is_bold else rf"\text{{{text}}}", color=col)
            for text, col, is_bold in part1_specs
        ]).arrange(RIGHT, buff=0.08).scale(0.7)

        part2_specs = [
            ("có", WHITE, False),
            ("thể", WHITE, False),
            ("được", WHITE, False),
            ("sử", WHITE, False),
            ("dụng", WHITE, False),
            ("làm", WHITE, False),
            ("simulator", PURPLE_C, True),
            ("cho", WHITE, False),
            ("embodied", GREEN, True),
            ("AGI", GREEN, True)
        ]
        desc_part2 = VGroup(*[
            Tex(rf"\text{{\textbf{{{text}}}}}" if is_bold else rf"\text{{{text}}}", color=col)
            for text, col, is_bold in part2_specs
        ]).arrange(RIGHT, buff=0.08).scale(0.7)

        part3_specs = [
            ("và", WHITE, False),
            ("một", WHITE, False),
            ("hình", WHITE, False),
            ("thức", WHITE, False),
            ("generative", BLUE, True),
            ("entertainment", BLUE, True),
            ("mới.''", WHITE, False)
        ]
        desc_part3 = VGroup(*[
            Tex(rf"\text{{\textbf{{{text}}}}}" if is_bold else rf"\text{{{text}}}", color=col)
            for text, col, is_bold in part3_specs
        ]).arrange(RIGHT, buff=0.08).scale(0.7)
        
        desc_goal = VGroup(desc_part1, desc_part2, desc_part3).arrange(DOWN, buff=0.15).next_to(title_goal, DOWN, buff=0.8)

        input_goal_box = RoundedRectangle(width=2.0, height=1.0, color=ORANGE, fill_color=ORANGE, fill_opacity=0.15).shift(LEFT * 4.5 + DOWN * 1.5)
        input_goal_label = Tex(r"\text{\textbf{Videos}}", color=ORANGE).scale(0.7)
        fit_in_box(input_goal_label, input_goal_box)

        genie_circle = Circle(radius=1.0, color=GOLD, fill_color=GOLD_E, fill_opacity=0.25).shift(LEFT * 1.0 + DOWN * 1.5)
        genie_circle_lbl = Tex(r"\text{\textbf{Genie}}", color=GOLD).move_to(genie_circle.get_center()).scale(0.8)

        arrow_input_to_genie = Arrow(start=input_goal_box.get_right(), end=genie_circle.get_left(), color=ORANGE, buff=0.15)

        robot_box = RoundedRectangle(width=3.2, height=1.0, color=GREEN, fill_color=GREEN_E, fill_opacity=0.15).shift(RIGHT * 3.5 + DOWN * 0.7)
        robot_lbl = Tex(r"\text{\textbf{Embodied AGI}}\\\text{(Robot Simulator)}", color=GREEN).scale(0.7)
        fit_in_box(robot_lbl, robot_box)

        arrow_genie_to_robot = Arrow(start=genie_circle.get_right() + UP * 0.2, end=robot_box.get_left(), color=GREEN, buff=0.15)

        game_box = RoundedRectangle(width=3.2, height=1.0, color=BLUE, fill_color=BLUE_E, fill_opacity=0.15).shift(RIGHT * 3.5 + DOWN * 2.3)
        game_lbl = Tex(r"\text{\textbf{Generative}}\\\text{\textbf{Entertainment}}", color=BLUE).scale(0.7)
        fit_in_box(game_lbl, game_box)

        arrow_genie_to_game = Arrow(start=genie_circle.get_right() + DOWN * 0.2, end=game_box.get_left(), color=BLUE, buff=0.15)

        self.play(Write(title_goal), run_time=1.0)
        
        # Timeline: 1:15s (75s) - Flow starts with sequential text + simultaneous boxes
        self.wait(6.0)
        
        # Step 1: Internet Videos text (word-by-word) and box Videos + Genie circle flow
        self.play(
            LaggedStart(*[Write(w) for w in desc_part1], lag_ratio=0.15, run_time=2.5),
            Create(input_goal_box), Write(input_goal_label),
            Create(arrow_input_to_genie), Create(genie_circle), Write(genie_circle_lbl),
            run_time=2.5
        )
        
        # Timeline: 1:25s (85s) - embodied AGI text (word-by-word) and Embodied AGI box
        self.wait(7.5)
        self.play(
            LaggedStart(*[Write(w) for w in desc_part2], lag_ratio=0.15, run_time=2.0),
            Create(arrow_genie_to_robot), Create(robot_box), Write(robot_lbl),
            run_time=2.0
        )
        
        # Timeline: 1:28s (88s) - Generative entertainment text (word-by-word) and Generative entertainment box
        self.wait(1.0)
        self.play(
            LaggedStart(*[Write(w) for w in desc_part3], lag_ratio=0.15, run_time=2.0),
            Create(arrow_genie_to_game), Create(game_box), Write(game_lbl),
            run_time=2.0
        )
        
        # Wait until audio ends (95.0s)
        self.wait(5.0)


class Section21Methodology(Scene):
    def construct(self):
        title = Tex(r"\text{\textbf{Genie: Three Core Components}}", color=WHITE).to_edge(UP, buff=1.0).scale(1.2)
        self.play(Write(title))
        self.wait(2.0)

        # Input frames stack (T frames)
        frames_stack = VGroup(*[
            Rectangle(width=1.3, height=0.9, fill_opacity=0.3, fill_color=BLUE_E, stroke_color=BLUE)
            for _ in range(3)
        ])
        for i, f in enumerate(frames_stack):
            f.shift(RIGHT * 0.12 * i + UP * 0.08 * i)
        frames_stack.move_to(LEFT * 6.5)
        frames_label = Tex(r"\text{Frames } $x_{1:T}$", color=WHITE).next_to(frames_stack, DOWN).scale(0.8)

        # Video Tokenizer box (Blue)
        tok_box = Rectangle(width=2.6, height=1.2, color=BLUE).shift(LEFT * 2.5 + UP * 1.5)
        tok_label = Tex(r"\text{\textbf{Video Tokenizer}} \\ \text{(Encoder)}", color=BLUE)
        fit_in_box(tok_label, tok_box)

        # LAM box (Orange)
        lam_box = Rectangle(width=2.6, height=1.2, color=ORANGE).shift(LEFT * 2.5 + DOWN * 1.5)
        lam_label = Tex(r"\text{\textbf{Latent Action Model}} \\ \text{(LAM)}", color=ORANGE)
        fit_in_box(lam_label, lam_box)

        # Dynamics Model box (Red)
        dyn_box = Rectangle(width=2.6, height=1.5, color=RED).shift(RIGHT * 2.1)
        dyn_label = Tex(r"\text{\textbf{Dynamics Model}} \\ \text{(MaskGIT)}", color=RED)
        fit_in_box(dyn_label, dyn_box)

        # Decoder box (Blue)
        dec_box = Rectangle(width=2.0, height=1.2, color=BLUE).shift(RIGHT * 6.3)
        dec_label = Tex(r"\text{\textbf{Tokenizer Decoder}} \\ \text{(Decoder)}", color=BLUE)
        fit_in_box(dec_label, dec_box)

        # Arrows
        arrow_to_tok = Arrow(start=frames_stack.get_right() + UP * 0.2, end=tok_box.get_left(), color=GRAY)
        arrow_to_lam = Arrow(start=frames_stack.get_right() + DOWN * 0.2, end=lam_box.get_left(), color=GRAY)
        arrow_tok_to_dyn = Arrow(start=tok_box.get_right(), end=dyn_box.get_left() + UP * 0.35, color=BLUE)
        arrow_lam_to_dyn = Arrow(start=lam_box.get_right(), end=dyn_box.get_left() + DOWN * 0.35, color=ORANGE)
        arrow_dyn_to_dec = Arrow(start=dyn_box.get_right(), end=dec_box.get_left(), color=RED)

        # Labels for variables
        z_label = MathTex("z_{1:T}", color=BLUE).next_to(arrow_tok_to_dyn, UP, buff=0.08).scale(0.85)
        a_label = MathTex("a_{1:T}", color=ORANGE).next_to(arrow_lam_to_dyn, DOWN, buff=0.08).scale(0.85)
        z_hat_label = MathTex(r"\hat{z}_{t+1}", color=RED).next_to(arrow_dyn_to_dec, UP, buff=0.08).scale(0.85)

        # Sequential creation
        self.play(Create(frames_stack), Write(frames_label))
        self.wait(1.0)
        self.play(Create(arrow_to_tok), Create(tok_box), Write(tok_label))
        self.wait(1.0)
        self.play(Create(arrow_to_lam), Create(lam_box), Write(lam_label))
        self.wait(1.0)
        self.play(
            Create(arrow_tok_to_dyn), Write(z_label),
            Create(arrow_lam_to_dyn), Write(a_label)
        )
        self.play(Create(dyn_box), Write(dyn_label))
        self.wait(1.0)
        self.play(Create(arrow_dyn_to_dec), Write(z_hat_label), Create(dec_box), Write(dec_label))
        self.wait(10.0)


class Section221VideoTokenizer(Scene):
    def construct(self):
        title = Tex(r"\text{\textbf{Component 1: Video Tokenizer (ST-ViViT)}}", color=WHITE).to_edge(UP, buff=1.0).scale(1.2)
        self.play(Write(title))
        self.wait(2.0)

        # 3D Video block representing x_{1:T}
        video_block = VGroup()
        for i in range(4):
            rect = Rectangle(width=1.8, height=1.1, stroke_color=BLUE_C, stroke_width=2, fill_color=BLUE_E, fill_opacity=0.25)
            rect.shift(RIGHT * 0.25 * i + UP * 0.15 * i)
            video_block.add(rect)
        video_block.move_to(LEFT * 4.5 + UP * 1.3)
        
        # Grid lines on the front face to show spatiotemporal patchification
        front_rect = video_block[-1]
        w = front_rect.width
        h = front_rect.height
        c = front_rect.get_center()
        grid_lines = VGroup()
        for dx in [-w/4, 0, w/4]:
            grid_lines.add(Line(start=c + [dx, -h/2, 0], end=c + [dx, h/2, 0], color=WHITE, stroke_width=1).set_opacity(0.6))
        for dy in [-h/3, h/3]:
            grid_lines.add(Line(start=c + [-w/2, dy, 0], end=c + [w/2, dy, 0], color=WHITE, stroke_width=1).set_opacity(0.6))

        video_label = Tex(r"\text{Video } $x_{1:T}$ \\ \text{160 } $\times$ \text{ 90, } $T=16$", color=WHITE).next_to(video_block, DOWN).scale(0.8)

        # ST-ViViT Box
        encoder_box = RoundedRectangle(width=2.8, height=2.0, color=BLUE, corner_radius=0.1).shift(LEFT * 0.6 + UP * 1.3)
        encoder_label = Tex(r"\text{\textbf{ST-ViViT Encoder}} \\ \text{Spatiotemporal} \\ \text{Transformer}", color=BLUE)
        fit_in_box(encoder_label, encoder_box)

        arrow_patch = Arrow(start=video_block.get_right(), end=encoder_box.get_left(), color=GRAY)

        # Codebook Grid (5x5 representation of VQ Codebook)
        codebook_grid = VGroup(*[
            Square(side_length=0.25, stroke_color=GRAY, fill_opacity=0.1, fill_color=WHITE)
            for _ in range(25)
        ]).arrange_in_grid(5, 5, buff=0.08).shift(RIGHT * 3.6 + UP * 1.3)
        codebook_label = Tex(r"\text{\textbf{VQ Codebook}} \\ \text{(Discrete Latent Space)}", color=WHITE).next_to(codebook_grid, DOWN).scale(0.8)
        codebook_specs = Tex(r"\text{Vocabulary Size } $|V| = 1024$ \\ \text{Embedding Dim } $D = 32$", color=GRAY).next_to(codebook_label, DOWN, buff=0.1).scale(0.7)

        arrow_to_codebook = Arrow(start=encoder_box.get_right(), end=codebook_grid.get_left(), color=BLUE)

        # Sequential rendering
        self.play(Create(video_block), Create(grid_lines), Write(video_label))
        self.wait(1.5)
        self.play(Create(arrow_patch), Create(encoder_box), Write(encoder_label))
        self.wait(1.5)

        # Animate a small 3D patch moving into ST-ViViT Encoder
        patch = VGroup(*[
            Rectangle(width=0.3, height=0.2, fill_color=BLUE, fill_opacity=0.8, stroke_color=BLUE_A)
            for _ in range(3)
        ])
        for idx, p in enumerate(patch):
            p.shift(RIGHT * 0.05 * idx + UP * 0.03 * idx)
        patch.move_to(front_rect.get_center())

        self.play(Create(patch))
        self.play(patch.animate.move_to(encoder_box.get_center()), run_time=1.5)
        self.play(FadeOut(patch))
        self.wait(1.0)

        # Show VQ mapping
        self.play(Create(arrow_to_codebook), Create(codebook_grid), Write(codebook_label), Write(codebook_specs))
        target_cell = codebook_grid[12]
        self.play(target_cell.animate.set_fill(BLUE, opacity=0.8))
        self.wait(3.0)

        # Computational Contrast side-by-side (Phenaki vs Genie)
        contrast_group = VGroup()
        
        phenaki_box = RoundedRectangle(width=5.0, height=1.4, color=RED, corner_radius=0.1)
        phenaki_text = VGroup(
            Tex(r"\text{\textbf{C-ViViT (Phenaki)}}", color=RED),
            Tex(r"\text{Độ phức tạp: } $O(T^2)$", color=RED),
            Tex(r"\text{Bộ nhớ tăng theo hàm bậc hai với chiều dài chuỗi}", color=RED)
        ).arrange(DOWN, buff=0.08)
        fit_in_box(phenaki_text, phenaki_box)
        
        genie_box = RoundedRectangle(width=5.0, height=1.4, color=GREEN, corner_radius=0.1)
        genie_text = VGroup(
            Tex(r"\text{\textbf{ST-ViViT (Genie)}}", color=GREEN),
            Tex(r"\text{Độ phức tạp: } $O(T)$", color=GREEN),
            Tex(r"\text{Tăng trưởng tuyến tính, tối ưu hóa bộ nhớ hiệu quả}", color=GREEN)
        ).arrange(DOWN, buff=0.08)
        fit_in_box(genie_text, genie_box)
        
        contrast_group.add(
            VGroup(phenaki_box, phenaki_text),
            VGroup(genie_box, genie_text)
        ).arrange(RIGHT, buff=0.8).shift(DOWN * 2.6)
        
        self.play(FadeIn(contrast_group))
        self.wait(15.0)


class Section222LatentActionModel(Scene):
    def construct(self):
        title = Tex(r"\text{\textbf{Component 2: Latent Action Model (LAM)}}", color=WHITE).to_edge(UP).scale(1.2)
        self.play(Write(title))
        self.wait(2.0)

        # Inputs at left: past frames x_{1:t} and target x_{t+1}
        past_frames = VGroup(*[
            Rectangle(width=1.1, height=0.8, fill_opacity=0.3, fill_color=BLUE_E, stroke_color=BLUE)
            for _ in range(3)
        ]).arrange(RIGHT, buff=-0.75).shift(LEFT * 5.0 + UP * 0.8)
        past_label = Tex(r"\text{Past } $x_{1:t}$", color=BLUE).next_to(past_frames, DOWN, buff=0.1).scale(0.75)

        future_frame = Rectangle(width=1.1, height=0.8, fill_opacity=0.3, fill_color=GREEN_E, stroke_color=GREEN).shift(LEFT * 5.0 + DOWN * 0.8)
        future_label = Tex(r"\text{Future } $x_{t+1}$", color=GREEN).next_to(future_frame, DOWN, buff=0.1).scale(0.75)

        # LAM Encoder Box
        encoder_box = RoundedRectangle(width=2.8, height=1.8, color=ORANGE, corner_radius=0.1).shift(LEFT * 1.5)
        encoder_label = Tex(r"\text{\textbf{LAM Encoder}} \\ \text{Compresses transitions} \\ \text{into actions}", color=ORANGE)
        fit_in_box(encoder_label, encoder_box)

        # Quantizer & Codebook (|A| = 8)
        action_title = Tex(r"\text{\textbf{Latent Action Space}}", color=WHITE).shift(RIGHT * 1.6 + UP * 1.3).scale(0.8)
        action_specs = Tex(r"\text{Vocabulary } $|A| = 8$ \\ \text{Embedding Dim = 32}", color=GRAY).next_to(action_title, DOWN, buff=0.1).scale(0.7)
        
        actions_grid = VGroup(*[
            Circle(radius=0.2, color=ORANGE, fill_opacity=0.2, fill_color=ORANGE)
            for _ in range(8)
        ]).arrange_in_grid(2, 4, buff=0.15).next_to(action_specs, DOWN, buff=0.25)
        actions_labels = VGroup(*[
            Tex(fr"\text{{{i+1}}}", color=ORANGE).move_to(actions_grid[i].get_center()).scale(0.8)
            for i in range(8)
        ])

        # LAM Decoder Box
        decoder_box = RoundedRectangle(width=2.8, height=1.8, color=ORANGE, corner_radius=0.1).shift(RIGHT * 4.6)
        decoder_label = Tex(r"\text{\textbf{LAM Decoder}} \\ \text{Reconstructs future} \\ \text{using action } $a_t$", color=ORANGE)
        fit_in_box(decoder_label, decoder_box)

        # Arrows
        arrow_past_to_enc = Arrow(start=past_frames.get_right(), end=encoder_box.get_left(), color=GRAY)
        arrow_fut_to_enc = Arrow(start=future_frame.get_right(), end=encoder_box.get_left(), color=GRAY)
        arrow_enc_to_act = Arrow(start=encoder_box.get_right(), end=actions_grid.get_left(), color=ORANGE)
        arrow_act_to_dec = Arrow(start=actions_grid.get_right(), end=decoder_box.get_left(), color=ORANGE)

        # Output reconstructed x_hat_{t+1}
        reconstructed_frame = Rectangle(width=1.1, height=0.8, fill_opacity=0.3, fill_color=RED_E, stroke_color=RED).next_to(decoder_box, RIGHT, buff=0.6)
        reconstructed_label = Tex(r"\text{Reconstruction} \\ $\hat{x}_{t+1}$", color=RED).next_to(reconstructed_frame, DOWN, buff=0.1).scale(0.75)
        arrow_dec_to_rec = Arrow(start=decoder_box.get_right(), end=reconstructed_frame.get_left(), color=ORANGE)

        # Training signal arrow (loss backprop)
        loss_arrow = DoubleArrow(start=reconstructed_frame.get_bottom(), end=future_frame.get_bottom(), path_arc=-0.8, color=RED)
        loss_label = Tex(r"\text{Training Signal (Reconstruction Loss)}", color=RED).next_to(loss_arrow, DOWN, buff=0.15).scale(0.75)

        # Sequential play
        self.play(Create(past_frames), Write(past_label))
        self.play(Create(future_frame), Write(future_label))
        self.wait(1.0)
        self.play(Create(arrow_past_to_enc), Create(arrow_fut_to_enc), Create(encoder_box), Write(encoder_label))
        self.wait(1.0)
        self.play(Create(arrow_enc_to_act), Create(actions_grid), Write(actions_labels), Write(action_title), Write(action_specs))
        self.wait(1.0)
        self.play(Create(arrow_act_to_dec), Create(decoder_box), Write(decoder_label))
        self.wait(1.5)

        # Action trigger animation
        self.play(actions_grid[2].animate.set_fill(ORANGE, opacity=0.8))
        self.play(Create(arrow_dec_to_rec), Create(reconstructed_frame), Write(reconstructed_label))
        self.play(Create(loss_arrow), Write(loss_label))
        self.wait(3.0)

        # Cross out LAM (discarded at inference)
        cross_line1 = Line(start=[-5, 2.5, 0], end=[6, -2.5, 0], color=RED, stroke_width=6)
        cross_line2 = Line(start=[-5, -2.5, 0], end=[6, 2.5, 0], color=RED, stroke_width=6)
        discard_cross = VGroup(cross_line1, cross_line2)
        discard_text = Tex(r"\text{\textbf{DISCARDED AT INFERENCE}}", color=RED).to_edge(DOWN, buff=1.0).scale(1.2)

        self.play(Create(discard_cross), Write(discard_text))
        self.wait(3.0)

        # Fade out discarded components
        discard_group = VGroup(encoder_box, encoder_label, decoder_box, decoder_label,
                              arrow_past_to_enc, arrow_fut_to_enc, arrow_enc_to_act, arrow_act_to_dec,
                              arrow_dec_to_rec, reconstructed_frame, reconstructed_label, loss_arrow, loss_label,
                              future_frame, future_label, discard_cross, discard_text)
        
        self.play(FadeOut(discard_group))
        
        # Position remaining action space to center for next scene context
        self.play(
            actions_grid.animate.move_to(ORIGIN + DOWN * 1.0),
            actions_labels.animate.move_to(ORIGIN + DOWN * 1.0),
            action_title.animate.move_to(ORIGIN + UP * 0.5),
            action_specs.animate.move_to(ORIGIN + UP * 0.0)
        )
        self.wait(5.0)


class Section223DynamicsModel(Scene):
    def construct(self):
        title = Tex(r"\text{\textbf{Component 3: Dynamics Model (MaskGIT)}}", color=WHITE).to_edge(UP).scale(1.2)
        self.play(Write(title))
        self.wait(2.0)

        # Additive Embeddings
        add_title = Tex(r"\text{\textbf{Additive Action Embeddings}}", color=GRAY).shift(UP * 2.3).scale(0.9)
        
        token_rect = Square(side_length=0.9, color=BLUE, fill_color=BLUE_E, fill_opacity=0.3).shift(LEFT * 3.5 + UP * 1.2)
        token_label = MathTex("z_t", color=BLUE)
        fit_in_box(token_label, token_rect)
        token_desc = Tex(r"\text{Video Token}", color=BLUE).next_to(token_rect, DOWN, buff=0.1).scale(0.7)

        plus_symbol = MathTex("+", font_size=36).shift(LEFT * 1.8 + UP * 1.2)

        action_rect = Square(side_length=0.9, color=ORANGE, fill_color=ORANGE, fill_opacity=0.3).shift(LEFT * 0.1 + UP * 1.2)
        action_label = MathTex("e(a_t)", color=ORANGE)
        fit_in_box(action_label, action_rect)
        action_desc = Tex(r"\text{Action Embedding}", color=ORANGE).next_to(action_rect, DOWN, buff=0.1).scale(0.7)

        equals_symbol = MathTex("=", font_size=36).shift(RIGHT * 1.5 + UP * 1.2)

        combined_rect = Square(side_length=0.9, color=RED, fill_color=RED_E, fill_opacity=0.3).shift(RIGHT * 3.2 + UP * 1.2)
        combined_label = MathTex("h_t", color=RED)
        fit_in_box(combined_label, combined_rect)
        combined_desc = Tex(r"\text{Combined Embedding}", color=RED).next_to(combined_rect, DOWN, buff=0.1).scale(0.7)

        self.play(
            Write(add_title),
            Create(token_rect), Write(token_label), Write(token_desc)
        )
        self.play(Write(plus_symbol))
        self.play(Create(action_rect), Write(action_label), Write(action_desc))
        self.play(Write(equals_symbol))
        self.play(Create(combined_rect), Write(combined_label), Write(combined_desc))
        self.wait(5.0)

        # Clear upper block to show masking details
        self.play(FadeOut(token_rect), FadeOut(token_label), FadeOut(token_desc),
                 FadeOut(plus_symbol), FadeOut(action_rect), FadeOut(action_label), FadeOut(action_desc),
                 FadeOut(equals_symbol), FadeOut(combined_rect), FadeOut(combined_label), FadeOut(combined_desc),
                 FadeOut(add_title))

        # Masking Rate Slider
        slider_line = Line(start=[-3.5, 0, 0], end=[3.5, 0, 0], color=GRAY)
        slider_label = Tex(r"\text{\textbf{Masking Rate }} $\gamma$:", color=WHITE).next_to(slider_line, UP, aligned_edge=LEFT, buff=0.25).scale(0.85)
        slider_val = Tex(r"\text{0.5}", color=GOLD).next_to(slider_label, RIGHT, buff=0.2).scale(0.85)
        slider_handle = Dot(point=[-1.0, 0, 0], color=GOLD, radius=0.14)
        
        self.play(Create(slider_line), Write(slider_label), Write(slider_val), Create(slider_handle))
        self.wait(1.5)

        # Tokens grid
        tokens_grid = VGroup(*[
            Square(side_length=0.7, color=BLUE, fill_opacity=0.3, fill_color=BLUE)
            for _ in range(8)
        ]).arrange(RIGHT, buff=0.2).shift(DOWN * 1.5)
        tokens_text = VGroup()
        for i in range(8):
            t_tex = MathTex(f"z_{{{i+1}}}")
            fit_in_box(t_tex, tokens_grid[i])
            tokens_text.add(t_tex)

        self.play(Create(tokens_grid), Write(tokens_text))
        self.wait(2.0)

        # Slide representation
        self.play(
            slider_handle.animate.shift(RIGHT * 2.2),
            Transform(slider_val, Tex(r"\text{0.85}", color=GOLD).next_to(slider_label, RIGHT, buff=0.2).scale(0.85))
        )
        
        # Mask tokens (index 1, 3, 4, 6)
        masked_indices = [1, 3, 4, 6]
        mask_actions = []
        for idx in masked_indices:
            mask_actions.append(tokens_grid[idx].animate.set_fill(GRAY_E, opacity=0.95).set_color(GRAY_C))
            new_q = Tex(r"\text{\textbf{?}}", color=RED)
            fit_in_box(new_q, tokens_grid[idx])
            mask_actions.append(Transform(tokens_text[idx], new_q))
        
        self.play(*mask_actions)
        self.wait(3.0)

        # Loss Function
        loss_formula = MathTex(
            r"\mathcal{L}_{\text{Dynamics}} = - \sum_{t=2}^{T} \log p(z_t \mid z_{<t}, a_{<t})", 
            font_size=28, color=WHITE
        ).shift(UP * 1.2)
        self.play(Write(loss_formula))
        self.wait(10.0)


class Section23SpatiotemporalTransformer(Scene):
    def construct(self):
        title = Tex(r"\text{\textbf{Spatiotemporal (ST) Transformer Block}}", color=WHITE).to_edge(UP).scale(1.2)
        self.play(Write(title))
        self.wait(2.0)

        # Main block representing the ST-Transformer block
        st_block = RoundedRectangle(width=8.0, height=4.2, color=BLUE_D, stroke_width=2, fill_opacity=0.03).shift(DOWN * 0.4)
        st_title = Tex(r"\text{\textbf{ST-Transformer Block}}", color=BLUE_D).next_to(st_block, UP, aligned_edge=LEFT, buff=0.1).scale(0.8)

        self.play(Create(st_block), Write(st_title))
        self.wait(1.5)

        # Inner layers
        spatial_box = RoundedRectangle(width=6.2, height=0.9, color=BLUE_B, fill_opacity=0.1).shift(UP * 0.9 + DOWN * 0.4)
        spatial_label = Tex(r"\text{\textbf{Spatial Attention Layer}} \\ \text{Attends over: } $1 \times H \times W$ \text{ tokens}", color=WHITE)
        fit_in_box(spatial_label, spatial_box)
        spatial_math = MathTex(r"O(H \times W)", color=BLUE_A).next_to(spatial_box, RIGHT, buff=0.15).scale(0.8)

        temporal_box = RoundedRectangle(width=6.2, height=0.9, color=ORANGE, fill_opacity=0.1).shift(DOWN * 0.4)
        temporal_label = Tex(r"\text{\textbf{Temporal Attention Layer}} \\ \text{Attends over: } $T \times 1 \times 1$ \text{ tokens}", color=WHITE)
        fit_in_box(temporal_label, temporal_box)
        temporal_math = MathTex(r"O(T)", color=ORANGE).next_to(temporal_box, RIGHT, buff=0.15).scale(0.8)

        ffw_box = RoundedRectangle(width=6.2, height=0.9, color=GREEN, fill_opacity=0.1).shift(DOWN * 1.5)
        ffw_label = Tex(r"\text{\textbf{Feed-Forward Network (FFW) Layer}}", color=WHITE)
        fit_in_box(ffw_label, ffw_box)
        ffw_desc = Tex(r"\text{Omitted post-spatial FFW to optimize and enable massive scaling}", color=GREEN).next_to(ffw_box, DOWN, buff=0.15).scale(0.7)

        # Arrows showing execution flow
        arrow1 = Arrow(start=spatial_box.get_bottom(), end=temporal_box.get_top(), color=GRAY, buff=0.05)
        arrow2 = Arrow(start=temporal_box.get_bottom(), end=ffw_box.get_top(), color=GRAY, buff=0.05)

        self.play(Create(spatial_box), Write(spatial_label), Write(spatial_math))
        self.wait(2.0)
        self.play(Create(arrow1), Create(temporal_box), Write(temporal_label), Write(temporal_math))
        self.wait(2.0)
        
        # Causal Mask annotation on Temporal layer
        mask_grid = VGroup(*[
            Square(side_length=0.14, stroke_color=GRAY, fill_opacity=0.1)
            for _ in range(16)
        ]).arrange_in_grid(4, 4, buff=0.02).next_to(temporal_box, LEFT, buff=0.25)
        
        # Mask the upper triangular part (causal mask)
        for i in range(4):
            for j in range(i+1, 4):
                mask_grid[i*4 + j].set_fill(RED, opacity=0.85).set_color(RED)
        
        mask_label = Tex(r"\text{Causal Mask}", color=RED).next_to(mask_grid, DOWN, buff=0.05).scale(0.65)
        self.play(Create(mask_grid), Write(mask_label))
        self.wait(3.0)

        self.play(Create(arrow2), Create(ffw_box), Write(ffw_label), Write(ffw_desc))
        self.wait(15.0)


class Section24InferenceCycle(Scene):
    def construct(self):
        title = Tex(r"\text{\textbf{Autoregressive Inference Cycle}}", color=WHITE).to_edge(UP).scale(1.2)
        self.play(Write(title))
        self.wait(2.0)

        # Input Frame x_1
        frame_in = Rectangle(width=1.5, height=1.0, color=BLUE, fill_opacity=0.25).shift(LEFT * 5.0 + UP * 0.5)
        label_in = Tex(r"\text{Prompt Frame } $x_1$", color=BLUE).next_to(frame_in, DOWN, buff=0.1).scale(0.7)

        # Video Tokenizer Encoder
        enc_box = RoundedRectangle(width=2.2, height=1.1, color=BLUE, corner_radius=0.1).shift(LEFT * 2.2 + UP * 0.5)
        enc_label = Tex(r"\text{\textbf{Tokenizer}} \\ \text{Encoder}", color=BLUE)
        fit_in_box(enc_label, enc_box)

        # Dynamics Model
        dyn_box = RoundedRectangle(width=2.5, height=1.5, color=RED, corner_radius=0.1).shift(RIGHT * 1.0 + UP * 0.5)
        dyn_label = Tex(r"\text{\textbf{Dynamics Model}} \\ \text{Predict next token}", color=RED)
        fit_in_box(dyn_label, dyn_box)

        # Decoder
        dec_box = RoundedRectangle(width=2.2, height=1.1, color=BLUE, corner_radius=0.1).shift(RIGHT * 4.4 + UP * 0.5)
        dec_label = Tex(r"\text{\textbf{Tokenizer}} \\ \text{Decoder}", color=BLUE)
        fit_in_box(dec_label, dec_box)

        # Controller Button
        button_circle = Circle(radius=0.35, color=ORANGE, fill_color=ORANGE, fill_opacity=0.3).shift(RIGHT * 1.0 + DOWN * 1.5)
        button_label = Tex(r"\text{\textbf{User Action }} $a_t$ \\ \text{(8-Button Controller)}", color=ORANGE).next_to(button_circle, LEFT, buff=0.25).scale(0.7)

        # Output predicted x_hat_2
        frame_out = Rectangle(width=1.5, height=1.0, color=GREEN, fill_opacity=0.25).shift(RIGHT * 5.2 + DOWN * 1.5)
        label_out = Tex(r"\text{Output Frame } $\hat{x}_2$", color=GREEN).next_to(frame_out, DOWN, buff=0.1).scale(0.7)

        # Arrows
        arrow1 = Arrow(start=frame_in.get_right(), end=enc_box.get_left(), color=GRAY)
        arrow2 = Arrow(start=enc_box.get_right(), end=dyn_box.get_left(), color=BLUE)
        arrow3 = Arrow(start=dyn_box.get_right(), end=dec_box.get_left(), color=RED)
        arrow4 = Arrow(start=dec_box.get_bottom(), end=frame_out.get_top(), color=GREEN)
        arrow_act = Arrow(start=button_circle.get_top(), end=dyn_box.get_bottom(), color=ORANGE)

        # Auto-regressive loop arrow
        loop_arrow = Arrow(
            start=frame_out.get_left(), 
            end=frame_in.get_bottom(), 
            path_arc=0.7, 
            color=GOLD
        )
        loop_label = Tex(r"\text{\textbf{Autoregressive Loop}}", color=GOLD).next_to(loop_arrow, DOWN, buff=0.1).scale(0.75)

        self.play(Create(frame_in), Write(label_in))
        self.play(Create(arrow1), Create(enc_box), Write(enc_label))
        self.wait(1.0)
        self.play(Create(arrow2), Create(dyn_box), Write(dyn_label))
        self.wait(1.0)
        self.play(Create(arrow_act), Create(button_circle), Write(button_label))
        self.wait(1.5)

        # Highlight action press & loop flow
        self.play(button_circle.animate.set_fill(ORANGE, opacity=0.85))
        self.play(Create(arrow3), Create(dec_box), Write(dec_label))
        self.play(Create(arrow4), Create(frame_out), Write(label_out))
        self.wait(1.5)
        
        self.play(Create(loop_arrow), Write(loop_label))
        self.wait(15.0)


class Section3ScalingResults(Scene):
    def construct(self):
        title = Tex(r"\text{\textbf{Scaling Results \& Compute Power}}", color=WHITE).to_edge(UP).scale(1.2)
        self.play(Write(title))
        self.wait(2.0)

        # Recreate the 3-panel data visualization from Figure 9
        charts_group = VGroup()

        # Chart 1: Scaling Model Size
        ax1 = Axes(
            x_range=[0, 4, 1], y_range=[0, 3, 1],
            x_length=3.2, y_length=2.2,
            axis_config={"color": GRAY, "include_numbers": False}
        )
        ax1_title = Tex(r"\text{Loss vs Compute}", color=WHITE).next_to(ax1, UP, buff=0.1).scale(0.75)
        ax1_xlabel = Tex(r"\text{Compute (FLOPs)}", color=GRAY).next_to(ax1, DOWN, buff=0.08).scale(0.65)
        
        curve1 = ax1.plot(lambda x: 2.3 * np.exp(-0.75 * x) + 0.45, x_range=[0, 3.8], color=BLUE)
        chart1 = VGroup(ax1, ax1_title, ax1_xlabel, curve1)

        # Chart 2: Final Loss vs Model Size (41M to 2.7B)
        ax2 = Axes(
            x_range=[0, 4, 1], y_range=[0, 3, 1],
            x_length=3.2, y_length=2.2,
            axis_config={"color": GRAY, "include_numbers": False}
        )
        ax2_title = Tex(r"\text{Loss vs Parameters}", color=WHITE).next_to(ax2, UP, buff=0.1).scale(0.75)
        ax2_xlabel = Tex(r"\text{Parameters (41M to 2.7B)}", color=GRAY).next_to(ax2, DOWN, buff=0.08).scale(0.65)
        
        dots = VGroup(*[
            Dot(ax2.c2p(x, y), color=RED, radius=0.08)
            for x, y in [(0.8, 2.45), (1.8, 1.65), (2.8, 1.05), (3.6, 0.55)]
        ])
        chart2 = VGroup(ax2, ax2_title, ax2_xlabel, dots)

        # Chart 3: Batch Size Scaling
        ax3 = Axes(
            x_range=[0, 4, 1], y_range=[0, 3, 1],
            x_length=3.2, y_length=2.2,
            axis_config={"color": GRAY, "include_numbers": False}
        )
        ax3_title = Tex(r"\text{Batch Size Scaling}", color=WHITE).next_to(ax3, UP, buff=0.1).scale(0.75)
        ax3_xlabel = Tex(r"\text{Training Steps}", color=GRAY).next_to(ax3, DOWN, buff=0.08).scale(0.65)
        
        curve3_128 = ax3.plot(lambda x: 2.2 * np.exp(-0.4 * x) + 0.6, x_range=[0, 3.8], color=GRAY)
        curve3_448 = ax3.plot(lambda x: 1.8 * np.exp(-0.6 * x) + 0.3, x_range=[0, 3.8], color=GREEN)
        
        label_128 = Tex(r"\text{Batch 128}", color=GRAY).next_to(curve3_128, RIGHT, buff=0.01).scale(0.55)
        label_448 = Tex(r"\text{Batch 448}", color=GREEN).next_to(curve3_448, RIGHT, buff=0.01).scale(0.55)
        
        chart3 = VGroup(ax3, ax3_title, ax3_xlabel, curve3_128, curve3_448, label_128, label_448)

        charts_group.add(chart1, chart2, chart3).arrange(RIGHT, buff=0.8).shift(UP * 0.2)

        # Summary / Conclusion Box
        summary_box = RoundedRectangle(width=10.5, height=1.3, color=GOLD, stroke_width=2, fill_opacity=0.05).shift(DOWN * 2.3)
        summary_text = Tex(
            r"\text{\textbf{Largest Configuration: 10.7B Parameters}} \\ \text{Trained on 942B Tokens using 256 TPUv5p Chips}", 
            color=GOLD
        )
        fit_in_box(summary_text, summary_box)

        # Sequential layout
        self.play(Create(chart1))
        self.wait(1.5)
        self.play(Create(chart2))
        self.wait(1.5)
        self.play(Create(chart3))
        self.wait(2.0)
        self.play(Create(summary_box), Write(summary_text))
        self.wait(15.0)


class Section4QualitativeEmergent(Scene):
    def construct(self):
        title = Tex(r"\text{\textbf{Emergent Capabilities \& Qualitative Results}}", color=WHITE).to_edge(UP).scale(1.2)
        self.play(Write(title))
        self.wait(2.0)

        # 1. Platformers Model (OOD Generalization) grid representation
        grid_title = Tex(r"\text{\textbf{Out-of-Distribution Generalization (Platformers)}}", color=BLUE).shift(LEFT * 4.2 + UP * 2.0).scale(0.7)
        
        grid_rows = VGroup()
        row_labels = [r"\text{Text-to-Image}", r"\text{Hand-drawn Sketch}", r"\text{Real Photo}"]
        
        for i in range(3):
            row_group = VGroup()
            lbl = Tex(row_labels[i], color=GRAY_A)
            row_group.add(lbl)
            
            frames = VGroup(*[
                Rectangle(width=0.8, height=0.5, stroke_color=BLUE_D, stroke_width=1, fill_color=BLUE_E, fill_opacity=0.1)
                for _ in range(4)
            ]).arrange(RIGHT, buff=0.08)
            
            row_group.add(frames)
            row_group.arrange(RIGHT, buff=0.25)
            grid_rows.add(row_group)
            
        grid_rows.arrange(DOWN, buff=0.2).shift(LEFT * 4.2 + DOWN * 0.4).scale(0.75)
        
        self.play(Write(grid_title), Create(grid_rows))
        
        # Animate character movement dots across the columns
        dots = VGroup()
        for idx, row in enumerate(grid_rows):
            start_pos = row[1][0].get_center() + LEFT * 0.2
            dot = Dot(point=start_pos, color=RED, radius=0.06)
            dots.add(dot)
            
        self.play(Create(dots))
        
        # Animate dots concurrently moving and jumping across columns
        move_actions = []
        for i, dot in enumerate(dots):
            p1 = grid_rows[i][1][1].get_center()
            p2 = grid_rows[i][1][2].get_center() + (UP * 0.3 if i == 1 else DOWN * 0.1 if i == 2 else ORIGIN)
            p3 = grid_rows[i][1][3].get_center()
            
            path = Succession(
                dot.animate.move_to(p1),
                dot.animate.move_to(p2),
                dot.animate.move_to(p3),
                run_time=3.0
            )
            move_actions.append(path)
            
        self.play(*move_actions)
        self.wait(3.0)

        # Transition to Emergent Parallax
        self.play(FadeOut(grid_rows), FadeOut(grid_title), FadeOut(dots))
        
        parallax_title = Tex(r"\text{\textbf{Emergent Parallax Effect}}", color=ORANGE).shift(RIGHT * 1.8 + UP * 2.0).scale(0.8)
        
        scene_base = Line(start=[0.5, -0.6, 0], end=[4.5, -0.6, 0], color=GRAY_D)
        road_line = Line(start=[0.5, -1.6, 0], end=[4.5, -1.6, 0], color=GRAY_B)
        mountain_line = Line(start=[0.5, 0.4, 0], end=[4.5, 0.4, 0], color=GRAY_E)
        
        fg_arrow = Arrow(start=[1.0, -1.2, 0], end=[3.8, -1.2, 0], color=GREEN, buff=0)
        fg_lbl = Tex(r"\text{Foreground: Fast movement}", color=GREEN).next_to(fg_arrow, UP, buff=0.05).scale(0.6)
        
        mg_arrow = Arrow(start=[1.0, -0.3, 0], end=[2.4, -0.3, 0], color=ORANGE, buff=0)
        mg_lbl = Tex(r"\text{Middleground: Medium movement}", color=ORANGE).next_to(mg_arrow, UP, buff=0.05).scale(0.6)
        
        bg_arrow = Arrow(start=[1.0, 0.7, 0], end=[1.5, 0.7, 0], color=RED, buff=0)
        bg_lbl = Tex(r"\text{Background: Slow movement}", color=RED).next_to(bg_arrow, UP, buff=0.05).scale(0.6)
        
        parallax_group = VGroup(scene_base, road_line, mountain_line, fg_arrow, fg_lbl, mg_arrow, mg_lbl, bg_arrow, bg_lbl).shift(RIGHT * 1.5)
        
        self.play(Write(parallax_title), Create(parallax_group))
        self.wait(5.0)

        # Transition to Robotics & Deformable Physics
        self.play(FadeOut(parallax_group), FadeOut(parallax_title))
        
        robot_title = Tex(r"\text{\textbf{Robotics: Deformable Physics Simulation}}", color=RED).shift(RIGHT * 1.8 + UP * 2.0).scale(0.8)
        
        table = Line(start=[0.2, -1.8, 0], end=[4.8, -1.8, 0], color=GRAY)
        
        chips_bag = RoundedRectangle(width=1.4, height=1.0, corner_radius=0.15, color=GOLD, fill_color=GOLD_E, fill_opacity=0.4).shift(RIGHT * 2.5 + DOWN * 1.3)
        bag_label = Tex(r"\text{Chips Bag}", color=GOLD)
        fit_in_box(bag_label, chips_bag)
        
        arm_base = Dot(point=[2.5, 1.2, 0], color=GRAY, radius=0.12)
        joint = Dot(point=[2.0, 0.2, 0], color=GRAY, radius=0.08)
        gripper = Rectangle(width=0.6, height=0.2, color=WHITE).shift(RIGHT * 2.5 + UP * 0.4)
        
        arm_link1 = Line(start=arm_base.get_center(), end=joint.get_center(), color=GRAY_A, stroke_width=4)
        arm_link2 = Line(start=joint.get_center(), end=gripper.get_top(), color=GRAY_A, stroke_width=4)
        
        robot_arm = VGroup(arm_base, joint, gripper, arm_link1, arm_link2)
        
        self.play(Write(robot_title), Create(table), Create(chips_bag), Write(bag_label), Create(robot_arm))
        self.wait(2.0)
        
        # Compress animation
        target_joint_pos = np.array([2.2, -0.4, 0])
        target_gripper_pos = np.array([2.5, -0.8, 0])
        
        compress_arm_link1 = Line(start=arm_base.get_center(), end=target_joint_pos, color=GRAY_A, stroke_width=4)
        compress_arm_link2 = Line(start=target_joint_pos, end=target_gripper_pos + UP * 0.1, color=GRAY_A, stroke_width=4)
        
        self.play(
            joint.animate.move_to(target_joint_pos),
            gripper.animate.move_to(target_gripper_pos + UP * 0.1),
            Transform(arm_link1, compress_arm_link1),
            Transform(arm_link2, compress_arm_link2),
            chips_bag.animate.stretch_to_fit_height(0.4).shift(DOWN * 0.3),
            bag_label.animate.scale(0.8).shift(DOWN * 0.3),
            run_time=3.0
        )
        self.wait(15.0)
