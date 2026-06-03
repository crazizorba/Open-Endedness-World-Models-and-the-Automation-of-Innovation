# VAI TRÒ

Bạn là:

* Chuyên gia Manim
* Motion Designer giáo dục
* Chuyên gia truyền thông khoa học
* Nhà nghiên cứu AI
* Đạo diễn video phong cách 3Blue1Brown
* Technical Director của dự án

Nhiệm vụ của bạn KHÔNG phải viết code Manim.

Nhiệm vụ của bạn là tạo ra một tài liệu:

# dos/04_Animation_Production_Plan.md

đủ chi tiết để sau đó có thể triển khai:

scenes/part_1_open_endedness/open_endedness.py

---

# BỐI CẢNH DỰ ÁN

Tôi đang xây dựng một video Manim phong cách 3Blue1Brown dựa trên Invited Talk:

"Open-Endedness, World Models, and the Automation of Innovation"

của Tim Rocktäschel tại ICLR 2025.

Phạm vi video:

* Bắt đầu từ đầu bài talk.
* Kết thúc NGAY TRƯỚC phần:

"02 Foundation World Models"

KHÔNG được đưa nội dung của Foundation World Models vào video này.

---

# CẤU TRÚC DỰ ÁN

Open-Endedness-World-Models-and-the-Automation-of-Innovation/

├── manim.cfg
├── README.md

└── scenes/
├── part_1_open_endedness/
│   ├── open_endedness.py
│   └── assets/
│
├── part_2_world_models/
│   ├── Genie.py
│   └── assets/
│
└── part_3_automation/

Toàn bộ code của phần Open-Endedness sẽ được triển khai trong:

scenes/part_1_open_endedness/open_endedness.py

---

# TÀI LIỆU ĐẦU VÀO

Tôi sẽ cung cấp:

1. link.md
2. 01_Coverage_Matrix.md
3. 02_Storyboard.md
4. 03_Voiceover_Script.md
5. Genie.py

Trong đó:

* Coverage Matrix là nguồn sự thật chính.
* Voice-over Script là nguồn sự thật về timeline.
* Storyboard là nguồn sự thật về visualization.

Nếu có mâu thuẫn:

Coverage Matrix
 >
 Voice-over Script
 > 
Storyboard

---

# VAI TRÒ CỦA FILE link.md

File link.md chứa các liên kết liên quan đến:

* ICLR Invited Talk
* Video talk
* Blog ICLR
* Paper
* Workshop
* Các nguồn học thuật liên quan

Yêu cầu:

KHÔNG chỉ dựa vào các file Markdown được tạo trước đó.

Hãy sử dụng link.md như nguồn kiểm chứng học thuật.

Khi phát hiện:

* Coverage Matrix thiếu ý quan trọng
* Storyboard diễn giải sai
* Voice-over diễn giải vượt quá nội dung talk

hãy ghi chú rõ trong báo cáo.

Không được tự động sửa nội dung.

Chỉ được đánh dấu:

* Potential Issue
* Possible Drift
* Needs Verification

---

# PHÂN TÍCH GENIE.PY

Trước khi lập kế hoạch animation:

Hãy phân tích Genie.py để rút ra:

## Scene Architecture

* Cách chia Scene
* Cách đặt tên Scene

## Base Classes

* Scene
* MovingCameraScene

## Helper Functions

* Triết lý thiết kế helper

## Timeline Design

* Cách chia timeline
* Cách đồng bộ voice-over

## Camera Strategy

* Zoom
* Pan
* Focus Shift
* Tracking

## Visual Language

* Color palette
* Typography
* Layout
* Label system

## Animation Style

* Pacing
* Complexity
* Educational emphasis

KHÔNG sao chép nội dung.

KHÔNG sao chép animation.

Chỉ kế thừa phong cách triển khai.

Mục tiêu:

open_endedness.py và Genie.py phải tạo cảm giác là cùng một dự án.

---

# MỤC TIÊU CỦA ANIMATION PRODUCTION PLAN

Animation Production Plan phải trả lời được:

1. Animation nào xuất hiện ở thời điểm nào.
2. Animation nào đang giải thích ý tưởng nào.
3. Voice-over nào tương ứng với animation nào.
4. Scene nào cần camera movement.
5. Asset nào cần chuẩn bị.
6. Helper function nào nên được xây dựng.
7. Kiến trúc open_endedness.py nên được tổ chức như thế nào.

Sau khi đọc tài liệu này:

Một lập trình viên Manim phải có thể bắt đầu triển khai code mà không phải tự thiết kế lại visualization từ đầu.

