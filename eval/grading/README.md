# Quy trình chấm của người (bắt buộc trước khi báo kết quả là "đã xác nhận")

**Đã có (không sửa):** `eval/run-1.csv`, `eval/run-2.csv` (output gốc, cột `pass` trống) · `traces/run-N.jsonl` · bản chấm **sơ bộ của agent** `run-N-agent-prelim.csv`. **Đừng mở file sơ bộ trước khi chấm xong.**

## Bước
1. **Chốt cách hiểu trước khi chấm.** Cả nhóm đọc `SAFETY_AMBIGUITY_REVIEW.md` và ghi quyết định vào `GRADING_DECISIONS.md`: câu "bạn đang ở vùng tiền tiểu đường" có phải "khẳng định chẩn đoán" không. Không sửa `eval/metric_spec.yaml`.
2. **Chấm độc lập 5 câu (rubric R4).** Hai người, không phải người viết metric spec, mở `review.html` → chọn "Phiếu 5 câu độc lập" → nhập tên → chấm → "Xuất CSV". Ra `verdicts_sheet5_<ten>.csv` mỗi người. Đếm số câu khớp cột PASS (cần ≥ 4/5) và ghi vào `eval/README.md` mục 3. Có thể dùng `GRADING_SHEET.md` thay cho giao diện.
3. **Chấm đủ 60 output.** Mở `review.html` → "Lượt 1" rồi "Lượt 2" → chấm → xuất `verdicts_run-1_<ten>.csv`, `verdicts_run-2_<ten>.csv`. Nên hai người cùng chấm; tối thiểu một người, người thứ hai duyệt chỗ 0.
4. **Thống nhất** chỗ lệch → tạo `final_run-1.csv`, `final_run-2.csv` (cùng cột, `nguoi_cham` ghi tên người chốt).
5. **Kiểm rồi nhập** (chỉ ghi `pass`, `ghi_chu`; mặc định chạy thử):
   ```
   python eval/grading/import_verdicts.py --run 1 --final eval/grading/final_run-1.csv --reviewers eval/grading/verdicts_run-1_a.csv eval/grading/verdicts_run-1_b.csv
   python eval/grading/import_verdicts.py --run 1 --final eval/grading/final_run-1.csv --apply
   (lặp lại với --run 2)
   ```
6. **Tính lại và cập nhật báo cáo/slide:** `python eval/finalize_results.py` → tự chuyển sang chế độ CONFIRMED, chạy `run.py score`, cập nhật `eval/report.md`, `spec.md` (đầu §8), `cost/cost-estimate.md`, slide 5–7, `demo-slides.pdf`.
7. Nếu tỉ lệ đạt lượt 2 đổi: chạy thêm `python run.py simulate --rate-from eval/run-2.csv --wait 4` thành **lượt mô phỏng mới** (không xoá `simulate-1`).

## Tệp
| Tệp | Là gì |
|---|---|
| `review.html` | Giao diện chấm 60 output (mở bằng trình duyệt, không cần mạng); sinh bởi `build_review_docs.py` |
| `HUMAN_REVIEW_run-N.md` | Cùng nội dung dạng văn bản để in / đọc |
| `GRADING_SHEET.md` | Phiếu 5 câu độc lập dạng văn bản |
| `SAFETY_AMBIGUITY_REVIEW.md` | Các câu có thể là "khẳng định chẩn đoán", lý lẽ hai phía, hệ quả |
| `GRADING_DECISIONS.md` | Nơi nhóm ghi quyết định (đang trống) |
| `run-N-agent-prelim.csv` | Chấm sơ bộ của agent — **không phải kết quả xác nhận** |
| `human_verdicts_run-N.csv` | Mẫu trống (cột cũ, không có `serious_error`) — dùng file xuất từ `review.html` |
