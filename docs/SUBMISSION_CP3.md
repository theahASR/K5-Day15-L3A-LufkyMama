# Gói nộp CP3 — 10:00 Thứ Bảy 28/11/2026

Đối chiếu README BTC mục CP3 + guide 3.4 + rubric. Trạng thái tính đến commit hiện tại của nhánh `LufkyMama` (xem `git log -1`).

| # | Yêu cầu BTC (nguyên văn rút gọn) | Bằng chứng | Trạng thái |
|---|---|---|---|
| 1 | Bằng chứng pain đạt ngưỡng ≥1 nguồn + ≥5 trích dẫn; link `evidence/summary.md` | `evidence/summary.md`, `evidence/data-mining.md`, script `evidence/mine_stackexchange.py` (luật commit `79b647b` trước dữ liệu `b3c87fb`); 8/125 (6,4%); 6 trích nguyên văn | **CÓ RỦI RO**: đủ thủ tục; chưa có người đọc tay (0/500 ô), chưa phỏng vấn; kết quả ngược giả thuyết |
| 2 | Bảng impact (guide 3.4) | `spec.md` §2 | Có, toàn *(tự ước tính)* |
| 3 | 20–30 câu, ≥5 `kho`, ≥2 `tu_choi` | `eval/benchmark.csv`: 30 · thuong 10 · kho 15 · tu_choi 5 · 3 tấn công · 15/30 nguồn thật; `python run.py check` → "Không thấy vấn đề" | **ĐỦ** |
| 4 | Bản chạy thử gọi AI thật | `codebase/ai.py` (Gemini); `eval/run-1.csv` cột model `gemini-3.1-flash-lite`, token > 0 cả 30 câu | **ĐỦ** |
| 5 | Video 30 giây (YouTube "Không công khai" / Drive "bất kỳ ai có link", mở được ở cửa sổ ẩn danh) | `docs/VIDEO_SCRIPT.md` | **THIẾU**: người quay (H9) |
| 6 | Kết quả lượt 1 (x/N) + run ID | run ID `run-1@20261128-010841` (commit `4eb2c01`) · `eval/run-1.csv` cột `pass` **trống** · chấm sơ bộ agent 28/30 | **THIẾU kết quả xác nhận**: guide 3.4 bước 3 yêu cầu người chấm điền `pass` rồi `score` |
| 7 | `spec.md` §0–§7 đã commit | `spec.md`; §7 khớp `98024ba` (kiểm bằng `eval/finalize_results.py`) | **ĐỦ** |
| 8 | Phần chưa xong | mục dưới | — |

## Điền form CP3
- Link repo: https://github.com/theahASR/K5-Day15-L3A-LufkyMama (sau khi push).
- Link `evidence/summary.md`.
- Bộ câu thử: 30 câu (10 thuong · 15 kho · 5 tu_choi).
- Video: ____ (sau khi quay).
- Lượt 1: `run-1@20261128-010841`, **x/30 = điền sau khi người chấm** (`python run.py score eval/run-1.csv`). Nếu chưa kịp chấm, ghi thật: "chấm sơ bộ 28/30, chưa có người duyệt; theo cách hiểu chặt về 'khẳng định chẩn đoán' là 26/30".
- Phần chưa xong: đọc tay 125 nhãn; phỏng vấn; 2 người chấm độc lập; cách hiểu Safety cho câu "bạn đang ở vùng tiền tiểu đường".

## Việc tối thiểu trước 10:00 (theo thứ tự)
1. Push (lệnh ở `docs/SUBMISSION_CP4.md` mục Git).
2. Chốt `eval/grading/GRADING_DECISIONS.md` D1 → chấm lượt 1 bằng `eval/grading/review.html` → `import_verdicts.py --run 1 … --apply` → `python run.py score eval/run-1.csv`.
3. Quay + upload video; dán link vào `README.md` mục 7.
4. Commit, push, nộp form.
