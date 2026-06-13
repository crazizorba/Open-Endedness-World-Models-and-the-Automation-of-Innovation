from manim import *
import numpy as np
import os


# ============================================================
# XeLaTeX template — bắt buộc để render tiếng Việt
# ============================================================
my_template = TexTemplate(tex_compiler="xelatex", output_format=".xdv")
my_template.add_to_preamble(r"\usepackage{xcolor}")
my_template.add_to_preamble(r"\usepackage{amsmath}")
config.tex_template = my_template


class VietnameseScene(Scene):
    def setup(self):
        config.tex_template = my_template
        super().setup()


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


ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")

# Vùng đáy frame dành cho phụ đề — tránh đặt chú thích sát mép dưới
SUBTITLE_ZONE = 1.35

# (class_name, numbered_output_stem) — khớp Genie2_NARRATION_SCRIPT.md
SCENES = [
    ("Genie2Intro", "01_Genie2Intro"),
    ("ArchitectureOverview", "02_ArchitectureOverview"),
    ("AutoencoderDeep", "03_AutoencoderDeep"),
    ("TransformerDynamics", "04_TransformerDynamics"),
    ("InferenceLoop", "05_InferenceLoop"),
    ("EmergentCapabilities", "06_EmergentCapabilities"),
    ("ComparisonAndSignificance", "07_ComparisonAndSignificance"),
]

QUALITY_DIRS = {
    "ql": "480p15",
    "qm": "720p30",
    "qh": "1080p60",
    "qk": "2160p60",
}


def add_scene_audio(scene, wav_name):
    """Gắn file .wav nếu có trong assets/audio/ (đồng bộ style Genie.py)."""
    path = os.path.join(AUDIO_DIR, wav_name)
    if os.path.exists(path):
        scene.add_sound(path)


