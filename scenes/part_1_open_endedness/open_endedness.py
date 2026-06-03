from manim import *
import numpy as np
import os

# Set default TexTemplate to support Vietnamese using XeLaTeX
vietnamese_template = TexTemplate(tex_compiler="xelatex", output_format=".xdv")
vietnamese_template.add_to_preamble(r"\usepackage{xcolor}")
vietnamese_template.add_to_preamble(r"\usepackage{amsmath}")
config.tex_template = vietnamese_template

# Color palette (3Blue1Brown & Genie-consistent style)
GOLD = "#F0AC5F"
GOLD_E = "#9B6A2F"
BLUE_C = "#58C4DD"
BLUE_E = "#1C758A"
GREEN_C = "#83C167"
GREEN_E = "#416832"
ORANGE = "#FF862F"
RED = "#FC6255"
RED_E = "#94231E"
GRAY_A = "#C8C8C8"
GRAY_E = "#222222"

# Layout Constants
SCREEN_WIDTH = 14.0
SCREEN_HEIGHT = 8.0
SAFE_PADDING = 0.25
COL3_LEFT = -4.5
COL3_CENTER = 0.0
COL3_RIGHT = 4.5
ROW_Y_TOP = 1.8
ROW_Y_MID = 0.0
ROW_Y_BOT = -1.8


# =========================================================================
# BASE SCENE CLASSES
# =========================================================================

class VietnameseScene(Scene):
    """
    Base Scene class optimized for Vietnamese text.
    Uses XeLaTeX and default pure black background.
    """
    def setup(self):
        config.tex_template = vietnamese_template
        super().setup()


class VietnameseMovingCameraScene(MovingCameraScene):
    """
    Base MovingCameraScene class optimized for Vietnamese text.
    Supports camera zooming and panning.
    """
    def setup(self):
        config.tex_template = vietnamese_template
        super().setup()


# =========================================================================
# HELPER FUNCTIONS
# =========================================================================

def fit_in_box(mobject, box, padding=0.15):
    """
    Helper function to scale and move any mobject to fit within a bounding box.
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
    Loads sound from local assets directory safely without failing compilation if missing.
    """
    audio_path = os.path.join(os.path.dirname(__file__), "assets", "audio", filename)
    if os.path.exists(audio_path):
        scene.add_sound(audio_path)
    else:
        print(f"WARNING: Audio file not found at: {audio_path}")


def create_title_banner(title_text, color=GOLD):
    """
    Creates a standardized title banner with an underline separator.
    """
    title = Tex(rf"\text{{\textbf{{{title_text}}}}}", color=color).scale(0.9)
    underline = Line(start=LEFT * 6.5, end=RIGHT * 6.5, color=GRAY, stroke_width=1.5)
    banner = VGroup(title, underline).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.5)
    return banner


def create_concept_card(title, content_list, border_color=BLUE_C, width=4.0, height=3.0):
    """
    Creates a card with a colored border, title, and bullet-pointed items.
    """
    box = RoundedRectangle(width=width, height=height, color=border_color, fill_color=BLACK, fill_opacity=0.8, corner_radius=0.15)
    card_title = Tex(rf"\text{{\textbf{{{title}}}}}", color=border_color).scale(0.85)
    card_title.next_to(box.get_top(), DOWN, buff=0.25)
    
    bullets = VGroup(*[
        Tex(rf"\bullet\ \text{{{item}}}", color=WHITE).scale(0.7)
        for item in content_list
    ]).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(card_title, DOWN, buff=0.3)
    
    card = VGroup(box, card_title, bullets)
    return card


def create_section_transition(scene, title_text, duration=2.0):
    """
    Fades in a large transition title in the center, waits, then fades it out.
    """
    transition_title = Tex(rf"\text{{\textbf{{{title_text}}}}}", color=GOLD).scale(1.2)
    scene.play(FadeIn(transition_title, shift=UP * 0.3), run_time=1.0)
    scene.wait(duration)
    scene.play(FadeOut(transition_title), run_time=1.0)


def create_comparison_table(headers, rows, col_widths=None, row_heights=None):
    """
    Creates a comparison grid table structure for display.
    """
    table = VGroup()
    num_cols = len(headers)
    num_rows = len(rows)
    
    cols = VGroup()
    for col_idx in range(num_cols):
        col_v = VGroup()
        hdr = Tex(headers[col_idx], color=GOLD).scale(0.8)
        col_v.add(hdr)
        for row_idx in range(num_rows):
            cell = Tex(rows[row_idx][col_idx], color=WHITE).scale(0.7)
            col_v.add(cell)
        col_v.arrange(DOWN, buff=0.4)
        cols.add(col_v)
    cols.arrange(RIGHT, buff=0.8)
    table.add(cols)
    return table


# =========================================================================
# CUSTOM MOBJECTS
# =========================================================================

class PetriDish(VGroup):
    """
    Visualizes Lisa Simpson's evolutionary Petri dish (SC_02).
    """
    def __init__(self, radius=2.5, **kwargs):
        super().__init__(**kwargs)
        self.dish_border = Circle(radius=radius, color=GRAY_A, stroke_width=2, stroke_style=DASHED)
        self.tooth_center = Square(side_length=0.6, color=WHITE, fill_color=WHITE, fill_opacity=0.2)
        
        # Red particles representing cola/nutrients
        self.particles = VGroup(*[
            Dot(point=np.array([np.random.uniform(-1.5, 1.5), np.random.uniform(-1.5, 1.5), 0.0]), radius=0.04, color=RED)
            for _ in range(20)
        ])
        self.add(self.dish_border, self.tooth_center, self.particles)

    def mutate_cells(self):
        """Animates tooth mutating into biological cell structures."""
        pass

    def evolve_to_city(self):
        """Animates cells transforming into a micro golden city."""
        pass


