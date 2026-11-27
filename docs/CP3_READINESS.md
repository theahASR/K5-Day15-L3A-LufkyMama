# CP3 Readiness — deadline 10:00 Thứ Bảy 28/11/2026 (ICT)

Kiểm lúc ~01:20 ICT 28/11/2026 theo README BTC mục CP3 và guide 3.4.

| # | Yêu cầu BTC | Artifact | Kiểm thực tế | Trạng thái |
|---|---|---|---|---|
| 1 | Bằng chứng pain đạt ngưỡng ≥1 nguồn + ≥5 trích dẫn | `evidence/summary.md`, `evidence/data-mining.md`, `evidence/mine_stackexchange.py`, `evidence/mining_labels.csv` | Đào data: N = 125, x/N = 8/125 (6,4%), cách đếm chốt trước (commit `79b647b` trước khi chạy), script chạy lại được, 6 ví dụ nguyên văn. Kết quả **ngược giả thuyết**, ghi thật. **Chưa có người đọc tay** (H7) | PARTIAL: đạt về cách làm; nên có người đọc tay + phỏng vấn để chắc |
| 2 | Bộ câu thử 20–30, ≥5 kho, ≥2 tu_choi | `eval/benchmark.csv` | 30 câu · thuong 10 · kho 15 · tu_choi 5 · 3 câu tấn công · 15/30 nguồn thật; `run.py check`: "Không thấy vấn đề" | DONE |
| 3 | Video 30 giây gọi AI thật | `docs/VIDEO_SCRIPT.md` | Agent không quay được màn hình | BLOCKED (H9: thành viên quay + upload) |
| 4 | Kết quả lượt 1 (x/N) + run ID | `eval/run-1.csv`, `traces/run-1.jsonl` | `run-1@20261128-010841`, gemini-3.1-flash-lite, 30/30 chạy, 0 lỗi. **Chấm sơ bộ của agent: 28/30 (93%)** (`eval/grading/run-1-agent-prelim.csv`) | PARTIAL: cột `pass` trong `run-1.csv` chờ người chấm (H6) |
| 5 | `spec.md` §0–§7 | `spec.md` | Đủ §0–§7; §7 giống hệt bản CP2 (kiểm bằng so khớp với commit `98024ba`) | DONE |
| 6 | Phần chưa xong | — | Người chấm `pass`; 2 người chấm thử 5 output (`eval/grading/GRADING_SHEET.md`); video; phỏng vấn | — |

## Nội dung đội trưởng điền form CP3
- Link `evidence/summary.md`.
- Bộ câu thử: 30 câu (10 thuong · 15 kho · 5 tu_choi).
- Link video: (sau khi quay).
- **Lượt 1:** run ID `run-1@20261128-010841`. Kết quả: điền số sau khi người chấm xác nhận cột `pass`; bản sơ bộ của agent là 28/30.
- Phần chưa xong: người đọc tay nhãn data mining, phỏng vấn, chấm độc lập 2 người.

## Đội trưởng cần làm trước 10:00
1. Một người mở `eval/grading/run-1-agent-prelim.csv`, đọc từng output, sửa chỗ không đồng ý, rồi chép cột `pass` và `ghi_chu` vào `eval/run-1.csv`. Chỉ được sửa 2 cột này (AGENTS.md). Sau đó chạy `python run.py score eval/run-1.csv`.
2. Quay video theo `docs/VIDEO_SCRIPT.md`, upload, dán link vào `README.md`.
3. `git pull` rồi commit, push, nộp form CP3.
