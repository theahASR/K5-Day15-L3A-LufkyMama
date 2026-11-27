# HANDOFF — để session khác / thành viên khác tiếp quản

Cập nhật 28/11/2026 ~02:00 ICT.

## Branch & baseline
- Nhánh làm việc `LufkyMama`; `origin/main` = `f2c61c6` (push 27/11 19:25, có commit chốt CP2 `98024ba`).
- **Các commit sau `f2c61c6` mới ở local** (agent bị chặn quyền push `main`). Đội trưởng push: `git push origin LufkyMama`, rồi merge/push `main`.
- Cấu trúc: repo ở thư mục gốc (đã bỏ `starter-repo/`).

## Đã xong (có bằng chứng trong repo)
- CP2: metric spec 7 metric, §7, benchmark 15 câu (sửa B01–B04: Glucose Pima = OGTT 2 giờ), data card, canvas, TEAMS.
- Evidence: đào data Stack Exchange, N = 125, 8/125 (6,4%), cách đếm chốt trước khi chạy; 6 trích nguyên văn.
- ML: `ml/train.py` (sklearn, chạy bằng `py -3.12`), LR AUC 0,787, RF 0,819; suy luận bằng thư viện chuẩn từ `ml/model.json`.
- KB: 13 đoạn từ CDC/NIDDK/WHO, đã mở từng URL để đối chiếu ngày 27/11.
- Workflow + 9 công cụ + Gemini (`gemini-3.1-flash-lite`).
- Benchmark 30 câu; lượt 1 `run-1@20261128-010841`, lượt 2 `run-2@20261128-011951`. Chấm sơ bộ của agent: 28/30 → 29/30.
- Cải tiến lượt 2: commit `23013c6` (tuyến ngoài phạm vi không đối chiếu ngưỡng người lớn).
- Simulate 50 phiên (`cost/simulate-1*`), cost-estimate, spec §0–§10, report, README, slides.

## Quyết định kỹ thuật
- Workflow cố định, không agent. Mọi công cụ là code tất định; chỉ có 1 lời gọi LLM mỗi câu (thêm 1 lần sửa nếu `validate_response` chặn).
- Model ML chỉ cho điểm khi: nữ, không mang thai, glucose là OGTT 2 giờ, đủ 4 chỉ số trong khoảng train. Không tự điền số thiếu.
- API lỗi: trong app demo (`LUFKY_FALLBACK=1`, đặt ở `codebase/app.py`) thì dùng mẫu an toàn; trong eval/simulate thì để lỗi hiện ở cột `error`.
- Không dùng nội dung MedlinePlus (trang cấm dùng cho AI).

## Chuẩn đánh giá đã khóa
`spec.md` §7 + `eval/metric_spec.yaml` tại commit `98024ba` (SHA-256 ở `docs/CP2_READINESS.md`). Không sửa.

## Còn mở
Xem `HUMAN_ACTIONS.md`: người duyệt cột `pass` (H6) · 2 người chấm độc lập (H5) · đọc tay nhãn (H7) · phỏng vấn (H8) · video (H9) · người dùng thử (H10) · reflection (H11) · push (H13) · nộp CP3/CP4.

## Lệnh kiểm nhanh
`python run.py check` · `python run.py eval --try` · `python run.py score eval/grading/run-2-agent-prelim.csv`

## Cập nhật sau audit (28/11)
- `FINAL_QA_AUDIT.md`: kết luận READY_WITH_LIMITATIONS, chưa xác nhận.
- Chấm người: `eval/grading/README.md` (review.html → import_verdicts.py → finalize_results.py). `finalize_results.py` tự ở chế độ PRELIMINARY cho tới khi có `final_run-N.csv` khớp cột `pass`.
- Cổng quyết định: `eval/grading/GRADING_DECISIONS.md` D1 (cách hiểu Safety), chi tiết `eval/grading/SAFETY_AMBIGUITY_REVIEW.md`.
- Nộp: `docs/SUBMISSION_CP3.md`, `docs/SUBMISSION_CP4.md`. Đề xuất (chưa làm): `docs/FUTURE_IMPROVEMENTS.md`.
