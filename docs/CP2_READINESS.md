# CP2 Readiness — deadline 19:30 Thứ Sáu 27/11/2026 (ICT)

Kiểm lúc 19:13 ICT ngày 27/11/2026 theo README BTC mục CP2 và guide 2.5.

| # | Yêu cầu BTC | Artifact | Kết quả kiểm thực tế | Trạng thái |
|---|---|---|---|---|
| 1 | Canvas cập nhật + 1–3 dòng "đã đổi gì so với CP1" | `canvas.md` | 7 dòng đủ; dòng 4 có số + trích dẫn (Miyakawa 2017, 254/376); dòng 7 phân công; 3 dòng thay đổi | DONE |
| 2 | Nguồn bằng chứng đang làm và đến đâu | `evidence/data-mining.md` | Đã chốt trước cách đếm (Stack Exchange, nhãn L1–L4, mẫu số); **chưa chạy đếm** | PARTIAL (đúng mức CP2: "đã đào và có cách đếm") |
| 3 | `spec.md` §4 có sơ đồ kiến trúc | `spec.md` §4 | Có sơ đồ Mermaid Input → AI Core → Chặn rủi ro → Output | DONE |
| 4 | `eval/benchmark.csv` ≥10 câu | `eval/benchmark.csv` | 15 câu · 6 thuong · 6 kho · 3 tu_choi · 2 câu tấn công (B14, B15) · 6/15 data_that; `python run.py check` qua | DONE |
| 5 | `eval/metric_spec.yaml` | `eval/metric_spec.yaml` | 7 metric đủ name/definition/grader/threshold/why; check báo "7 metric đã điền đủ" | DONE |
| 6 | `data/DATA_CARD.md` bản đầu | `data/DATA_CARD.md` | Pima: nguồn, hash, 768 dòng, từ điển, bias, quyền dùng | DONE |
| 7 | Chuẩn "đạt" bằng số trong `spec.md` §7 | `spec.md` §7 | 7 tiêu chí có ngưỡng %, đồng bộ metric_spec | DONE |
| 8 | `python run.py` đi hết luồng với AI giả | `run.py`, `codebase/` | Chạy thử 19:12: in câu trả lời giả, model fake, 1 lần gọi model, 1 lần gọi công cụ | DONE (khung mẫu; luồng của nhóm thay ngay sau CP2) |
| 9 | Hai người chấm thử 5 output khớp ≥4/5 | `eval/README.md` mục 3 | Chưa có output thật để chấm | NOT_STARTED (yêu cầu R4, không phải điều kiện CP2) |

## Sửa benchmark trước khi chốt (có lý do)
- B01–B04 ghi "đường huyết lúc đói" nhưng nguồn là cột `Glucose` của Pima, vốn là **glucose huyết tương 2 giờ sau OGTT** (mô tả gốc UCI). Đã đổi input sang "sau nghiệm pháp dung nạp glucose 2 giờ (OGTT)". Ở B02–B04 đổi ngưỡng trong expected sang ngưỡng OGTT của ADA (<140 bình thường, 140–199 rối loạn dung nạp glucose). B02 thôi gọi 116 mg/dL là "tiền tiểu đường". Diff: `git show 98024ba -- eval/benchmark.csv`.
- 6 dòng Pima được trích (1, 2, 6, 9, 10, 15) đã đối chiếu từng giá trị với file gốc (SHA-256 ở DATA_CARD).

## Phiên bản chốt
| File | SHA-256 tại commit `98024ba` |
|---|---|
| `eval/benchmark.csv` | `8e7655707be42c439904ee7ca60d8d0af057ef0e8f2a35ebed6949b3d51fadd4` |
| `eval/metric_spec.yaml` | `14e7b8ba17ba7e35edd2c1a3b2d41a29b0e720d912c33d873a76cb2015d1e35e` |

Commit `98024ba` tạo lúc 19:09 ICT 27/11/2026 trên máy local. **Chỉ được coi là "chốt trước 19:30" nếu đã push lên GitHub trước 19:30.** Agent không push; đội trưởng push.

## Đội trưởng cần làm ngay
1. `git push origin LufkyMama` **trước 19:30**. Nếu BTC chấm nhánh `main`, merge hoặc mở PR vào `main` theo quy ước của nhóm.
2. Nộp form CP2 kèm: link repo; link `spec.md` và `eval/benchmark.csv`; nguồn bằng chứng đang làm (data mining Stack Exchange, mới chốt cách đếm; nghiên cứu Miyakawa 2017 làm số đầu); chuẩn "đạt" chép từ `spec.md` §7.
3. Xác nhận lại với nhóm phân công ở `TEAMS.md` / `canvas.md` dòng 7.