def find_scene_video(class_name, quality_flag="ql"):
    """Tìm .mp4 đã render — Manim CE có thể lưu phẳng hoặc theo thư mục quality."""
    quality_dir = QUALITY_DIRS.get(quality_flag, quality_flag)
    repo_root = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
    candidates = [
        os.path.join(repo_root, "media", "videos", "Genie2", quality_dir, f"{class_name}.mp4"),
        os.path.join(repo_root, "media", "videos", class_name, quality_dir, f"{class_name}.mp4"),
        os.path.join(repo_root, "media", "videos", f"{class_name}.mp4"),
        os.path.join(ASSETS_DIR, "videos", "Genie2", quality_dir, f"{class_name}.mp4"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    return None


def copy_rendered_videos(quality_flag="ql"):
    """Copy .mp4 từ thư mục render Manim sang assets/ với tên đánh số."""
    import shutil

    os.makedirs(ASSETS_DIR, exist_ok=True)

    for class_name, file_stem in SCENES:
        src = find_scene_video(class_name, quality_flag)
        dst = os.path.join(ASSETS_DIR, f"{file_stem}.mp4")
        if src:
            shutil.copy2(src, dst)
            print(f"Copied -> {dst}")
        else:
            print(f"Warning: missing render for {class_name} (quality={quality_flag})")


# ============================================================
# SCENE 1 — Genie2Intro
# Thời lượng: ~45s
# ============================================================
class Genie2Intro(VietnameseScene):
    def construct(self):
        add_scene_audio(self, "01_Genie2Intro.wav")

        title_main = Tex(
            r"\text{\textbf{Genie 2}}",
            color=BLUE_C
        ).scale(1.6).to_edge(UP, buff=0.8)

        subtitle_main = Tex(
            r"\text{Foundation World Model}",
            color=GRAY_A
        ).scale(0.85).next_to(title_main, DOWN, buff=0.3)

        self.wait(2.0)
        self.play(Write(title_main), run_time=1.5)
        self.wait(1.0)
        self.play(FadeIn(subtitle_main, shift=UP * 0.15), run_time=1.0)
        self.wait(3.5)

        question = Tex(
            r"\text{Genie 1 vẫn còn \textbf{hai giới hạn} lớn:}",
            color=WHITE
        ).scale(0.82).shift(UP * 0.6)

        limit1_box = RoundedRectangle(
            width=5.4, height=1.1, corner_radius=0.1,
            color=RED_C, fill_color=DARK_GRAY, fill_opacity=0.15
        ).shift(LEFT * 3.0 + DOWN * 0.6)
        limit1_label = Tex(
            r"\text{Chỉ sinh được môi trường \textbf{2D} (256x256)}",
            color=RED_C
        ).scale(0.72)
        fit_in_box(limit1_label, limit1_box)

        limit2_box = RoundedRectangle(
            width=5.4, height=1.1, corner_radius=0.1,
            color=RED_C, fill_color=DARK_GRAY, fill_opacity=0.15
        ).shift(RIGHT * 3.0 + DOWN * 0.6)
        limit2_label = Tex(
            r"\text{Nhất quán thời gian \textbf{rất ngắn}}",
            color=RED_C
        ).scale(0.72)
        fit_in_box(limit2_label, limit2_box)

        cross1 = Cross(limit1_box, stroke_color=RED, stroke_width=5)
        cross2 = Cross(limit2_box, stroke_color=RED, stroke_width=5)

        self.play(Write(question), run_time=1.2)
        self.wait(2.0)
        self.play(Create(limit1_box), Write(limit1_label), run_time=1.2)
        self.wait(4.0)
        self.play(Create(cross1), run_time=0.8)
        self.wait(1.5)
        self.play(Create(limit2_box), Write(limit2_label), run_time=1.2)
        self.wait(4.0)
        self.play(Create(cross2), run_time=0.8)
        self.wait(3.0)

        self.play(
            FadeOut(question),
            FadeOut(limit1_box), FadeOut(limit1_label), FadeOut(cross1),
            FadeOut(limit2_box), FadeOut(limit2_label), FadeOut(cross2),
            run_time=1.0
        )
        self.wait(1.5)

        solution_box = RoundedRectangle(
            width=9.5, height=1.3, corner_radius=0.12,
            color=GREEN_C, fill_color=GREEN_E, fill_opacity=0.18
        ).shift(DOWN * 0.1)
        solution_label = Tex(
            r"\text{Genie 2: \textbf{3D đầy đủ} + \textbf{Tương tác} + \textbf{Nhất quán lâu hơn}}",
            color=GREEN_C
        ).scale(0.82)
        fit_in_box(solution_label, solution_box)

        detail = Tex(
            r"\text{Chỉ từ \textbf{một ảnh đầu vào}, mô hình sinh ra vô số môi trường có thể điều khiển.}",
            color=GRAY_A
        ).scale(0.72).next_to(solution_box, DOWN, buff=0.4)

        self.play(Create(solution_box), Write(solution_label), run_time=1.5)
        self.wait(2.0)
        self.play(Write(detail), run_time=1.2)
        self.wait(10.0)


# ============================================================
# SCENE 2 — ArchitectureOverview
# FIX: Layout pipeline nằm gọn trong màn hình, không bị cut off
# Thời lượng: ~80s
# ============================================================
class ArchitectureOverview(VietnameseScene):
    def construct(self):
        add_scene_audio(self, "02_ArchitectureOverview.wav")

        title = Tex(
            r"\text{\textbf{Kiến trúc tổng quan --- Genie 2}}",
            color=WHITE
        ).scale(1.1).to_edge(UP, buff=0.8)

        self.wait(3.0)
        self.play(Write(title), run_time=1.5)

        # Pipeline đẩy lên để dành vùng phụ đề ở đáy frame
        y_row = UP * 0.95
        y_action = DOWN * 0.95
        y_dyn = UP * 0.25

        raw_box = RoundedRectangle(
            width=2.0, height=0.95, corner_radius=0.1,
            color=BLUE_C, fill_color=BLUE_E, fill_opacity=0.18
        ).move_to(LEFT * 5.6 + y_row)
        raw_label = Tex(r"\text{Video}\\\text{Frames}", color=BLUE_C).scale(0.62)
        fit_in_box(raw_label, raw_box)

        ae_box = RoundedRectangle(
            width=2.4, height=0.95, corner_radius=0.1,
            color=BLUE_C, fill_color=BLUE_E, fill_opacity=0.18
        ).move_to(LEFT * 3.2 + y_row)
        ae_label = Tex(r"\text{\textbf{Autoencoder}}", color=BLUE_C).scale(0.68)
        fit_in_box(ae_label, ae_box)

        latent_box = RoundedRectangle(
            width=2.0, height=0.95, corner_radius=0.1,
            color=GOLD, fill_color=GOLD_E, fill_opacity=0.22
        ).move_to(LEFT * 0.9 + y_row)
        latent_label = Tex(r"\text{\textbf{Latent}} $z_t$", color=GOLD).scale(0.68)
        fit_in_box(latent_label, latent_box)

        dyn_box = RoundedRectangle(
            width=2.5, height=1.55, corner_radius=0.12,
            color=GREEN_C, fill_color=GREEN_E, fill_opacity=0.18
        ).move_to(RIGHT * 2.0 + y_dyn)
        dyn_label = Tex(
            r"\text{\textbf{Transformer}}\\[3pt]\text{\textbf{Dynamics}}",
            color=GREEN_C
        ).scale(0.65)
        fit_in_box(dyn_label, dyn_box)

        action_box = RoundedRectangle(
            width=2.0, height=0.95, corner_radius=0.1,
            color=ORANGE, fill_color=DARK_GRAY, fill_opacity=0.15
        ).move_to(LEFT * 0.9 + y_action)
        action_label = Tex(r"\text{\textbf{Action}} $a_t$", color=ORANGE).scale(0.68)
        fit_in_box(action_label, action_box)

        pred_box = RoundedRectangle(
            width=2.0, height=0.95, corner_radius=0.1,
            color=GOLD, fill_color=GOLD_E, fill_opacity=0.18
        ).move_to(RIGHT * 5.0 + y_row)
        pred_label = MathTex(r"\hat{z}_{t+1}", color=GOLD).scale(0.85)
        fit_in_box(pred_label, pred_box)

        dec_box = RoundedRectangle(
            width=2.0, height=0.95, corner_radius=0.1,
            color=BLUE_C, fill_color=BLUE_E, fill_opacity=0.18
        ).move_to(RIGHT * 5.0 + DOWN * 1.0)
        dec_label = Tex(r"\text{\textbf{Decoder}}", color=BLUE_C).scale(0.68)
        fit_in_box(dec_label, dec_box)

        arrow_raw_ae = Arrow(raw_box.get_right(), ae_box.get_left(), buff=0.12, color=BLUE_C)
        arrow_ae_z = Arrow(ae_box.get_right(), latent_box.get_left(), buff=0.12, color=BLUE_C)

        arrow_z_to_dyn = Arrow(
            latent_box.get_right(), dyn_box.get_left() + UP * 0.35,
            buff=0.12, color=GOLD
        )
        arrow_a_to_dyn = Arrow(
            action_box.get_top(), dyn_box.get_left() + DOWN * 0.35,
            buff=0.12, color=ORANGE
        )
        arrow_dyn_to_pred = Arrow(
            dyn_box.get_right(), pred_box.get_left(),
            buff=0.12, color=GOLD
        )
        arrow_pred_to_dec = Arrow(
            pred_box.get_bottom(), dec_box.get_top(),
            buff=0.12, color=BLUE_C
        )
        out_label = Tex(
            r"\text{Frame } $\hat{x}_{t+1}$", color=BLUE_C
        ).scale(0.58).next_to(dec_box, RIGHT, buff=0.25)

        # Animations — nhịp chậm khớp kịch bản ~80s (bỏ chú thích đáy, dành chỗ phụ đề)
        self.wait(4.0)
        self.play(Create(raw_box), Write(raw_label), run_time=1.0)
        self.wait(2.0)
        self.play(GrowArrow(arrow_raw_ae), Create(ae_box), Write(ae_label), run_time=1.2)
        self.wait(5.0)
        self.play(GrowArrow(arrow_ae_z), Create(latent_box), Write(latent_label), run_time=1.2)
        self.wait(5.0)
        self.play(Create(action_box), Write(action_label), run_time=1.0)
        self.wait(3.0)
        self.play(Create(dyn_box), Write(dyn_label), run_time=1.2)
        self.wait(2.0)
        self.play(GrowArrow(arrow_z_to_dyn), run_time=0.9)
        self.play(GrowArrow(arrow_a_to_dyn), run_time=0.9)
        self.wait(5.0)
        self.play(GrowArrow(arrow_dyn_to_pred), Create(pred_box), Write(pred_label), run_time=1.2)
        self.wait(4.0)
        self.play(GrowArrow(arrow_pred_to_dec), Create(dec_box), Write(dec_label), Write(out_label), run_time=1.2)
        self.wait(36.0)


# ============================================================
# SCENE 3 — AutoencoderDeep
# Thời lượng: ~95s
# ============================================================
class AutoencoderDeep(VietnameseScene):
    def construct(self):
        add_scene_audio(self, "03_AutoencoderDeep.wav")

        title = Tex(
            r"\text{\textbf{Component 1: Autoencoder}}",
            color=WHITE
        ).scale(1.1).to_edge(UP, buff=0.8)

        # ── Encoder: Raw frame → Latent ─────────────────────
        raw_frame = Rectangle(
            width=2.8, height=2.0,
            stroke_color=BLUE_C, stroke_width=3,
            fill_color=BLUE_E, fill_opacity=0.22
        ).shift(LEFT * 4.5 + UP * 0.5)

        c = raw_frame.get_center()
        w, h = raw_frame.width, raw_frame.height
        grid = VGroup()
        for dx in [-w/3, 0, w/3]:
            grid.add(Line(c + [dx, -h/2, 0], c + [dx, h/2, 0], color=WHITE, stroke_width=0.6).set_opacity(0.45))
        for dy in [-h/4, 0, h/4]:
            grid.add(Line(c + [-w/2, dy, 0], c + [w/2, dy, 0], color=WHITE, stroke_width=0.6).set_opacity(0.45))

        raw_label = Tex(r"\text{Raw Frame (pixel)}", color=BLUE_C).scale(0.68).next_to(raw_frame, DOWN, buff=0.2)

        encoder_box = RoundedRectangle(
            width=2.4, height=1.1, corner_radius=0.1,
            color=BLUE_C, fill_color=BLUE_E, fill_opacity=0.18
        ).shift(UP * 0.5)
        encoder_label = Tex(r"\text{\textbf{Encoder}}", color=BLUE_C).scale(0.78)
        fit_in_box(encoder_label, encoder_box)

        arrow_raw_to_enc = Arrow(raw_frame.get_right(), encoder_box.get_left(), buff=0.1, color=BLUE_C)
        enc_arrow_label = Tex(r"\text{Encode}", color=BLUE_C).scale(0.6).next_to(arrow_raw_to_enc, UP, buff=0.1)

        latent_small = RoundedRectangle(
            width=1.6, height=1.1, corner_radius=0.08,
            color=GOLD, fill_color=GOLD_E, fill_opacity=0.3
        ).shift(RIGHT * 3.2 + UP * 0.5)
        latent_small_label = MathTex(r"z_t", color=GOLD).scale(1.0)
        fit_in_box(latent_small_label, latent_small)

        latent_desc = Tex(r"\text{Latent Frame (nhỏ gọn)}", color=GOLD).scale(0.65).next_to(latent_small, DOWN, buff=0.2)
        arrow_enc_to_z = Arrow(encoder_box.get_right(), latent_small.get_left(), buff=0.1, color=GOLD)

        key_note = Tex(
            r"\text{Transformer \textbf{không} làm việc trên pixel, chỉ trên latent frames.}",
            color=GREEN_C
        ).scale(0.7).next_to(latent_desc, DOWN, buff=0.55)

        self.wait(3.0)
        self.play(Write(title), run_time=1.5)
        self.wait(4.0)
        self.play(Create(raw_frame), FadeIn(grid), Write(raw_label), run_time=1.2)
        self.wait(5.0)
        self.play(Create(arrow_raw_to_enc), Create(encoder_box), Write(encoder_label), Write(enc_arrow_label), run_time=1.2)
        self.wait(6.0)
        self.play(Create(arrow_enc_to_z), Create(latent_small), Write(latent_small_label), Write(latent_desc), run_time=1.2)
        self.wait(5.0)
        self.play(Write(key_note), run_time=1.2)
        self.wait(12.0)

        self.play(
            FadeOut(raw_frame), FadeOut(grid), FadeOut(raw_label),
            FadeOut(arrow_raw_to_enc), FadeOut(encoder_box), FadeOut(encoder_label),
            FadeOut(enc_arrow_label), FadeOut(arrow_enc_to_z),
            FadeOut(latent_small), FadeOut(latent_small_label), FadeOut(latent_desc),
            FadeOut(key_note),
            run_time=0.8
        )

        # ── Decoder ──────────────────────────────────────────
        dec_title = Tex(r"\text{\textbf{Component 2: Decoder}}", color=BLUE_C).scale(0.92).next_to(title, DOWN, buff=0.4)

        latent_in = RoundedRectangle(
            width=1.6, height=1.1, corner_radius=0.08,
            color=GOLD, fill_color=GOLD_E, fill_opacity=0.3
        ).shift(LEFT * 4.0 + DOWN * 0.2)
        latent_in_label = MathTex(r"\hat{z}_{t+1}", color=GOLD).scale(0.9)
        fit_in_box(latent_in_label, latent_in)

        decoder_box = RoundedRectangle(
            width=2.4, height=1.1, corner_radius=0.1,
            color=BLUE_C, fill_color=BLUE_E, fill_opacity=0.18
        ).shift(DOWN * 0.2)
        decoder_label = Tex(r"\text{\textbf{Decoder}}", color=BLUE_C).scale(0.78)
        fit_in_box(decoder_label, decoder_box)

        out_frame = Rectangle(
            width=2.6, height=2.0,
            stroke_color=BLUE_C, stroke_width=3,
            fill_color=BLUE_E, fill_opacity=0.22
        ).shift(RIGHT * 4.0 + DOWN * 0.2)
        out_lbl = Tex(
            r"\text{Output Frame } $\hat{x}_{t+1}$", color=BLUE_C
        ).scale(0.65).next_to(out_frame, DOWN, buff=0.2)

        arrow_lat_to_dec = Arrow(latent_in.get_right(), decoder_box.get_left(), buff=0.1, color=GOLD)
        arrow_dec_to_out = Arrow(decoder_box.get_right(), out_frame.get_left(), buff=0.1, color=BLUE_C)
        dec_arrow_lbl = Tex(r"\text{Decode}", color=BLUE_C).scale(0.6).next_to(arrow_dec_to_out, UP, buff=0.1)

        self.play(Write(dec_title), run_time=1.0)
        self.wait(4.0)
        self.play(Create(latent_in), Write(latent_in_label), run_time=1.0)
        self.wait(5.0)
        self.play(Create(arrow_lat_to_dec), Create(decoder_box), Write(decoder_label), run_time=1.2)
        self.wait(5.0)
        self.play(Create(arrow_dec_to_out), Write(dec_arrow_lbl), Create(out_frame), Write(out_lbl), run_time=1.2)
        self.wait(34.0)


# ============================================================
# SCENE 4 — TransformerDynamics
# FIX: Bỏ tex_to_color_map + inline $, thay bằng MathTex riêng
# Thời lượng: ~100s
# ============================================================
class TransformerDynamics(VietnameseScene):
    def construct(self):
        add_scene_audio(self, "04_TransformerDynamics.wav")

        title = Tex(
            r"\text{\textbf{Transformer Dynamics Model}}",
            color=WHITE
        ).scale(1.1).to_edge(UP, buff=0.8)

        # ── PHẦN A: Causal Mask ──────────────────────────────
        part_a = Tex(
            r"\text{\textbf{A. Causal Mask (Mặt nạ nhân quả)}}",
            color=GREEN_C
        ).scale(0.85).shift(UP * 2.1)

        frames = VGroup(*[
            RoundedRectangle(
                width=0.9, height=0.7, corner_radius=0.06,
                color=GOLD, fill_color=GOLD_E, fill_opacity=0.3
            ) for _ in range(5)
        ]).arrange(RIGHT, buff=0.28).shift(UP * 1.2)

        frame_labels = VGroup(*[
            MathTex(f"z_{i+1}", color=GOLD).scale(0.65).move_to(frames[i])
            for i in range(5)
        ])

        matrix = VGroup()
        for i in range(5):
            for j in range(5):
                visible = j <= i
                cell = Square(
                    0.38,
                    stroke_color=GRAY_C, stroke_width=1,
                    fill_color=WHITE if visible else GRAY_D,
                    fill_opacity=0.85 if visible else 0.25
                )
                matrix.add(cell)
        matrix.arrange_in_grid(5, 5, buff=0.04).shift(DOWN * 0.35)

        # FIX: Không dùng dấu ngoặc kép tiếng Việt trong raw string
        mask_note = Tex(
            r"\text{Tại bước } $t$\text{: chỉ nhìn } $z_1,\ldots,z_{t-1}$ \text{ --- không nhìn tương lai.}",
            color=GRAY_A
        ).scale(0.72).next_to(matrix, DOWN, buff=0.28)

        highlight_row = SurroundingRectangle(
            VGroup(*[matrix[20 + j] for j in range(5)]),
            color=GREEN_C, buff=0.05, corner_radius=0.04
        )

        self.wait(3.0)
        self.play(Write(title), run_time=1.5)
        self.wait(3.0)
        self.play(Write(part_a), run_time=1.0)
        self.wait(3.0)
        self.play(Create(frames), Write(frame_labels), run_time=1.2)
        self.wait(4.0)
        self.play(FadeIn(matrix), run_time=1.2)
        self.wait(4.0)
        self.play(Write(mask_note), run_time=1.2)
        self.wait(3.0)
        self.play(Create(highlight_row), run_time=1.0)
        self.wait(8.0)
        self.play(
            FadeOut(part_a), FadeOut(frames), FadeOut(frame_labels),
            FadeOut(matrix), FadeOut(mask_note), FadeOut(highlight_row),
            run_time=0.8
        )

# ── PHẦN B: Action Conditioning (ĐÃ CHỈNH SỬA) ──────────────────────
        part_b = Tex(
            r"\text{\textbf{B. Action Conditioning}}",
            color=ORANGE
        ).scale(0.85).shift(UP * 2.1)

        # Diagram chính - căn giữa màn hình
        z_box = RoundedRectangle(
            width=2.5, height=1.1, corner_radius=0.12,
            color=GOLD, fill_color=GOLD_E, fill_opacity=0.32
        )

        z_label = MathTex(r"z_t", color=GOLD).scale(0.95)
        fit_in_box(z_label, z_box)

        embed_box = RoundedRectangle(
            width=2.9, height=1.1, corner_radius=0.12,
            color=ORANGE, fill_color=ORANGE, fill_opacity=0.28
        ).next_to(z_box, DOWN, buff=0.45)

        embed_label = MathTex(r"\mathrm{embed}(a_t)", color=ORANGE).scale(0.78)
        fit_in_box(embed_label, embed_box)

        plus_sign = MathTex(r"+", color=WHITE).scale(1.3).move_to(
            z_box.get_bottom() + DOWN * 0.22
        )

        cond_diagram = VGroup(z_box, z_label, embed_box, embed_label, plus_sign)
        cond_diagram.move_to(ORIGIN)        # Căn giữa màn hình

        # Formula bên dưới
        formula_text = Tex(r"\text{Đầu vào Transformer:}", color=WHITE).scale(0.76)
        formula_math = MathTex(r"z_t + \mathrm{embed}(a_t)", color=WHITE).scale(0.82)
        formula_math[0][0:3].set_color(GOLD)
        formula_math[0][6:].set_color(ORANGE)

        formula_group = VGroup(formula_text, formula_math).arrange(DOWN, buff=0.2)
        formula_group.next_to(cond_diagram, DOWN, buff=0.75)

        self.play(Write(part_b), run_time=1.0)
        self.wait(3.0)
        self.play(Create(z_box), Write(z_label), run_time=1.0)
        self.wait(2.5)
        self.play(Create(embed_box), Write(embed_label), run_time=1.0)
        self.wait(2.5)
        self.play(Write(plus_sign), run_time=0.8)
        self.wait(3.0)
        self.play(Write(formula_group), run_time=1.3)
        self.wait(11.0)

        self.play(
            FadeOut(part_b), FadeOut(cond_diagram),
            FadeOut(formula_group),
            run_time=0.8
        )

        # ── PHẦN C: Classifier-Free Guidance ─────────────────
        part_c = Tex(
            r"\text{\textbf{C. Classifier-Free Guidance (CFG)}}",
            color=GOLD
        ).scale(0.85).shift(UP * 2.1)

        no_action_box = RoundedRectangle(
            width=3.4, height=1.1, corner_radius=0.1,
            color=GRAY_B, fill_color=DARK_GRAY, fill_opacity=0.2
        ).shift(LEFT * 3.2 + DOWN * 0.05)
        no_action_label = Tex(r"\text{Dự đoán không điều kiện}", color=GRAY_B).scale(0.68)
        fit_in_box(no_action_label, no_action_box)

        with_action_box = RoundedRectangle(
            width=3.4, height=1.1, corner_radius=0.1,
            color=ORANGE, fill_color=DARK_GRAY, fill_opacity=0.18
        ).shift(RIGHT * 3.2 + DOWN * 0.05)
        with_action_label = Tex(r"\text{Dự đoán có điều kiện (action)}", color=ORANGE).scale(0.65)
        fit_in_box(with_action_label, with_action_box)

        cfg_arrow = Arrow(
            no_action_box.get_right(), with_action_box.get_left(),
            buff=0.15, color=GOLD, stroke_width=4
        )
        cfg_label = Tex(
            r"\text{Đẩy mạnh hướng có action}", color=GOLD
        ).scale(0.62).next_to(cfg_arrow, UP, buff=0.45)

        self.play(Write(part_c), run_time=1.0)
        self.wait(4.0)
        self.play(Create(no_action_box), Write(no_action_label), run_time=1.0)
        self.wait(5.0)
        self.play(
            Create(cfg_arrow), Write(cfg_label),
            Create(with_action_box), Write(with_action_label),
            run_time=1.2
        )
        self.wait(18.0)


# ============================================================
# SCENE 5 — InferenceLoop
# ============================================================
class InferenceLoop(VietnameseScene):
    def construct(self):
        add_scene_audio(self, "05_InferenceLoop.wav")

        title = Tex(
            r"\text{\textbf{Inference: Sinh video có thể điều khiển}}",
            color=WHITE
        ).scale(1.05).to_edge(UP, buff=0.65)

        step_data = [
            (r"\text{1. Ảnh đầu vào } $x_1$",                     BLUE_C),
            (r"\text{2. Encoder } $\rightarrow z_1$",              BLUE_C),
            (r"\text{3. Hành động } $a_t$ \text{ (bàn phím/chuột)}", ORANGE),
            (r"\text{4. Dynamics + Diffusion } $\rightarrow \hat{z}_{t+1}$", GREEN_C),
            (r"\text{5. Decoder } $\rightarrow \hat{x}_{t+1}$",   BLUE_C),
        ]

        step_boxes = VGroup()
        for text, color in step_data:
            box = RoundedRectangle(
                width=5.45, 
                height=0.84, 
                corner_radius=0.1,
                color=color, 
                fill_color=DARK_GRAY, 
                fill_opacity=0.16
            )
            label = Tex(text, color=color).scale(0.71)
            fit_in_box(label, box)
            step_boxes.add(VGroup(box, label))

        # Dịch xuống thấp hơn để tránh đè tiêu đề
        step_boxes.arrange(DOWN, buff=0.33).shift(LEFT * 3.7 + DOWN * 0.1)

        # Vùng Latent Diffusion bên phải
        panel_title = Tex(
            r"\text{\textbf{Latent Diffusion}}", color=GREEN_C
        ).scale(0.82).move_to([4.7, 1.55, 0])

        noisy_square = Square(
            1.45, 
            fill_color=GRAY, 
            fill_opacity=0.38,
            stroke_color=GRAY_B, 
            stroke_width=2.5
        ).move_to([4.7, 0.1, 0])

        noise_label = Tex(r"\text{Noisy latent}", color=GRAY_A).scale(0.65).next_to(noisy_square, DOWN, buff=0.25)

        self.wait(4.0)
        self.play(Write(title), run_time=1.4)
        self.wait(3.0)

        self.play(FadeIn(step_boxes[0], shift=UP * 0.12), run_time=0.9)
        step_waits = [3.8, 3.2, 3.5, 3.8, 4.0]

        for i in range(1, 5):
            self.play(
                FadeIn(step_boxes[i], shift=UP * 0.12),
                run_time=0.85
            )
            self.wait(step_waits[i - 1])

        self.wait(2.5)
        self.play(Write(panel_title), run_time=0.9)
        self.play(Create(noisy_square), Write(noise_label), run_time=1.1)

        for k in range(6):
            self.play(
                noisy_square.animate.set_fill(
                    interpolate_color(GRAY, GOLD_E, k / 5),
                    opacity=0.38 + k * 0.07
                ),
                run_time=0.32
            )

        self.wait(32.0)


# ============================================================
# SCENE 6 — EmergentCapabilities
# FIX: Tách physics_list ra phải rõ ràng, không đè lên path/ball
# Thời lượng: ~80s
# ============================================================
class EmergentCapabilities(VietnameseScene):
    def construct(self):
        add_scene_audio(self, "06_EmergentCapabilities.wav")

        title = Tex(
            r"\text{\textbf{Emergent Capabilities --- Khả năng nổi sinh}}",
            color=WHITE
        ).scale(1.1).to_edge(UP, buff=0.8)

        self.wait(2.0)
        self.play(Write(title), run_time=1.5)

        # ── PHẦN A: Vật lý ───────────────────────────────────
        part_a = Tex(
            r"\text{\textbf{A. Vật lý thực tế --- Physics Simulation}}",
            color=BLUE_C
        ).scale(0.85).shift(UP * 1.9)

        # Đường parabol mượt mà, không có ground line
        path = ParametricFunction(
            lambda t: np.array([
                -6.2 + 4.4 * t,                    # Bắt đầu từ trái
                -1.8 + 2.2 * (1 - t) + 1.9 * t * (1 - t),  # Cao độ rơi tự nhiên
                0,
            ]),
            t_range=[0, 1], 
            color=GRAY_B,
            stroke_width=2.8
        )
        
        ball = Circle(0.22, color=BLUE_C, fill_color=BLUE_C, fill_opacity=0.92).move_to(path.get_start())

        # Danh sách vật lý căn phải, thoáng và cân đối
        physics_list = VGroup(
            Tex(r"\text{Nước và khói: chảy theo quy luật}", color=GRAY_A).scale(0.68),
            Tex(r"\text{Trọng lực: vật rơi, nhân vật nhảy}", color=GRAY_A).scale(0.68),
            Tex(r"\text{Ánh sáng: bóng đổ, phản chiếu}", color=GRAY_A).scale(0.68),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).shift(RIGHT * 3.8 + DOWN * 0.1)

        part_a_group = VGroup(part_a, path, ball, physics_list)

        self.wait(4.0)
        self.play(Write(part_a), run_time=1.0)
        self.wait(3.0)
        self.play(Create(path), run_time=1.1)
        self.play(MoveAlongPath(ball, path), run_time=1.65, rate_func=linear)
        self.wait(2.5)
        self.play(FadeIn(physics_list, shift=LEFT * 0.2), run_time=1.0)
        self.wait(8.0)
        self.play(FadeOut(part_a_group), run_time=0.8)

        # ── PHẦN B: Object Permanence ─────────────────────────
        part_b = Tex(
            r"\text{\textbf{B. Object Permanence --- Tính bền vững vật thể}}",
            color=GOLD
        ).scale(0.85).shift(UP * 1.9)

        camera_rect = Rectangle(
            width=4.5, height=2.4,
            stroke_color=WHITE, stroke_width=3
        ).shift(UP * 0.1)
        camera_lbl = Tex(r"\text{Góc nhìn camera}", color=GRAY_A).scale(0.62).next_to(camera_rect, UP, buff=0.12)

        obj_circle = Circle(
            0.32, color=YELLOW, fill_color=YELLOW, fill_opacity=0.9
        ).move_to(camera_rect.get_center() + LEFT * 0.8)

        look_away = Tex(r"\text{Camera quay mặt đi...}", color=GRAY_A).scale(0.7).shift(DOWN * 1.35)
        come_back = Tex(r"\text{Quay lại: vật thể \textbf{vẫn ở đó}!}", color=GREEN_C).scale(0.7).shift(DOWN * 1.95)
        baby_compare = Tex(
            r"\text{Trẻ dưới 8 tháng không làm được --- Genie 2 học được chỉ từ xem video.}",
            color=GRAY_A
        ).scale(0.65).shift(DOWN * 2.55)

        part_b_group = VGroup(part_b, camera_rect, camera_lbl, obj_circle, look_away, come_back, baby_compare)

        self.play(Write(part_b), run_time=1.0)
        self.wait(3.0)
        self.play(Create(camera_rect), Write(camera_lbl), FadeIn(obj_circle), run_time=1.0)
        self.wait(4.0)
        self.play(
            camera_rect.animate.shift(RIGHT * 1.5),
            obj_circle.animate.set_opacity(0.0),
            Write(look_away), run_time=1.0
        )
        self.wait(4.0)
        self.play(
            camera_rect.animate.shift(LEFT * 1.5),
            obj_circle.animate.set_opacity(1.0),
            Write(come_back), run_time=1.0
        )
        self.wait(3.0)
        self.play(Write(baby_compare), run_time=1.0)
        self.wait(6.0)
        self.play(FadeOut(part_b_group), run_time=0.8)

        # ── PHẦN C: Temporal Consistency ─────────────────────
        part_c = Tex(
            r"\text{\textbf{C. Temporal Consistency --- Nhất quán thời gian}}",
            color=GREEN_C
        ).scale(0.85).shift(UP * 1.9)

        timeline = NumberLine(
            x_range=[0, 60, 10], length=9.0,
            include_numbers=True, color=GRAY_B, font_size=22
        ).shift(UP * 0.35)
        for num in timeline.numbers:
            num.shift(DOWN * 0.06)

        g1_bar = Line(
            timeline.n2p(0), timeline.n2p(2.5),
            color=RED_C, stroke_width=10
        ).shift(UP * 0.55)
        g1_lbl = Tex(r"\text{Genie 1}", color=RED_C).scale(0.7).next_to(g1_bar, LEFT, buff=0.28)

        # SỬA TẠI ĐÂY: Thay timeline.n2p(50) thành timeline.n2p(60) để thanh dài đến hết trục số
        g2_bar = Line(
            timeline.n2p(0), timeline.n2p(60),
            color=GREEN_C, stroke_width=10
        ).shift(DOWN * 0.82)
        g2_lbl = Tex(r"\text{Genie 2}", color=GREEN_C).scale(0.7).next_to(g2_bar, LEFT, buff=0.28)
        
        # SỬA TẠI ĐÂY: Đổi vị trí dòng chữ chú thích về mốc 30 (chính giữa thanh) để bố cục cân đối hơn
        g2_note = Tex(
            r"\text{10--60 giây nhất quán}", color=GREEN_C
        ).scale(0.68).move_to(timeline.n2p(30) + UP * 0.55)

        seconds_label = Tex(r"\text{Thời gian (giây)}", color=GRAY_A).scale(0.65)
        seconds_label.next_to(timeline, DOWN, buff=1.05)

        self.play(Write(part_c), run_time=1.0)
        self.wait(3.0)
        self.play(Create(timeline), Write(seconds_label), run_time=1.2)
        self.wait(4.0)
        self.play(FadeIn(g1_lbl), Create(g1_bar), run_time=1.0)
        self.wait(4.0)
        self.play(FadeIn(g2_lbl), Create(g2_bar), Write(g2_note), run_time=1.2)
        self.wait(10.0)

# ============================================================
# SCENE 7 — ComparisonAndSignificance
# FIX: Cột bảng rộng hơn, không đè nhau
#      Open-Endedness nodes: gán label TRƯỚC arrange → ĐÚNG
# Thời lượng: ~80s
# ============================================================
class ComparisonAndSignificance(VietnameseScene):
    def construct(self):
        add_scene_audio(self, "07_ComparisonAndSignificance.wav")

        title = Tex(
            r"\text{\textbf{So sánh Genie 1 và Genie 2}}",
            color=WHITE
        ).scale(1.1).to_edge(UP, buff=0.8)

        col_x = [-5.0, -0.8, 4.2]
        row_y = [1.75, 0.65, -0.35, -1.35, -2.25]

        headers = [
            Tex(r"\text{\textbf{Tiêu chí}}", color=GOLD).scale(0.8).move_to([col_x[0], row_y[0], 0]),
            Tex(r"\text{\textbf{Genie 1 (2/2024)}}", color=GRAY_A).scale(0.8).move_to([col_x[1], row_y[0], 0]),
            Tex(r"\text{\textbf{Genie 2 (12/2024)}}", color=GREEN_C).scale(0.8).move_to([col_x[2], row_y[0], 0]),
        ]

        table_data = [
            (r"\text{Không gian}",       r"\text{2D}",                      r"\text{3D đầy đủ}"),
            (r"\text{Kiến trúc}",        r"\text{ST-Transformer+MaskGIT}",  r"\text{Autoregressive Latent Diffusion}"),
            (r"\text{Nhất quán}",        r"\text{Rất ngắn}",                 r"\text{10--60 giây}"),
            (r"\text{Object permanence}",r"\text{Không có}",                 r"\text{Có}"),
        ]

        row_mobs = VGroup()
        for r, (crit, g1, g2) in enumerate(table_data):
            y = row_y[r + 1]
            row_mobs.add(VGroup(
                Tex(crit, color=WHITE).scale(0.7).move_to([col_x[0], y, 0]),
                Tex(g1, color=GRAY_A).scale(0.62).move_to([col_x[1], y, 0]),
                Tex(g2, color=GREEN_C).scale(0.62).move_to([col_x[2], y, 0]),
            ))

        line_header = Line([-6.5, 2.15, 0], [6.5, 2.15, 0], color=GRAY_C)
        line_top    = Line([-6.5, 1.22, 0], [6.5, 1.22, 0], color=GRAY_C)
        line_bottom = Line([-6.5, -2.65, 0], [6.5, -2.65, 0], color=GRAY_C)

        self.wait(3.0)
        self.play(Write(title), run_time=1.5)
        self.wait(3.0)
        self.play(Create(line_header), Create(line_top), Create(line_bottom), run_time=1.0)
        self.play(*[Write(h) for h in headers], run_time=1.0)

        for row in row_mobs:
            self.wait(3.0)
            self.play(FadeIn(row, shift=UP * 0.08), run_time=0.9)

        self.wait(14.0)
        self.play(
            FadeOut(title),
            FadeOut(line_header), FadeOut(line_top), FadeOut(line_bottom),
            FadeOut(VGroup(*headers)), FadeOut(row_mobs),
            run_time=0.8
        )

        # ── Open-Endedness diagram ────────────────────────────
        oe_title = Tex(
            r"\text{\textbf{Ý nghĩa với Open-Endedness}}",
            color=GOLD
        ).scale(1.0).to_edge(UP, buff=0.8)

        problem = Tex(
            r"\text{\textbf{Vấn đề cũ:} phải thiết kế tay từng môi trường --- tốn kém, chậm, thiên lệch.}",
            color=GRAY_A
        ).scale(0.72).shift(UP * 2.05)

        # FIX: Tạo từng VGroup(box, label) TRƯỚC rồi arrange toàn bộ
        node_data = [
            (r"\text{Genie 2 sinh môi trường 3D từ ảnh}", BLUE_C,  BLUE_E),
            (r"\text{AI Agent luyện tập trong đó}",        GREEN_C, GREEN_E),
            (r"\text{Agent giỏi hơn, khám phá tình huống mới}", ORANGE, DARK_GRAY),
            (r"\text{Open-Endedness} $\infty$",            GOLD,   GOLD_E),
        ]

        node_groups = VGroup()
        for text, stroke_c, fill_c in node_data:
            box = RoundedRectangle(
                width=5.5, height=0.80, corner_radius=0.09,
                color=stroke_c,
                fill_color=fill_c,
                fill_opacity=0.2
            )
            lbl = Tex(text, color=stroke_c).scale(0.72)
            fit_in_box(lbl, box)
            node_groups.add(VGroup(box, lbl))

        node_groups.arrange(DOWN, buff=0.28).shift(DOWN * 0.55)

        node_arrows = VGroup(*[
            Arrow(
                node_groups[i].get_bottom(), node_groups[i + 1].get_top(),
                buff=0.06, color=GRAY_B, stroke_width=3
            ) for i in range(3)
        ])

        final = Tex(
            r"\text{Genie 2 là bước đầu tiên để \textbf{AI tự xây dựng môi trường để tự học}.}",
            color=WHITE
        ).scale(0.70).next_to(node_groups, DOWN, buff=0.45)

        self.play(Write(oe_title), run_time=1.0)
        self.wait(3.0)
        self.play(Write(problem), run_time=1.2)
        self.wait(4.0)
        self.play(Create(node_groups[0]), run_time=1.0)
        for i in range(1, 4):
            self.wait(2.5)
            self.play(
                GrowArrow(node_arrows[i - 1]),
                Create(node_groups[i]),
                run_time=1.0
            )
        self.wait(4.0)
        self.play(Write(final), run_time=1.5)
        self.wait(14.0)


if __name__ == "__main__":
    import sys
    quality = sys.argv[1] if len(sys.argv) > 1 else "ql"
    copy_rendered_videos(quality)