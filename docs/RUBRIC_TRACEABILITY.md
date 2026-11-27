# Rubric traceability — mỗi tiêu chí trỏ về file nào, trạng thái thật

Cập nhật 28/11/2026 ~02:00 ICT. DONE = có bằng chứng · PARTIAL = có một phần · BLOCKED = cần người.

## Điều kiện cứng (Phần 0)
| # | Điều kiện | Bằng chứng | Trạng thái |
|---|---|---|---|
| 1 | Bản chạy thử gọi AI thật ở quyết định trung tâm | `codebase/ai.py` (Gemini), `eval/run-1.csv`, `eval/run-2.csv`: model `gemini-3.1-flash-lite`, token > 0 mọi câu | DONE |
| 2 | Bằng chứng pain ≥1 nguồn đạt ngưỡng | `evidence/data-mining.md`: x/N = 8/125, cách đếm chốt trước (commit `79b647b`), script, 6 ví dụ | PARTIAL: đạt về cách làm theo R1; chưa có người đọc tay (H7). Giám khảo có thể đánh giá khác |
| 3 | ≥20 câu thử + % đạt | 30 câu; % đạt: 28/30 → 29/30 | PARTIAL: % hiện là chấm sơ bộ của agent; cần người chép cột `pass` vào `eval/run-N.csv` (H6) |
| 4 | `demo-slides.pdf` ở gốc | `demo-slides.pdf` (8 trang) | DONE khi file được commit |

## Phần 2
| Khối | Tiêu chí | Bằng chứng | Trạng thái |
|---|---|---|---|
| R1 (14) | Đạt ngưỡng ≥1 nguồn | `evidence/data-mining.md`, `evidence/mine_stackexchange.py`, `evidence/mining_labels.csv` | PARTIAL |
| | ≥5 trích dẫn nguyên văn | `evidence/summary.md` mục 3 (6 trích) | DONE |
| | Nguồn thứ hai kiểm lại | Miyakawa 2017 là tài liệu tham khảo, không phải nguồn của nhóm; chưa phỏng vấn | NOT_STARTED (H8) |
| R2 (11) | Pain + bảng ≥3 hướng, hướng loại giữ lại | `spec.md` §1–§2 (4 hướng) | DONE (số trong bảng là tự ước tính, không lấy từ R1) |
| | Công thức impact ra một số, thừa số có nguồn hoặc *(tự ước tính)* | `spec.md` §2: 5.000 × 1,5 × 20 = 150.000 phút | DONE (toàn tự ước tính) |
| R3 (16) | Thiết kế §4: lát cắt, ≥3 không làm, sơ đồ + hình dạng + lý do, bảng công cụ, mức tự động, người duyệt, chặn rủi ro, ≥3 nguyên tắc (G10) | `spec.md` §4 | DONE |
| | Bản chạy thử: AI thật, khớp sơ đồ, "không có" khi ngoài dữ liệu, chặn rủi ro, README chạy được, phần giả ghi rõ | `codebase/`, `README.md` | DONE (B22 cho thấy "không có căn cứ" chưa luôn đúng) |
| R4 (14) | 20–30 câu, đủ cột, ≥5 kho, ≥2 tu_choi + 2 tấn công, ≥1/3 nguồn thật | `eval/benchmark.csv`: 30 câu, 15 kho, 5 tu_choi, 3 tấn công, 15/30 nguồn thật | DONE |
| | metric_spec ≥3 metric · người thứ hai chấm 5 output khớp ≥4/5 · chuẩn §7 commit trước 19:30 | `eval/metric_spec.yaml` (7 metric) · `eval/grading/GRADING_SHEET.md` · commit `98024ba` push 19:25 | PARTIAL: chưa có 2 người chấm (H5) |
| | Data card + chạy một lệnh ra run-N có run ID, model, token | `data/DATA_CARD.md`, `eval/run-1.csv` | DONE |
| R5 (8) | Lượt 1 từng câu + %, ≥3 lỗi có input/output/vì sao, gom nhóm có tên | `eval/report.md` mục 2 (3 nhóm, B30, B12, B22 + nhóm C) | DONE (số chờ người duyệt) |
| | Một cải tiến nhắm nhóm lỗi đau nhất + lượt 2 cùng bộ, % 1→2 · `eval/README.md` một trang | `eval/report.md` mục 3–4, `eval/README.md` | DONE |
| R6 (12) | ≥3 persona, nguồn hoặc tự ước tính · simulate ≥50 phiên, seed, chạy thật | `cost/personas.yaml`, `cost/simulate-1.csv` | xem `cost/cost-estimate.md` |
| | Chi phí/task thành công theo tỉ lệ lượt 2 cùng model · 3 kịch bản · ≥2 model có link + ngày · so với impact | `cost/cost-estimate.md`, `spec.md` §8 | xem `cost/cost-estimate.md` |
| R7 (10) | Slide 8 trang, mỗi trang có số/nguồn | `demo-slides.pdf`, `slides/outline.md` | DONE |
| | Demo trực tiếp + câu lạ + video dự phòng | `docs/VIDEO_SCRIPT.md` | BLOCKED (video: H9) |
| | Ai cũng trả lời được | `slides/outline.md` (ai nói trang nào) | Cần nhóm tập |
| Bonus | ≥2 người dùng thử | `validation/SCRIPT.md`, `validation/log.md` trống | BLOCKED (H10) |
