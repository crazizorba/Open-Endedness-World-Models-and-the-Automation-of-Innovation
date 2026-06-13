# Open-Endedness, World Models, and the Automation of Innovation
> **Dự án mô phỏng hoạt họa các khái niệm khoa học bằng thư viện Manim dựa trên bài thuyết trình tại Hội nghị ICLR 2025.**

---

## Thông tin môn học & Nhóm thực hiện

### Thành viên nhóm
| STT | Họ và tên | MSSV | Vai trò |
| :---: | :--- | :---: | :--- |
| 1 | **Mai Đình Trí** | 23120377 | Thành viên nhóm |
| 2 | **Nguyễn Đức Tiến** | 23120368 | Thành viên nhóm |
| 3 | **Trần Ngọc Diễm Thúy** | 23120367 | Thành viên nhóm |
| 4 | **Trần Đình Thi** | 23120359 | Thành viên nhóm |
| 5 | **Phạm Ngọc Duy** | 23120035 | Thành viên nhóm |

### Thông tin môn học
* **Tên môn học:** Nhập môn học máy
* **Khóa:** 2023
* **Lớp:** CQ2023/21
* **Giảng viên lý thuyết:** Lê Hoàng Thái
* **Trợ giảng / Giảng viên thực hành:** Huỳnh Lâm Hải Đăng, Nguyễn Thanh Tình

---