---

# OUTPUT FORMAT

Tạo Animation Production Plan theo từng Scene.

---

# ĐỐI VỚI MỖI SCENE

## Scene Overview

* Scene ID
* Scene Name
* Narrative Role
* Learning Objective
* Main Message
* Estimated Duration
* Suggested Manim Class Name

---

## Class Design Recommendation

Đề xuất:

* Scene
  hoặc
* MovingCameraScene

Giải thích lý do lựa chọn.

---

## Voice Synchronization Summary

Tóm tắt:

* đoạn narration tương ứng
* thời lượng
* ý chính

---

## Camera Strategy

Mô tả:

* Static
* Pan
* Zoom In
* Zoom Out
* Focus Shift
* Follow Object

Giải thích giá trị sư phạm.

---

## Misconceptions To Avoid

Liệt kê:

* hiểu lầm phổ biến
* hiểu lầm có thể do animation gây ra
* hiểu lầm học thuật

---

## Scene Dependency

### Reused Objects

### Destroyed Objects

### Transformed Objects

### Newly Created Objects

---

# ANIMATION TIMELINE

Chia Scene thành các block khoảng:

5–20 giây

Định dạng:

## Time Range

### Voice Summary

### Animation Description

### Objects

### Motion

### Transformations

### Pedagogical Purpose

### Key Visual Focus

---

# VISUALIZATION REVIEW

Đối với các concept:

* Open-Endedness
* Closed Systems
* Lisa Simpson's Petri Dish
* Innovation
* Exploration
* NetHack
* Objective Design
* Stepping Stones
* XLand
* Goldilocks Zone

Hãy trình bày:

## Visualization Goal

## Why It Works

## Potential Misinterpretations

## Safeguards

---

# ACADEMIC FIDELITY REVIEW

Đối với mọi visualization quan trọng:

Phân loại:

* Directly From The Talk
* Derived From The Talk
* Additional Educational Analogy

Nếu là:

Additional Educational Analogy

phải giải thích:

* tại sao cần thêm
* giúp người xem hiểu gì
* không phải nội dung gốc của Tim Rocktäschel

---

# VISUAL ASSET PLANNING

Đối với từng Scene:

## Text Objects

## Labels

## Captions

## Math Objects

Đánh dấu:

* Required
* Optional

## Shapes

## Graphs

## Icons

## Images

Phân loại:

* Draw In Manim
* External Asset

## Sound Effects

* Optional
* Recommended
* Critical

---

# REUSABLE COMPONENTS

## Helper Functions

Liệt kê:

* Tên hàm
* Trách nhiệm

## Custom Mobjects

Liệt kê:

* Tên class
* Vai trò

## Common Animation Patterns

## Common Color Scheme

Đề xuất màu sắc nhất quán cho:

* Open-Endedness
* Closed Systems
* Exploration
* Innovation
* NetHack
* XLand
* Goldilocks Zone

Phải tương thích với Genie.py.

---

# IMPLEMENTATION FEASIBILITY

Đối với mỗi Scene:

## Complexity

* Easy
* Medium
* Hard

## Estimated Coding Effort

## Estimated Render Cost

## Potential Bottlenecks

## Simplified Alternative

Ưu tiên:

Educational Clarity > Visual Spectacle

---

# KIẾN TRÚC OPEN_ENDEDNESS.PY

Sau khi hoàn thành Production Plan:

Hãy đề xuất kiến trúc tổng thể của:

open_endedness.py

KHÔNG viết code.

Chỉ mô tả.

Bao gồm:

## Global Configuration

* Fonts
* Colors
* Constants
* TexTemplate

## Base Scene Classes

Ví dụ:

* VietnameseScene
* VietnameseMovingCameraScene

## Reusable Helper Functions

## Custom Mobjects

## Scene Class Hierarchy

## Suggested Render Order

## Asset Organization Strategy

---

# FINAL REVIEW

Tạo bảng:

| Scene | Duration | Complexity | Camera Type | Major Assets |

Sau đó kiểm tra:

1. Mọi concept trong Coverage Matrix đã có visualization chưa.
2. Mọi narration trong Voice-over Script đã có animation tương ứng chưa.
3. Có concept nào còn mơ hồ không.
4. Có asset nào còn thiếu không.
5. Có scene nào khó triển khai bằng Manim không.
6. Có scene nào có nguy cơ làm sai lệch nội dung học thuật không.

Không kết thúc cho đến khi mọi concept quan trọng đều được đánh dấu:

COVERED.
