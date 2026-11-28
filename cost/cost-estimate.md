# Chi phí khi dùng thật

<!-- AUTO:cost:start -->
Chế độ tỉ lệ đạt: **CONFIRMED**. Tỉ lệ đạt lượt 2 dùng để tính: 29/30 (96.7%). Token đo thật: 50 phiên, 194001 vào / 35917 ra (`cost/simulate-1.csv`).

| Model | Đo hay ước tính | / phiên | / task thành công | / người / tháng | / tháng thấp (1000) | cơ sở (5000) | cao (20000) |
|---|---|---|---|---|---|---|---|
| gemini-3.1-flash-lite (0.25 / 1.50 $/1M) | token đo trên model này | $0.0020 | $0.0021 | $0.0042 | $4.17 | $20.83 | $83.31 |
| gemini-3.8-flash (1.50 / 7.50 $/1M) | ƯỚC TÍNH: token của model khác × giá model này | $0.0112 | $0.0116 | $0.0228 | $22.81 | $114.05 | $456.18 |
<!-- AUTO:cost:end -->


> Số lấy nguyên từ `cost/simulate-1-summary.md` (do `python run.py simulate` sinh ra, không điền tay). Chấm ở rubric R6.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): 3 kiểu. `mot_lan_sau_kham` 60% · 1 phiên/tháng · 2 lượt; `tu_do_tai_nha` 30% · 4 phiên/tháng · 2 lượt; `hoi_ho_nguoi_than` 10% · 2 phiên/tháng · 3 lượt. Nguồn: **(tự ước tính)**, gợi ý từ ví dụ ở `evidence/data-mining.md`.
- **Số người dùng thật** 3 kịch bản: thấp 1.000 · cơ sở 5.000 · cao 20.000. Nguồn: **(tự ước tính)**, quy mô thí điểm; chưa có nguồn công khai.
- **Giá** (bảng giá BTC `further-reading/model-prices.md`, xem 25/11/2026; trang gốc https://ai.google.dev/gemini-api/docs/pricing):
  - `gemini-3.1-flash-lite` (Nhỏ): vào 0,25 · ra 1,50 USD / 1M token. Đây là model đã dùng để đo.
  - `gemini-3.8-flash` (Vừa): vào 1,50 · ra 7,50 USD / 1M token, giá áp dụng **từ 01/01/2027**. Giá thấp 0,75 / 3,75 chỉ đến 31/12/2026, nên dùng giá cao cho lúc dùng thật.
- **Tỉ lệ đạt:** 29/30 (96,7%), lượt `run-2@20261128-011951`, cùng model `gemini-3.1-flash-lite`. ⚠️ Đây là **chấm sơ bộ của agent** (`eval/grading/run-2-agent-prelim.csv`). Nếu người chấm đổi số, chạy lại `python run.py simulate --rate-from eval/run-2.csv` thành lượt mới.
- **Đo token trên `gemini-3.1-flash-lite`, tính giá cả `gemini-3.1-flash-lite` và `gemini-3.8-flash`.** Hai model cùng hãng nên cách tách token có lẽ gần nhau, nhưng nhóm chưa đo trên 3.8-flash.

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-1.csv` · run ID `simulate-1@20261128-012440` · **50 phiên** · seed 42 · 0/50 phiên lỗi · chạy thật qua `codebase/agent.py`, token đọc từ `usageMetadata` của API.

| Persona | Số phiên | Lượt / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên |
|---|---:|---:|---:|---:|---:|
| mot_lan_sau_kham | 30 | 2 | 3.757 | 704 | 2,0 |
| tu_do_tai_nha | 17 | 2 | 3.827 | 701 | 2,1 |
| hoi_ho_nguoi_than | 3 | 3 | 5.414 | 960 | 3,0 |

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp (1.000) | / tháng — cơ sở (5.000) | / tháng — cao (20.000) | / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite | $0,0020 | **$0,0021** | $4,17 | $20,83 | $83,31 | $0,0042 |
| gemini-3.8-flash | $0,0112 | $0,0116 | $22,81 | $114,05 | $456,18 | $0,0228 |

Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt lượt 2 (96,7%), **không coi như đạt 100%**.

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): **30 phút tra cứu tiết kiệm** *(tự ước tính)*.
- Chi phí / người / tháng (cơ sở, `gemini-3.1-flash-lite`): **$0,0042**; với `gemini-3.8-flash`: $0,0228.
- **Kết luận:** chi phí model không phải là rào cản: dưới 1 xu Mỹ mỗi người mỗi tháng, so với 30 phút tiết kiệm *(tự ước tính)*. Rủi ro của bài nằm ở chỗ pain và impact chưa được đo thật (`evidence/summary.md`), không nằm ở chi phí.

## 4. Giới hạn
- Persona, số người dùng, số phút đều *(tự ước tính)*.
- Chưa tính chi phí ngoài model (hosting, người duyệt KB, bác sĩ kiểm nội dung).
- Câu hỏi trong mô phỏng lấy ngẫu nhiên từ benchmark (thuong/kho, thêm tu_choi cho persona hỏi hộ). Câu thật có thể dài hơn.