class InnovationNode(VGroup):
    """
    Represents discovery/innovation nodes in an evolutionary search tree (SC_01, SC_03, SC_07).
    """
    def __init__(self, label_text, color=BLUE_C, **kwargs):
        super().__init__(**kwargs)
        self.core_node = Circle(radius=0.4, color=color, fill_color=BLACK, fill_opacity=1.0)
        self.label = Tex(rf"\text{{{label_text}}}", color=color).scale(0.6)
        fit_in_box(self.label, self.core_node)
        self.child_connections = VGroup()
        self.add(self.core_node, self.label, self.child_connections)

    def glow_activation(self):
        """Animates node border pulsing/glowing with GOLD/ORANGE."""
        pass


class ObjectiveLandscape(VGroup):
    """
    Visualizes objective function contours and local minima entrapment (SC_04, SC_06).
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.contours = VGroup(*[
            Annulus(inner_radius=r, outer_radius=r+0.05, color=GREEN_E).scale(1 + 0.1 * np.sin(r * PI))
            for r in np.arange(0.5, 3.0, 0.5)
        ])
        self.flag = Tex(r"\text{Goal}", color=GOLD).scale(0.7)
        self.agent_dot = Dot(color=BLUE_C).shift(LEFT * 2 + DOWN * 1)
        self.add(self.contours, self.flag, self.agent_dot)

    def simulate_gradient_descent(self):
        """Animates agent dot sliding down gradient curves into local optima."""
        pass


class ExplorationGraph(VGroup):
    """
    Visualizes Stepping Stones and the fog of uncertainty (SC_04).
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nodes = VGroup(*[
            RoundedRectangle(width=1.2, height=0.6, color=GRAY_A, fill_color=GRAY_E, fill_opacity=0.9, corner_radius=0.1)
            for _ in range(5)
        ])
        positions = [
            LEFT * 3 + DOWN * 1.5,
            LEFT * 1.5 + DOWN * 0.5,
            ORIGIN + UP * 0.5,
            RIGHT * 1.5 + DOWN * 0.5,
            RIGHT * 3 + UP * 1.0
        ]
        for node, pos in zip(self.nodes, positions):
            node.move_to(pos)
        self.add(self.nodes)

    def reveal_stepping_stone(self, index):
        """Animates clearing of fog and thumping activation of stepping stone."""
        pass


