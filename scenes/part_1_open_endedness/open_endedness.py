from manim import *
import numpy as np
import os
import random
# Set default TexTemplate to support Vietnamese using XeLaTeX
vietnamese_template = TexTemplate(tex_compiler="xelatex", output_format=".xdv")
vietnamese_template.add_to_preamble(r"\usepackage{xcolor}")
vietnamese_template.add_to_preamble(r"\usepackage{amsmath}")
vietnamese_template.add_to_preamble(r"\usepackage{amsfonts}")
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
        Tex(rf"$\bullet$\ \text{{{item}}}", color=WHITE).scale(0.7)
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
    Visualizes Lisa Simpson's evolutionary Petri dish (SC_02) with high-fidelity organic cells
    and golden city structures.
    """
    def __init__(self, radius=2.5, **kwargs):
        super().__init__(**kwargs)
        # Thick glass outer ring
        self.glass_outer = Circle(radius=radius + 0.1, color=GRAY_A, stroke_width=4, stroke_opacity=0.4)
        self.glass_inner = Circle(radius=radius, color=GRAY_B, stroke_width=2, stroke_opacity=0.6)
        
        # Dish background agar jelly (semi-transparent teal/blue tint)
        self.agar = Circle(radius=radius, color=BLUE_E, fill_color=BLUE_E, fill_opacity=0.08, stroke_width=0)
        
        # Red and yellow organic nutrient particles floating around
        self.nutrients = VGroup()
        for _ in range(40):
            p = Dot(point=np.array([
                np.random.uniform(-1.8, 1.8),
                np.random.uniform(-1.8, 1.8),
                0.0
            ]), radius=np.random.uniform(0.02, 0.05), color=random.choice([RED, GOLD, ORANGE]), fill_opacity=0.6)
            if np.linalg.norm(p.get_center()) < radius - 0.25:
                self.nutrients.add(p)
        
        # The initial Tooth structure
        self.tooth_base = Circle(radius=0.25, color=WHITE, fill_color=WHITE, fill_opacity=0.85).shift(UP * 0.1)
        self.tooth_root1 = Circle(radius=0.15, color=WHITE, fill_color=WHITE, fill_opacity=0.85).shift(DOWN * 0.15 + LEFT * 0.1)
        self.tooth_root2 = Circle(radius=0.15, color=WHITE, fill_color=WHITE, fill_opacity=0.85).shift(DOWN * 0.15 + RIGHT * 0.1)
        self.tooth = VGroup(self.tooth_base, self.tooth_root1, self.tooth_root2).move_to(ORIGIN)
        self.tooth_center = self.tooth  # Backwards compatibility with SC_02 usage
        
        # Organic cells (initially empty)
        self.cells = VGroup()
        
        # Golden city elements (initially empty)
        self.city = VGroup()
        
        self.add(self.agar, self.glass_outer, self.glass_inner, self.nutrients, self.tooth, self.cells, self.city)

    def wiggle_updater(self, m, dt):
        for cell in m:
            noise = np.array([np.random.normal(0, 0.1), np.random.normal(0, 0.1), 0.0])
            home = cell.home_pos
            current = cell.get_center()
            dir_to_home = home - current
            cell.shift(noise * dt + dir_to_home * dt * 0.4)

    def mutate_cells_animation(self, scene):
        cell_positions = [
            UP * 0.3 + LEFT * 0.2, UP * 0.4 + RIGHT * 0.3,
            DOWN * 0.2 + LEFT * 0.4, DOWN * 0.3 + RIGHT * 0.1,
            LEFT * 0.6, RIGHT * 0.5, UP * 0.8 + LEFT * 0.5, DOWN * 0.6 + RIGHT * 0.4
        ]
        
        for pos in cell_positions:
            r = np.random.uniform(0.12, 0.22)
            c_color = random.choice([GREEN_C, BLUE_C])
            cell_body = Circle(radius=r, color=c_color, fill_color=c_color, fill_opacity=0.35, stroke_width=2)
            cell_nucleus = Dot(radius=r * 0.25, color=c_color).move_to(pos + np.random.uniform(-0.03, 0.03, 3))
            single_cell = VGroup(cell_body, cell_nucleus).move_to(pos)
            single_cell.home_pos = pos
            self.cells.add(single_cell)
            
        # Shockwave ring
        glow_ring = Circle(radius=0.1, color=YELLOW, stroke_width=3).move_to(self.tooth.get_center())
        
        scene.play(
            FadeOut(self.tooth, scale=1.5),
            glow_ring.animate.scale(12.0).set_stroke(opacity=0),
            FadeIn(self.cells, scale=0.5),
            run_time=0.8
        )
        scene.remove(glow_ring)
        
        self.cells.add_updater(lambda m, dt: self.wiggle_updater(m, dt))

    def evolve_to_city_animation(self, scene):
        # Create city structures
        skyline = VGroup()
        x_offsets = [-0.9, -0.6, -0.3, 0.0, 0.3, 0.6, 0.9]
        for x in x_offsets:
            h = np.random.uniform(0.3, 0.95)
            w = 0.15
            building = Rectangle(width=w, height=h, color=GOLD, fill_color=GOLD_E, fill_opacity=0.7, stroke_width=1.5)
            building.move_to(np.array([x, -0.6 + h/2.0, 0.0]))
            skyline.add(building)
            
        circuits = VGroup()
        nodes = VGroup()
        circuit_points = [
            [np.array([-1.5, -0.6, 0.0]), np.array([-0.9, -0.6, 0.0])],
            [np.array([1.5, -0.6, 0.0]), np.array([0.9, -0.6, 0.0])],
            [np.array([-0.6, 0.2, 0.0]), np.array([-0.3, 0.5, 0.0]), np.array([0.3, 0.5, 0.0]), np.array([0.6, 0.1, 0.0])],
            [np.array([-1.0, 0.5, 0.0]), np.array([-0.6, 0.8, 0.0])],
            [np.array([1.0, 0.5, 0.0]), np.array([0.6, 0.8, 0.0])]
        ]
        
        for path in circuit_points:
            for j in range(len(path) - 1):
                circuits.add(Line(path[j], path[j+1], color=GOLD, stroke_width=1.5, stroke_opacity=0.6))
            for pt in path:
                nodes.add(Dot(point=pt, radius=0.045, color=ORANGE))
                
        self.city.add(circuits, skyline, nodes)
        self.city.scale(1.1)
        
        self.cells.clear_updaters()
        
        scene.play(
            FadeOut(self.cells, scale=1.3),
            FadeIn(self.city, scale=0.8),
            run_time=2.0
        )
        
        city_pulses = VGroup(*[
            Dot(radius=0.035, color=WHITE).move_to(circuits[i % len(circuits)].get_start())
            for i in range(5)
        ])
        self.city.add(city_pulses)
        
        def update_city_pulses(m, dt):
            for i, p in enumerate(city_pulses):
                line = circuits[i % len(circuits)]
                start = line.get_start()
                end = line.get_end()
                if not hasattr(p, "progress"):
                    p.progress = np.random.uniform(0.0, 1.0)
                p.progress += dt * 1.5
                if p.progress >= 1.0:
                    p.progress = 0.0
                p.move_to((1 - p.progress) * start + p.progress * end)
                
        city_pulses.add_updater(update_city_pulses)


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
            ["\\#", "\\#", "\\#", "\\#", "\\#", "\\#", "\\#", "\\#"],
            ["\\#", ".", ".", ".", ".", ".", ".", "\\#"],
            ["\\#", ".", "@", ".", ".", "d", ".", "\\#"],
            ["\\#", ".", ".", ".", ".", ".", "D", "\\#"],
            ["\\#", "\\#", "\\#", "\\#", "\\#", "\\#", "\\#", "\\#"]
        ]
        self.ascii_grid = VGroup()
        self.grid_cells = []
        for r_idx, row in enumerate(grid_data):
            row_grp = VGroup()
            for c_idx, val in enumerate(row):
                color = BLUE_C if val == "@" else (ORANGE if val == "d" else (RED if val == "D" else GRAY_A))
                char_tex = Tex(rf"\texttt{{{val}}}", color=color).scale(0.85)
                char_pos = RIGHT * (c_idx - 3.5) * 0.75 + DOWN * (r_idx - 2.0) * 0.75
                char_tex.move_to(char_pos)
                row_grp.add(char_tex)
                self.grid_cells.append((r_idx, c_idx, val, char_tex))
            self.ascii_grid.add(row_grp)
        
        self.lens = Circle(radius=0.9, color=GOLD, stroke_width=3, fill_color=BLACK, fill_opacity=0.1)
        self.lens_handle = Line(start=self.lens.get_bottom(), end=self.lens.get_bottom() + DOWN * 0.5 + RIGHT * 0.5, color=GOLD, stroke_width=3)
        self.magnifier = VGroup(self.lens, self.lens_handle)
        self.magnifier.move_to(LEFT * 4.0 + UP * 1.5)
        
        self.add(self.ascii_grid, self.magnifier)


class GoldilocksZoneMeter(VGroup):
    """
    Visualizes task difficulty distributions: Easy, Goldilocks, and Hard zones (SC_06, SC_07).
    """
    def __init__(self, width=0.8, height=4.0, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.height = height
        zone_height = height / 3
        self.easy_zone = Rectangle(width=width, height=zone_height, color=BLUE_C, fill_color=BLUE_E, fill_opacity=0.46, stroke_width=0)
        self.goldilocks_zone = Rectangle(width=width, height=zone_height, color=GOLD, fill_color=GOLD_E, fill_opacity=0.68, stroke_width=0)
        self.hard_zone = Rectangle(width=width, height=zone_height, color=RED, fill_color=RED_E, fill_opacity=0.50, stroke_width=0)
        
        self.easy_zone.shift(DOWN * zone_height)
        self.goldilocks_zone.move_to(ORIGIN)
        self.hard_zone.shift(UP * zone_height)
        
        self.zones = VGroup(self.easy_zone, self.goldilocks_zone, self.hard_zone)
        self.frame = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.08,
            color=GRAY_A,
            stroke_width=1.4,
            stroke_opacity=0.82,
        )
        self.dividers = VGroup(
            Line(LEFT * width / 2, RIGHT * width / 2, color=GRAY_A, stroke_width=1.0, stroke_opacity=0.45).shift(DOWN * zone_height / 2),
            Line(LEFT * width / 2, RIGHT * width / 2, color=GRAY_A, stroke_width=1.0, stroke_opacity=0.45).shift(UP * zone_height / 2),
        )
        self.ticks = VGroup()
        for y in np.linspace(-height / 2, height / 2, 9):
            tick = Line(
                RIGHT * (width / 2 + 0.03) + UP * y,
                RIGHT * (width / 2 + 0.18) + UP * y,
                color=GRAY_B,
                stroke_width=0.9,
                stroke_opacity=0.55,
            )
            self.ticks.add(tick)
        
        self.easy_lbl = Tex(r"\text{Quá dễ}", color=BLUE_C).scale(0.50).next_to(self.easy_zone, LEFT, buff=0.24)
        self.gold_lbl = Tex(r"\text{Goldilocks}", color=GOLD).scale(0.54).next_to(self.goldilocks_zone, LEFT, buff=0.24)
        self.hard_lbl = Tex(r"\text{Quá khó}", color=RED).scale(0.50).next_to(self.hard_zone, LEFT, buff=0.24)
        self.labels = VGroup(self.easy_lbl, self.gold_lbl, self.hard_lbl)
        
        pointer_y = -zone_height
        self.pointer_line = Line(
            RIGHT * (width / 2 + 0.16),
            RIGHT * (width / 2 + 0.92),
            color=WHITE,
            stroke_width=2.6,
            stroke_opacity=0.92,
        ).shift(UP * pointer_y)
        self.pointer_tip = Triangle(color=WHITE, fill_color=WHITE, fill_opacity=1.0).scale(0.11).rotate(PI / 2)
        self.pointer_tip.next_to(self.pointer_line.get_start(), LEFT, buff=0.01)
        self.pointer_glow = Line(
            LEFT * width / 2,
            RIGHT * width / 2,
            color=WHITE,
            stroke_width=5.0,
            stroke_opacity=0.18,
        ).shift(UP * pointer_y)
        self.pointer = VGroup(self.pointer_glow, self.pointer_tip, self.pointer_line)
        
        self.add(self.zones, self.frame, self.dividers, self.ticks, self.labels, self.pointer)

    def point_for_level(self, level):
        level = np.clip(level, 0.0, 1.0)
        return self.get_center() + UP * (-self.height / 2 + level * self.height)


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
        title.scale(0.88).to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=1.0)

        def glass_card(width, height, color, center=ORIGIN, fill_opacity=0.12, stroke_width=1.4):
            base = RoundedRectangle(
                width=width,
                height=height,
                corner_radius=0.18,
                color=color,
                fill_color=color,
                fill_opacity=fill_opacity,
                stroke_width=stroke_width,
                stroke_opacity=0.75,
            ).move_to(center)
            shine = Line(
                base.get_corner(UL) + RIGHT * 0.25 + DOWN * 0.18,
                base.get_corner(UR) + LEFT * 0.25 + DOWN * 0.18,
                color=WHITE,
                stroke_width=1.0,
                stroke_opacity=0.18,
            )
            return VGroup(base, shine)

        def safe_tex_lines(lines, color=WHITE, scale=0.58, buff=0.16, aligned_edge=ORIGIN):
            group = VGroup(*[Tex(rf"\text{{{line}}}", color=color).scale(scale) for line in lines])
            if aligned_edge is ORIGIN:
                group.arrange(DOWN, buff=buff)
            else:
                group.arrange(DOWN, buff=buff, aligned_edge=aligned_edge)
            return group

        def make_label(text, color, scale=0.5):
            return Tex(rf"\text{{{text}}}", color=color).scale(scale)

        self.wait(0.4)

        # =========================================================================
        # PHASE 1: DATA SATURATION CHALLENGE (0.0s - 30.0s)
        # =========================================================================
        phase1_title = make_label("Pha 1: Giới hạn của dữ liệu tĩnh", GOLD, 0.62)
        phase1_title.next_to(title, DOWN, buff=0.24)

        db_center = LEFT * 4.0 + DOWN * 0.25
        db_layers = VGroup()
        for idx, opacity in enumerate([0.20, 0.32, 0.46]):
            layer = RoundedRectangle(
                width=3.35,
                height=0.52,
                corner_radius=0.12,
                color=interpolate_color(ManimColor(BLUE_D), ManimColor(BLUE_C), idx / 3),
                fill_color=interpolate_color(ManimColor(BLUE_D), ManimColor(BLUE_C), idx / 3),
                fill_opacity=opacity,
                stroke_width=1.4,
                stroke_opacity=0.85,
            ).move_to(db_center + UP * idx * 0.68)
            rim = Arc(
                radius=1.58,
                start_angle=PI,
                angle=PI,
                color=GRAY_B,
                stroke_width=1.0,
                stroke_opacity=0.22,
            ).stretch_to_fit_height(0.25).move_to(layer.get_top() + DOWN * 0.03)
            db_layers.add(VGroup(layer, rim))

        db_label = VGroup(
            Tex(r"\text{Offline Data}", color=BLUE_C).scale(0.58),
            Tex(r"$10^{15}\ \text{tokens}$", color=BLUE_C).scale(0.58),
        ).arrange(DOWN, buff=0.10)
        db_label.move_to(db_layers[1].get_center())
        db_caption = make_label("Kho tri thức nhân loại", GRAY_A, 0.45).next_to(db_layers, DOWN, buff=0.28)
        database = VGroup(db_layers, db_label, db_caption)

        network_box = RoundedRectangle(
            width=4.15,
            height=2.55,
            corner_radius=0.16,
            color=GRAY_A,
            fill_color=BLACK,
            fill_opacity=0.55,
            stroke_width=1.1,
            stroke_opacity=0.55,
        ).move_to(RIGHT * 3.8 + UP * 0.35)
        network_title = make_label("Neural Model", GRAY_B, 0.48).next_to(network_box, UP, buff=0.20)

        input_nodes = VGroup(*[
            Circle(radius=0.105, color=BLUE_C, fill_color=BLUE_D, fill_opacity=0.75, stroke_width=1.1)
            for _ in range(3)
        ]).arrange(DOWN, buff=0.38).move_to(network_box.get_center() + LEFT * 1.35)
        hidden_nodes = VGroup(*[
            Circle(radius=0.095, color=GRAY_A, fill_color=GRAY_E, fill_opacity=0.78, stroke_width=1.0)
            for _ in range(4)
        ]).arrange(DOWN, buff=0.27).move_to(network_box.get_center())
        output_nodes = VGroup(*[
            Circle(radius=0.105, color=ORANGE, fill_color=ORANGE, fill_opacity=0.65, stroke_width=1.0)
            for _ in range(2)
        ]).arrange(DOWN, buff=0.50).move_to(network_box.get_center() + RIGHT * 1.35)

        connections = VGroup()
        for left_node in input_nodes:
            for mid_node in hidden_nodes:
                connections.add(Line(
                    left_node.get_center(),
                    mid_node.get_center(),
                    color=GRAY_B,
                    stroke_width=0.9,
                    stroke_opacity=0.24,
                ))
        for mid_node in hidden_nodes:
            for right_node in output_nodes:
                connections.add(Line(
                    mid_node.get_center(),
                    right_node.get_center(),
                    color=GRAY_B,
                    stroke_width=0.9,
                    stroke_opacity=0.24,
                ))
        network = VGroup(network_box, connections, input_nodes, hidden_nodes, output_nodes, network_title)

        pipe = DashedLine(
            database.get_right() + RIGHT * 0.18,
            network_box.get_left() + LEFT * 0.18,
            color=GRAY_B,
            stroke_width=1.2,
            dashed_ratio=0.55,
        ).set_opacity(0.35)

        self.play(
            FadeIn(phase1_title, shift=DOWN * 0.1),
            LaggedStart(*[FadeIn(layer, shift=UP * 0.1) for layer in db_layers], lag_ratio=0.18),
            FadeIn(db_label),
            FadeIn(db_caption),
            Create(pipe),
            Create(network_box),
            FadeIn(network_title),
            Create(connections),
            LaggedStart(FadeIn(input_nodes), FadeIn(hidden_nodes), FadeIn(output_nodes), lag_ratio=0.22),
            run_time=2.4,
        )

        data_particles = VGroup()
        for idx in range(20):
            dot = Dot(color=interpolate_color(ManimColor(BLUE_C), ManimColor(WHITE), 0.20), radius=0.032 + 0.006 * (idx % 3))
            dot.progress = random.random()
            dot.y_offset = np.random.uniform(-0.32, 0.32)
            data_particles.add(dot)

        neural_pulses = VGroup()
        all_paths = []
        for left_node in input_nodes:
            for mid_node in hidden_nodes:
                for right_node in output_nodes:
                    all_paths.append([left_node.get_center(), mid_node.get_center(), right_node.get_center()])
        for idx in range(8):
            pulse = Dot(color=GOLD, radius=0.036)
            pulse.progress = random.random()
            pulse.path_points = random.choice(all_paths)
            neural_pulses.add(pulse)

        stream_start = db_layers.get_right() + RIGHT * 0.12
        stream_end = input_nodes.get_left() + LEFT * 0.12

        def update_data_particles(group, dt):
            for dot in group:
                dot.progress = (dot.progress + dt * 0.27) % 1.0
                eased = smooth(dot.progress)
                pos = interpolate(stream_start, stream_end, eased)
                pos += UP * (dot.y_offset + 0.05 * np.sin(TAU * dot.progress * 2.0))
                dot.move_to(pos)
                dot.set_opacity(0.30 + 0.70 * np.sin(PI * dot.progress))

        def update_neural_pulses(group, dt):
            for pulse in group:
                pulse.progress += dt * np.random.uniform(0.42, 0.48)
                if pulse.progress >= 1.0:
                    pulse.progress = 0.0
                    pulse.path_points = random.choice(all_paths)
                p_val = pulse.progress
                if p_val < 0.5:
                    local_t = smooth(p_val * 2.0)
                    pos = interpolate(pulse.path_points[0], pulse.path_points[1], local_t)
                else:
                    local_t = smooth((p_val - 0.5) * 2.0)
                    pos = interpolate(pulse.path_points[1], pulse.path_points[2], local_t)
                pulse.move_to(pos)
                pulse.set_opacity(0.20 + 0.80 * np.sin(PI * p_val))

        data_particles.add_updater(update_data_particles)
        neural_pulses.add_updater(update_neural_pulses)
        self.add(data_particles, neural_pulses)
        self.wait(8.0)

        data_particles.clear_updaters()
        neural_pulses.clear_updaters()
        saturation_line = DashedLine(
            network_box.get_left() + UP * 1.03,
            network_box.get_right() + UP * 1.03,
            color=RED,
            stroke_width=3.2,
            dashed_ratio=0.56,
        )
        warning_card = RoundedRectangle(
            width=4.25,
            height=1.02,
            corner_radius=0.14,
            color=RED,
            fill_color=RED_E,
            fill_opacity=0.24,
            stroke_width=1.4,
            stroke_opacity=0.88,
        ).next_to(network_box, DOWN, buff=0.34)
        warning_lines = safe_tex_lines(
            ["Physical Saturation Point", "Điểm bão hòa vật lý"],
            color=RED,
            scale=0.52,
            buff=0.10,
        )
        warning_lines.move_to(warning_card.get_center())
        warning_group = VGroup(warning_card, warning_lines)

        self.play(
            db_layers.animate.set_color(GRAY_E).set_fill(GRAY_E, opacity=0.12),
            db_label.animate.set_color(GRAY_B),
            db_caption.animate.set_color(GRAY_B),
            pipe.animate.set_color(GRAY_E).set_opacity(0.18),
            connections.animate.set_color(GRAY_E).set_opacity(0.12),
            input_nodes.animate.set_color(GRAY_B).set_fill(GRAY_E, opacity=0.50),
            hidden_nodes.animate.set_color(GRAY_B).set_fill(GRAY_E, opacity=0.50),
            output_nodes.animate.set_color(GRAY_B).set_fill(GRAY_E, opacity=0.50),
            FadeOut(data_particles),
            FadeOut(neural_pulses),
            Create(saturation_line),
            FadeIn(warning_card, shift=UP * 0.12),
            LaggedStart(*[Write(line) for line in warning_lines], lag_ratio=0.18),
            run_time=2.2,
        )
        self.wait(16.0)

        # =========================================================================
        # PHASE 2: ERA OF EXPERIENCE INTRODUCTION (30.0s - 70.0s)
        # =========================================================================
        self.play(
            FadeOut(phase1_title),
            FadeOut(database),
            FadeOut(network),
            FadeOut(pipe),
            FadeOut(saturation_line),
            FadeOut(warning_group),
            run_time=1.4,
        )

        card = glass_card(10.4, 4.75, GOLD, center=DOWN * 0.20, fill_opacity=0.10, stroke_width=1.5)
        card_bg = card[0]
        quote_left = Tex(r"\text{``}", color=GOLD_E).scale(2.8)
        quote_right = Tex(r"\text{''}", color=GOLD_E).scale(2.8)
        quote_left.move_to(card_bg.get_corner(UL) + RIGHT * 0.52 + DOWN * 0.50)
        quote_right.move_to(card_bg.get_corner(DR) + LEFT * 0.52 + UP * 0.55)

        question = make_label("Làm sao để AI tự quyết định nên học gì tiếp theo?", WHITE, 0.68)
        question.move_to(card_bg.get_center() + UP * 1.20)
        question_underline = Line(
            question.get_left() + DOWN * 0.22,
            question.get_right() + DOWN * 0.22,
            color=GOLD,
            stroke_width=1.4,
            stroke_opacity=0.50,
        )

        quote_lines = VGroup(
            make_label("The Era of Experience", GOLD, 0.74),
            make_label("Tri thức mới đến từ vòng lặp hành động", GRAY_A, 0.55),
            make_label("quan sát, thử nghiệm, và tự chọn dữ liệu để học", GRAY_A, 0.55),
            make_label("David Silver \\& Richard Sutton", BLUE_C, 0.52),
        ).arrange(DOWN, buff=0.18).move_to(card_bg.get_center() + DOWN * 0.48)

        self.play(FadeIn(card, shift=UP * 0.12), FadeIn(quote_left), FadeIn(quote_right), run_time=1.4)
        self.play(Write(question), Create(question_underline), run_time=1.8)
        self.wait(8.5)
        self.play(
            LaggedStart(*[FadeIn(line, shift=UP * 0.12) for line in quote_lines], lag_ratio=0.22),
            run_time=2.6,
        )
        self.wait(25.7)

        # =========================================================================
        # PHASE 3: Watts' ORGANISM-ENVIRONMENT MUTUALITY (70.0s - 110.0s)
        # =========================================================================
        self.play(
            FadeOut(card),
            FadeOut(quote_left),
            FadeOut(quote_right),
            FadeOut(question),
            FadeOut(question_underline),
            FadeOut(quote_lines),
            run_time=1.3,
        )

        watts_title = make_label("Alan Watts (1972): Sinh vật và môi trường đồng kiến tạo", GOLD, 0.68)
        watts_title.next_to(title, DOWN, buff=0.26)
        watts_quote = make_label("Môi trường nuôi dưỡng sinh vật, sinh vật kiến tạo môi trường.", GRAY_A, 0.50)
        watts_quote.next_to(watts_title, DOWN, buff=0.22)

        org_center = LEFT * 3.35 + DOWN * 0.60
        cell_glow = VGroup(*[
            Circle(
                radius=0.86 + 0.12 * idx,
                color=BLUE_C,
                stroke_width=1.0,
                stroke_opacity=0.16 - idx * 0.035,
            ).move_to(org_center)
            for idx in range(3)
        ])
        cell_body = Circle(
            radius=0.82,
            color=BLUE_C,
            fill_color=BLUE_E,
            fill_opacity=0.20,
            stroke_width=2.2,
            stroke_opacity=0.80,
        ).move_to(org_center)
        nucleus = Circle(
            radius=0.18,
            color=BLUE_D,
            fill_color=BLUE_D,
            fill_opacity=0.85,
            stroke_width=1.0,
        ).move_to(org_center)
        orbit_a = Ellipse(width=1.20, height=0.58, color=BLUE_C, stroke_width=1.0, stroke_opacity=0.38).move_to(org_center)
        orbit_b = Ellipse(width=0.72, height=1.22, color=BLUE_C, stroke_width=1.0, stroke_opacity=0.32).move_to(org_center).rotate(18 * DEGREES)
        electron_a = Dot(color=interpolate_color(ManimColor(BLUE_C), ManimColor(WHITE), 0.25), radius=0.045)
        electron_b = Dot(color=interpolate_color(ManimColor(BLUE_C), ManimColor(WHITE), 0.10), radius=0.04)
        electron_a.theta = 0.15
        electron_b.theta = PI

        def orbit_point(center, width, height, angle, rotation=0.0):
            raw = np.array([0.5 * width * np.cos(angle), 0.5 * height * np.sin(angle), 0.0])
            rot = np.array([
                raw[0] * np.cos(rotation) - raw[1] * np.sin(rotation),
                raw[0] * np.sin(rotation) + raw[1] * np.cos(rotation),
                0.0,
            ])
            return center + rot

        def update_electron_a(dot, dt):
            dot.theta += 2.35 * dt
            dot.move_to(orbit_point(org_center, 1.20, 0.58, dot.theta))

        def update_electron_b(dot, dt):
            dot.theta -= 1.75 * dt
            dot.move_to(orbit_point(org_center, 0.72, 1.22, dot.theta, 18 * DEGREES))

        electron_a.add_updater(update_electron_a)
        electron_b.add_updater(update_electron_b)
        organism = VGroup(cell_glow, cell_body, nucleus, orbit_a, orbit_b, electron_a, electron_b)
        org_label = make_label("Sinh vật (Organism)", BLUE_C, 0.58).next_to(cell_body, UP, buff=0.28)

        env_center = RIGHT * 3.35 + DOWN * 0.60
        env_offsets = [UP * 0.78, LEFT * 0.76 + UP * 0.25, RIGHT * 0.76 + UP * 0.20, LEFT * 0.46 + DOWN * 0.72, RIGHT * 0.50 + DOWN * 0.68]
        env_nodes = VGroup(*[
            Circle(radius=0.105, color=GREEN_C, fill_color=GREEN_E, fill_opacity=0.74, stroke_width=1.0).move_to(env_center + offset)
            for offset in env_offsets
        ])
        env_edges = VGroup()
        edge_pairs = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4), (0, 4), (2, 3)]
        for left_idx, right_idx in edge_pairs:
            env_edges.add(Line(
                env_nodes[left_idx].get_center(),
                env_nodes[right_idx].get_center(),
                color=GREEN_C,
                stroke_width=1.0,
                stroke_opacity=0.32,
            ))
        environment = VGroup(env_edges, env_nodes)
        env_label = make_label("Môi trường (Environment)", GREEN_C, 0.58).next_to(env_nodes, UP, buff=0.28)

        grows_arc = ArcBetweenPoints(
            env_center + LEFT * 0.78 + UP * 0.88,
            org_center + RIGHT * 0.78 + UP * 0.88,
            angle=-TAU / 7,
            color=GREEN_C,
            stroke_width=2.0,
        ).add_tip(tip_length=0.16, tip_width=0.10)
        creates_arc = ArcBetweenPoints(
            org_center + RIGHT * 0.78 + DOWN * 0.88,
            env_center + LEFT * 0.78 + DOWN * 0.88,
            angle=-TAU / 7,
            color=BLUE_C,
            stroke_width=2.0,
        ).add_tip(tip_length=0.16, tip_width=0.10)
        grows_label = make_label("Nuôi dưỡng (Grows)", GREEN_C, 0.43).next_to(grows_arc, UP, buff=0.18)
        creates_label = make_label("Kiến tạo (Creates)", BLUE_C, 0.43).next_to(creates_arc, DOWN, buff=0.18)

        grows_pulse = Dot(color=GREEN_C, radius=0.055)
        creates_pulse = Dot(color=BLUE_C, radius=0.055)
        grows_pulse.alpha = 0.0
        creates_pulse.alpha = 0.45

        def update_arc_pulse(dot, dt, path):
            dot.alpha = (dot.alpha + dt * 0.18) % 1.0
            dot.move_to(path.point_from_proportion(smooth(dot.alpha)))
            dot.set_opacity(0.25 + 0.75 * np.sin(PI * dot.alpha))

        grows_pulse.add_updater(lambda m, dt: update_arc_pulse(m, dt, grows_arc))
        creates_pulse.add_updater(lambda m, dt: update_arc_pulse(m, dt, creates_arc))

        self.play(
            FadeIn(watts_title, shift=DOWN * 0.1),
            FadeIn(watts_quote, shift=DOWN * 0.1),
            LaggedStart(Create(cell_glow), Create(cell_body), FadeIn(nucleus), Create(orbit_a), Create(orbit_b), lag_ratio=0.15),
            FadeIn(electron_a),
            FadeIn(electron_b),
            Write(org_label),
            LaggedStart(Create(env_edges), FadeIn(env_nodes), lag_ratio=0.24),
            Write(env_label),
            run_time=2.8,
        )
        self.wait(8.8)
        self.play(
            Create(grows_arc),
            Create(creates_arc),
            FadeIn(grows_label, shift=DOWN * 0.08),
            FadeIn(creates_label, shift=UP * 0.08),
            run_time=2.0,
        )
        self.add(grows_pulse, creates_pulse)
        self.wait(25.1)

        # =========================================================================
        # PHASE 4: NON-LINEAR TECHNOLOGICAL PROGRESS (110.0s - 180.0s)
        # =========================================================================
        electron_a.clear_updaters()
        electron_b.clear_updaters()
        grows_pulse.clear_updaters()
        creates_pulse.clear_updaters()
        self.play(
            FadeOut(watts_title),
            FadeOut(watts_quote),
            FadeOut(organism),
            FadeOut(org_label),
            FadeOut(environment),
            FadeOut(env_label),
            FadeOut(grows_arc),
            FadeOut(grows_label),
            FadeOut(creates_arc),
            FadeOut(creates_label),
            FadeOut(grows_pulse),
            FadeOut(creates_pulse),
            run_time=1.4,
        )

        phase4_title = make_label("Tiến bộ mở không đi theo đường thẳng", GOLD, 0.70)
        phase4_title.next_to(title, DOWN, buff=0.26)

        left_card = glass_card(4.75, 3.45, BLUE_C, center=LEFT * 2.85 + DOWN * 0.35, fill_opacity=0.08)
        right_card = glass_card(4.75, 3.45, ORANGE, center=RIGHT * 2.85 + DOWN * 0.35, fill_opacity=0.08)

        left_card_box = left_card[0]
        right_card_box = right_card[0]
        vacuum_title = make_label("Ống chân không", BLUE_C, 0.60).next_to(left_card_box.get_top(), DOWN, buff=0.30)
        vacuum_year = make_label("1900s", GRAY_A, 0.45).next_to(vacuum_title, DOWN, buff=0.12)
        eniac_title = make_label("Máy tính ENIAC", ORANGE, 0.60).next_to(right_card_box.get_top(), DOWN, buff=0.30)
        eniac_year = make_label("1940s", GRAY_A, 0.45).next_to(eniac_title, DOWN, buff=0.12)

        bulb_glow = Circle(radius=0.48, color=GOLD, stroke_width=1.0, stroke_opacity=0.18).move_to(left_card_box.get_center() + DOWN * 0.10)
        bulb = Circle(radius=0.34, color=GOLD, fill_color=GOLD_E, fill_opacity=0.16, stroke_width=1.8).move_to(bulb_glow.get_center() + UP * 0.12)
        filament = VMobject(color=GOLD, stroke_width=2.2)
        filament.set_points_smoothly([
            bulb.get_center() + LEFT * 0.16 + DOWN * 0.02,
            bulb.get_center() + LEFT * 0.08 + UP * 0.08,
            bulb.get_center() + RIGHT * 0.02 + DOWN * 0.02,
            bulb.get_center() + RIGHT * 0.12 + UP * 0.08,
            bulb.get_center() + RIGHT * 0.18 + DOWN * 0.02,
        ])
        bulb_base = VGroup(
            Rectangle(width=0.42, height=0.16, color=GRAY_A, fill_color=GRAY_E, fill_opacity=0.82, stroke_width=1.0),
            Rectangle(width=0.30, height=0.18, color=GRAY_A, fill_color=GRAY_E, fill_opacity=0.82, stroke_width=1.0),
        ).arrange(DOWN, buff=0.02).next_to(bulb, DOWN, buff=0.02)
        vacuum_icon = VGroup(bulb_glow, bulb, filament, bulb_base)

        chip = RoundedRectangle(
            width=1.46,
            height=1.06,
            corner_radius=0.06,
            color=ORANGE,
            fill_color=GRAY_E,
            fill_opacity=0.75,
            stroke_width=1.4,
        ).move_to(right_card_box.get_center() + DOWN * 0.04)
        circuit_lines = VGroup()
        for idx, y in enumerate(np.linspace(-0.34, 0.34, 4)):
            circuit_lines.add(Line(
                chip.get_left() + RIGHT * 0.18 + UP * y,
                chip.get_right() + LEFT * 0.18 + UP * y,
                color=GOLD if idx % 2 == 0 else ORANGE,
                stroke_width=1.2,
                stroke_opacity=0.72,
            ))
        for idx, x in enumerate(np.linspace(-0.48, 0.48, 4)):
            circuit_lines.add(Line(
                chip.get_bottom() + UP * 0.15 + RIGHT * x,
                chip.get_top() + DOWN * 0.15 + RIGHT * x,
                color=ORANGE if idx % 2 == 0 else GOLD,
                stroke_width=1.0,
                stroke_opacity=0.58,
            ))
        pins = VGroup()
        for side in [UP, DOWN]:
            for x in np.linspace(-0.52, 0.52, 5):
                pins.add(Line(
                    chip.get_center() + RIGHT * x + side * 0.53,
                    chip.get_center() + RIGHT * x + side * 0.72,
                    color=GRAY_A,
                    stroke_width=1.0,
                    stroke_opacity=0.58,
                ))
        eniac_icon = VGroup(chip, circuit_lines, pins)

        straight_arrow = Arrow(
            left_card_box.get_right() + RIGHT * 0.10,
            right_card_box.get_left() + LEFT * 0.10,
            color=GRAY_B,
            stroke_width=2.0,
            buff=0.18,
            max_tip_length_to_length_ratio=0.12,
        ).set_opacity(0.35)
        nonlinear_arc = ArcBetweenPoints(
            left_card_box.get_top() + RIGHT * 0.35,
            right_card_box.get_top() + LEFT * 0.35,
            angle=-TAU / 5,
            color=GOLD,
            stroke_width=3.0,
        ).add_tip(tip_length=0.18, tip_width=0.12)
        arc_label = make_label("Stepping stone", GOLD, 0.46).next_to(nonlinear_arc, UP, buff=0.18)

        claim_lines = VGroup(
            make_label("Một bước đệm hữu ích hôm nay", GRAY_A, 0.52),
            make_label("có thể mở ra một chiều công nghệ hoàn toàn mới.", GRAY_A, 0.52),
            make_label("Đó là tiến bộ phi tuyến tính.", GOLD, 0.58),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.54)

        self.play(
            FadeIn(phase4_title, shift=DOWN * 0.1),
            FadeIn(left_card, shift=RIGHT * 0.12),
            FadeIn(right_card, shift=LEFT * 0.12),
            run_time=1.6,
        )
        self.play(
            LaggedStart(Write(vacuum_title), FadeIn(vacuum_year), Create(vacuum_icon), lag_ratio=0.18),
            LaggedStart(Write(eniac_title), FadeIn(eniac_year), Create(eniac_icon), lag_ratio=0.18),
            run_time=2.5,
        )
        self.play(Create(straight_arrow), run_time=1.0)
        cross_center = straight_arrow.get_center()
        cross = VGroup(
            Line(cross_center + LEFT * 0.20 + UP * 0.20, cross_center + RIGHT * 0.20 + DOWN * 0.20, color=RED, stroke_width=3.2),
            Line(cross_center + LEFT * 0.20 + DOWN * 0.20, cross_center + RIGHT * 0.20 + UP * 0.20, color=RED, stroke_width=3.2),
        )
        self.play(Create(cross), straight_arrow.animate.set_opacity(0.16), run_time=0.8)
        self.play(Create(nonlinear_arc), FadeIn(arc_label, shift=DOWN * 0.08), run_time=1.5)

        glow_ring = Circle(radius=0.42, color=GOLD, stroke_width=2.0).move_to(bulb.get_center())
        self.play(glow_ring.animate.scale(2.25).set_stroke(opacity=0), run_time=1.2)
        self.remove(glow_ring)
        self.play(LaggedStart(*[FadeIn(line, shift=UP * 0.10) for line in claim_lines], lag_ratio=0.20), run_time=2.2)
        self.wait(57.8)

        ending_group = VGroup(
            phase4_title,
            left_card,
            right_card,
            vacuum_title,
            vacuum_year,
            eniac_title,
            eniac_year,
            vacuum_icon,
            eniac_icon,
            straight_arrow,
            cross,
            nonlinear_arc,
            arc_label,
            claim_lines,
            title,
        )
        self.play(FadeOut(ending_group), run_time=1.4)


class SC_02_TheMetaphorOfThePetriDish(VietnameseMovingCameraScene):
    """
    SC_02: The Metaphor of the Petri Dish.
    Focus: Simpsons' Genesis Tub anecdote, evolution of cells to golden city structures, contrasting with closed Go/Chess environments.
    """
    def construct(self):
        load_safe_sound(self, "SC_02_PetriDish.wav")
        title = create_title_banner(r"SC\_02: The Metaphor of the Petri Dish")
        title.scale(0.88).to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=1.0)

        initial_frame_width = self.camera.frame.width
        self.camera.frame.save_state()

        def make_label(text, color=WHITE, scale=0.5):
            return Tex(rf"\text{{{text}}}", color=color).scale(scale)

        def make_text_block(lines, color=WHITE, scale=0.48, buff=0.12):
            return VGroup(*[
                Tex(rf"\text{{{line}}}", color=color).scale(scale)
                for line in lines
            ]).arrange(DOWN, buff=buff)

        def make_tooth(center=ORIGIN):
            body = VMobject(
                color=WHITE,
                fill_color=WHITE,
                fill_opacity=0.90,
                stroke_width=1.4,
                stroke_opacity=0.90,
            )
            points = [
                center + LEFT * 0.24 + UP * 0.20,
                center + LEFT * 0.34 + DOWN * 0.02,
                center + LEFT * 0.20 + DOWN * 0.40,
                center + LEFT * 0.03 + DOWN * 0.23,
                center + RIGHT * 0.13 + DOWN * 0.43,
                center + RIGHT * 0.34 + DOWN * 0.02,
                center + RIGHT * 0.24 + UP * 0.20,
                center + UP * 0.34,
            ]
            body.set_points_smoothly(points + [points[0]])
            highlight = Arc(
                radius=0.18,
                start_angle=PI * 0.82,
                angle=PI * 0.55,
                color=BLUE_C,
                stroke_width=1.0,
                stroke_opacity=0.24,
            ).move_to(center + UP * 0.08 + LEFT * 0.04)
            return VGroup(body, highlight)

        def make_cell(center, radius=0.17, color=GREEN_C, phase=0.0, gold=False):
            body = Circle(
                radius=radius,
                color=GOLD if gold else color,
                fill_color=GOLD_E if gold else color,
                fill_opacity=0.34 if gold else 0.28,
                stroke_width=1.4,
                stroke_opacity=0.88,
            ).move_to(center)
            nucleus = Dot(
                radius=radius * 0.28,
                color=GOLD if gold else GREEN_E,
                fill_opacity=0.92,
            ).move_to(center + RIGHT * radius * 0.16 + UP * radius * 0.08)
            membrane = Circle(
                radius=radius * 1.22,
                color=GOLD if gold else GREEN_C,
                stroke_width=0.8,
                stroke_opacity=0.14,
            ).move_to(center)
            cell = VGroup(membrane, body, nucleus)
            cell.home = np.array(center)
            cell.phase = phase
            cell.drift = np.array([np.cos(phase), np.sin(phase * 1.7), 0.0])
            return cell

        def add_cell_wiggle(cells, amplitude=0.055, speed=1.0, home_pull=3.5):
            def update(group, dt):
                for cell in group:
                    cell.phase += dt * speed * (0.75 + 0.18 * np.sin(cell.phase))
                    offset = np.array([
                        np.sin(cell.phase * 1.3),
                        np.cos(cell.phase * 1.7),
                        0.0,
                    ]) * amplitude
                    target = cell.home + offset + 0.018 * cell.drift * np.sin(cell.phase * 0.6)
                    cell.shift((target - cell.get_center()) * min(1.0, dt * home_pull))
            cells.add_updater(update)

        def make_lightning(start, end, segments=7, color=GOLD):
            direction = end - start
            normal = rotate_vector(direction / max(np.linalg.norm(direction), 1e-6), PI / 2)
            points = [start]
            for i in range(1, segments):
                alpha = i / segments
                jitter = normal * np.random.uniform(-0.18, 0.18)
                points.append(interpolate(start, end, alpha) + jitter)
            points.append(end)
            bolt = VMobject(color=color, stroke_width=3.0, stroke_opacity=0.95)
            bolt.set_points_as_corners(points)
            glow = VMobject(color=BLUE_C, stroke_width=6.0, stroke_opacity=0.18)
            glow.set_points_as_corners(points)
            return VGroup(glow, bolt)

        # =========================================================================
        # PHASE 1: GENESIS TUB ANECDOTE (0.0s - 40.0s)
        # =========================================================================
        dish_center = DOWN * 0.38
        dish_radius = 2.45
        glass_outer = Circle(
            radius=dish_radius + 0.14,
            color=BLUE_C,
            stroke_width=3.5,
            stroke_opacity=0.45,
        ).move_to(dish_center)
        glass_inner = Circle(
            radius=dish_radius,
            color=BLUE_E,
            stroke_width=1.5,
            stroke_opacity=0.66,
        ).move_to(dish_center)
        agar = Circle(
            radius=dish_radius - 0.08,
            color=BLUE_E,
            fill_color=BLUE_E,
            fill_opacity=0.10,
            stroke_width=0,
        ).move_to(dish_center)
        meniscus = Arc(
            radius=dish_radius * 0.78,
            start_angle=PI * 0.08,
            angle=PI * 0.84,
            color=WHITE,
            stroke_width=1.0,
            stroke_opacity=0.12,
        ).move_to(dish_center + UP * 0.24)

        nutrients = VGroup()
        for idx in range(58):
            angle = np.random.uniform(0, TAU)
            radius = dish_radius * np.sqrt(np.random.uniform(0.05, 0.86))
            point = dish_center + np.array([np.cos(angle), np.sin(angle), 0.0]) * radius
            nutrient = Dot(
                point=point,
                radius=np.random.uniform(0.012, 0.030),
                color=random.choice([BLUE_C, GREEN_C, GOLD, WHITE]),
                fill_opacity=np.random.uniform(0.22, 0.52),
            )
            nutrients.add(nutrient)

        tooth = make_tooth(dish_center)
        petri_dish = VGroup(agar, nutrients, meniscus, glass_outer, glass_inner, tooth)
        anecdote_title = make_label("Lisa Simpson: The Genesis Tub (1996)", GOLD, 0.70)
        anecdote_title.next_to(title, DOWN, buff=0.26)
        phase1_note = make_text_block(
            ["Một chiếc răng sữa, nước cola, và một cú kích hoạt ngẫu nhiên."],
            color=GRAY_A,
            scale=0.42,
        ).next_to(glass_outer, DOWN, buff=0.34)

        self.play(
            FadeIn(anecdote_title, shift=DOWN * 0.10),
            FadeIn(agar),
            LaggedStart(FadeIn(nutrients), Create(glass_outer), Create(glass_inner), Create(meniscus), lag_ratio=0.18),
            FadeIn(tooth, scale=0.75),
            FadeIn(phase1_note, shift=UP * 0.08),
            run_time=2.4,
        )
        self.wait(8.6)

        bolt_starts = [
            glass_outer.point_at_angle(PI * 0.20),
            glass_outer.point_at_angle(PI * 0.63),
            glass_outer.point_at_angle(PI * 1.14),
            glass_outer.point_at_angle(PI * 1.72),
        ]
        bolts = VGroup(*[
            make_lightning(start, dish_center + np.random.uniform(-0.14, 0.14, 3), color=GOLD if idx % 2 else BLUE_C)
            for idx, start in enumerate(bolt_starts)
        ])
        flash = Circle(
            radius=0.18,
            color=GOLD,
            fill_color=GOLD,
            fill_opacity=0.25,
            stroke_width=2.0,
        ).move_to(dish_center)

        self.play(
            LaggedStart(*[Create(bolt) for bolt in bolts], lag_ratio=0.08),
            flash.animate.scale(11.0).set_fill(opacity=0).set_stroke(opacity=0),
            run_time=0.65,
            rate_func=linear,
        )
        self.remove(flash)
        for shake in [RIGHT * 0.07, LEFT * 0.10, UP * 0.055, DOWN * 0.04]:
            self.play(self.camera.frame.animate.shift(shake), run_time=0.07)
        self.play(self.camera.frame.animate.move_to(ORIGIN).set(width=initial_frame_width), run_time=0.12)

        bio_cells = VGroup()
        cell_offsets = [
            LEFT * 0.55 + UP * 0.20,
            RIGHT * 0.45 + UP * 0.28,
            LEFT * 0.25 + DOWN * 0.35,
            RIGHT * 0.18 + DOWN * 0.50,
            UP * 0.68,
            LEFT * 0.76 + DOWN * 0.06,
            RIGHT * 0.74 + DOWN * 0.02,
            DOWN * 0.82,
        ]
        for idx, offset in enumerate(cell_offsets):
            bio_cells.add(make_cell(dish_center + offset, radius=np.random.uniform(0.13, 0.21), color=GREEN_C, phase=idx * 0.72))
        add_cell_wiggle(bio_cells, amplitude=0.045, speed=1.15)

        mutation_label = make_label("Lightning Mutate", GOLD, 0.46).next_to(glass_outer, RIGHT, buff=0.38)
        self.play(
            FadeOut(bolts),
            ReplacementTransform(tooth, bio_cells),
            Write(mutation_label),
            run_time=1.4,
        )
        self.wait(26.0)

        self.play(FadeOut(phase1_note), FadeOut(mutation_label), run_time=0.8)

        # =========================================================================
        # PHASE 2: BIOLOGICAL TO CULTURAL EVOLUTION (40.0s - 80.0s)
        # =========================================================================
        self.play(
            self.camera.frame.animate.move_to(dish_center).scale(0.4),
            run_time=2.6,
            rate_func=smooth,
        )
        self.wait(4.4)

        city_label = VGroup(
            Tex(r"\text{Tiến hóa Sinh học}", color=GREEN_C).scale(0.32),
            Tex(r"$\rightarrow$", color=GOLD).scale(0.42),
            Tex(r"\text{Tiến hóa Văn hóa \& Công nghệ}", color=GOLD).scale(0.32),
        ).arrange(RIGHT, buff=0.12)
        city_label.move_to(dish_center + UP * 1.38)

        self.play(Write(city_label), run_time=1.2)

        bio_cells.clear_updaters()
        city_base_y = dish_center[1] - 0.68
        buildings = VGroup()
        for idx, x in enumerate(np.linspace(-1.10, 1.10, 9)):
            height = [0.48, 0.72, 0.58, 0.95, 0.76, 1.18, 0.64, 0.88, 0.52][idx]
            width = 0.16 if idx != 5 else 0.19
            building = Rectangle(
                width=width,
                height=height,
                color=GOLD,
                fill_color=GOLD_E,
                fill_opacity=0.56,
                stroke_width=1.2,
                stroke_opacity=0.92,
            ).move_to(dish_center + RIGHT * x + UP * (city_base_y - dish_center[1] + height / 2))
            if idx in [3, 5, 7]:
                spire = Triangle(
                    color=GOLD,
                    fill_color=GOLD,
                    fill_opacity=0.34,
                    stroke_width=1.0,
                ).scale(0.12).next_to(building, UP, buff=0.00)
                buildings.add(VGroup(building, spire))
            else:
                buildings.add(building)

        roads = VGroup()
        city_nodes = VGroup()
        for y in [-0.90, -0.58, -0.25]:
            roads.add(Line(
                dish_center + LEFT * 1.35 + UP * y,
                dish_center + RIGHT * 1.35 + UP * y,
                color=GOLD,
                stroke_width=1.1,
                stroke_opacity=0.42,
            ))
        for x in [-0.85, -0.35, 0.20, 0.74]:
            roads.add(Line(
                dish_center + RIGHT * x + DOWN * 1.00,
                dish_center + RIGHT * x + UP * 0.02,
                color=GOLD,
                stroke_width=0.9,
                stroke_opacity=0.32,
            ))
        for idx in range(14):
            city_nodes.add(Dot(
                point=dish_center + np.array([np.random.uniform(-1.25, 1.25), np.random.uniform(-0.95, 0.08), 0.0]),
                radius=0.022,
                color=ORANGE,
                fill_opacity=0.85,
            ))
        city_glow = VGroup(*[
            Circle(
                radius=0.55 + 0.22 * idx,
                color=GOLD,
                stroke_width=1.0,
                stroke_opacity=0.12 - idx * 0.025,
            ).move_to(dish_center + DOWN * 0.36)
            for idx in range(3)
        ])
        micro_city = VGroup(city_glow, roads, buildings, city_nodes)

        city_pulses = VGroup()
        for idx in range(6):
            pulse = Dot(color=GOLD, radius=0.020)
            pulse.alpha = random.random()
            pulse.path = random.choice(list(roads))
            city_pulses.add(pulse)

        def update_city_pulses(group, dt):
            for pulse in group:
                pulse.alpha = (pulse.alpha + dt * 0.38) % 1.0
                pulse.move_to(pulse.path.point_from_proportion(smooth(pulse.alpha)))
                pulse.set_opacity(0.25 + 0.75 * np.sin(PI * pulse.alpha))

        city_pulses.add_updater(update_city_pulses)

        self.play(
            ReplacementTransform(bio_cells.copy(), micro_city),
            FadeOut(bio_cells),
            run_time=2.4,
        )
        self.add(city_pulses)
        self.play(city_glow.animate.scale(1.08).set_stroke(opacity=0.05), run_time=1.0, rate_func=there_and_back)
        self.wait(28.2)

        # =========================================================================
        # PHASE 3: CONTRAST WITH CLOSED AI SYSTEMS (80.0s - 120.0s)
        # =========================================================================
        city_pulses.clear_updaters()
        self.play(Restore(self.camera.frame), run_time=2.1, rate_func=smooth)
        self.play(
            FadeOut(petri_dish),
            FadeOut(micro_city),
            FadeOut(city_pulses),
            FadeOut(anecdote_title),
            FadeOut(city_label),
            run_time=1.0,
        )

        compare_title = make_label("Đĩa Petri mở vs. thuật toán trong hộp kín", GOLD, 0.64)
        compare_title.next_to(title, DOWN, buff=0.24)

        closed_box = RoundedRectangle(
            width=5.35,
            height=3.72,
            corner_radius=0.16,
            color=RED,
            fill_color=RED_E,
            fill_opacity=0.10,
            stroke_width=1.5,
            stroke_opacity=0.78,
        ).move_to(LEFT * 3.15 + DOWN * 0.48)
        open_box = RoundedRectangle(
            width=5.35,
            height=3.72,
            corner_radius=0.16,
            color=GREEN_C,
            fill_color=GREEN_E,
            fill_opacity=0.12,
            stroke_width=1.5,
            stroke_opacity=0.78,
        ).move_to(RIGHT * 3.15 + DOWN * 0.48)

        closed_title = make_label("Hệ thống Đóng", RED, 0.58).next_to(closed_box.get_top(), DOWN, buff=0.28)
        closed_subtitle = make_label("Go board: luật cố định", GRAY_A, 0.40).next_to(closed_title, DOWN, buff=0.10)
        open_title = make_label("Hệ thống Mở", GREEN_C, 0.58).next_to(open_box.get_top(), DOWN, buff=0.28)
        open_subtitle = make_label("Sinh trưởng vượt biên", GRAY_A, 0.40).next_to(open_title, DOWN, buff=0.10)

        board_center = closed_box.get_center() + DOWN * 0.38
        board_size = 2.12
        go_board = VGroup()
        coords = np.linspace(-board_size / 2, board_size / 2, 9)
        for x in coords:
            go_board.add(Line(
                board_center + RIGHT * x + DOWN * board_size / 2,
                board_center + RIGHT * x + UP * board_size / 2,
                color=RED,
                stroke_width=0.9,
                stroke_opacity=0.28,
            ))
        for y in coords:
            go_board.add(Line(
                board_center + LEFT * board_size / 2 + UP * y,
                board_center + RIGHT * board_size / 2 + UP * y,
                color=RED,
                stroke_width=0.9,
                stroke_opacity=0.28,
            ))
        board_frame = Square(
            side_length=board_size,
            color=RED,
            stroke_width=1.2,
            stroke_opacity=0.48,
        ).move_to(board_center)
        stones = VGroup()
        stone_specs = [(-2, 2, WHITE), (1, 2, BLACK), (0, 0, WHITE), (2, -1, BLACK), (-1, -2, BLACK), (2, 1, WHITE)]
        step = board_size / 8
        for ix, iy, color in stone_specs:
            stones.add(Circle(
                radius=0.075,
                color=GRAY_A if color == BLACK else WHITE,
                fill_color=color,
                fill_opacity=0.95,
                stroke_width=0.8,
                stroke_opacity=0.85,
            ).move_to(board_center + RIGHT * ix * step + UP * iy * step))
        lock_line = DashedLine(
            closed_box.get_left() + RIGHT * 0.22 + DOWN * 1.47,
            closed_box.get_right() + LEFT * 0.22 + DOWN * 1.47,
            color=RED,
            stroke_width=1.2,
            dashed_ratio=0.48,
        ).set_opacity(0.55)

        open_cells = VGroup()
        open_specs = [
            (LEFT * 1.20 + UP * 0.36, 0.18, GREEN_C, False),
            (LEFT * 0.44 + DOWN * 0.28, 0.22, GREEN_C, False),
            (RIGHT * 0.38 + UP * 0.42, 0.17, GREEN_C, False),
            (RIGHT * 1.04 + DOWN * 0.42, 0.20, GREEN_C, False),
            (RIGHT * 1.95 + UP * 0.20, 0.24, GOLD, True),
            (RIGHT * 2.42 + DOWN * 0.58, 0.18, GOLD, True),
        ]
        for idx, (offset, radius, color, gold) in enumerate(open_specs):
            cell = make_cell(open_box.get_center() + offset, radius=radius, color=color, phase=idx * 0.9, gold=gold)
            if gold:
                cell.home += RIGHT * 0.38
            open_cells.add(cell)

        division_bridge = VGroup()
        for cell in open_cells[-2:]:
            division_bridge.add(Line(
                cell.get_center() + LEFT * 0.16,
                cell.get_center() + RIGHT * 0.16,
                color=GOLD,
                stroke_width=1.1,
                stroke_opacity=0.44,
            ))
        escape_arrow = Arrow(
            open_box.get_right() + LEFT * 0.92 + DOWN * 0.42,
            open_box.get_right() + RIGHT * 0.64 + DOWN * 0.28,
            color=GOLD,
            stroke_width=2.0,
            buff=0.05,
            max_tip_length_to_length_ratio=0.16,
        )

        self.play(
            FadeIn(compare_title, shift=DOWN * 0.10),
            Create(closed_box),
            Create(open_box),
            FadeIn(closed_title),
            FadeIn(closed_subtitle),
            FadeIn(open_title),
            FadeIn(open_subtitle),
            run_time=1.8,
        )
        self.play(
            Create(board_frame),
            Create(go_board),
            FadeIn(stones, scale=0.75),
            Create(lock_line),
            LaggedStart(*[FadeIn(cell, scale=0.70) for cell in open_cells], lag_ratio=0.12),
            Create(division_bridge),
            Create(escape_arrow),
            run_time=2.6,
        )

        add_cell_wiggle(open_cells, amplitude=0.050, speed=1.0)
        self.play(
            open_cells[-2:].animate.shift(RIGHT * 0.55),
            escape_arrow.animate.shift(RIGHT * 0.12),
            run_time=2.6,
            rate_func=smooth,
        )
        self.wait(31.0)

        open_cells.clear_updaters()
        self.play(
            FadeOut(compare_title),
            FadeOut(closed_box),
            FadeOut(open_box),
            FadeOut(closed_title),
            FadeOut(closed_subtitle),
            FadeOut(open_title),
            FadeOut(open_subtitle),
            FadeOut(board_frame),
            FadeOut(go_board),
            FadeOut(stones),
            FadeOut(lock_line),
            FadeOut(open_cells),
            FadeOut(division_bridge),
            FadeOut(escape_arrow),
            FadeOut(title),
            run_time=1.5
        )


class SC_03_DeconstructingOpenEndedSystems(VietnameseScene):
    """
    SC_03: Deconstructing Open-Ended Systems.
    Focus: Standish definition (observer-dependent), Noisy TV paradox, Venn diagram of Novelty and Learnability.
    """
    def construct(self):
        load_safe_sound(self, "SC_03_ObserverVenn.wav")
        title = create_title_banner(r"SC\_03: Deconstructing Open-Ended Systems")
        title.scale(0.88).to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=1.0)

        def make_label(text, color=WHITE, scale=0.5):
            return Tex(rf"\text{{{text}}}", color=color).scale(scale)

        def make_text_block(lines, color=WHITE, scale=0.48, buff=0.12, aligned_edge=ORIGIN):
            group = VGroup(*[
                Tex(rf"\text{{{line}}}", color=color).scale(scale)
                for line in lines
            ])
            if aligned_edge is ORIGIN:
                group.arrange(DOWN, buff=buff)
            else:
                group.arrange(DOWN, buff=buff, aligned_edge=aligned_edge)
            return group

        def make_eye(center=ORIGIN):
            upper = CubicBezier(
                center + LEFT * 2.0,
                center + LEFT * 0.95 + UP * 0.82,
                center + RIGHT * 0.95 + UP * 0.82,
                center + RIGHT * 2.0,
                color=GOLD,
                stroke_width=3.2,
            )
            lower = CubicBezier(
                center + LEFT * 2.0,
                center + LEFT * 0.95 + DOWN * 0.82,
                center + RIGHT * 0.95 + DOWN * 0.82,
                center + RIGHT * 2.0,
                color=GOLD,
                stroke_width=3.2,
            )
            inner_upper = upper.copy().scale(0.78, about_point=center).set_stroke(width=1.1, opacity=0.22)
            inner_lower = lower.copy().scale(0.78, about_point=center).set_stroke(width=1.1, opacity=0.22)
            iris = Circle(
                radius=0.46,
                color=BLUE_C,
                fill_color=BLUE_E,
                fill_opacity=0.72,
                stroke_width=1.8,
            ).move_to(center)
            iris_rings = VGroup(*[
                Circle(
                    radius=0.17 + idx * 0.10,
                    color=BLUE_C,
                    stroke_width=0.8,
                    stroke_opacity=0.18,
                ).move_to(center)
                for idx in range(3)
            ])
            pupil = Circle(radius=0.17, color=BLACK, fill_color=BLACK, fill_opacity=1.0, stroke_width=0).move_to(center)
            reflection = Dot(radius=0.055, color=WHITE).move_to(center + UP * 0.15 + RIGHT * 0.12)
            eye_group = VGroup(upper, lower, inner_upper, inner_lower, iris, iris_rings, pupil, reflection)
            eye_group.iris = iris
            eye_group.iris_rings = iris_rings
            eye_group.pupil = pupil
            eye_group.reflection = reflection
            return eye_group

        def move_eye_focus(eye_group, center, offset, run_time=0.8):
            target = center + offset
            return AnimationGroup(
                eye_group.iris.animate.move_to(target),
                eye_group.iris_rings.animate.move_to(target),
                eye_group.pupil.animate.move_to(target),
                eye_group.reflection.animate.move_to(target + UP * 0.15 + RIGHT * 0.12),
                lag_ratio=0.0,
                run_time=run_time,
            )

        def make_retro_tv(center):
            body = RoundedRectangle(
                width=5.20,
                height=3.34,
                corner_radius=0.25,
                color=GRAY_A,
                fill_color=GRAY_E,
                fill_opacity=0.72,
                stroke_width=1.5,
                stroke_opacity=0.78,
            ).move_to(center)
            screen = RoundedRectangle(
                width=3.72,
                height=2.34,
                corner_radius=0.14,
                color=RED,
                fill_color=BLACK,
                fill_opacity=1.0,
                stroke_width=1.2,
                stroke_opacity=0.70,
            ).move_to(center + LEFT * 0.36)
            glass = screen.copy().set_fill(WHITE, opacity=0.035).set_stroke(opacity=0.0)
            shine = Line(
                screen.get_corner(UL) + RIGHT * 0.22 + DOWN * 0.14,
                screen.get_corner(UR) + LEFT * 0.30 + DOWN * 0.14,
                color=WHITE,
                stroke_width=1.0,
                stroke_opacity=0.11,
            )
            antenna_base = Dot(point=body.get_top() + DOWN * 0.03, radius=0.045, color=GRAY_A)
            antenna_left = Line(antenna_base.get_center(), antenna_base.get_center() + UP * 0.74 + LEFT * 0.72, color=GRAY_A, stroke_width=2.5)
            antenna_right = Line(antenna_base.get_center(), antenna_base.get_center() + UP * 0.76 + RIGHT * 0.70, color=GRAY_A, stroke_width=2.5)
            knob_column = VGroup()
            for idx, y in enumerate([0.70, 0.25, -0.34]):
                knob = Circle(
                    radius=0.16 if idx == 0 else 0.12,
                    color=GRAY_A,
                    fill_color=GRAY_B,
                    fill_opacity=0.82,
                    stroke_width=1.0,
                ).move_to(center + RIGHT * 2.05 + UP * y)
                notch = Line(
                    knob.get_center(),
                    knob.get_center() + UP * knob.radius * 0.70,
                    color=RED if idx == 0 else GRAY_A,
                    stroke_width=1.0,
                    stroke_opacity=0.70,
                ).rotate(idx * 35 * DEGREES, about_point=knob.get_center())
                knob_column.add(VGroup(knob, notch))
            speaker_lines = VGroup(*[
                Line(
                    center + RIGHT * 1.72 + DOWN * (0.78 + i * 0.13),
                    center + RIGHT * 2.36 + DOWN * (0.78 + i * 0.13),
                    color=GRAY_A,
                    stroke_width=0.9,
                    stroke_opacity=0.28,
                )
                for i in range(5)
            ])
            tv = VGroup(body, screen, glass, shine, antenna_left, antenna_right, antenna_base, knob_column, speaker_lines)
            tv.screen = screen
            return tv

        def make_oscilloscope(center):
            frame = RoundedRectangle(
                width=5.20,
                height=3.34,
                corner_radius=0.25,
                color=BLUE_C,
                fill_color=GRAY_E,
                fill_opacity=0.66,
                stroke_width=1.5,
                stroke_opacity=0.78,
            ).move_to(center)
            screen = RoundedRectangle(
                width=4.30,
                height=2.42,
                corner_radius=0.12,
                color=BLUE_C,
                fill_color=BLACK,
                fill_opacity=1.0,
                stroke_width=1.2,
                stroke_opacity=0.60,
            ).move_to(center + UP * 0.02)
            grid = VGroup()
            for x in np.linspace(-1.85, 1.85, 7):
                grid.add(Line(
                    screen.get_center() + RIGHT * x + DOWN * 1.05,
                    screen.get_center() + RIGHT * x + UP * 1.05,
                    color=BLUE_C,
                    stroke_width=0.65,
                    stroke_opacity=0.18,
                ))
            for y in np.linspace(-1.00, 1.00, 5):
                grid.add(Line(
                    screen.get_center() + LEFT * 1.98 + UP * y,
                    screen.get_center() + RIGHT * 1.98 + UP * y,
                    color=BLUE_C,
                    stroke_width=0.65,
                    stroke_opacity=0.18,
                ))
            center_line = Line(
                screen.get_left() + RIGHT * 0.18,
                screen.get_right() + LEFT * 0.18,
                color=BLUE_C,
                stroke_width=1.0,
                stroke_opacity=0.32,
            )
            controls = VGroup()
            for idx, x in enumerate([-1.56, -1.18, 1.18, 1.56]):
                controls.add(Circle(
                    radius=0.07,
                    color=BLUE_C,
                    fill_color=BLUE_E,
                    fill_opacity=0.75,
                    stroke_width=0.8,
                ).move_to(frame.get_bottom() + UP * 0.23 + RIGHT * x))
            scope = VGroup(frame, screen, grid, center_line, controls)
            scope.screen = screen
            return scope

        # =========================================================================
        # PHASE 1: STANDISH & OBSERVER PERSPECTIVE (0.0s - 45.0s)
        # =========================================================================
        eye_center = UP * 1.28
        eye = make_eye(eye_center)
        observer_lbl = make_label("Quan sát viên (Observer Perspective)", GOLD, 0.66)
        observer_lbl.next_to(eye, UP, buff=0.30)
        standish_card = RoundedRectangle(
            width=9.35,
            height=1.50,
            corner_radius=0.16,
            color=GOLD,
            fill_color=GRAY_E,
            fill_opacity=0.34,
            stroke_width=1.1,
            stroke_opacity=0.60,
        ).move_to(DOWN * 1.48)
        standish_text = make_text_block(
            [
                "Standish: tính mở không nằm cô lập bên trong hệ thống.",
                "Nó phụ thuộc vào bộ lọc nhận diện của một quan sát viên.",
            ],
            color=WHITE,
            scale=0.50,
            buff=0.13,
        ).move_to(standish_card.get_center())

        rays = VGroup(*[
            DashedLine(
                eye_center + DOWN * 0.72,
                standish_card.get_top() + RIGHT * offset,
                color=GOLD,
                stroke_width=1.25,
                stroke_opacity=0.26,
                dashed_ratio=0.50,
            )
            for offset in [-3.6, -1.8, 0.0, 1.8, 3.6]
        ])

        self.play(
            LaggedStart(*[Create(part) for part in eye[:4]], lag_ratio=0.12),
            FadeIn(eye[4], scale=0.85),
            FadeIn(eye[5]),
            FadeIn(eye[6]),
            FadeIn(eye[7]),
            Write(observer_lbl),
            run_time=2.3,
        )
        self.play(move_eye_focus(eye, eye_center, LEFT * 0.22, run_time=0.75))
        self.wait(1.0)
        self.play(move_eye_focus(eye, eye_center, RIGHT * 0.28, run_time=0.90))
        self.wait(0.9)
        self.play(move_eye_focus(eye, eye_center, ORIGIN, run_time=0.80))
        self.play(
            LaggedStart(*[Create(ray) for ray in rays], lag_ratio=0.08),
            FadeIn(standish_card, shift=UP * 0.10),
            LaggedStart(*[Write(line) for line in standish_text], lag_ratio=0.18),
            run_time=2.4,
        )
        self.wait(33.45)

        # =========================================================================
        # PHASE 2: NOISY TV PARADOX (45.0s - 100.0s)
        # =========================================================================
        self.play(
            FadeOut(eye),
            FadeOut(observer_lbl),
            FadeOut(standish_card),
            FadeOut(standish_text),
            FadeOut(rays),
            run_time=1.0,
        )

        tv = make_retro_tv(LEFT * 3.25 + DOWN * 0.40)
        tv_screen = tv.screen
        static_dots = VGroup(*[
            Dot(
                radius=np.random.uniform(0.010, 0.032),
                color=random.choice([GRAY_A, GRAY_B, WHITE, RED]),
                fill_opacity=np.random.uniform(0.35, 0.95),
            )
            for _ in range(60)
        ])
        for dot in static_dots:
            dot.move_to(tv_screen.get_center() + np.array([
                np.random.uniform(-1.70, 1.70),
                np.random.uniform(-1.02, 1.02),
                0.0
            ]))

        def update_static(group, dt):
            for dot in group:
                dot.move_to(tv_screen.get_center() + np.array([
                    np.random.uniform(-1.70, 1.70),
                    np.random.uniform(-1.02, 1.02),
                    0.0
                ]))
                dot.set_opacity(np.random.uniform(0.18, 0.98))
                dot.set_color(random.choice([GRAY_A, GRAY_B, WHITE, RED]))

        noisy_title = make_label("Noisy TV Paradox", RED, 0.53).next_to(tv, UP, buff=0.34)
        noisy_lines = make_text_block(
            ["Entropy tối đa", "Mới mẻ nhưng không học được"],
            color=RED,
            scale=0.34,
            buff=0.08,
        ).next_to(noisy_title, DOWN, buff=0.08)

        osc = make_oscilloscope(RIGHT * 3.25 + DOWN * 0.40)
        osc_screen = osc.screen
        osc_axes = Axes(
            x_range=[0, 4, 1],
            y_range=[-1.4, 1.4, 1],
            x_length=4.00,
            y_length=2.10,
            axis_config={"stroke_width": 0.0, "include_ticks": False},
            tips=False,
        ).move_to(osc_screen.get_center())
        wave_phase = ValueTracker(0.0)
        wave_phase.add_updater(lambda m, dt: m.increment_value(dt * 3.2))
        sine_wave = always_redraw(lambda: osc_axes.plot(
            lambda x: 0.72 * np.sin(x * 4.0 - wave_phase.get_value()),
            x_range=[0, 4],
            color=BLUE_C,
            stroke_width=3.0,
        ))
        scope_title = make_label("Oscilloscope Pattern", BLUE_C, 0.53).next_to(osc, UP, buff=0.34)
        scope_lines = make_text_block(
            ["Có quy luật, dễ học", "nhưng thiếu bất ngờ thực sự"],
            color=BLUE_C,
            scale=0.34,
            buff=0.08,
        ).next_to(scope_title, DOWN, buff=0.08)

        self.play(
            LaggedStart(Create(tv), FadeIn(static_dots), lag_ratio=0.15),
            LaggedStart(Create(osc), Create(osc_axes), Create(sine_wave), lag_ratio=0.15),
            FadeIn(noisy_title, shift=DOWN * 0.08),
            LaggedStart(*[Write(line) for line in noisy_lines], lag_ratio=0.12),
            FadeIn(scope_title, shift=DOWN * 0.08),
            LaggedStart(*[Write(line) for line in scope_lines], lag_ratio=0.12),
            run_time=2.8,
        )
        static_dots.add_updater(update_static)
        self.add(wave_phase)
        self.wait(51.2)

        # =========================================================================
        # PHASE 3: VENN DIAGRAM & LOGIC EQUATION (100.0s - 180.0s)
        # =========================================================================
        static_dots.clear_updaters()
        wave_phase.clear_updaters()
        self.play(
            FadeOut(tv),
            FadeOut(static_dots),
            FadeOut(noisy_title),
            FadeOut(noisy_lines),
            FadeOut(osc),
            FadeOut(osc_axes),
            FadeOut(sine_wave),
            FadeOut(scope_title),
            FadeOut(scope_lines),
            FadeOut(wave_phase),
            run_time=1.0,
        )

        equation = MathTex(
            r"\mathcal{S} \text{ is Open-Ended} \iff \forall t,\ "
            r"\text{Artifact}(t) \in \{\text{Novel} \cap \text{Learnable}\}",
            color=WHITE,
        ).scale(0.62).to_edge(UP, buff=1.18)

        novelty_circle = Circle(
            radius=2.05,
            color=BLUE_C,
            fill_color=BLUE_E,
            fill_opacity=0.17,
            stroke_width=2.5,
            stroke_opacity=0.84,
        ).move_to(LEFT * 1.08 + DOWN * 0.54)
        learnability_circle = Circle(
            radius=2.05,
            color=GREEN_C,
            fill_color=GREEN_E,
            fill_opacity=0.17,
            stroke_width=2.5,
            stroke_opacity=0.84,
        ).move_to(RIGHT * 1.08 + DOWN * 0.54)
        novelty_lbl = make_label("Novelty (Mới mẻ)", BLUE_C, 0.62).next_to(novelty_circle, LEFT, buff=0.20)
        learnability_lbl = make_label("Learnability (Học được)", GREEN_C, 0.62).next_to(learnability_circle, RIGHT, buff=0.20)

        self.play(
            Write(equation),
            run_time=2.0,
        )
        self.play(
            Create(novelty_circle),
            FadeIn(novelty_lbl, shift=RIGHT * 0.10),
            Create(learnability_circle),
            FadeIn(learnability_lbl, shift=LEFT * 0.10),
            run_time=2.2,
        )
        self.wait(9.0)

        intersection = Intersection(
            novelty_circle,
            learnability_circle,
            color=GOLD,
            fill_color=GOLD,
            fill_opacity=0.42,
            stroke_width=1.8,
            stroke_opacity=0.90,
        )
        intersection_glow = intersection.copy().set_fill(GOLD, opacity=0.16).set_stroke(GOLD, width=6.0, opacity=0.20)
        intersection_lbl = make_label("Open-Endedness", GOLD, 0.72).move_to(intersection.get_center())
        balance_lines = make_text_block(
            ["Mới lạ đủ để bất ngờ", "có cấu trúc đủ để học"],
            color=GRAY_A,
            scale=0.42,
            buff=0.09,
        ).next_to(intersection_lbl, DOWN, buff=0.30)

        self.play(
            FadeIn(intersection_glow),
            FadeIn(intersection),
            Write(intersection_lbl),
            FadeIn(balance_lines, shift=UP * 0.10),
            run_time=1.8,
        )

        pulse = ValueTracker(0.0)
        pulse.add_updater(lambda m, dt: m.increment_value(dt * 2.2))

        def pulse_intersection(mobject):
            alpha = 0.42 + 0.17 * (0.5 + 0.5 * np.sin(pulse.get_value()))
            mobject.set_fill(GOLD, opacity=alpha)
            mobject.set_stroke(GOLD, opacity=0.78 + 0.18 * np.sin(pulse.get_value()), width=1.8)

        def pulse_glow(mobject):
            alpha = 0.12 + 0.08 * (0.5 + 0.5 * np.sin(pulse.get_value()))
            mobject.set_fill(GOLD, opacity=alpha)
            mobject.set_stroke(GOLD, opacity=alpha, width=6.0)

        intersection.add_updater(pulse_intersection)
        intersection_glow.add_updater(pulse_glow)
        self.add(pulse)

        novelty_artifacts = VGroup(*[
            RegularPolygon(n=random.choice([3, 5, 6]), radius=0.08, color=BLUE_C, fill_color=BLUE_E, fill_opacity=0.44)
            .move_to(novelty_circle.get_center() + np.array([np.random.uniform(-1.25, -0.25), np.random.uniform(-1.20, 1.20), 0.0]))
            for _ in range(9)
        ])
        learnable_artifacts = VGroup(*[
            Square(side_length=0.13, color=GREEN_C, fill_color=GREEN_E, fill_opacity=0.44)
            .move_to(learnability_circle.get_center() + np.array([np.random.uniform(0.25, 1.25), np.random.uniform(-1.20, 1.20), 0.0]))
            for _ in range(9)
        ])
        self.play(
            LaggedStart(*[FadeIn(mob, scale=0.6) for mob in novelty_artifacts], lag_ratio=0.05),
            LaggedStart(*[FadeIn(mob, scale=0.6) for mob in learnable_artifacts], lag_ratio=0.05),
            run_time=1.3,
        )
        self.wait(61.7)

        intersection.clear_updaters()
        intersection_glow.clear_updaters()
        pulse.clear_updaters()
        self.play(
            FadeOut(equation),
            FadeOut(novelty_circle),
            FadeOut(novelty_lbl),
            FadeOut(learnability_circle),
            FadeOut(learnability_lbl),
            FadeOut(intersection_glow),
            FadeOut(intersection),
            FadeOut(intersection_lbl),
            FadeOut(balance_lines),
            FadeOut(novelty_artifacts),
            FadeOut(learnable_artifacts),
            FadeOut(pulse),
            FadeOut(title),
            run_time=1.5,
        )


def create_vacuum_tube_card():
    frame = RoundedRectangle(width=4.8, height=3.2, color=BLUE_C, fill_color=GRAY_E, fill_opacity=0.4, corner_radius=0.15)
    title = Tex(r"\text{Ống chân không (1900s)}", color=BLUE_C).scale(0.7).move_to(frame.get_top() + DOWN * 0.35)
    
    bulb = Circle(radius=0.45, color=GRAY_A, fill_color=BLACK, fill_opacity=0.5).move_to(frame.get_center() + UP * 0.1)
    base = Rectangle(width=0.35, height=0.18, color=GRAY_A, fill_color=GRAY_B, fill_opacity=1.0).next_to(bulb, DOWN, buff=0.0)
    filament = VMobject(color=YELLOW, stroke_width=2.5)
    filament.set_points_as_corners([
        base.get_center() + LEFT * 0.08,
        bulb.get_center() + LEFT * 0.08 + UP * 0.22,
        bulb.get_center() + RIGHT * 0.08 + UP * 0.22,
        base.get_center() + RIGHT * 0.08
    ]).make_smooth()
    filament_glow = filament.copy().set_stroke(width=6, opacity=0.35)
    tube = VGroup(bulb, base, filament_glow, filament)
    
    desc = Tex(r"\text{Mục tiêu: Khuếch đại tín hiệu Radio}\\\text{\textbf{Không phải} để tạo ra Computer}", color=WHITE).scale(0.55).move_to(frame.get_bottom() + UP * 0.5)
    return VGroup(frame, title, tube, desc)

def create_computer_card():
    frame = RoundedRectangle(width=4.8, height=3.2, color=ORANGE, fill_color=GRAY_E, fill_opacity=0.4, corner_radius=0.15)
    title = Tex(r"\text{Máy tính ENIAC (1940s)}", color=ORANGE).scale(0.7).move_to(frame.get_top() + DOWN * 0.35)
    
    circuit = VGroup()
    grid_pts = [
        [-0.6, -0.3], [0.6, -0.3], [-0.6, 0.3], [0.6, 0.3], [0.0, 0.0]
    ]
    for pt in grid_pts:
        circuit.add(Dot(point=frame.get_center() + np.array([pt[0], pt[1] + 0.1, 0.0]), radius=0.06, color=ORANGE))
    connections = [
        [0, 4], [1, 4], [2, 4], [3, 4]
    ]
    for conn in connections:
        p1 = circuit[conn[0]].get_center()
        p2 = circuit[conn[1]].get_center()
        circuit.add(Line(p1, p2, color=ORANGE, stroke_width=1.5, stroke_opacity=0.6))
        
    desc = Tex(r"\text{Được chế tạo từ hàng ngàn Ống chân không}\\\text{Tiến bộ nhảy vọt, phi tuyến tính}", color=WHITE).scale(0.55).move_to(frame.get_bottom() + UP * 0.5)
    return VGroup(frame, title, circuit, desc)


class SC_04_TheIllusionOfGoals(VietnameseScene):
    """
    SC_04: The Illusion of Goals (Objective Design).
    Focus: Pitfalls of target optimization in open spaces, Stepping stones theory (Vacuum tube -> Radio -> Computer).
    """
    def construct(self):
        load_safe_sound(self, "SC_04_SteppingStones.wav")
        title = create_title_banner(r"SC\_04: The Illusion of Goals (Objective Design)")
        title.scale(0.88).to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=1.0)

        def make_label(text, color=WHITE, scale=0.5):
            return Tex(rf"\text{{{text}}}", color=color).scale(scale)

        def make_text_block(lines, color=WHITE, scale=0.44, buff=0.10, aligned_edge=ORIGIN):
            group = VGroup(*[
                Tex(rf"\text{{{line}}}", color=color).scale(scale)
                for line in lines
            ])
            if aligned_edge is ORIGIN:
                group.arrange(DOWN, buff=buff)
            else:
                group.arrange(DOWN, buff=buff, aligned_edge=aligned_edge)
            return group

        def objective_curve(x):
            return (
                0.055 * (x - 7.4) ** 2
                - 1.35 * np.exp(-((x - 2.35) / 0.48) ** 2)
                - 2.05 * np.exp(-((x - 7.55) / 0.88) ** 2)
                + 0.26 * np.sin(1.65 * x)
                + 1.05
            )

        def make_vacuum_card(center):
            card = RoundedRectangle(
                width=5.15,
                height=3.20,
                corner_radius=0.16,
                color=GOLD,
                fill_color=GRAY_E,
                fill_opacity=0.36,
                stroke_width=1.25,
                stroke_opacity=0.78,
            ).move_to(center)
            card_title = make_label("Ống Chân Không", GOLD, 0.58).next_to(card.get_top(), DOWN, buff=0.28)
            year = make_label("Vacuum Tube", GRAY_A, 0.37).next_to(card_title, DOWN, buff=0.08)
            glass = Circle(
                radius=0.42,
                color=GRAY_A,
                fill_color=BLACK,
                fill_opacity=0.45,
                stroke_width=1.1,
                stroke_opacity=0.75,
            ).move_to(card.get_center() + UP * 0.16)
            glow = Circle(radius=0.50, color=GOLD, stroke_width=1.0, stroke_opacity=0.16).move_to(glass.get_center())
            base = VGroup(
                Rectangle(width=0.42, height=0.16, color=GRAY_A, fill_color=GRAY_E, fill_opacity=0.88, stroke_width=0.9),
                Rectangle(width=0.30, height=0.18, color=GRAY_A, fill_color=GRAY_E, fill_opacity=0.88, stroke_width=0.9),
            ).arrange(DOWN, buff=0.02).next_to(glass, DOWN, buff=0.02)
            filament = VMobject(color=GOLD, stroke_width=2.2)
            filament.set_points_smoothly([
                glass.get_center() + LEFT * 0.18 + DOWN * 0.08,
                glass.get_center() + LEFT * 0.08 + UP * 0.10,
                glass.get_center() + RIGHT * 0.03 + DOWN * 0.08,
                glass.get_center() + RIGHT * 0.14 + UP * 0.10,
                glass.get_center() + RIGHT * 0.20 + DOWN * 0.08,
            ])
            pins = VGroup(*[
                Line(
                    base.get_bottom() + RIGHT * x,
                    base.get_bottom() + RIGHT * x + DOWN * 0.24,
                    color=GRAY_A,
                    stroke_width=0.85,
                    stroke_opacity=0.58,
                )
                for x in [-0.14, 0.0, 0.14]
            ])
            desc = make_text_block(
                ["Mục tiêu ban đầu:", "khuếch đại dòng điện vô tuyến"],
                color=GRAY_A,
                scale=0.36,
                buff=0.07,
            ).next_to(card.get_bottom(), UP, buff=0.28)
            return VGroup(card, card_title, year, glow, glass, filament, base, pins, desc)

        def make_eniac_card(center):
            card = RoundedRectangle(
                width=5.15,
                height=3.20,
                corner_radius=0.16,
                color=GOLD,
                fill_color=GRAY_E,
                fill_opacity=0.36,
                stroke_width=1.25,
                stroke_opacity=0.78,
            ).move_to(center)
            card_title = make_label("Máy Tính ENIAC", GOLD, 0.58).next_to(card.get_top(), DOWN, buff=0.28)
            year = make_label("1940s", GRAY_A, 0.37).next_to(card_title, DOWN, buff=0.08)
            chip = RoundedRectangle(
                width=1.55,
                height=1.10,
                corner_radius=0.06,
                color=GOLD,
                fill_color=BLACK,
                fill_opacity=0.48,
                stroke_width=1.1,
            ).move_to(card.get_center() + UP * 0.08)
            circuit = VGroup()
            nodes = []
            for x in [-0.50, 0.0, 0.50]:
                for y in [-0.32, 0.05, 0.38]:
                    node = Dot(chip.get_center() + RIGHT * x + UP * y, radius=0.035, color=ORANGE)
                    nodes.append(node)
                    circuit.add(node)
            for i, node_a in enumerate(nodes):
                if i + 1 < len(nodes) and i % 3 != 2:
                    circuit.add(Line(node_a.get_center(), nodes[i + 1].get_center(), color=GOLD, stroke_width=0.9, stroke_opacity=0.58))
                if i + 3 < len(nodes):
                    circuit.add(Line(node_a.get_center(), nodes[i + 3].get_center(), color=GOLD, stroke_width=0.9, stroke_opacity=0.44))
            pins = VGroup()
            for side in [UP, DOWN]:
                for x in np.linspace(-0.58, 0.58, 6):
                    pins.add(Line(
                        chip.get_center() + RIGHT * x + side * 0.55,
                        chip.get_center() + RIGHT * x + side * 0.77,
                        color=GRAY_A,
                        stroke_width=0.8,
                        stroke_opacity=0.52,
                    ))
            desc = make_text_block(
                ["Kết quả phi tuyến tính:", "hàng ngàn ống chân không"],
                color=GRAY_A,
                scale=0.36,
                buff=0.07,
            ).next_to(card.get_bottom(), UP, buff=0.28)
            return VGroup(card, card_title, year, chip, circuit, pins, desc)

        # =========================================================================
        # PHASE 1: GOAL MAP & GRADIENT TRAP (0.0s - 45.0s)
        # =========================================================================
        phase1_title = make_label("Bản đồ mục tiêu: la bàn giả của Gradient", GOLD, 0.64)
        phase1_title.next_to(title, DOWN, buff=0.24)

        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-1.6, 4.0, 1],
            x_length=10.8,
            y_length=4.15,
            axis_config={"color": GRAY_B, "stroke_width": 1.0, "stroke_opacity": 0.55},
            tips=False,
        ).shift(DOWN * 0.52)
        grid = VGroup()
        for x in np.arange(1, 10, 1):
            grid.add(Line(axes.c2p(x, -1.6), axes.c2p(x, 4.0), color=GRAY_B, stroke_width=0.55, stroke_opacity=0.13))
        for y in np.arange(-1, 4, 1):
            grid.add(Line(axes.c2p(0, y), axes.c2p(10, y), color=GRAY_B, stroke_width=0.55, stroke_opacity=0.13))
        terrain = axes.plot(objective_curve, x_range=[0.15, 9.85], color=GRAY_A, stroke_width=3.0)

        local_x = 2.35
        global_x = 7.55
        local_point = axes.c2p(local_x, objective_curve(local_x))
        global_point = axes.c2p(global_x, objective_curve(global_x))
        local_marker = VGroup(
            Dot(local_point, radius=0.09, color=RED),
            Circle(radius=0.32, color=RED, stroke_width=1.4, stroke_opacity=0.55).move_to(local_point),
        )
        global_marker = VGroup(
            Dot(global_point, radius=0.09, color=GREEN_C),
            Circle(radius=0.38, color=GREEN_C, stroke_width=1.4, stroke_opacity=0.58).move_to(global_point),
        )
        local_lbl = make_label("Local Minimum", RED, 0.45).next_to(local_marker, DOWN, buff=0.18)
        global_lbl = make_label("Global Optimum", GREEN_C, 0.45).next_to(global_marker, DOWN, buff=0.18)

        agent_x = ValueTracker(0.70)
        agent = always_redraw(lambda: Dot(
            axes.c2p(agent_x.get_value(), objective_curve(agent_x.get_value())),
            color=ORANGE,
            radius=0.105,
        ))
        agent_label = always_redraw(lambda: make_label("Agent", ORANGE, 0.40).next_to(agent, UP, buff=0.14))
        trace = TracedPath(agent.get_center, stroke_color=ORANGE, stroke_width=2.2, stroke_opacity=0.70)
        descent_arrow = Arrow(
            axes.c2p(0.95, objective_curve(0.95)) + UP * 0.26,
            local_point + UP * 0.22,
            color=RED,
            stroke_width=2.0,
            buff=0.12,
            max_tip_length_to_length_ratio=0.10,
        ).set_opacity(0.62)
        warning = make_text_block(
            ["Objective Design ép tác nhân đi theo dốc gần nhất.", "Trong không gian mở, dốc gần nhất có thể là bẫy."],
            color=RED,
            scale=0.46,
            buff=0.09,
        ).to_edge(DOWN, buff=0.40)

        self.play(
            FadeIn(phase1_title, shift=DOWN * 0.10),
            Create(grid),
            Create(axes),
            Create(terrain),
            FadeIn(agent),
            FadeIn(agent_label),
            run_time=2.4,
        )
        self.add(trace)
        self.play(Create(descent_arrow), run_time=0.9)
        self.play(
            agent_x.animate.set_value(local_x),
            run_time=4.6,
            rate_func=smooth,
        )
        trapped_agent = Dot(local_point, color=RED, radius=0.12)
        self.play(
            FadeOut(agent),
            FadeOut(agent_label),
            FadeIn(trapped_agent),
            FadeIn(local_marker),
            Write(local_lbl),
            FadeIn(global_marker),
            Write(global_lbl),
            LaggedStart(*[Write(line) for line in warning], lag_ratio=0.14),
            run_time=2.1,
        )

        trapped_agent.phase = 0.0

        def trapped_wobble(dot, dt):
            dot.phase += dt * 8.0
            dot.move_to(local_point + RIGHT * 0.065 * np.sin(dot.phase) + UP * 0.025 * np.sin(dot.phase * 1.7))

        trapped_agent.add_updater(trapped_wobble)
        self.wait(34.5)

        # =========================================================================
        # PHASE 2: FOG OF UNCERTAINTY CLEARING (45.0s - 100.0s)
        # =========================================================================
        trapped_agent.clear_updaters()
        self.play(FadeOut(warning), FadeOut(descent_arrow), run_time=0.8)

        fog_title = make_label("Sương mù bế tắc: mục tiêu thật bị che khuất", GOLD, 0.58)
        fog_title.next_to(title, DOWN, buff=0.24)
        fog_bands = VGroup()
        for i, x in enumerate(np.linspace(5.0, 9.5, 8)):
            band = Rectangle(
                width=0.78,
                height=4.70,
                stroke_width=0,
                fill_color=interpolate_color(ManimColor(GRAY_E), ManimColor(BLUE_E), i / 8),
                fill_opacity=0.78,
            ).move_to(axes.c2p(x, 1.10))
            band.base_opacity = 0.78 - i * 0.035
            fog_bands.add(band)

        exploration_agent = Dot(local_point, color=ORANGE, radius=0.115)
        exploration_path = VMobject(color=GOLD, stroke_width=2.4, stroke_opacity=0.82)
        path_points = [
            axes.c2p(local_x, objective_curve(local_x)),
            axes.c2p(3.55, objective_curve(3.55) + 0.55),
            axes.c2p(4.75, objective_curve(4.75) + 0.15),
            axes.c2p(6.30, objective_curve(6.30) + 0.42),
            global_point,
        ]
        exploration_path.set_points_smoothly(path_points)
        fog_agent_tracker = ValueTracker(local_x)

        def fog_clear_updater(group, dt):
            frontier_x = fog_agent_tracker.get_value() + 0.45
            for band in group:
                band_x = axes.p2c(band.get_center())[0]
                fade = np.clip((frontier_x - band_x + 0.9) / 1.6, 0.0, 1.0)
                band.set_fill(opacity=band.base_opacity * (1.0 - fade))

        fog_bands.add_updater(fog_clear_updater)
        self.play(
            Transform(phase1_title, fog_title),
            FadeIn(fog_bands),
            FadeOut(trapped_agent),
            FadeIn(exploration_agent),
            run_time=1.2,
        )
        self.play(Create(exploration_path), run_time=1.6)

        self.play(
            MoveAlongPath(exploration_agent, exploration_path),
            fog_agent_tracker.animate.set_value(global_x),
            global_marker.animate.set_color(GREEN_C),
            run_time=7.0,
            rate_func=smooth,
        )
        revealed_note = make_text_block(
            ["Đi ngang qua vùng mới lạ mở rộng bản đồ.", "Không phải bước nào cũng tăng điểm ngay lập tức."],
            color=GOLD,
            scale=0.44,
            buff=0.10,
        ).to_edge(DOWN, buff=0.42)
        self.play(LaggedStart(*[Write(line) for line in revealed_note], lag_ratio=0.12), run_time=1.4)
        self.wait(41.8)

        # =========================================================================
        # PHASE 3: STEPPING STONES (100.0s - 180.0s)
        # =========================================================================
        fog_bands.clear_updaters()
        self.play(
            FadeOut(phase1_title),
            FadeOut(axes),
            FadeOut(grid),
            FadeOut(terrain),
            FadeOut(trace),
            FadeOut(local_marker),
            FadeOut(local_lbl),
            FadeOut(global_marker),
            FadeOut(global_lbl),
            FadeOut(fog_bands),
            FadeOut(exploration_agent),
            FadeOut(exploration_path),
            FadeOut(revealed_note),
            run_time=1.2,
        )

        concept_title = make_label("Stepping Stones: tiến bộ phi tuyến tính", GOLD, 0.70)
        concept_title.next_to(title, DOWN, buff=0.26)
        card1 = make_vacuum_card(LEFT * 3.05 + DOWN * 0.35)
        card2 = make_eniac_card(RIGHT * 3.05 + DOWN * 0.35)
        bridge = DashedLine(
            card1.get_right() + RIGHT * 0.18,
            card2.get_left() + LEFT * 0.18,
            color=GOLD,
            stroke_width=2.6,
            dashed_ratio=0.55,
        ).add_tip(tip_length=0.18, tip_width=0.12)
        bridge_label_text = make_text_block(
            ["Stepping Stone", "không cùng mục tiêu trực tiếp", "nhưng là cầu nối bắt buộc"],
            color=GOLD,
            scale=0.36,
            buff=0.06,
        )
        bridge_label_back = RoundedRectangle(
            width=2.36,
            height=0.76,
            corner_radius=0.10,
            color=GOLD,
            fill_color=BLACK,
            fill_opacity=0.72,
            stroke_width=0.9,
            stroke_opacity=0.46,
        )
        bridge_label = VGroup(bridge_label_back, bridge_label_text)
        bridge_label.move_to(bridge.get_center() + UP * 0.64)
        nonlinear_message = make_text_block(
            ["Điều dẫn đến phát kiến thường không giống phát kiến cuối cùng.", "Tối ưu hóa mục tiêu cố định dễ loại bỏ chính những bước đệm cần thiết."],
            color=GRAY_A,
            scale=0.44,
            buff=0.10,
        ).to_edge(DOWN, buff=0.42)

        self.play(
            FadeIn(concept_title, shift=DOWN * 0.10),
            FadeIn(card1, shift=RIGHT * 0.16),
            FadeIn(card2, shift=LEFT * 0.16),
            run_time=1.9,
        )
        self.play(Create(bridge), FadeIn(bridge_label, shift=DOWN * 0.08), run_time=1.4)
        glow_ring = Circle(radius=0.52, color=GOLD, stroke_width=2.0).move_to(card1[4].get_center())
        self.play(glow_ring.animate.scale(2.6).set_stroke(opacity=0), run_time=1.1)
        self.remove(glow_ring)
        self.play(LaggedStart(*[FadeIn(line, shift=UP * 0.08) for line in nonlinear_message], lag_ratio=0.12), run_time=1.5)
        self.wait(71.4)

        self.play(
            FadeOut(concept_title),
            FadeOut(card1),
            FadeOut(card2),
            FadeOut(bridge),
            FadeOut(bridge_label),
            FadeOut(nonlinear_message),
            FadeOut(title),
            run_time=1.5,
        )


class SC_05_TheConcretePlaygrounds(VietnameseMovingCameraScene):
    """
    SC_05: The Concrete Playgrounds: NetHack to XLand.
    Focus: NetHack complex ASCII grid mechanics, XLand matrices (Terrain x Objects x Rules), 25 billion tasks explosion.
    """
    def construct(self):
        load_safe_sound(self, "SC_05_Concrete_Playgrounds.wav")
        title = create_title_banner(r"SC\_05: The Concrete Playgrounds: NetHack to XLand")
        title.scale(0.88).to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=1.0)

        def make_label(text, color=WHITE, scale=0.52):
            return Tex(rf"\text{{{text}}}", color=color).scale(scale)

        def make_text_block(lines, color=WHITE, scale=0.42, buff=0.09, aligned_edge=ORIGIN):
            block = VGroup(*[make_label(line, color=color, scale=scale) for line in lines])
            if aligned_edge is ORIGIN:
                block.arrange(DOWN, buff=buff)
            else:
                block.arrange(DOWN, buff=buff, aligned_edge=aligned_edge)
            return block

        def cell_pos(row, col):
            return grid_origin + RIGHT * (col - 3.5) * cell_step + DOWN * (row - 2.0) * cell_step

        def make_agent_icon(center):
            body = Dot(radius=0.26, color=BLUE_C).move_to(center)
            halo = Circle(radius=0.42, color=BLUE_C, stroke_width=1.6, stroke_opacity=0.42).move_to(center)
            core = Dot(radius=0.055, color=WHITE).move_to(center)
            return VGroup(halo, body, core)

        def make_dog_icon(center):
            shield = VMobject(color=ORANGE, fill_color=ORANGE, fill_opacity=0.40, stroke_width=2.0)
            shield.set_points_smoothly([
                center + UP * 0.32,
                center + RIGHT * 0.26 + UP * 0.14,
                center + RIGHT * 0.18 + DOWN * 0.22,
                center + DOWN * 0.36,
                center + LEFT * 0.18 + DOWN * 0.22,
                center + LEFT * 0.26 + UP * 0.14,
                center + UP * 0.32,
            ])
            inner = shield.copy().scale(0.62).set_fill(opacity=0).set_stroke(GOLD, width=1.0, opacity=0.72)
            return VGroup(shield, inner)

        def make_xland_cube(center, size=0.48, depth=0.18, color=BLUE_C, opacity=0.26):
            front = Square(side_length=size, color=color, fill_color=BLUE_E, fill_opacity=opacity, stroke_width=1.0)
            front.move_to(center)
            offset = RIGHT * depth + UP * depth * 0.55
            top = Polygon(
                front.get_corner(UL),
                front.get_corner(UR),
                front.get_corner(UR) + offset,
                front.get_corner(UL) + offset,
                color=color,
                fill_color=BLUE_C,
                fill_opacity=opacity * 0.72,
                stroke_width=0.8,
            )
            side = Polygon(
                front.get_corner(UR),
                front.get_corner(DR),
                front.get_corner(DR) + offset,
                front.get_corner(UR) + offset,
                color=color,
                fill_color=BLUE_D,
                fill_opacity=opacity * 0.62,
                stroke_width=0.8,
            )
            return VGroup(top, side, front)

        # =========================================================================
        # PHASE 1: NETHACK ASCII GRID & MAGNIFIER (0.0s - 45.0s)
        # =========================================================================
        phase1_title = make_label("NetHack: một thế giới nằm trong ký tự ASCII", GREEN_C, 0.62)
        phase1_title.next_to(title, DOWN, buff=0.24)
        grid_origin = DOWN * 0.34
        cell_step = 0.72
        grid_data = [
            ["\\#", "\\#", "\\#", "\\#", "\\#", "\\#", "\\#", "\\#"],
            ["\\#", ".", ".", ".", ".", ".", ".", "\\#"],
            ["\\#", ".", "@", ".", ".", "d", ".", "\\#"],
            ["\\#", ".", ".", ".", ".", ".", "D", "\\#"],
            ["\\#", "\\#", "\\#", "\\#", "\\#", "\\#", "\\#", "\\#"],
        ]
        ascii_grid = VGroup()
        cell_map = {}
        for row, values in enumerate(grid_data):
            row_group = VGroup()
            for col, char in enumerate(values):
                if char == "@":
                    color = GOLD
                elif char == "d":
                    color = ORANGE
                elif char == "D":
                    color = RED
                elif char == "\\#":
                    color = GREEN_C
                else:
                    color = GRAY_A
                glyph = Tex(rf"\texttt{{{char}}}", color=color).scale(0.82).move_to(cell_pos(row, col))
                row_group.add(glyph)
                cell_map[(row, col)] = glyph
            ascii_grid.add(row_group)

        grid_back = RoundedRectangle(
            width=6.45,
            height=4.05,
            corner_radius=0.12,
            color=GREEN_C,
            fill_color=BLACK,
            fill_opacity=0.28,
            stroke_width=1.2,
            stroke_opacity=0.50,
        ).move_to(grid_origin)
        scan_lines = VGroup(*[
            Line(grid_back.get_left() + RIGHT * 0.20 + UP * y, grid_back.get_right() + LEFT * 0.20 + UP * y, color=GREEN_C, stroke_width=0.45, stroke_opacity=0.11)
            for y in np.linspace(-1.65, 1.65, 9)
        ])
        player_tex = cell_map[(2, 2)]
        dog_tex = cell_map[(2, 5)]
        focus_center = (player_tex.get_center() + dog_tex.get_center()) / 2
        lens = Circle(radius=1.34, color=GOLD, stroke_width=4.0, fill_color=GOLD, fill_opacity=0.055).move_to(LEFT * 4.6 + UP * 1.55)
        lens_highlight = Arc(radius=1.12, start_angle=0.35 * PI, angle=0.34 * PI, color=WHITE, stroke_width=1.3, stroke_opacity=0.34).move_to(lens.get_center())
        lens_handle = Line(lens.get_center() + DOWN * 0.92 + RIGHT * 0.92, lens.get_center() + DOWN * 1.72 + RIGHT * 1.72, color=GOLD, stroke_width=5.0, stroke_opacity=0.84)
        magnifier = VGroup(lens, lens_highlight, lens_handle)

        self.play(
            FadeIn(phase1_title, shift=DOWN * 0.10),
            FadeIn(grid_back),
            Create(scan_lines),
            LaggedStart(*[FadeIn(row, shift=UP * 0.04) for row in ascii_grid], lag_ratio=0.08),
            run_time=2.8,
        )
        self.play(Create(magnifier), run_time=1.2)
        self.play(magnifier.animate.move_to(focus_center), run_time=2.4, rate_func=smooth)

        player_path = [(2, 2), (2, 3), (2, 4)]
        dog_path = [(2, 5), (2, 4), (2, 3)]
        for step in range(1, 3):
            self.play(
                player_tex.animate.move_to(cell_pos(*player_path[step])),
                dog_tex.animate.move_to(cell_pos(*dog_path[step])),
                magnifier.animate.move_to((cell_pos(*player_path[step]) + cell_pos(*dog_path[step])) / 2),
                run_time=1.35,
                rate_func=smooth,
            )
        pulse_a = Circle(radius=0.34, color=GOLD, stroke_width=2.0).move_to(player_tex.get_center())
        pulse_d = Circle(radius=0.34, color=ORANGE, stroke_width=2.0).move_to(dog_tex.get_center())
        self.play(
            pulse_a.animate.scale(3.0).set_stroke(opacity=0),
            pulse_d.animate.scale(3.0).set_stroke(opacity=0),
            run_time=1.2,
        )
        self.remove(pulse_a, pulse_d)
        self.wait(32.5)

        # =========================================================================
        # PHASE 2: SYMBOL GROUNDING MORPHING (45.0s - 95.0s)
        # =========================================================================
        self.play(cell_map[(3, 6)].animate.set_opacity(0.20), run_time=0.4)
        self.play(self.camera.frame.animate.move_to(magnifier.get_center()).set(width=3.85), run_time=2.4, rate_func=smooth)
        phase2_title_text = make_text_block(
            ["Symbol Grounding", "ký hiệu bắt đầu có nghĩa"],
            color=GOLD,
            scale=0.17,
            buff=0.03,
        )
        phase2_title_back = RoundedRectangle(
            width=1.72,
            height=0.40,
            corner_radius=0.05,
            color=GOLD,
            fill_color=BLACK,
            fill_opacity=0.66,
            stroke_width=0.45,
            stroke_opacity=0.30,
        )
        phase2_title = VGroup(phase2_title_back, phase2_title_text)
        phase2_title.set_z_index(20)
        phase2_title.move_to(self.camera.frame.get_center() + UP * 0.78)
        grounding_text_body = make_text_block(
            ["Từ ký tự ASCII khô khan", "sang biểu tượng vật thể có ngữ nghĩa"],
            color=GRAY_A,
            scale=0.15,
            buff=0.03,
        )
        grounding_text_back = RoundedRectangle(
            width=2.30,
            height=0.34,
            corner_radius=0.05,
            color=GRAY_A,
            fill_color=BLACK,
            fill_opacity=0.68,
            stroke_width=0.35,
            stroke_opacity=0.20,
        )
        grounding_text = VGroup(grounding_text_back, grounding_text_body)
        grounding_text.set_z_index(20)
        grounding_text.move_to(self.camera.frame.get_center() + DOWN * 0.88)
        self.play(Transform(phase1_title, phase2_title), FadeIn(grounding_text, shift=UP * 0.05), run_time=1.2)

        player_big = player_tex.copy().scale(2.2).move_to(player_tex.get_center() + LEFT * 0.03)
        dog_big = dog_tex.copy().scale(2.2).move_to(dog_tex.get_center() + RIGHT * 0.03)
        agent_icon = make_agent_icon(player_tex.get_center())
        dog_icon = make_dog_icon(dog_tex.get_center())
        agent_ring = Circle(radius=0.22, color=GOLD, stroke_width=2.2).move_to(player_tex.get_center())
        dog_ring = Circle(radius=0.22, color=ORANGE, stroke_width=2.2).move_to(dog_tex.get_center())

        self.play(
            TransformFromCopy(player_tex, player_big),
            TransformFromCopy(dog_tex, dog_big),
            run_time=1.0,
        )
        self.play(
            FadeTransform(player_big, agent_icon),
            FadeTransform(dog_big, dog_icon),
            FadeOut(player_tex),
            FadeOut(dog_tex),
            agent_ring.animate.scale(3.6).set_stroke(opacity=0),
            dog_ring.animate.scale(3.6).set_stroke(opacity=0),
            run_time=1.6,
            rate_func=smooth,
        )
        self.remove(player_big, dog_big)
        self.add(agent_icon, dog_icon)
        self.remove(agent_ring, dog_ring)
        semantic_rings = VGroup(
            Circle(radius=0.55, color=GOLD, stroke_width=1.1, stroke_opacity=0.0).move_to(agent_icon.get_center()),
            Circle(radius=0.48, color=ORANGE, stroke_width=1.1, stroke_opacity=0.0).move_to(dog_icon.get_center()),
        )

        def pulse_semantics(group, dt):
            for i, ring in enumerate(group):
                if not hasattr(ring, "phase"):
                    ring.phase = i * 0.65
                ring.phase += dt
                alpha = 0.18 + 0.22 * (0.5 + 0.5 * np.sin(ring.phase * 2.1))
                ring.set_stroke(opacity=alpha)
                ring.scale_to_fit_width(0.95 + 0.16 * np.sin(ring.phase * 2.1))

        semantic_rings.add_updater(pulse_semantics)
        self.add(semantic_rings)
        self.wait(43.8)
        semantic_rings.clear_updaters()

        # =========================================================================
        # PHASE 3: XLAND COMBINATORIAL GENERATION (95.0s - 210.0s)
        # =========================================================================
        self.play(self.camera.frame.animate.move_to(ORIGIN).set(width=config.frame_width), run_time=2.0, rate_func=smooth)
        xland_title = make_label("XLand: Procedural Generation", GOLD, 0.64)
        xland_title.next_to(title, DOWN, buff=0.24)
        self.play(
            FadeOut(phase1_title),
            FadeOut(grounding_text),
            FadeOut(grid_back),
            FadeOut(scan_lines),
            FadeOut(ascii_grid),
            FadeOut(magnifier),
            FadeOut(agent_icon),
            FadeOut(dog_icon),
            FadeOut(semantic_rings),
            FadeIn(xland_title, shift=DOWN * 0.10),
            run_time=1.4,
        )

        def make_param_matrix(label, subtitle, color, center, icon_builders):
            frame = RoundedRectangle(
                width=3.25,
                height=3.05,
                corner_radius=0.12,
                color=color,
                fill_color=BLACK,
                fill_opacity=0.34,
                stroke_width=1.2,
                stroke_opacity=0.72,
            ).move_to(center)
            title_tex = MathTex(label, color=color).scale(0.74).next_to(frame.get_top(), DOWN, buff=0.18)
            subtitle_tex = make_label(subtitle, color, 0.34).next_to(title_tex, DOWN, buff=0.06)
            cells = VGroup()
            icons = VGroup()
            for r in range(3):
                for c in range(3):
                    cell = Square(side_length=0.52, color=color, fill_color=color, fill_opacity=0.08, stroke_width=0.7, stroke_opacity=0.38)
                    cell.move_to(frame.get_center() + RIGHT * (c - 1) * 0.72 + DOWN * (r - 0.72) * 0.58)
                    icon = icon_builders[(r * 3 + c) % len(icon_builders)]().scale(0.34).move_to(cell.get_center())
                    cells.add(cell)
                    icons.add(icon)
            return VGroup(frame, title_tex, subtitle_tex, cells, icons)

        terrain_icons = [
            lambda: Triangle(color=BLUE_C, fill_color=BLUE_E, fill_opacity=0.55),
            lambda: VMobject(color=BLUE_C, stroke_width=2.0).set_points_smoothly([LEFT * 0.35, LEFT * 0.1 + UP * 0.12, RIGHT * 0.12 + DOWN * 0.08, RIGHT * 0.35 + UP * 0.08]),
            lambda: Square(color=BLUE_C, fill_color=BLUE_E, fill_opacity=0.35),
        ]
        object_icons = [
            lambda: Square(color=GRAY_A, fill_color=BLACK, fill_opacity=0.65),
            lambda: Circle(color=ORANGE, fill_color=ORANGE, fill_opacity=0.45),
            lambda: RegularPolygon(n=6, color=GOLD, fill_color=GOLD, fill_opacity=0.38),
        ]
        rule_icons = [
            lambda: Tex(r"\text{\small co-op}", color=GREEN_C),
            lambda: Tex(r"\text{\small battle}", color=RED),
            lambda: Arrow(LEFT * 0.28, RIGHT * 0.28, color=GREEN_C, stroke_width=2.0, max_tip_length_to_length_ratio=0.22),
        ]
        matrix_t = make_param_matrix("T", "Địa hình", BLUE_C, LEFT * 4.0 + UP * 0.65, terrain_icons)
        matrix_o = make_param_matrix("O", "Vật thể", ORANGE, UP * 0.65, object_icons)
        matrix_r = make_param_matrix("R", "Luật chơi", GREEN_C, RIGHT * 4.0 + UP * 0.65, rule_icons)
        matrices = VGroup(matrix_t, matrix_o, matrix_r)

        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.12) for m in matrices], lag_ratio=0.16), run_time=2.4)
        self.wait(13.6)

        combo_title = make_label("T x O x R  ->  Tổ hợp môi trường", GOLD, 0.56).next_to(matrices, DOWN, buff=0.28)
        self.play(FadeIn(combo_title, shift=UP * 0.08), run_time=0.9)

        connectors = VGroup()
        selected_cells = VGroup()
        mini_windows = VGroup()

        def make_game_window(center, terrain_kind=0, object_kind=0, rule_kind=0):
            win = RoundedRectangle(width=2.24, height=1.28, corner_radius=0.08, color=GRAY_A, fill_color=BLACK, fill_opacity=0.50, stroke_width=0.75)
            win.move_to(center)
            ground_color = BLUE_E if terrain_kind % 2 == 0 else GREEN_E
            ground = Rectangle(width=2.04, height=0.36, color=ground_color, fill_color=ground_color, fill_opacity=0.28, stroke_width=0).next_to(win.get_bottom(), UP, buff=0.12)
            obj = VGroup(
                Square(side_length=0.20, color=ORANGE if object_kind % 2 else GRAY_A, fill_color=ORANGE if object_kind % 2 else GRAY_A, fill_opacity=0.60).move_to(win.get_center() + LEFT * 0.34 + DOWN * 0.10),
                Dot(radius=0.07, color=BLUE_C).move_to(win.get_center() + RIGHT * 0.36 + DOWN * 0.05),
            )
            rule_arrow = Arrow(win.get_left() + RIGHT * 0.34, win.get_right() + LEFT * 0.34, color=GOLD if rule_kind % 2 else GREEN_C, stroke_width=1.4, max_tip_length_to_length_ratio=0.08).shift(UP * 0.28)
            return VGroup(win, ground, obj, rule_arrow)

        window_positions = [LEFT * 3.0 + DOWN * 2.35, ORIGIN + DOWN * 2.35, RIGHT * 3.0 + DOWN * 2.35]
        for i, pos in enumerate(window_positions):
            mini_windows.add(make_game_window(pos, i, i + 1, i + 2))

        def selection_for(matrix, index):
            cell = matrix[3][index].copy()
            cell.set_fill(GOLD, opacity=0.30).set_stroke(GOLD, width=2.0, opacity=0.95)
            return cell

        for cycle in range(5):
            indices = [(cycle * 2) % 9, (cycle * 2 + 3) % 9, (cycle * 2 + 6) % 9]
            selected = VGroup(selection_for(matrix_t, indices[0]), selection_for(matrix_o, indices[1]), selection_for(matrix_r, indices[2]))
            starts = [matrix_t[3][indices[0]].get_center(), matrix_o[3][indices[1]].get_center(), matrix_r[3][indices[2]].get_center()]
            target = window_positions[cycle % 3] + UP * 0.72
            lines = VGroup(*[
                Line(start, target, color=GOLD, stroke_width=2.0, stroke_opacity=0.70)
                for start in starts
            ])
            game = make_game_window(window_positions[cycle % 3], indices[0], indices[1], indices[2])
            self.play(FadeOut(selected_cells), FadeOut(connectors), run_time=0.25)
            selected_cells = selected
            connectors = lines
            self.play(FadeIn(selected_cells), Create(connectors), ReplacementTransform(mini_windows[cycle % 3], game), run_time=1.05)
            mini_windows[cycle % 3] = game
        self.wait(14.0)

        count_tracker = ValueTracker(0)
        counter = DecimalNumber(
            0,
            num_decimal_places=0,
            group_with_commas=True,
            color=ORANGE,
        ).scale(1.25).to_edge(DOWN, buff=0.34)
        counter.add_updater(lambda m: m.set_value(count_tracker.get_value()))
        count_label = make_text_block(
            ["25 tỷ môi trường mô phỏng số", "được sinh từ tổ hợp tham số gốc"],
            color=GRAY_A,
            scale=0.40,
            buff=0.08,
        ).next_to(counter, UP, buff=0.12)
        self.play(FadeIn(counter, shift=UP * 0.08), FadeIn(count_label, shift=UP * 0.08), run_time=0.8)
        self.play(count_tracker.animate.set_value(25_000_000_000), run_time=2.4, rate_func=exponential_decay)
        counter.clear_updaters()
        counter.set_value(25_000_000_000)

        petri_ring = Circle(radius=1.95, color=BLUE_C, stroke_width=2.2, stroke_opacity=0.62).move_to(ORIGIN + UP * 0.05)
        digital_agents = VGroup()
        for i in range(34):
            dot = Dot(radius=np.random.uniform(0.018, 0.045), color=random.choice([BLUE_C, GREEN_C, GOLD, ORANGE]), fill_opacity=0.82)
            angle = np.random.uniform(0, TAU)
            rad = np.random.uniform(0.15, 1.65)
            dot.move_to(petri_ring.get_center() + np.array([np.cos(angle) * rad, np.sin(angle) * rad, 0.0]))
            dot.velocity = rotate_vector(RIGHT, np.random.uniform(0, TAU)) * np.random.uniform(0.15, 0.55)
            digital_agents.add(dot)

        def update_digital_agents(group, dt):
            center = petri_ring.get_center()
            for dot in group:
                dot.shift(dot.velocity * dt)
                v = dot.get_center() - center
                if np.linalg.norm(v) > 1.72:
                    dot.velocity -= normalize(v) * 0.75
                dot.velocity += rotate_vector(dot.velocity, PI / 2) * 0.03 * dt
                dot.set_opacity(0.55 + 0.35 * np.random.random())

        self.play(
            FadeOut(selected_cells),
            FadeOut(connectors),
            FadeOut(combo_title),
            FadeOut(matrices, shift=UP * 0.12),
            FadeOut(mini_windows),
            FadeIn(petri_ring, scale=0.75),
            FadeIn(digital_agents),
            run_time=2.2,
        )
        digital_agents.add_updater(update_digital_agents)
        counter.phase = 0.0

        def pulse_counter(mob, dt):
            mob.phase += dt
            mob.set_opacity(0.74 + 0.26 * (0.5 + 0.5 * np.sin(mob.phase * 1.1)))

        counter.add_updater(pulse_counter)
        self.wait(60.4)
        digital_agents.clear_updaters()
        counter.clear_updaters()

        slider_title = make_label("Biên giới hạn học tập", GOLD, 0.52).next_to(title, DOWN, buff=0.24)
        slider_line = Line(LEFT * 4.2, RIGHT * 4.2, color=GRAY_A, stroke_width=3.0, stroke_opacity=0.72).shift(DOWN * 0.65)
        slider_track = VGroup(
            Line(slider_line.get_start(), slider_line.get_center(), color=BLUE_C, stroke_width=6.0, stroke_opacity=0.55),
            Line(slider_line.get_center(), slider_line.get_end(), color=RED, stroke_width=6.0, stroke_opacity=0.35),
        )
        slider_dot = Dot(slider_line.get_center(), radius=0.13, color=GOLD)
        slider_label = make_text_block(
            ["Không thiếu môi trường.", "Vấn đề là định tuyến năng lực học."],
            color=GRAY_A,
            scale=0.42,
            buff=0.08,
        ).next_to(slider_line, DOWN, buff=0.36)
        self.play(
            Transform(xland_title, slider_title),
            FadeOut(petri_ring),
            FadeOut(digital_agents),
            FadeOut(count_label),
            counter.animate.scale(0.42).next_to(slider_line, UP, buff=0.35),
            FadeIn(slider_track),
            Create(slider_line),
            FadeIn(slider_dot),
            FadeIn(slider_label),
            run_time=2.0,
        )
        self.play(slider_dot.animate.shift(RIGHT * 2.1), run_time=1.4, rate_func=smooth)
        self.wait(4.0)
        self.play(
            FadeOut(xland_title),
            FadeOut(counter),
            FadeOut(slider_track),
            FadeOut(slider_line),
            FadeOut(slider_dot),
            FadeOut(slider_label),
            FadeOut(title),
            run_time=1.5,
        )


class SC_06_TheAutocurriculaBottleneck(VietnameseScene):
    """
    SC_06: The Autocurricula Bottleneck & Goldilocks Zone.
    Focus: Failure of self-play (niche entrapment), difficulty scaling, cognitive Goldilocks Zone.
    """
    def construct(self):
        load_safe_sound(self, "SC_06_GoldilocksNiche.wav")
        title = create_title_banner(r"SC\_06: The Autocurricula Bottleneck \& Goldilocks Zone")
        title.scale(0.90).to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=1.0)
        self.wait(0.5)

        def make_label(text, color=WHITE, scale=0.58):
            return Tex(rf"\text{{{text}}}", color=color).scale(scale)

        def make_text_block(lines, colors=None, scale=0.55, buff=0.16, aligned_edge=LEFT):
            if colors is None:
                colors = [WHITE] * len(lines)
            block = VGroup(*[
                Tex(rf"\text{{{line}}}", color=color).scale(scale)
                for line, color in zip(lines, colors)
            ])
            block.arrange(DOWN, aligned_edge=aligned_edge, buff=buff)
            return block

        # =========================================================================
        # PHASE 1: SELF-PLAY & NICHE ENTRAPMENT (0.0s - 45.0s)
        # =========================================================================
        loop_center = LEFT * 3.25 + DOWN * 0.35
        open_grid = VGroup()
        for x in np.linspace(-2.2, 2.2, 9):
            open_grid.add(Line(UP * -1.9 + RIGHT * x, UP * 1.9 + RIGHT * x, color=GRAY_B, stroke_width=0.7, stroke_opacity=0.12))
        for y in np.linspace(-1.9, 1.9, 7):
            open_grid.add(Line(LEFT * 2.2 + UP * y, RIGHT * 2.2 + UP * y, color=GRAY_B, stroke_width=0.7, stroke_opacity=0.12))
        open_grid.move_to(loop_center)

        go_board = VGroup()
        board_size = 1.18
        board_center = LEFT * 5.55 + DOWN * 1.55
        for i in range(5):
            offset = -board_size / 2 + i * board_size / 4
            go_board.add(Line(LEFT * board_size / 2 + UP * offset, RIGHT * board_size / 2 + UP * offset, color=GRAY_B, stroke_width=0.75, stroke_opacity=0.45))
            go_board.add(Line(DOWN * board_size / 2 + RIGHT * offset, UP * board_size / 2 + RIGHT * offset, color=GRAY_B, stroke_width=0.75, stroke_opacity=0.45))
        go_board.move_to(board_center)
        go_agent = Dot(color=BLUE_C, radius=0.055).move_to(go_board.get_center() + LEFT * 0.30 + DOWN * 0.30)
        go_stones = VGroup(
            Dot(color=BLACK, radius=0.07).move_to(go_board.get_center() + RIGHT * 0.30 + UP * 0.30),
            Dot(color=WHITE, radius=0.065).move_to(go_board.get_center() + LEFT * 0.30 + UP * 0.30),
        )
        go_label = make_label("Self-play trong game đóng", GRAY_A, 0.33).next_to(go_board, DOWN, buff=0.10)
        go_group = VGroup(go_board, go_agent, go_stones, go_label)

        loop_circle = Circle(radius=1.35, color=RED, stroke_width=3.0, stroke_opacity=0.82).move_to(loop_center)
        inner_loop = Circle(radius=1.05, color=RED_E, stroke_width=1.0, stroke_opacity=0.22).move_to(loop_center)
        orbit_ticks = VGroup(*[
            Line(UP * 1.26, UP * 1.38, color=RED_E, stroke_width=1.1, stroke_opacity=0.42)
            .rotate(angle)
            .move_to(loop_center + rotate_vector(UP * 1.32, angle))
            for angle in np.linspace(0, TAU, 16, endpoint=False)
        ])
        trap_box = DashedVMobject(
            RoundedRectangle(width=3.65, height=3.65, corner_radius=0.18, color=RED_E, stroke_width=1.5, stroke_opacity=0.72),
            num_dashes=72,
            dashed_ratio=0.58,
        ).move_to(loop_center)
        trap_lbl = make_label("Bẫy Vòng Lặp Đóng (Closed Loop Niche)", RED, 0.52).next_to(trap_box, UP, buff=0.16)
        
        agent_a = VGroup(
            Circle(radius=0.19, color=BLUE_C, stroke_width=2.0, stroke_opacity=0.65),
            Dot(color=BLUE_C, radius=0.095),
        ).move_to(loop_circle.point_at_angle(0))
        lbl_a = make_label("Agent A", BLUE_C, 0.43).next_to(agent_a, UP, buff=0.08)
        agent_b = VGroup(
            Circle(radius=0.19, color=ORANGE, stroke_width=2.0, stroke_opacity=0.65),
            Dot(color=ORANGE, radius=0.095),
        ).move_to(loop_circle.point_at_angle(PI))
        lbl_b = make_label("Agent B", ORANGE, 0.43).next_to(agent_b, DOWN, buff=0.08)
        chase_trail = Arc(radius=1.35, start_angle=-0.35, angle=0.70, color=GOLD, stroke_width=4.0, stroke_opacity=0.42).move_arc_center_to(loop_center)
        
        niche_card = RoundedRectangle(
            width=5.05,
            height=2.35,
            corner_radius=0.16,
            color=RED_E,
            fill_color=BLACK,
            fill_opacity=0.55,
            stroke_width=1.2,
            stroke_opacity=0.62,
        ).move_to(RIGHT * 2.65 + DOWN * 0.35)
        niche_lbl = make_text_block(
            [
                "Thất bại của Tự chơi (Self-play Failure):",
                "Entrapment trong phân khúc chiến thuật hẹp",
            ],
            colors=[RED, GRAY_A],
            scale=0.55,
            buff=0.20,
            aligned_edge=LEFT,
        ).move_to(niche_card.get_center())
        niche_hint = make_label("Tác nhân học cách thắng đối thủ quen thuộc, không học cách mở rộng thế giới.", GRAY_B, 0.37)
        niche_hint.next_to(niche_card, DOWN, buff=0.22)
        trial_tracker = ValueTracker(0)
        trial_counter = DecimalNumber(0, num_decimal_places=0, group_with_commas=True, color=GOLD).scale(0.55)
        trial_counter.add_updater(lambda m: m.set_value(trial_tracker.get_value()))
        trial_label = make_label("closed-loop trials", GRAY_B, 0.35).next_to(trial_counter, DOWN, buff=0.08)
        trial_group = VGroup(trial_counter, trial_label).next_to(niche_card, UP, buff=0.22)
        phase1 = VGroup(open_grid, go_group, loop_circle, inner_loop, orbit_ticks, trap_box, trap_lbl, agent_a, lbl_a, agent_b, lbl_b, chase_trail, niche_card, niche_lbl, niche_hint, trial_group)

        self.play(
            FadeIn(open_grid),
            FadeIn(go_group, shift=RIGHT * 0.10),
            Create(trap_box),
            Create(loop_circle),
            Create(inner_loop),
            LaggedStart(*[Create(tick) for tick in orbit_ticks], lag_ratio=0.02),
            FadeIn(trap_lbl, shift=DOWN * 0.08),
            FadeIn(agent_a, scale=0.75),
            FadeIn(agent_b, scale=0.75),
            FadeIn(lbl_a),
            FadeIn(lbl_b),
            run_time=2.2,
        )
        self.play(FadeIn(chase_trail), FadeIn(niche_card, shift=LEFT * 0.12), Write(niche_lbl), FadeIn(niche_hint), FadeIn(trial_group), run_time=1.4)
        
        def update_agent_a(m, dt):
            angle = (self.time * 1.35) % TAU
            m.move_to(loop_circle.point_at_angle(angle))
            lbl_a.next_to(m, UP, buff=0.08)
            
        def update_agent_b(m, dt):
            angle = (self.time * 1.35 + PI * 0.82) % TAU
            m.move_to(loop_circle.point_at_angle(angle))
            lbl_b.next_to(m, DOWN, buff=0.08)

        def update_trail(m, dt):
            m.rotate(1.35 * dt, about_point=loop_center)

        def update_go_agent(m, dt):
            progress = (self.time * 0.24) % 1.0
            points = [
                go_board.get_center() + LEFT * 0.30 + DOWN * 0.30,
                go_board.get_center() + RIGHT * 0.30 + DOWN * 0.30,
                go_board.get_center() + RIGHT * 0.30 + UP * 0.30,
                go_board.get_center() + LEFT * 0.30 + UP * 0.30,
            ]
            edge = int(progress * 4) % 4
            local_t = (progress * 4) % 1
            m.move_to(interpolate(points[edge], points[(edge + 1) % 4], local_t))
            
        agent_a.add_updater(update_agent_a)
        agent_b.add_updater(update_agent_b)
        chase_trail.add_updater(update_trail)
        go_agent.add_updater(update_go_agent)
        
        self.play(trial_tracker.animate.set_value(9_800_000), run_time=39.9, rate_func=linear)
        trial_counter.clear_updaters()
        go_agent.clear_updaters()

        # =========================================================================
        # PHASE 2: COGNITIVE GOLDILOCKS ZONE (45.0s - 95.0s)
        # =========================================================================
        agent_a.clear_updaters()
        agent_b.clear_updaters()
        chase_trail.clear_updaters()
        
        self.play(FadeOut(phase1, shift=DOWN * 0.12), run_time=1.0)

        phase2_title = make_label("Vùng Goldilocks nhận thức (Cognitive Zone)", GOLD, 0.60).next_to(title, DOWN, buff=0.24)
        meter = GoldilocksZoneMeter(width=0.82, height=3.75).shift(RIGHT * 3.45 + DOWN * 0.25)
        gold_window = RoundedRectangle(
            width=1.22,
            height=1.34,
            corner_radius=0.10,
            color=GOLD,
            stroke_width=2.4,
            stroke_opacity=0.78,
        ).move_to(meter.goldilocks_zone.get_center())
        ability_dot = Dot(meter.point_for_level(0.18) + RIGHT * 1.13, radius=0.085, color=BLUE_C)
        ability_label = make_label("năng lực Agent", BLUE_C, 0.34).next_to(ability_dot, RIGHT, buff=0.12)
        analysis_panel = RoundedRectangle(
            width=5.3,
            height=3.35,
            corner_radius=0.16,
            color=GRAY_B,
            fill_color=BLACK,
            fill_opacity=0.46,
            stroke_width=1.0,
            stroke_opacity=0.45,
        ).shift(LEFT * 2.5 + DOWN * 0.35)
        meter_explain = make_text_block(
            [
                "Quá dễ: gradient triệt tiêu, đóng băng năng lực",
                "Quá khó: bế tắc, không thể học hỏi được",
                "Goldilocks: nhiệm vụ nằm ở biên nỗ lực phù hợp",
            ],
            colors=[BLUE_C, RED, GOLD],
            scale=0.49,
            buff=0.28,
            aligned_edge=LEFT,
        ).move_to(analysis_panel.get_center())
        calibration_line = DashedLine(
            analysis_panel.get_right() + RIGHT * 0.16,
            meter.goldilocks_zone.get_left() + LEFT * 0.05,
            color=GOLD,
            stroke_width=1.4,
            stroke_opacity=0.45,
        )

        self.play(
            FadeIn(phase2_title, shift=DOWN * 0.08),
            Create(meter),
            FadeIn(analysis_panel, shift=RIGHT * 0.12),
            LaggedStart(*[FadeIn(line, shift=UP * 0.08) for line in meter_explain], lag_ratio=0.15),
            Create(calibration_line),
            Create(gold_window),
            FadeIn(ability_dot),
            FadeIn(ability_label),
            run_time=2.4,
        )
        self.wait(8.0)
        
        target_y = meter.point_for_level(0.50)[1]
        self.play(
            meter.pointer.animate.shift(UP * (target_y - meter.pointer.get_center()[1])),
            ability_dot.animate.move_to(meter.point_for_level(0.50) + RIGHT * 1.13),
            ability_label.animate.next_to(meter.point_for_level(0.50) + RIGHT * 1.13, RIGHT, buff=0.12),
            run_time=2.8,
            rate_func=smooth,
        )
        self.wait(35.8)

        # =========================================================================
        # PHASE 3: UNIFORM SAMPLING & BREAKDOWN (95.0s - 180.0s)
        # =========================================================================
        self.play(FadeOut(phase2_title), FadeOut(analysis_panel), FadeOut(meter_explain), FadeOut(calibration_line), FadeOut(gold_window), FadeOut(ability_label), run_time=1.0)
        
        graph_axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 1.2, 0.3],
            x_length=5.3,
            y_length=3.0,
            axis_config={"stroke_width": 1.4, "color": GRAY_A},
            tips=False,
        ).shift(LEFT * 2.75 + DOWN * 0.55)
        
        graph_lbl = make_label("Phân phối độ khó nhiệm vụ (Task Difficulty)", GRAY_A, 0.50).next_to(graph_axes, UP, buff=0.18)
        x_lbl = MathTex(r"\text{difficulty}", color=GRAY_B).scale(0.45).next_to(graph_axes.x_axis, DOWN, buff=0.20)
        y_lbl = MathTex(r"\text{probability}", color=GRAY_B).scale(0.45).rotate(PI / 2).next_to(graph_axes.y_axis, LEFT, buff=0.25)
        
        ideal_curve = graph_axes.plot(lambda x: np.exp(-((x - 3.0) ** 2) / (2 * 0.72 ** 2)), color=GREEN_C, stroke_width=3.2)
        ideal_area = graph_axes.get_area(ideal_curve, x_range=[1.1, 4.9], color=GOLD, opacity=0.13)
        ideal_lbl = make_label("Giáo trình lý tưởng (Curriculum)", GREEN_C, 0.43).next_to(ideal_curve.get_top(), UP, buff=0.12)
        
        uniform_curve = graph_axes.plot(lambda x: 0.32, color=RED, stroke_width=2.8)
        uniform_lbl = make_label("Lấy mẫu đều (Uniform Sampling)", RED, 0.42).next_to(graph_axes.c2p(4.25, 0.32), UP, buff=0.12)
        
        collapse_lbl = VGroup(
            Tex(r"\text{Uniform Sampling}", color=RED).scale(0.58),
            MathTex(r"\rightarrow", color=RED).scale(0.60),
            Tex(r"\text{Đứt gãy giáo trình huấn luyện}", color=RED).scale(0.58),
        ).arrange(RIGHT, buff=0.16).to_edge(DOWN, buff=0.34)
        alert_box = RoundedRectangle(
            width=collapse_lbl.width + 0.60,
            height=0.62,
            corner_radius=0.12,
            color=RED_E,
            fill_color=RED_E,
            fill_opacity=0.10,
            stroke_width=1.1,
            stroke_opacity=0.55,
        ).move_to(collapse_lbl)
        
        self.play(
            Create(graph_axes),
            FadeIn(graph_lbl),
            FadeIn(x_lbl),
            FadeIn(y_lbl),
            FadeIn(ideal_area),
            Create(ideal_curve),
            FadeIn(ideal_lbl, shift=DOWN * 0.08),
            Create(uniform_curve),
            FadeIn(uniform_lbl, shift=UP * 0.08),
            FadeIn(alert_box),
            Write(collapse_lbl),
            run_time=3.2,
        )

        sampler_arrow = Arrow(ORIGIN + RIGHT * 0.68, ORIGIN, color=RED, stroke_width=3.0, max_tip_length_to_length_ratio=0.32)
        sampler_label = make_label("Uniform Sampling", RED, 0.38)
        sampler_group = VGroup(sampler_arrow, sampler_label).arrange(DOWN, buff=0.08)
        sampler_group.move_to(meter.point_for_level(0.12) + RIGHT * 1.25)
        sample_levels = [0.12, 0.92, 0.18, 0.84, 0.06]
        self.play(FadeIn(sampler_group, shift=LEFT * 0.08), run_time=0.4)
        for level in sample_levels[1:]:
            target = meter.point_for_level(level) + RIGHT * 1.25
            self.play(sampler_group.animate.move_to(target), ability_dot.animate.move_to(target + LEFT * 0.35), run_time=0.32, rate_func=there_and_back)
        
        for direction in [RIGHT, LEFT, RIGHT, LEFT, UP, DOWN]:
            self.play(meter.animate.shift(direction * 0.12), run_time=0.12, rate_func=there_and_back)
        
        self.wait(72.56)

        crack_lines = VGroup()
        crack_anchor = meter.get_center()
        crack_specs = [
            [UP * 1.75 + LEFT * 0.28, UP * 1.15 + RIGHT * 0.10, UP * 0.45 + LEFT * 0.20],
            [UP * 0.95 + RIGHT * 0.35, UP * 0.20 + LEFT * 0.05, DOWN * 0.58 + RIGHT * 0.25],
            [DOWN * 0.35 + LEFT * 0.30, DOWN * 1.05 + RIGHT * 0.12, DOWN * 1.72 + LEFT * 0.24],
        ]
        for spec in crack_specs:
            line = VMobject(color=RED, stroke_width=2.2, stroke_opacity=0.82)
            line.set_points_as_corners([crack_anchor + point for point in spec])
            crack_lines.add(line)
        lost_compass = make_label("La bàn định hướng bị mất", RED, 0.66).next_to(title, DOWN, buff=0.28)
        self.play(Create(crack_lines), FadeIn(lost_compass, shift=DOWN * 0.10), run_time=1.2)
        self.play(meter.animate.shift(DOWN * 0.18).set_opacity(0.45), sampler_group.animate.set_opacity(0.25), ability_dot.animate.set_opacity(0.25), run_time=1.0)
        self.wait(2.0)
        self.play(
            FadeOut(meter),
            FadeOut(crack_lines),
            FadeOut(lost_compass),
            FadeOut(sampler_group),
            FadeOut(ability_dot),
            FadeOut(alert_box),
            FadeOut(collapse_lbl),
            FadeOut(graph_axes),
            FadeOut(graph_lbl),
            FadeOut(x_lbl),
            FadeOut(y_lbl),
            FadeOut(ideal_area),
            FadeOut(ideal_curve),
            FadeOut(ideal_lbl),
            FadeOut(uniform_curve),
            FadeOut(uniform_lbl),
            FadeOut(title),
            run_time=1.5
        )


class SC_07_TheEvolutionaryEngines(VietnameseMovingCameraScene):
    """
    SC_07: The Evolutionary Engines: Foundation Models.
    Premium implementation of LLM-driven semantic variation/selection, sample efficiency, AI Safety, and Chapter 2 transition.
    """
    def construct(self):
        load_safe_sound(self, "SC_07_Evolutionary_Engines.wav")
        title = create_title_banner(r"SC\_07: The Evolutionary Engines: Foundation Models")
        title.scale(0.90).to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=1.0)
        self.wait(0.5)

        def make_label(text, color=WHITE, scale=0.55):
            return Tex(rf"\text{{{text}}}", color=color).scale(scale)

        def make_text_block(lines, colors=None, scale=0.48, buff=0.10, aligned_edge=LEFT):
            if colors is None:
                colors = [WHITE] * len(lines)
            group = VGroup(*[
                Tex(rf"\text{{{line}}}", color=color).scale(scale)
                for line, color in zip(lines, colors)
            ])
            group.arrange(DOWN, aligned_edge=aligned_edge, buff=buff)
            return group

        def sequence_label(words, color=GRAY_A, scale=0.42):
            parts = []
            for index, word in enumerate(words):
                if index > 0:
                    parts.append(MathTex(r"\rightarrow", color=color).scale(scale))
                parts.append(Tex(rf"\text{{{word}}}", color=color).scale(scale))
            return VGroup(*parts).arrange(RIGHT, buff=0.10)

        def make_chip(text, color=WHITE, scale=0.34, min_width=1.28):
            label = make_label(text, color, scale)
            box = RoundedRectangle(
                width=max(min_width, label.width + 0.30),
                height=max(0.34, label.height + 0.16),
                corner_radius=0.08,
                color=color,
                fill_color=BLACK,
                fill_opacity=0.72,
                stroke_width=1.0,
                stroke_opacity=0.72,
            )
            label.move_to(box)
            return VGroup(box, label)

        # =========================================================================
        # PHASE 1: CORE SYSTEM BLOCKS (0.0s - 45.0s)
        # =========================================================================
        sim_box = RoundedRectangle(
            width=4.35,
            height=2.55,
            corner_radius=0.16,
            color=BLUE_C,
            fill_color=BLUE_E,
            fill_opacity=0.12,
            stroke_width=1.5,
            stroke_opacity=0.78,
        ).move_to(LEFT * 3.35 + UP * 0.25)
        floor_front_left = sim_box.get_center() + LEFT * 1.72 + DOWN * 0.92
        floor_front_right = sim_box.get_center() + RIGHT * 1.72 + DOWN * 0.92
        floor_back_left = sim_box.get_center() + LEFT * 0.72 + DOWN * 0.02
        floor_back_right = sim_box.get_center() + RIGHT * 0.72 + DOWN * 0.02
        floor_outline = VGroup(
            Line(floor_front_left, floor_front_right, color=BLUE_C, stroke_width=1.3, stroke_opacity=0.60),
            Line(floor_front_left, floor_back_left, color=BLUE_C, stroke_width=1.1, stroke_opacity=0.46),
            Line(floor_front_right, floor_back_right, color=BLUE_C, stroke_width=1.1, stroke_opacity=0.46),
            Line(floor_back_left, floor_back_right, color=BLUE_C, stroke_width=1.0, stroke_opacity=0.36),
        )
        perspective_grid = VGroup()
        for alpha in np.linspace(0.12, 0.88, 7):
            perspective_grid.add(Line(
                interpolate(floor_front_left, floor_front_right, alpha),
                interpolate(floor_back_left, floor_back_right, alpha),
                color=BLUE_C,
                stroke_width=0.8,
                stroke_opacity=0.28,
            ))
        for beta in np.linspace(0.18, 0.82, 5):
            perspective_grid.add(Line(
                interpolate(floor_front_left, floor_back_left, beta),
                interpolate(floor_front_right, floor_back_right, beta),
                color=BLUE_C,
                stroke_width=0.8,
                stroke_opacity=0.24,
            ))
        sim_agent = VGroup(
            Circle(radius=0.22, color=BLUE_C, stroke_width=2.0, stroke_opacity=0.55),
            Dot(radius=0.09, color=BLUE_C),
        ).move_to(sim_box.get_center() + DOWN * 0.36)
        sim_label = make_label("XLand simulation space", BLUE_C, 0.48).next_to(sim_box, DOWN, buff=0.16)
        sim_group = VGroup(sim_box, floor_outline, perspective_grid, sim_agent, sim_label)

        llm_box = RoundedRectangle(
            width=4.25,
            height=2.75,
            corner_radius=0.18,
            color=ORANGE,
            fill_color=BLACK,
            fill_opacity=0.82,
            stroke_width=1.8,
            stroke_opacity=0.88,
        ).move_to(RIGHT * 3.35 + UP * 0.25)
        llm_label = make_label("LLM Task Proposer", ORANGE, 0.64).next_to(llm_box, UP, buff=0.18)
        nn_layers = []
        for layer_index, count in enumerate([4, 5, 4, 3]):
            layer = VGroup()
            for node_index in range(count):
                node = Circle(radius=0.065, color=ORANGE, fill_color=ORANGE, fill_opacity=0.84, stroke_width=1.0)
                node.move_to(
                    llm_box.get_center()
                    + LEFT * 1.35
                    + RIGHT * layer_index * 0.90
                    + DOWN * (node_index - (count - 1) / 2) * 0.34
                )
                layer.add(node)
            nn_layers.append(layer)
        nn_nodes = VGroup(*nn_layers)
        synapses = VGroup()
        for layer_index in range(len(nn_layers) - 1):
            for left_node in nn_layers[layer_index]:
                for right_node in nn_layers[layer_index + 1]:
                    synapses.add(Line(
                        left_node.get_center(),
                        right_node.get_center(),
                        color=ORANGE,
                        stroke_width=0.55,
                        stroke_opacity=0.22,
                    ))
        llm_caption = make_text_block(
            ["Pre-trained semantic prior", "curriculum routing"],
            colors=[GRAY_A, GRAY_A],
            scale=0.34,
            buff=0.05,
            aligned_edge=ORIGIN,
        ).next_to(llm_box, DOWN, buff=0.15)
        llm_group = VGroup(llm_box, synapses, nn_nodes, llm_label, llm_caption)

        self.play(
            FadeIn(sim_box, shift=RIGHT * 0.18),
            Create(floor_outline),
            LaggedStart(*[Create(line) for line in perspective_grid], lag_ratio=0.02),
            FadeIn(sim_agent, scale=0.80),
            FadeIn(sim_label),
            FadeIn(llm_box, shift=LEFT * 0.18),
            Create(synapses),
            LaggedStart(*[FadeIn(layer, scale=0.75) for layer in nn_nodes], lag_ratio=0.08),
            FadeIn(llm_label, shift=DOWN * 0.08),
            FadeIn(llm_caption),
            run_time=2.8,
        )

        ripple_waves = VGroup()
        for index in range(3):
            wave = Circle(radius=0.42, color=ORANGE, stroke_width=2.0, stroke_opacity=0.0).move_to(llm_box)
            wave.phase = index / 3
            ripple_waves.add(wave)

        def update_ripples(group, dt):
            for wave in group:
                wave.phase = (wave.phase + dt * 0.32) % 1.0
                radius = 0.65 + wave.phase * 1.85
                opacity = 0.34 * (1.0 - wave.phase)
                wave.become(Circle(radius=radius, color=ORANGE, stroke_width=2.0, stroke_opacity=opacity).move_to(llm_box.get_center()))

        ripple_waves.add_updater(update_ripples)
        self.add(ripple_waves)

        phase1_note = make_chip("semantic proposal probes", GOLD, 0.34, min_width=2.50).to_edge(DOWN, buff=0.54)
        proposal_path = Line(llm_box.get_left() + LEFT * 0.06, sim_box.get_right() + RIGHT * 0.06)
        probe_packets = VGroup(*[
            Dot(radius=0.055, color=GOLD if index % 2 == 0 else ORANGE, fill_opacity=0.88).move_to(proposal_path.get_start())
            for index in range(5)
        ])
        synapse_highlights = VGroup(*[
            line.copy().set_color(GOLD).set_stroke(width=1.25, opacity=0.70)
            for index, line in enumerate(synapses)
            if index % 7 == 0
        ])
        focus_ring = Circle(radius=0.28, color=BLUE_C, stroke_width=2.0, stroke_opacity=0.72).move_to(sim_agent.get_center())
        curriculum_hint = sequence_label(["đề xuất", "thử nghiệm", "phản hồi"], GOLD, 0.36).to_edge(DOWN, buff=0.56)

        self.play(
            FadeIn(phase1_note, shift=UP * 0.08),
            llm_box.animate.set_stroke(width=2.7, opacity=1.0),
            run_time=2.5,
        )
        self.play(
            LaggedStart(*[MoveAlongPath(packet, proposal_path.copy()) for packet in probe_packets], lag_ratio=0.18),
            run_time=5.5,
        )
        self.play(
            FadeOut(probe_packets),
            sim_agent.animate.shift(LEFT * 0.34),
            rate_func=there_and_back,
            run_time=4.0,
        )
        self.play(
            LaggedStart(*[FadeIn(line) for line in synapse_highlights], lag_ratio=0.025),
            run_time=1.8,
        )
        self.play(FadeOut(synapse_highlights), run_time=2.4)
        self.play(Create(focus_ring), run_time=0.8)
        self.play(focus_ring.animate.scale(1.85).set_opacity(0.0), run_time=2.7)
        self.play(self.camera.frame.animate.shift(RIGHT * 0.22).scale(0.98), run_time=4.8, rate_func=smooth)
        self.play(self.camera.frame.animate.shift(LEFT * 0.22).scale(1 / 0.98), run_time=4.8, rate_func=smooth)
        self.play(
            FadeIn(curriculum_hint, shift=UP * 0.06),
            sim_box.animate.set_fill(opacity=0.18),
            run_time=2.7,
        )
        self.play(
            FadeOut(curriculum_hint, shift=DOWN * 0.06),
            FadeOut(phase1_note, shift=DOWN * 0.06),
            llm_box.animate.set_stroke(width=1.8, opacity=0.88),
            sim_box.animate.set_fill(opacity=0.12),
            run_time=2.7,
        )
        self.wait(6.0)

        # =========================================================================
        # PHASE 2: SEMANTIC DARWINIAN LOOP (45.0s - 85.0s)
        # =========================================================================
        arrow_variation = ArcBetweenPoints(
            llm_box.get_top() + LEFT * 0.25,
            sim_box.get_top() + RIGHT * 0.25,
            angle=-TAU / 6,
            color=ORANGE,
            stroke_width=3.0,
        ).add_tip(tip_length=0.20)
        var_lbl = make_label("Biến dị Ngữ nghĩa (Variation)", ORANGE, 0.47).next_to(arrow_variation, UP, buff=0.12)
        var_sequence = sequence_label(["Nhặt đá", "Chế rìu", "Dựng lều"], ORANGE, 0.38).next_to(var_lbl, DOWN, buff=0.08)

        arrow_selection = ArcBetweenPoints(
            sim_box.get_bottom() + RIGHT * 0.25,
            llm_box.get_bottom() + LEFT * 0.25,
            angle=-TAU / 6,
            color=GOLD,
            stroke_width=3.0,
        ).add_tip(tip_length=0.20)
        sel_lbl = make_label("Chọn lọc Ngữ nghĩa (Selection)", GOLD, 0.47).next_to(arrow_selection, DOWN, buff=0.12)
        sel_sequence = sequence_label(["Kết quả hành vi", "Đánh giá phản hồi"], GOLD, 0.36).next_to(sel_lbl, UP, buff=0.08)

        particles_var = VGroup(*[Dot(radius=0.045, color=ORANGE, fill_opacity=0.86) for _ in range(6)])
        particles_sel = VGroup(*[Dot(radius=0.045, color=GOLD, fill_opacity=0.82) for _ in range(6)])

        def make_flow_updater(path, speed=0.48, delay=0.13):
            def updater(m, dt):
                for i, dot in enumerate(m):
                    t = (self.time * speed - i * delay) % 1.0
                    dot.move_to(path.point_from_proportion(t))
                    dot.set_opacity(0.30 + 0.70 * np.sin(PI * t))
            return updater

        self.play(Create(arrow_variation), FadeIn(var_lbl, shift=DOWN * 0.08), FadeIn(var_sequence), run_time=1.6)
        self.play(Create(arrow_selection), FadeIn(sel_lbl, shift=UP * 0.08), FadeIn(sel_sequence), run_time=1.4)
        particles_var.add_updater(make_flow_updater(arrow_variation, speed=0.50, delay=0.11))
        particles_sel.add_updater(make_flow_updater(arrow_selection, speed=0.44, delay=0.12))
        self.add(particles_var, particles_sel)
        loop_group = VGroup(
            sim_group, llm_group, ripple_waves,
            arrow_variation, var_lbl, var_sequence,
            arrow_selection, sel_lbl, sel_sequence,
            particles_var, particles_sel,
        )

        loop_hint = make_chip("vòng lặp đề xuất và chọn lọc", GOLD, 0.34, min_width=2.75).to_edge(DOWN, buff=0.52)
        agent_motion_path = VMobject(color=BLUE_C, stroke_opacity=0.0)
        agent_motion_path.set_points_smoothly([
            sim_agent.get_center(),
            sim_agent.get_center() + LEFT * 0.42 + UP * 0.18,
            sim_agent.get_center() + RIGHT * 0.34 + UP * 0.34,
            sim_agent.get_center() + RIGHT * 0.48 + DOWN * 0.10,
        ])
        agent_trace = TracedPath(sim_agent.get_center, stroke_color=BLUE_C, stroke_width=2.0, stroke_opacity=0.44, dissipating_time=5.5)
        self.add(agent_trace)
        loop_group.add(agent_trace)

        self.play(FadeIn(loop_hint, shift=UP * 0.08), run_time=2.0)
        for task_name in ["Nhặt đá", "Chế rìu", "Dựng lều"]:
            task_chip = make_chip(task_name, ORANGE, 0.33, min_width=1.18).move_to(arrow_variation.point_from_proportion(0.0))
            self.play(FadeIn(task_chip, scale=0.85), MoveAlongPath(task_chip, arrow_variation), run_time=2.2)
            self.play(FadeOut(task_chip, scale=0.90), run_time=0.4)
        self.play(
            MoveAlongPath(sim_agent, agent_motion_path),
            arrow_variation.animate.set_stroke(width=4.2, opacity=1.0),
            run_time=6.5,
            rate_func=smooth,
        )
        feedback_chip = make_chip("đánh giá phản hồi", GOLD, 0.32, min_width=1.75).move_to(arrow_selection.point_from_proportion(0.0))
        self.play(FadeIn(feedback_chip, scale=0.85), MoveAlongPath(feedback_chip, arrow_selection), run_time=5.1)
        self.play(FadeOut(feedback_chip, scale=0.90), run_time=0.6)
        self.play(
            arrow_variation.animate.set_stroke(width=3.0, opacity=0.88),
            arrow_selection.animate.set_stroke(width=4.2, opacity=1.0),
            sim_agent.animate.scale(1.15),
            run_time=2.0,
        )
        self.play(
            arrow_selection.animate.set_stroke(width=3.0, opacity=0.88),
            sim_agent.animate.scale(1 / 1.15),
            run_time=2.0,
        )
        self.play(self.camera.frame.animate.shift(LEFT * 0.20), run_time=3.0, rate_func=smooth)
        self.play(self.camera.frame.animate.shift(RIGHT * 0.20), run_time=3.0, rate_func=smooth)
        self.play(FadeOut(loop_hint, shift=DOWN * 0.06), run_time=2.0)
        self.wait(3.0)

        # =========================================================================
        # PHASE 3: SAMPLE EFFICIENCY GRAPH (85.0s - 110.0s)
        # =========================================================================
        graph_axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            x_length=7.0,
            y_length=2.8,
            axis_config={"stroke_width": 1.3, "color": GRAY_A},
            tips=False,
        ).shift(DOWN * 1.75)
        graph_title = make_label("Sample Efficiency", GOLD, 0.55).next_to(graph_axes, UP, buff=0.22)
        x_axis_label = make_label("Số lượng mẫu huấn luyện", GRAY_A, 0.36).next_to(graph_axes.x_axis, DOWN, buff=0.22)
        y_axis_label = make_label("Hiệu suất", GRAY_A, 0.36).rotate(PI / 2).next_to(graph_axes.y_axis, LEFT, buff=0.28)
        llm_curve = graph_axes.plot(lambda x: 9.0 * (1.0 - np.exp(-x / 1.55)), color=GREEN_C, stroke_width=3.8)
        llm_curve_lbl = make_label("LLM Proposer", GREEN_C, 0.40).next_to(graph_axes.c2p(6.2, 8.7), RIGHT, buff=0.12)
        random_curve = graph_axes.plot(lambda x: 0.85 + 0.10 * np.sin(x * 1.3), color=GRAY_E, stroke_width=3.2)
        random_curve_lbl = make_label("Random / Uniform", GRAY_A, 0.38).next_to(graph_axes.c2p(6.6, 0.92), UP, buff=0.10)

        self.play(loop_group.animate.scale(0.52).to_edge(UP, buff=0.80), run_time=2.0, rate_func=smooth)
        self.play(
            Create(graph_axes),
            FadeIn(graph_title),
            FadeIn(x_axis_label),
            FadeIn(y_axis_label),
            Create(random_curve),
            FadeIn(random_curve_lbl),
            Create(llm_curve),
            FadeIn(llm_curve_lbl),
            run_time=3.0,
        )
        llm_marker = Dot(radius=0.07, color=GREEN_C).move_to(llm_curve.get_start())
        random_marker = Dot(radius=0.065, color=GRAY_E).move_to(random_curve.get_start())
        efficiency_gap = DashedLine(
            graph_axes.c2p(7.0, 1.0),
            graph_axes.c2p(7.0, 8.8),
            color=GOLD,
            stroke_width=2.0,
            dash_length=0.08,
            dashed_ratio=0.55,
        )
        gap_label = make_label("sample-efficiency gap", GOLD, 0.34).next_to(efficiency_gap, RIGHT, buff=0.14)
        graph_group = VGroup(
            graph_axes, graph_title, x_axis_label, y_axis_label,
            random_curve, random_curve_lbl, llm_curve, llm_curve_lbl,
            llm_marker, random_marker, efficiency_gap, gap_label,
        )
        self.play(
            FadeIn(llm_marker, scale=0.70),
            FadeIn(random_marker, scale=0.70),
            MoveAlongPath(llm_marker, llm_curve),
            MoveAlongPath(random_marker, random_curve),
            run_time=6.0,
            rate_func=smooth,
        )
        self.play(Create(efficiency_gap), FadeIn(gap_label, shift=LEFT * 0.08), run_time=3.0)
        self.play(llm_curve.animate.set_stroke(width=5.2, opacity=1.0), llm_curve_lbl.animate.scale(1.08), run_time=2.5)
        self.play(llm_curve.animate.set_stroke(width=3.8, opacity=1.0), llm_curve_lbl.animate.scale(1 / 1.08), run_time=2.5)
        self.play(random_curve.animate.set_stroke(opacity=0.36), random_curve_lbl.animate.set_color(GRAY_B), run_time=2.0)
        self.play(random_curve.animate.set_stroke(opacity=1.0), random_curve_lbl.animate.set_color(GRAY_A), run_time=2.0)
        self.wait(2.0)

        # =========================================================================
        # PHASE 4: AI SAFETY & SPECIFICATION GAMING (110.0s - 135.0s)
        # =========================================================================
        particles_var.clear_updaters()
        particles_sel.clear_updaters()
        ripple_waves.clear_updaters()
        self.play(
            FadeOut(graph_group, shift=DOWN * 0.12),
            FadeOut(loop_group, shift=UP * 0.10),
            run_time=1.0,
        )

        safety_title = make_label("AI Safety: Proxy Observer", GOLD, 0.56).next_to(title, DOWN, buff=0.22)
        protected_agent = VGroup(
            Circle(radius=0.85, color=BLUE_C, fill_color=BLUE_E, fill_opacity=0.10, stroke_width=2.6, stroke_opacity=0.86),
            Arc(radius=0.92, start_angle=PI * 0.06, angle=PI * 0.88, color=BLUE_C, stroke_width=3.0, stroke_opacity=0.72),
            Dot(radius=0.10, color=BLUE_C),
        ).move_to(DOWN * 0.20)
        proxy_label = make_label("Proxy Observer", BLUE_C, 0.50).next_to(protected_agent, DOWN, buff=0.24)
        safety_group = VGroup(safety_title, protected_agent, proxy_label)
        attack_specs = [
            (LEFT * 5.2 + UP * 1.35, protected_agent.get_center() + LEFT * 0.75 + UP * 0.34),
            (RIGHT * 5.2 + UP * 1.00, protected_agent.get_center() + RIGHT * 0.78 + UP * 0.18),
            (LEFT * 4.5 + DOWN * 1.70, protected_agent.get_center() + LEFT * 0.65 + DOWN * 0.42),
            (RIGHT * 4.7 + DOWN * 1.55, protected_agent.get_center() + RIGHT * 0.66 + DOWN * 0.40),
        ]
        attacks = VGroup(*[
            Arrow(start, end, color=RED, stroke_width=3.0, max_tip_length_to_length_ratio=0.14)
            for start, end in attack_specs
        ])
        attack_label = make_label("Specification Gaming", RED, 0.48).to_edge(DOWN, buff=0.58)
        shards = VGroup()
        for _, end in attack_specs:
            for angle in [PI / 5, -PI / 4, PI / 2]:
                shards.add(Line(end, end + rotate_vector(RIGHT * 0.22, angle), color=RED, stroke_width=1.8, stroke_opacity=0.78))
        self.play(FadeIn(safety_group, shift=UP * 0.10), run_time=1.4)
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in attacks], lag_ratio=0.10), FadeIn(attack_label), run_time=1.8)
        self.play(FadeIn(shards), attacks.animate.set_opacity(0.10), run_time=0.8)

        defense_particles = VGroup()
        for index in range(10):
            particle = Dot(radius=0.028, color=BLUE_C, fill_opacity=0.80)
            particle.phase = index / 10
            defense_particles.add(particle)

        def update_defense_particles(group, dt):
            for index, particle in enumerate(group):
                particle.phase = (particle.phase + dt * (0.12 + 0.015 * (index % 3))) % 1.0
                angle = TAU * particle.phase
                particle.move_to(
                    protected_agent.get_center()
                    + RIGHT * np.cos(angle) * 1.02
                    + UP * np.sin(angle) * 0.92
                )
                particle.set_opacity(0.32 + 0.55 * (0.5 + 0.5 * np.sin(self.time * 2.0 + index)))

        defense_particles.add_updater(update_defense_particles)
        self.add(defense_particles)
        safety_group.add(defense_particles)
        impact_rings = VGroup(*[
            Circle(radius=0.86 + 0.14 * index, color=BLUE_C, stroke_width=1.6, stroke_opacity=0.38 - 0.08 * index).move_to(protected_agent)
            for index in range(3)
        ])
        self.play(protected_agent.animate.scale(1.06), attacks.animate.set_opacity(0.18), run_time=3.0)
        self.play(protected_agent.animate.scale(1 / 1.06), attacks.animate.set_opacity(0.10), run_time=3.0)
        self.play(LaggedStart(*[Create(ring) for ring in impact_rings], lag_ratio=0.20), run_time=3.0)
        self.play(impact_rings.animate.scale(1.45).set_opacity(0.0), run_time=3.0)
        self.play(attack_label.animate.set_color(GRAY_A), run_time=2.0)
        self.play(attack_label.animate.set_color(RED), run_time=2.0)
        self.wait(4.0)

        # =========================================================================
        # PHASE 5: TRANSITION TO FOUNDATION WORLD MODELS (135.0s - 180.0s)
        # =========================================================================
        defense_particles.clear_updaters()
        self.play(
            FadeOut(safety_group),
            FadeOut(attacks),
            FadeOut(shards),
            FadeOut(attack_label),
            FadeOut(title),
            run_time=1.5,
        )

        learned_env_text = make_text_block(
            [
                "Bước đi tất yếu:",
                "Dịch chuyển từ Engine nhân tạo sang Môi trường tự học được",
                "(Learned Simulators)",
            ],
            colors=[GOLD, WHITE, GRAY_A],
            scale=0.58,
            buff=0.18,
            aligned_edge=ORIGIN,
        )
        self.play(FadeIn(learned_env_text, shift=UP * 0.16), run_time=2.2)
        self.play(learned_env_text[0].animate.scale(1.06), run_time=2.0)
        self.play(learned_env_text[1].animate.set_color(BLUE_C), run_time=3.0)
        self.play(learned_env_text[2].animate.set_color(GOLD), run_time=2.0)
        self.play(learned_env_text.animate.shift(UP * 0.06), rate_func=there_and_back, run_time=3.0)
        self.wait(2.0)

        ch2_title = Tex(r"\text{\textbf{02. Foundation World Models}}", color=GOLD).scale(1.25)
        ch2_title.set_z_index(2)
        title_glow = ch2_title.copy()
        title_glow.set_fill(opacity=0.0)
        title_glow.set_stroke(color=GOLD, width=8.0, opacity=0.22)
        title_glow.set_z_index(1)
        self.play(
            ReplacementTransform(learned_env_text, ch2_title),
            FadeIn(title_glow, scale=1.05),
            self.camera.frame.animate.scale(0.88),
            run_time=2.8,
            rate_func=smooth,
        )
        title_sparks = VGroup()
        for index in range(18):
            spark = Dot(radius=0.025, color=GOLD if index % 2 == 0 else ORANGE, fill_opacity=0.72)
            spark.phase = index / 18
            title_sparks.add(spark)

        def update_title_sparks(group, dt):
            for index, spark in enumerate(group):
                spark.phase = (spark.phase + dt * (0.045 + 0.006 * (index % 4))) % 1.0
                angle = TAU * spark.phase
                spark.move_to(
                    ch2_title.get_center()
                    + RIGHT * np.cos(angle) * (3.35 + 0.10 * np.sin(self.time + index))
                    + UP * np.sin(angle) * 0.70
                )
                spark.set_opacity(0.22 + 0.60 * (0.5 + 0.5 * np.sin(self.time * 2.4 + index)))

        title_sparks.add_updater(update_title_sparks)
        self.add(title_sparks)
        self.play(title_glow.animate.set_stroke(width=10.0, opacity=0.32), run_time=4.0)
        self.play(title_glow.animate.set_stroke(width=7.0, opacity=0.18), run_time=4.0)
        self.play(ch2_title.animate.scale(1.025), run_time=4.0)
        self.play(ch2_title.animate.scale(1 / 1.025), run_time=4.0)
        self.wait(5.0)
        self.play(title_glow.animate.set_stroke(width=9.0, opacity=0.28), rate_func=there_and_back, run_time=4.0)
        title_sparks.clear_updaters()
        self.play(
            self.camera.frame.animate.scale(1 / 0.88),
            FadeOut(title_sparks),
            FadeOut(title_glow),
            FadeOut(ch2_title),
            run_time=1.5,
        )
