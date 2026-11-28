# Gói nộp CP3 — 10:00 Thứ Bảy 28/11/2026

Đối chiếu README BTC mục CP3 + guide 3.4 + rubric. Trạng thái tính đến commit hiện tại của nhánh `LufkyMama` (xem `git log -1`).

| # | Yêu cầu BTC (nguyên văn rút gọn) | Bằng chứng | Trạng thái |
|---|---|---|---|
| 1 | Bằng chứng pain đạt ngưỡng ≥1 nguồn + ≥5 trích dẫn; link `evidence/summary.md` | `evidence/summary.md`, `evidence/data-mining.md`, script `evidence/mine_stackexchange.py` (luật commit `79b647b` trước dữ liệu `b3c87fb`); 8/125 (6,4%); 6 trích nguyên văn | **CÓ RỦI RO**: đủ thủ tục; chưa có người đọc tay (0/500 ô), chưa phỏng vấn; kết quả ngược giả thuyết |
| 2 | Bảng impact (guide 3.4) | `spec.md` §2 | Có, toàn *(tự ước tính)* |
| 3 | 20–30 câu, ≥5 `kho`, ≥2 `tu_choi` | `eval/benchmark.csv`: 30 · thuong 10 · kho 15 · tu_choi 5 · 3 tấn công · 15/30 nguồn thật; `python run.py check` → "Không thấy vấn đề" | **ĐỦ** |
| 4 | Bản chạy thử gọi AI thật | `codebase/ai.py` (Gemini); `eval/run-1.csv` cột model `gemini-3.1-flash-lite`, token > 0 cả 30 câu | **ĐỦ** |
| 5 | Video 30 giây (YouTube "Không công khai" / Drive "bất kỳ ai có link", mở được ở cửa sổ ẩn danh) | https://drive.google.com/file/d/1UdxZRih6MQq_qQkwUHtvIF-jtcfTa8h6/view?usp=sharing | **ĐỦ** (đã quay 29.3s gọi `gemini-3.1-flash-lite` thật, cập nhật vào `README.md`) |
| 6 | Kết quả lượt 1 (x/N) + run ID | run ID `run-1@20261128-010841` · `eval/run-1.csv` cột `pass` đã xác nhận (`3c75b97`) · `python run.py score eval/run-1.csv` → **28/30 (93%)** | **ĐỦ** (`thuong 10/10 · kho 13/15 · tu_choi 5/5`, D1=R0, Hồ Đức Mạnh) |
| 7 | `spec.md` §0–§7 đã commit | `spec.md`; §7 khớp `98024ba` (kiểm bằng `eval/finalize_results.py`) | **ĐỦ** |
| 8 | Phần chưa xong | mục dưới | — |

## Điền form CP3
- Link repo: https://github.com/theahASR/K5-Day15-L3A-LufkyMama (sau khi push).
- Link `evidence/summary.md`.
- Bộ câu thử: 30 câu (10 thuong · 15 kho · 5 tu_choi).
- Video: https://drive.google.com/file/d/1UdxZRih6MQq_qQkwUHtvIF-jtcfTa8h6/view?usp=sharing
- Lượt 1: `run-1@20261128-010841`, **28/30 đạt (93%)** — `thuong 10/10 (100%)`, `kho 13/15 (87%)`, `tu_choi 5/5 (100%)` (trượt B22, B30; đã xác nhận cột `pass` trong `eval/run-1.csv` theo quyết định D1=R0).
- Phần chưa xong: đọc tay 125 nhãn data mining (`evidence/mining_labels.csv`), phỏng vấn ≥3 người dùng ngoài nhóm (nguồn đối chiếu thứ 2), chấm chéo độc lập 2 người trên 5 output (`eval/README.md` mục 3), người dùng thử (bonus) và xuất lại `demo-slides.pdf` bản CONFIRMED trước CP4.

## Việc tối thiểu trước 10:00 (theo thứ tự)
1. Push (lệnh ở `docs/SUBMISSION_CP4.md` mục Git).
2. Chốt `eval/grading/GRADING_DECISIONS.md` D1 → chấm lượt 1 bằng `eval/grading/review.html` → `import_verdicts.py --run 1 … --apply` → `python run.py score eval/run-1.csv`.
3. Quay + upload video; dán link vào `README.md` mục 7.
4. Commit, push, nộp form.