class NetHackEnvironment(VGroup):
    """
    Simulates NetHack logic grid and magnifying lens interpretation (SC_05).
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        grid_data = [
            ["#", "#", "#", "#", "#", "#", "#", "#"],
            ["#", ".", ".", ".", ".", ".", ".", "#"],
            ["#", ".", "@", ".", ".", "d", ".", "#"],
            ["#", ".", ".", ".", ".", ".", "D", "#"],
            ["#", "#", "#", "#", "#", "#", "#", "#"]
        ]
        self.ascii_grid = VGroup()
        for r_idx, row in enumerate(grid_data):
            row_grp = VGroup()
            for c_idx, val in enumerate(row):
                color = BLUE_C if val == "@" else (ORANGE if val in ["d", "D"] else GRAY_A)
                char_tex = Tex(rf"\texttt{{{val}}}", color=color).scale(0.85)
                char_tex.shift(RIGHT * c_idx * 0.5 + DOWN * r_idx * 0.5)
                row_grp.add(char_tex)
            self.ascii_grid.add(row_grp)
        self.ascii_grid.move_to(ORIGIN)
        
        self.lens = Circle(radius=0.8, color=GOLD, stroke_width=3)
        self.lens_handle = Line(start=self.lens.get_bottom(), end=self.lens.get_bottom() + DOWN * 0.5 + RIGHT * 0.5, color=GOLD, stroke_width=3)
        self.magnifier = VGroup(self.lens, self.lens_handle)
        self.add(self.ascii_grid, self.magnifier)

    def transform_lens_focus(self):
        """Transforms ASCII characters underneath magnifier lens into graphical icons."""
        pass


class GoldilocksZoneMeter(VGroup):
    """
    Visualizes task difficulty distributions: Easy, Goldilocks, and Hard zones (SC_06, SC_07).
    """
    def __init__(self, width=0.8, height=4.0, **kwargs):
        super().__init__(**kwargs)
        self.easy_zone = Rectangle(width=width, height=height/3, color=BLUE_E, fill_color=BLUE_E, fill_opacity=0.6)
        self.goldilocks_zone = Rectangle(width=width, height=height/3, color=GOLD_E, fill_color=GOLD_E, fill_opacity=0.8)
        self.hard_zone = Rectangle(width=width, height=height/3, color=RED_E, fill_color=RED_E, fill_opacity=0.6)
        
        self.easy_zone.shift(DOWN * (height/3))
        self.goldilocks_zone.move_to(ORIGIN)
        self.hard_zone.shift(UP * (height/3))
        
        self.zones = VGroup(self.easy_zone, self.goldilocks_zone, self.hard_zone)
        
        self.easy_lbl = Tex(r"\text{Quá dễ}", color=BLUE_C).scale(0.6).next_to(self.easy_zone, LEFT)
        self.gold_lbl = Tex(r"\text{Goldilocks}", color=GOLD).scale(0.65).next_to(self.goldilocks_zone, LEFT)
        self.hard_lbl = Tex(r"\text{Quá khó}", color=RED).scale(0.6).next_to(self.hard_zone, LEFT)
        self.labels = VGroup(self.easy_lbl, self.gold_lbl, self.hard_lbl)
        
        self.pointer = Triangle(color=WHITE, fill_color=WHITE, fill_opacity=1.0).scale(0.12).rotate(-PI/2)
        self.pointer.next_to(self.easy_zone, RIGHT, buff=0.1)
        
        self.add(self.zones, self.labels, self.pointer)

    def update_agent_level(self, new_level):
        """Updates slider pointer to target level value."""
        pass


# =========================================================================
# VIDEO SCENE CLASSES (SC_01 to SC_07)
# =========================================================================

class SC_01_TheHorizonOfAGI(VietnameseScene):
    """
    SC_01: The Horizon of AGI & The Paradigm Shift.
    Focus: Explaining static dataset limits, Silver & Sutton's Era of Experience, Watts' organism-environment transaction.
    """
    def construct(self):
        load_safe_sound(self, "SC_01_ParadigmShift.wav")
        title = create_title_banner(r"SC\_01: The Horizon of AGI \& The Paradigm Shift")
        self.play(FadeIn(title), run_time=1.0)
        self.wait(0.5)

        # =========================================================================
        # PHASE 1: DATA SATURATION CHALLENGE (0.0s - 30.0s)
        # =========================================================================
        # Setup static dataset cubes & network model representations
        dataset_box = RoundedRectangle(width=3.5, height=2.2, color=BLUE_E, fill_color=BLUE_E, fill_opacity=0.1).shift(LEFT * 3.5)
        dataset_lbl = Tex(r"\text{Dữ liệu tĩnh (Offline Data)}\\$10^{15}$ \text{ tokens}", color=BLUE_C).scale(0.7)
        fit_in_box(dataset_lbl, dataset_box)

        network_box = RoundedRectangle(width=3.5, height=2.2, color=GRAY_A, fill_color=GRAY_E, fill_opacity=0.2).shift(RIGHT * 3.5)
        network_lbl = Tex(r"\text{Mô hình Neural}\\\text{(LLM / Transformer)}", color=GRAY_A).scale(0.7)
        fit_in_box(network_lbl, network_box)

        self.play(
            Create(dataset_box), Write(dataset_lbl),
            Create(network_box), Write(network_lbl),
            run_time=2.0
        )
        self.wait(10.0) # Accumulate time to 12.5s

        # saturation indicator
        saturation_warn = Tex(r"\text{\textbf{Điểm Bão Hòa Vật Lý (Saturation Point)}}", color=RED).scale(0.85).to_edge(DOWN, buff=1.0)
        self.play(Write(saturation_warn), run_time=1.5)
        self.wait(16.0) # Accumulate time to 30.0s

        # =========================================================================
        # PHASE 2: ERA OF EXPERIENCE INTRODUCTION (30.0s - 70.0s)
        # =========================================================================
        self.play(
            FadeOut(dataset_box), FadeOut(dataset_lbl),
            FadeOut(network_box), FadeOut(network_lbl),
            FadeOut(saturation_warn),
            run_time=1.5
        )

        question = Tex(r"\text{Làm sao để AI tự học xem nên học dữ liệu nào?}", color=GOLD).scale(0.85).shift(UP * 1.5)
        era_quote = Tex(
            r"\text{\textbf{``Kỷ nguyên Trải nghiệm'' (The Era of Experience)}}",
            r"\text{-- David Silver \& Richard Sutton (DeepMind)}",
            tex_to_color_map={"Kỷ nguyên Trải nghiệm": GOLD, "David Silver & Richard Sutton": BLUE_C}
        ).arrange(DOWN, buff=0.25).scale(0.8).shift(DOWN * 0.5)

        self.play(Write(question), run_time=2.0)
        self.wait(10.0) # Accumulate time to 43.5s
        self.play(FadeIn(era_quote, shift=UP * 0.2), run_time=2.0)
        self.wait(24.5) # Accumulate time to 70.0s

        # =========================================================================
        # PHASE 3: Watts' ORGANISM-ENVIRONMENT MUTUALITY (70.0s - 110.0s)
        # =========================================================================
        self.play(FadeOut(question), FadeOut(era_quote), run_time=1.5)

        organism = RoundedRectangle(width=3.2, height=1.2, color=BLUE_C, fill_color=BLUE_E, fill_opacity=0.15).shift(LEFT * 3.5 + DOWN * 0.8)
        org_lbl = Tex(r"\text{\textbf{Sinh vật (Organism)}}", color=BLUE_C)
        fit_in_box(org_lbl, organism)

        environment = RoundedRectangle(width=3.2, height=1.2, color=GREEN_C, fill_color=GREEN_E, fill_opacity=0.15).shift(RIGHT * 3.5 + DOWN * 0.8)
        env_lbl = Tex(r"\text{\textbf{Môi trường (Environment)}}", color=GREEN_C)
        fit_in_box(env_lbl, environment)

        watts_title = Tex(r"\text{\textbf{Alan Watts (1972)}}", color=GOLD).scale(1.0).shift(UP * 1.8)
        watts_quote = Tex(
            r"``The environment grows the organism, and the organism creates the environment.''",
            color=WHITE
        ).scale(0.7).next_to(watts_title, DOWN, buff=0.3)

        arrow_grows = ArcBetweenPoints(start=environment.get_top() + LEFT * 0.2, end=organism.get_top() + RIGHT * 0.2, angle=-TAU/6, color=GOLD).add_tip(tip_length=0.2)
        arrow_creates = ArcBetweenPoints(start=organism.get_bottom() + RIGHT * 0.2, end=environment.get_bottom() + LEFT * 0.2, angle=-TAU/6, color=GOLD).add_tip(tip_length=0.2)

        self.play(
            Write(watts_title), FadeIn(watts_quote),
            Create(organism), Write(org_lbl),
            Create(environment), Write(env_lbl),
            run_time=2.5
        )
        self.wait(15.0) # Accumulate time to 89.0s
        self.play(Create(arrow_grows), Create(arrow_creates), run_time=2.0)
        self.wait(19.0) # Accumulate time to 110.0s

        # =========================================================================
        # PHASE 4: OBJECTIVE CURRICULUM EVOLUTION (110.0s - 150.0s)
        # =========================================================================
        self.play(
            FadeOut(watts_title), FadeOut(watts_quote),
            FadeOut(organism), FadeOut(org_lbl),
            FadeOut(environment), FadeOut(env_lbl),
            FadeOut(arrow_grows), FadeOut(arrow_creates),
            run_time=1.5
        )

        future_direction = Tex(r"\text{\textbf{Đích đến: Thực thể tự sinh giáo trình huấn luyện}}", color=GOLD).scale(0.9)
        self.play(Write(future_direction), run_time=2.0)
        self.wait(36.5) # Wait to finish total 150 seconds
        self.play(FadeOut(future_direction), FadeOut(title), run_time=1.5)


class SC_02_TheMetaphorOfThePetriDish(VietnameseMovingCameraScene):
    """
    SC_02: The Metaphor of the Petri Dish.
    Focus: Simpsons' Genesis Tub anecdote, evolution of cells to golden city structures, contrasting with closed Go/Chess environments.
    """
    def construct(self):
        load_safe_sound(self, "SC_02_PetriDish.wav")
        title = create_title_banner(r"SC\_02: The Metaphor of the Petri Dish")
        self.add(title)
        self.wait(0.5)

        # =========================================================================
        # PHASE 1: GENESIS TUB ANECDOTE (0.0s - 40.0s)
        # =========================================================================
        petri_dish = PetriDish().shift(DOWN * 0.5)
        anecdote_title = Tex(r"\text{Lisa Simpson: The Genesis Tub (1996)}", color=GOLD).scale(0.85).next_to(title, DOWN, buff=0.3)
        
        self.play(Create(petri_dish), Write(anecdote_title), run_time=2.0)
        self.wait(10.0) # Accumulate to 12.5s
        
        # Trigger mock lightning and initial cell mutation
        lightning = Line(UP * 3, petri_dish.tooth_center.get_top(), color=YELLOW, stroke_width=4)
        self.play(Create(lightning), run_time=0.3)
        self.play(FadeOut(lightning), run_time=0.2)
        self.wait(27.0) # Accumulate to 40.0s

        # =========================================================================
        # PHASE 2: BIOLOGICAL TO CULTURAL EVOLUTION (40.0s - 80.0s)
        # =========================================================================
        # Focus camera on petri dish center
        self.play(
            self.camera.frame.animate.move_to(petri_dish.get_center()).set(width=petri_dish.width * 1.5),
            run_time=2.0
        )
        self.wait(5.0) # Accumulate to 47.0s
        
        # Mutate tooth to cities mock
        city_label = Tex(r"\text{Tiến hóa Sinh học } \rightarrow \text{ Tiến hóa Văn hóa \& Công nghệ}", color=GOLD).scale(0.35).next_to(petri_dish.tooth_center, UP, buff=0.1)
        self.play(Write(city_label), run_time=1.5)
        self.wait(31.5) # Accumulate to 80.0s

        # =========================================================================
        # PHASE 3: CONTRAST WITH CLOSED AI SYSTEMS (80.0s - 120.0s)
        # =========================================================================
        # Reset camera
        self.play(
            self.camera.frame.animate.move_to(ORIGIN).set(width=SCREEN_WIDTH),
            run_time=2.0
        )
        self.play(
            FadeOut(petri_dish), FadeOut(anecdote_title), FadeOut(city_label),
            run_time=1.0
        )

        closed_box = RoundedRectangle(width=5.0, height=3.5, color=RED, fill_color=RED_E, fill_opacity=0.1).shift(LEFT * 3.2 + DOWN * 0.5)
        closed_lbl = Tex(r"\text{\textbf{Hệ thống Đóng (Closed System)}}\\e.g. Cờ Vây (Go) 19x19", color=RED).scale(0.7)
        fit_in_box(closed_lbl, closed_box)

        open_box = RoundedRectangle(width=5.0, height=3.5, color=GREEN_C, fill_color=GREEN_E, fill_opacity=0.15).shift(RIGHT * 3.2 + DOWN * 0.5)
        open_lbl = Tex(r"\text{\textbf{Hệ thống Mở (Open-Ended System)}}\\Đĩa Petri Vô hạn", color=GREEN_C).scale(0.7)
        fit_in_box(open_lbl, open_box)

        self.play(
            Create(closed_box), Write(closed_lbl),
            Create(open_box), Write(open_lbl),
            run_time=2.5
        )
        self.wait(34.0) # Wait to finish total 120 seconds
        self.play(FadeOut(closed_box), FadeOut(closed_lbl), FadeOut(open_box), FadeOut(open_lbl), FadeOut(title), run_time=1.5)


class SC_03_DeconstructingOpenEndedSystems(VietnameseScene):
    """
    SC_03: Deconstructing Open-Ended Systems.
    Focus: Standish definition (observer-dependent), Noisy TV paradox, Venn diagram of Novelty and Learnability.
    """
    def construct(self):
        load_safe_sound(self, "SC_03_ObserverVenn.wav")
        title = create_title_banner(r"SC\_03: Deconstructing Open-Ended Systems")
        self.play(FadeIn(title), run_time=1.0)
        self.wait(0.5)

        # =========================================================================
        # PHASE 1: STANDISH & OBSERVER PERSPECTIVE (0.0s - 45.0s)
        # =========================================================================
        observer_eye = Circle(radius=0.6, color=GOLD).shift(UP * 1.2)
        eye_pupil = Dot(point=observer_eye.get_center(), radius=0.2, color=GOLD)
        observer_lbl = Tex(r"\text{Quan sát viên (Observer Perspective)}", color=GOLD).scale(0.75).next_to(observer_eye, UP, buff=0.15)
        
        standish_text = Tex(
            r"\text{Standish: Tính mở phụ thuộc vào lăng kính nhận diện của Observer}",
            color=WHITE
        ).scale(0.75).shift(DOWN * 1.2)

        self.play(
            Create(observer_eye), Create(eye_pupil), Write(observer_lbl),
            run_time=2.0
        )
        self.play(Write(standish_text), run_time=1.5)
        self.wait(40.0) # Accumulate to 45.0s

        # =========================================================================
        # PHASE 2: NOISY TV PARADOX (45.0s - 100.0s)
        # =========================================================================
        self.play(
            FadeOut(observer_eye), FadeOut(eye_pupil), FadeOut(observer_lbl), FadeOut(standish_text),
            run_time=1.0
        )
        
        noisy_tv_box = RoundedRectangle(width=5.5, height=3.2, color=RED, fill_color=GRAY_E, fill_opacity=0.3).shift(LEFT * 3.2 + DOWN * 0.5)
        noisy_tv_lbl = Tex(r"\text{Nghịch lý TV Nhiễu Hạt}\\\text{Entropy tối đa} \rightarrow \text{Mới mẻ (Novel)}\\\text{nhưng không học được (Unlearnable)}", color=RED).scale(0.75)
        fit_in_box(noisy_tv_lbl, noisy_tv_box)

        dennis_hughes_box = RoundedRectangle(width=5.5, height=3.2, color=BLUE_C, fill_color=BLUE_E, fill_opacity=0.1).shift(RIGHT * 3.2 + DOWN * 0.5)
        dennis_hughes_lbl = Tex(r"\text{Dennis \& Hughes Definition}\\\text{Hiện vật vừa phải Mới mẻ (Novel)}\\\text{\textbf{Vừa phải học được (Learnable)}}", color=BLUE_C).scale(0.75)
        fit_in_box(dennis_hughes_lbl, dennis_hughes_box)

        self.play(
            Create(noisy_tv_box), Write(noisy_tv_lbl),
            Create(dennis_hughes_box), Write(dennis_hughes_lbl),
            run_time=2.5
        )
        self.wait(51.5) # Accumulate to 100.0s

        # =========================================================================
        # PHASE 3: VENN DIAGRAM & LOGIC EQUATION (100.0s - 180.0s)
        # =========================================================================
        self.play(
            FadeOut(noisy_tv_box), FadeOut(noisy_tv_lbl),
            FadeOut(dennis_hughes_box), FadeOut(dennis_hughes_lbl),
            run_time=1.0
        )

        # Venn Diagram representation
        novelty_circle = Circle(radius=1.8, color=BLUE_C, fill_color=BLUE_E, fill_opacity=0.35).shift(LEFT * 1.0 + DOWN * 0.5)
        novelty_lbl = Tex(r"\text{Novelty (Mới mẻ)}", color=BLUE_C).scale(0.7).next_to(novelty_circle.get_left(), UP, buff=0.1)

        learnability_circle = Circle(radius=1.8, color=GREEN_C, fill_color=GREEN_E, fill_opacity=0.35).shift(RIGHT * 1.0 + DOWN * 0.5)
        learnability_lbl = Tex(r"\text{Learnability (Học được)}", color=GREEN_C).scale(0.7).next_to(learnability_circle.get_right(), UP, buff=0.1)

        self.play(
            Create(novelty_circle), Write(novelty_lbl),
            Create(learnability_circle), Write(learnability_lbl),
            run_time=2.0
        )
        self.wait(10.0) # Accumulate to 113.0s

        # Highlight intersection
        intersection_lbl = Tex(r"\text{\textbf{Open-Endedness}}", color=GOLD).scale(0.85).shift(DOWN * 0.5)
        self.play(Write(intersection_lbl), run_time=1.5)
        self.wait(20.0) # Accumulate to 134.5s

        # Show logic equation
        equation = MathTex(
            r"\mathcal{S} \text{ is Open-Ended} \iff \forall t, \text{ Artifact}(t) \in \{\text{Novel} \cap \text{Learnable}\}"
        ).scale(0.75).shift(UP * 1.5)
        self.play(Write(equation), run_time=2.0)
        
        self.wait(42.0) # Wait to finish total 180 seconds
        self.play(
            FadeOut(novelty_circle), FadeOut(novelty_lbl),
            FadeOut(learnability_circle), FadeOut(learnability_lbl),
            FadeOut(intersection_lbl), FadeOut(equation),
            FadeOut(title),
            run_time=1.5
        )


class SC_04_TheIllusionOfGoals(VietnameseScene):
    """
    SC_04: The Illusion of Goals (Objective Design).
    Focus: Pitfalls of target optimization in open spaces, Stepping stones theory (Vacuum tube -> Radio -> Computer).
    """
    def construct(self):
        load_safe_sound(self, "SC_04_SteppingStones.wav")
        title = create_title_banner(r"SC\_04: The Illusion of Goals (Objective Design)")
        self.play(FadeIn(title), run_time=1.0)
        self.wait(0.5)

        # =========================================================================
        # PHASE 1: Objective Design Pitfall (0.0s - 50.0s)
        # =========================================================================
        landscape = ObjectiveLandscape().shift(DOWN * 0.5)
        warn_lbl = Tex(r"\text{La bàn giả (False Compass) trong Hệ Thống Mở}", color=RED).scale(0.8).to_edge(DOWN, buff=0.8)
        
        self.play(Create(landscape.contours), Create(landscape.flag), Create(landscape.agent_dot), run_time=2.5)
        self.wait(10.0) # Accumulate to 14.0s
        self.play(Write(warn_lbl), run_time=1.5)
        self.wait(34.5) # Accumulate to 50.0s

        # =========================================================================
        # PHASE 2: STEPPING STONES THEORY (50.0s - 100.0s)
        # =========================================================================
        self.play(
            FadeOut(landscape.contours), FadeOut(landscape.flag), FadeOut(landscape.agent_dot), FadeOut(warn_lbl),
            run_time=1.0
        )

        concept_title = Tex(r"\text{\textbf{Lý thuyết Bước đệm (Stepping Stones) -- Kenneth Stanley}}", color=GOLD).scale(0.85).shift(UP * 1.5)
        
        card1 = create_concept_card("Ống chân không (1900s)", ["Không nhằm mục đích chế tạo PC", "Để khuếch đại tín hiệu radio"], border_color=BLUE_C).shift(LEFT * 4.5 + DOWN * 0.5)
        card2 = create_concept_card("Máy tính điện tử (1940s)", ["Được xây dựng từ ống chân không", "Tiến bộ phi tuyến tính"], border_color=ORANGE).shift(RIGHT * 4.5 + DOWN * 0.5)
        arrow = Arrow(start=card1.get_right(), end=card2.get_left(), color=GOLD)

        self.play(Write(concept_title), run_time=1.5)
        self.play(Create(card1), run_time=1.5)
        self.play(Create(arrow), Create(card2), run_time=2.0)
        self.wait(44.0) # Accumulate to 100.0s

        # =========================================================================
        # PHASE 3: CONTOUR EXPLORATION & FOG CLEARING (100.0s - 180.0s)
        # =========================================================================
        self.play(
            FadeOut(concept_title), FadeOut(card1), FadeOut(card2), FadeOut(arrow),
            run_time=1.0
        )

        exp_graph = ExplorationGraph().shift(DOWN * 0.5)
        fog_box = Rectangle(width=12.0, height=4.5, color=GRAY_E, fill_color=GRAY_E, fill_opacity=0.75).shift(DOWN * 0.5)
        fog_lbl = Tex(r"\text{Sương mù tri thức (Uncertainty Fog)}", color=WHITE).scale(0.8).move_to(fog_box.get_center())

        self.play(Create(exp_graph), Create(fog_box), Write(fog_lbl), run_time=2.5)
        self.wait(15.0) # Accumulate to 118.5s
        
        # Clear fog and highlight stepping stones
        self.play(FadeOut(fog_box), FadeOut(fog_lbl), run_time=2.0)
        self.wait(58.0) # Wait to finish total 180 seconds
        self.play(FadeOut(exp_graph), FadeOut(title), run_time=1.5)


class SC_05_TheConcretePlaygrounds(VietnameseMovingCameraScene):
    """
    SC_05: The Concrete Playgrounds: NetHack to XLand.
    Focus: NetHack complex ASCII grid mechanics, XLand matrices (Terrain x Objects x Rules), 25 billion tasks explosion.
    """
    def construct(self):
        load_safe_sound(self, "SC_05_NetHackXLand.wav")
        title = create_title_banner(r"SC\_05: The Concrete Playgrounds: NetHack to XLand")
        self.add(title)
        self.wait(0.5)

        # =========================================================================
        # PHASE 1: NETHACK ASCII GAMEPLAY (0.0s - 45.0s)
        # =========================================================================
        nethack_env = NetHackEnvironment().shift(DOWN * 0.5)
        nethack_lbl = Tex(r"\text{NetHack: Không gian tìm kiếm toàn vẹn Turing (Turing-Complete)}", color=BLUE_C).scale(0.85).next_to(title, DOWN, buff=0.3)

        self.play(Create(nethack_env.ascii_grid), Create(nethack_env.magnifier), Write(nethack_lbl), run_time=2.5)
        self.wait(10.0) # Accumulate to 13.0s
        
        # Zoom camera onto the magnifier lens center
        self.play(
            self.camera.frame.animate.move_to(nethack_env.lens.get_center()).set(width=nethack_env.lens.width * 2.5),
            run_time=2.0
        )
        self.wait(28.5) # Accumulate to 45.0s

        # =========================================================================
        # PHASE 2: XLAND SYSTEM INTRO (45.0s - 90.0s)
        # =========================================================================
        # Reset camera
        self.play(
            self.camera.frame.animate.move_to(ORIGIN).set(width=SCREEN_WIDTH),
            run_time=2.0
        )
        self.play(
            FadeOut(nethack_env), FadeOut(nethack_lbl),
            run_time=1.0
        )

        xland_lbl = Tex(r"\text{XLand: Sinh môi trường thủ tục (Procedural Generation)}", color=GOLD).scale(0.85).next_to(title, DOWN, buff=0.3)
        self.play(Write(xland_lbl), run_time=1.5)

        # Create three matrices representations
        matrix_t = RoundedRectangle(width=2.5, height=2.5, color=BLUE_C, fill_color=BLUE_E, fill_opacity=0.15).shift(LEFT * 4.0 + DOWN * 0.5)
        lbl_t = Tex(r"\text{\textbf{Địa hình (T)}}\\Mountains / Plains", color=BLUE_C).scale(0.65)
        fit_in_box(lbl_t, matrix_t)

        matrix_o = RoundedRectangle(width=2.5, height=2.5, color=ORANGE, fill_color=BLACK, fill_opacity=0.8).shift(DOWN * 0.5)
        lbl_o = Tex(r"\text{\textbf{Vật thể (O)}}\\Objects / Tools", color=ORANGE).scale(0.65)
        fit_in_box(lbl_o, matrix_o)

        matrix_r = RoundedRectangle(width=2.5, height=2.5, color=GREEN_C, fill_color=GREEN_E, fill_opacity=0.15).shift(RIGHT * 4.0 + DOWN * 0.5)
        lbl_r = Tex(r"\text{\textbf{Luật chơi (R)}}\\Co-op / Adversarial", color=GREEN_C).scale(0.65)
        fit_in_box(lbl_r, matrix_r)

        self.play(
            Create(matrix_t), Write(lbl_t),
            Create(matrix_o), Write(lbl_o),
            Create(matrix_r), Write(lbl_r),
            run_time=3.0
        )
        self.wait(35.5) # Accumulate to 90.0s

        # =========================================================================
        # PHASE 3: COMBINATORIAL TASK EXPLOSION (90.0s - 210.0s)
        # =========================================================================
        self.play(
            FadeOut(matrix_t), FadeOut(lbl_t),
            FadeOut(matrix_o), FadeOut(lbl_o),
            FadeOut(matrix_r), FadeOut(lbl_r),
            FadeOut(xland_lbl),
            run_time=1.5
        )

        big_number = Tex(r"\text{\textbf{25,000,000,000}}", color=ORANGE).scale(2.2).shift(UP * 0.5)
        tasks_lbl = Tex(r"\text{Nhiệm vụ độc lập trong XLand (Combinatorial Explosion)}", color=WHITE).scale(0.85).next_to(big_number, DOWN, buff=0.4)

        self.play(Write(big_number), run_time=2.0)
        self.play(FadeIn(tasks_lbl, shift=UP * 0.2), run_time=1.5)
        self.wait(115.0) # Wait to finish total 210 seconds
        
        self.play(FadeOut(big_number), FadeOut(tasks_lbl), FadeOut(title), run_time=1.5)


class SC_06_TheAutocurriculaBottleneck(VietnameseScene):
    """
    SC_06: The Autocurricula Bottleneck & Goldilocks Zone.
    Focus: Failure of self-play (niche entrapment), difficulty scaling, cognitive Goldilocks Zone.
    """
    def construct(self):
        load_safe_sound(self, "SC_06_GoldilocksNiche.wav")
        title = create_title_banner(r"SC\_06: The Autocurricula Bottleneck \& Goldilocks Zone")
        self.play(FadeIn(title), run_time=1.0)
        self.wait(0.5)

        # =========================================================================
        # PHASE 1: SELF-PLAY & NICHE ENTRAPMENT (0.0s - 45.0s)
        # =========================================================================
        loop_circle = Circle(radius=1.5, color=RED, stroke_width=3).shift(LEFT * 3.5 + DOWN * 0.5)
        agent_dot = Dot(color=BLUE_C).move_to(loop_circle.point_at_angle(0))
        niche_lbl = Tex(r"\text{Kẹt trong phân khúc hẹp}\\\text{(Niche Entrapment Loop)}", color=RED).scale(0.75).next_to(loop_circle, UP, buff=0.2)

        self.play(Create(loop_circle), Create(agent_dot), Write(niche_lbl), run_time=2.0)
        # Spin agent in circular trap loop
        self.play(MoveAlongPath(agent_dot, loop_circle), run_time=3.0, rate_func=linear)
        self.wait(38.0) # Accumulate to 45.0s

        # =========================================================================
        # PHASE 2: COGNITIVE GOLDILOCKS ZONE (45.0s - 95.0s)
        # =========================================================================
        self.play(
            FadeOut(loop_circle), FadeOut(agent_dot), FadeOut(niche_lbl),
            run_time=1.0
        )

        meter = GoldilocksZoneMeter(height=3.5).shift(RIGHT * 3.0 + DOWN * 0.5)
        meter_explain = Tex(
            r"\text{\textbf{Vùng Goldilocks nhận thức (Cognitive Zone)}}\\",
            r"\text{\textbf{Quá dễ:} gradient triệt tiêu, đóng băng năng lực\\}",
            r"\text{\textbf{Quá khó:} bế tắc, không thể học hỏi được\\}",
            r"\text{\textbf{Goldilocks (Vàng):} nhiệm vụ nằm ở biên nỗ lực}",
            tex_to_color_map={
                "Quá dễ:": BLUE_C,
                "Quá khó:": RED,
                "Goldilocks (Vàng):": GOLD
            }
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).scale(0.65).shift(LEFT * 3.0 + DOWN * 0.5)

        self.play(Create(meter), run_time=2.0)
        self.play(FadeIn(meter_explain, shift=RIGHT * 0.2), run_time=2.0)
        self.wait(10.0) # Accumulate to 60s
        
        # update indicator pointer to Goldilocks
        self.play(meter.pointer.animate.shift(UP * 1.15), run_time=1.5)
        self.wait(32.5) # Accumulate to 95.0s

        # =========================================================================
        # PHASE 3: UNIFORM SAMPLING & BREAKDOWN (95.0s - 180.0s)
        # =========================================================================
        self.play(FadeOut(meter_explain), run_time=1.0)
        
        collapse_lbl = Tex(r"\text{Uniform Sampling } \rightarrow \text{ Đứt gãy giáo trình huấn luyện}", color=RED).scale(0.85).shift(LEFT * 3.0 + DOWN * 0.5)
        self.play(Write(collapse_lbl), run_time=1.5)
        
        # Breakdown shake effect on meter
        self.play(meter.animate.shift(UP * 0.1), run_time=0.1)
        self.play(meter.animate.shift(DOWN * 0.2), run_time=0.1)
        self.play(meter.animate.shift(UP * 0.1), run_time=0.1)
        
        self.wait(80.7) # Wait to finish total 180 seconds
        self.play(FadeOut(meter), FadeOut(collapse_lbl), FadeOut(title), run_time=1.5)


class SC_07_TheEvolutionaryEngines(VietnameseScene):
    """
    SC_07: The Evolutionary Engines: Foundation Models.
    Focus: LLM Task Proposer as semantic variation/selection operators, sample efficiency graph, AI Safety / Specification Gaming, and transition.
    """
    def construct(self):
        load_safe_sound(self, "SC_07_EvolutionOperators.wav")
        title = create_title_banner(r"SC\_07: The Evolutionary Engines: Foundation Models")
        self.play(FadeIn(title), run_time=1.0)
        self.wait(0.5)

        # =========================================================================
        # PHASE 1: FOUNDATION MODELS AS EVOLUTIONARY OPERATORS (0.0s - 45.0s)
        # =========================================================================
        llm_box = RoundedRectangle(width=3.8, height=2.2, color=ORANGE, fill_color=BLACK, fill_opacity=0.8).shift(RIGHT * 3.5 + UP * 0.5)
        llm_lbl = Tex(r"\text{LLM Task Proposer}\\\text{(Toán tử Tiến hóa)}", color=ORANGE).scale(0.8)
        fit_in_box(llm_lbl, llm_box)

        sim_box = RoundedRectangle(width=3.8, height=2.2, color=BLUE_C, fill_color=BLUE_E, fill_opacity=0.15).shift(LEFT * 3.5 + UP * 0.5)
        sim_lbl = Tex(r"\text{Không gian mô phỏng 3D}\\\text{(Agent \& Environment)}", color=BLUE_C).scale(0.8)
        fit_in_box(sim_lbl, sim_box)

        self.play(
            Create(llm_box), Write(llm_lbl),
            Create(sim_box), Write(sim_lbl),
            run_time=2.5
        )
        self.wait(41.0) # Accumulate to 45.0s

        # =========================================================================
        # PHASE 2: FEEDBACK LOOP FOR VARIATION & SELECTION (45.0s - 95.0s)
        # =========================================================================
        # Draw dynamic feedback flow arrows
        arrow_variation = ArcBetweenPoints(start=llm_box.get_top(), end=sim_box.get_top(), angle=TAU/8, color=GOLD).add_tip(tip_length=0.2)
        var_lbl = Tex(r"\text{Biến dị Ngữ nghĩa (Variation)}", color=GOLD).scale(0.6).next_to(arrow_variation, UP, buff=0.1)

        arrow_selection = ArcBetweenPoints(start=sim_box.get_bottom(), end=llm_box.get_bottom(), angle=TAU/8, color=GOLD).add_tip(tip_length=0.2)
        sel_lbl = Tex(r"\text{Chọn lọc Ngữ nghĩa (Selection)}", color=GOLD).scale(0.6).next_to(arrow_selection, DOWN, buff=0.1)

        self.play(
            Create(arrow_variation), Write(var_lbl),
            Create(arrow_selection), Write(sel_lbl),
            run_time=2.5
        )
        self.wait(46.0) # Accumulate to 95.0s

        # =========================================================================
        # PHASE 3: PERFORMANCE GRAPH & AI SAFETY (95.0s - 135.0s)
        # =========================================================================
        self.play(
            FadeOut(llm_box), FadeOut(llm_lbl),
            FadeOut(sim_box), FadeOut(sim_lbl),
            FadeOut(arrow_variation), FadeOut(var_lbl),
            FadeOut(arrow_selection), FadeOut(sel_lbl),
            run_time=1.5
        )

        # Performance Graph Mockup
        graph_axes = Axes(x_range=[0, 10, 2], y_range=[0, 10, 2], x_length=5, y_length=3, axis_config={"color": GRAY}).shift(LEFT * 3.5 + DOWN * 0.8)
        graph_lbl = Tex(r"\text{Hiệu suất mẫu (Sample Efficiency)}", color=WHITE).scale(0.7).next_to(graph_axes, UP, buff=0.2)

        # Lines representing performance curves
        llm_curve = Line(start=graph_axes.c2p(0, 1), end=graph_axes.c2p(8, 9), color=GREEN_C, stroke_width=4)
        uniform_curve = Line(start=graph_axes.c2p(0, 1), end=graph_axes.c2p(8, 2), color=GRAY, stroke_width=4)

        # AI Safety Card
        safety_card = create_concept_card("An toàn AI (AI Safety)", ["Specification Gaming (Lừa dối)", "Cần Proxy Observer độc lập"], border_color=RED, width=5.2, height=3.0).shift(RIGHT * 3.5 + DOWN * 0.8)

        self.play(Create(graph_axes), Write(graph_lbl), run_time=2.0)
        self.play(Create(llm_curve), Create(uniform_curve), run_time=2.0)
        self.play(Create(safety_card), run_time=2.0)
        self.wait(30.0) # Accumulate to 135.0s

        # =========================================================================
        # PHASE 4: CHAPTER 2 INTRODUCTION TRANSITION (135.0s - 180.0s)
        # =========================================================================
        self.play(
            FadeOut(graph_axes), FadeOut(graph_lbl),
            FadeOut(llm_curve), FadeOut(uniform_curve),
            FadeOut(safety_card),
            run_time=1.5
        )

        learned_env_lbl = Tex(r"\text{Bước chuyển tất yếu: Dịch chuyển sang các Môi trường Tự học được (Learned Simulators)}", color=WHITE).scale(0.8)
        self.play(Write(learned_env_lbl), run_time=2.0)
        self.wait(10.0) # Accumulate to 148.5s
        
        # Final Chapter Title transition
        ch2_title = Tex(r"\text{\textbf{02. Foundation World Models}}", color=GOLD).scale(1.3)
        self.play(ReplacementTransform(learned_env_lbl, ch2_title), run_time=2.5)
        self.wait(27.5) # Wait to finish total 180 seconds
        
        self.play(FadeOut(ch2_title), FadeOut(title), run_time=1.5)