## Thông tin Tutorials & Nguồn tham khảo
* **Tên bài thuyết trình (Invited Talk):** Open-Endedness, World Models, and the Automation of Innovation
* **Hội nghị:** ICLR (International Conference on Learning Representations)
* **Năm:** 2025
* **Link chi tiết:** [ICLR 2025 Invited Talk](https://iclr.cc/virtual/2025/invited-talk/36780)

---

## Cấu trúc thư mục dự án

Dự án được phân chia thành các thư mục tương ứng với từng phần nội dung của bài nói chuyện:

```text
├── media/                       # Thư mục chứa video và hình ảnh được Manim kết xuất (render)
├── scenes/                      # Mã nguồn Python định nghĩa các cảnh hoạt họa (Manim)
│   ├── part_1_open_endedness/   # Phần 1: Khái niệm Open-Endedness (Hệ thống mở)
│   │   ├── assets/              # Tài nguyên hình ảnh, âm thanh đi kèm Phần 1
│   │   └── open_endedness.py    # Các cảnh của Phần 1 (SC_01 đến SC_07)
│   │
│   ├── part_2_world_models/      # Phần 2.1: World Models & Genie 1
│   │   ├── assets/              # Tài nguyên đi kèm Phần 2.1
│   │   └── Genie.py             # Các phân cảnh giới thiệu mô hình Genie 1
│   │
│   ├── part_2_genie2/           # Phần 2.2: Genie 2 (Mô hình thế giới quy mô lớn)
│   │   ├── assets/              # Tài nguyên đi kèm Phần 2.2
│   │   └── Genie2.py            # Phân cảnh kiến trúc và khả năng của Genie 2
│   │
│   └── part_3_automation/       # Phần 3: Tự động hóa sự đổi mới (Automation of Innovation)
│       ├── assets/              # Tài nguyên đi kèm Phần 3
│       ├── s1.py -> s6.py       # Từng phân cảnh chi tiết (Cảnh 1 đến 6)
│
├── manim.cfg                    # Cấu hình Manim toàn cục (Màu nền dark theme, độ phân giải...)
├── requirements.txt             # Danh sách thư viện Python cần thiết
```

---

## Hướng dẫn cài đặt & Thiết lập môi trường

Để chạy và render các cảnh hoạt họa trong dự án, bạn cần cài đặt **Python** cùng các công cụ bổ trợ hệ thống mà thư viện **Manim** yêu cầu.

### 1. Cài đặt các công cụ hệ thống (Bắt buộc)
Manim yêu cầu một số công cụ dòng lệnh để render video và xử lý LaTeX:
* **FFmpeg:** Dùng để xử lý và xuất video.
* **LaTeX (tùy chọn nhưng khuyến nghị):** Để render các công thức toán học (ví dụ: MiKTeX trên Windows hoặc TeX Live trên Linux/macOS).
* **Cairo & Pango:** Thư viện đồ họa và văn bản.

> **Mẹo cài đặt nhanh trên Windows qua Chocolatey:**
> ```powershell
> choco install ffmpeg miktex python
> ```

### 2. Thiết lập môi trường ảo và cài đặt thư viện Python
Trong thư mục gốc của dự án, thực hiện các lệnh sau:

```bash
# Tạo môi trường ảo (nếu chưa có)
python -m venv venv

# Kích hoạt môi trường ảo
# Trên Windows (Command Prompt):
call venv\Scripts\activate
# Trên Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Trên Linux/macOS:
source venv/bin/activate

# Nâng cấp pip và cài đặt dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Hướng dẫn Render các Phân cảnh (Scenes)

Sử dụng lệnh `manim` để biên dịch file Python thành video. Cú pháp cơ bản:
```bash
manim -pql <đường-dẫn-file.py> <Tên-Class-Scene>
```
*Lưu ý:* 
* `-p`: Tự động mở video sau khi render xong.
* `-q`: Chọn chất lượng render (l: low - 480p, m: medium - 720p, h: high - 1080p, k: 4k).

### Phần 1: Open-Endedness
Biên dịch các cảnh trong `scenes/part_1_open_endedness/open_endedness.py`:
```bash
# Render cảnh 1 (The Horizon of AGI)
manim -pqh scenes/part_1_open_endedness/open_endedness.py SC_01_TheHorizonOfAGI

# Render cảnh 2 (The Metaphor of the Petri Dish)
manim -pqh scenes/part_1_open_endedness/open_endedness.py SC_02_TheMetaphorOfThePetriDish

# Render cảnh 3 (Deconstructing Open Ended Systems)
manim -pqh scenes/part_1_open_endedness/open_endedness.py SC_03_DeconstructingOpenEndedSystems
```
*(Thay thế tên lớp tương ứng từ `SC_01_TheHorizonOfAGI` đến `SC_07_TheEvolutionaryEngines` để render các phần khác).*

### Phần 2: World Models & Genie 1
Biên dịch các cảnh trong `scenes/part_2_world_models/Genie.py`:
```bash
# Render phần mở đầu
manim -pqh scenes/part_2_world_models/Genie.py Section1IntroductionPart1

# Render kiến trúc tokenizer
manim -pqh scenes/part_2_world_models/Genie.py Section221VideoTokenizer

# Render mô hình Dynamics
manim -pqh scenes/part_2_world_models/Genie.py Section223DynamicsModel
```
*(Các scene khả dụng khác: `Section1IntroductionPart2`, `Section21Methodology`, `Section222LatentActionModel`, `Section3ScalingResults`, `Section4QualitativeEmergent`).*

### Phần 2.2: Genie 2
Biên dịch các cảnh trong `scenes/part_2_genie2/Genie2.py`:
```bash
# Render giới thiệu Genie 2
manim -pqh scenes/part_2_genie2/Genie2.py Genie2Intro

# Render tổng quan kiến trúc Genie 2
manim -pqh scenes/part_2_genie2/Genie2.py ArchitectureOverview

# Render chu trình suy luận (Inference Loop)
manim -pqh scenes/part_2_genie2/Genie2.py InferenceLoop
```
*(Các scene khả dụng khác: `AutoencoderDeep`, `TransformerDynamics`, `EmergentCapabilities`, `ComparisonAndSignificance`).*

### Phần 3: Automation of Innovation (Tự động hóa Đổi mới)
Mỗi phân cảnh trong phần 3 được lưu ở các file riêng biệt từ `s1.py` đến `s6.py`:
```bash
# Render Cảnh 1: Đặt vấn đề và giới thiệu
manim -pqh scenes/part_3_automation/s1.py AutomationOfInnovationSection1

# Render Cảnh 5a: Case Study về The AI Scientist
manim -pqh scenes/part_3_automation/s5a.py AutomationOfInnovationSection5a

# Render Cảnh 6: Tác động và Kết luận
manim -pqh scenes/part_3_automation/s6.py AutomationOfInnovationSection6
```
*(Tương tự đối với các file `s2.py` -> `s5.py` bằng cách chỉ định đúng tên class tương ứng như `AutomationOfInnovationSection2` -> `AutomationOfInnovationSection5`).*