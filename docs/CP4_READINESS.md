# CP4 Readiness — deadline 14:30 Thứ Bảy 28/11/2026 (ICT)

Kiểm lúc ~01:50 ICT 28/11/2026 theo README BTC mục CP4, guide 4.4, rubric.

| # | Yêu cầu BTC | Artifact | Kiểm thực tế | Trạng thái |
|---|---|---|---|---|
| 1 | Phòng demo + link repo | — | Phòng/zone chưa có trong spec (`Phòng __ · Zone __`) | Đội trưởng điền |
| 2 | Tích 7 hạng mục bắt buộc | `README.md` bảng 7 hạng mục | Đủ file cho 7 mục; mục 7 thiếu link video | PARTIAL (video H9) |
| 3 | Kết quả lượt 1 → lượt 2 | `eval/report.md` | **28/30 → 29/30** (93,3% → 96,7%), `run-1@20261128-010841` → `run-2@20261128-011951`, cùng 30 câu, cùng model | DONE (số do agent chấm sơ bộ, chờ người duyệt H6) |
| 4 | Chi phí / task thành công ở kịch bản cơ sở + tên model | `cost/cost-estimate.md` | **$0,0021 / task thành công · gemini-3.1-flash-lite**; cơ sở 5.000 người: $20,83/tháng | DONE |
| 5 | `demo-slides.pdf` ở gốc + link video dự phòng | `demo-slides.pdf` | 8 trang, mở được (kiểm bằng PyMuPDF, đã xem từng trang); link video chưa có | PARTIAL (video) |
| 6 | Phần chưa xong | — | xem dưới | — |

## Kiểm cuối
- **Bí mật:** không file `.env`/key nào được track; quét chuỗi dạng key: 0 kết quả.
- **Chuẩn "đạt":** `eval/metric_spec.yaml` không đổi so với `98024ba`; `spec.md` §7 khớp từng byte với `98024ba` (kiểm bằng script khi sửa spec).
- **Benchmark:** lượt 1 và lượt 2 cùng 30 câu; so với CP2 chỉ thêm dòng, không xoá hay sửa câu nào.
- **Kết quả các lượt:** `eval/run-1.csv`, `eval/run-2.csv`, `cost/simulate-1.csv`, `traces/*` commit nguyên trạng ngay sau khi chạy, không sửa.
- **Chạy lại được:** `python run.py check` "Không thấy vấn đề"; bản chạy thử chỉ cần thư viện chuẩn.
- **Số trong slide:** mỗi trang có dòng nguồn trỏ về file trong repo.

## Còn thiếu / cần người (`HUMAN_ACTIONS.md`)
1. **Push** (H13): 12+ commit mới ở local, `origin/main` dừng ở `f2c61c6`.
2. Người duyệt cột `pass` lượt 1, 2 (H6) → nếu số đổi: cập nhật `eval/report.md`, slide 5, chạy lại `simulate --rate-from eval/run-2.csv`.
3. 2 người chấm độc lập 5 output (H5).
4. Video 30 giây + video dự phòng (H9).
5. Đọc tay nhãn data mining (H7), phỏng vấn (H8) — R1.
6. Người dùng thử (H10, bonus). Reflection (H11).

## Đội trưởng điền form CP4
- Lượt 1 → lượt 2: 28/30 → 29/30 (chép số sau khi duyệt).
- Chi phí / task thành công (cơ sở): $0,0021, model gemini-3.1-flash-lite (thêm: $0,0116 với gemini-3.8-flash).
- `demo-slides.pdf` ở gốc repo; link video dự phòng.
- Phần chưa xong: như mục trên.
