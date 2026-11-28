# LufkyMama — Sàng lọc nguy cơ tiểu đường tham khảo + tư vấn lối sống có nguồn

**Thành viên, lớp, track:** xem [TEAMS.md](TEAMS.md) · Track **B — Y tế**

*Lát cắt:* một người 25–60 tuổi nhập chỉ số đường huyết (kèm lúc đo), BMI, tuổi → hệ thống kiểm cấp cứu và phạm vi, đối chiếu ngưỡng có nguồn (CDC, WHO), chạy mô hình ML khi hồ sơ trong phạm vi → **AI (Gemini) soạn câu trả lời**: vùng chỉ số, mức nguy cơ tham khảo, 2–3 hành động cụ thể, có cần đi khám không. Chi tiết: [spec.md](spec.md) §4.

> ⚠️ Công cụ giáo dục sức khỏe, **không** chẩn đoán, không kê thuốc. Có dấu hiệu cấp cứu: gọi **115**. Không nhập tên, số điện thoại hay thông tin định danh: câu hỏi được gửi tới API model của Google.

## Chạy trong 3 phút

Cần **Python 3.10+**. Bản chạy thử **chỉ dùng thư viện chuẩn**, không cần `pip install` (scikit-learn chỉ cần khi train lại model: `ml/requirements-train.txt`).

```
copy .env.example .env        # macOS/Linux: cp .env.example .env
# điền: MODEL_PROVIDER=gemini · MODEL_NAME=gemini-3.1-flash-lite · API_KEY=<key Google AI Studio>
python run.py                 # gõ câu hỏi, Enter; thoát: Enter 2 lần
python run.py check           # kiểm benchmark + metric spec + TEAMS.md
python run.py eval --try      # thử 3 câu với model thật
python run.py eval --wait 4   # chạy cả 30 câu → eval/run-N.csv + traces/run-N.jsonl
python run.py score eval/run-N.csv
python run.py simulate --wait 4   # mô phỏng chi phí 50 phiên
```

Chưa có `.env` thì chạy **chế độ giả** (model `fake`): luồng vẫn chạy hết, câu trả lời là mẫu an toàn soạn bằng code, có ghi rõ ở dòng đầu.

Thử ngay: `Nữ 53 tuổi, đường huyết sau nghiệm pháp dung nạp glucose 2 giờ 197 mg/dL, huyết áp tâm trương 70 mmHg, BMI 30.5. Đánh giá nguy cơ giúp tôi.` · Sửa dữ liệu trong phiên: `sửa: BMI 27`.

## Phần nào thật, phần nào giả

| Thành phần | Thật / Giả | Ghi chú |
|---|---|---|
| Lời gọi AI ở quyết định trung tâm (soạn tư vấn) | **Thật** | `gemini-3.1-flash-lite` qua Gemini API; token lấy từ `usageMetadata` |
| Mô hình ML sàng lọc | **Thật** | Logistic Regression train trên Pima (`ml/train.py`, seed 42, ROC-AUC test 0,787); suy luận bằng thư viện chuẩn từ `ml/model.json`. Chỉ cho điểm khi hồ sơ trong phạm vi dữ liệu (nữ, OGTT 2 giờ) |
| Knowledge base | **Thật** | 13 đoạn tự viết lại từ CDC, NIDDK, WHO, có URL + ngày (`data/knowledge_base.json`) |
| Chặn rủi ro | **Thật** (code) | cấp cứu trước, phạm vi, kiểm câu trả lời sau model (`codebase/tools.py`) |
| Người dùng, phòng khám, hồ sơ | Không có | Không đăng nhập, không lưu dữ liệu |

## Dùng AI vào việc gì

Coding agent Claude Code viết bản đầu code, script đào data, tài liệu và câu thử B16–B30. Agent tra nguồn y khoa và chấm sơ bộ lượt chạy. Mỗi thành viên đọc lại và chịu trách nhiệm phần có tên mình; cột `pass` do người chấm. Chi tiết: [docs/ai-usage.md](docs/ai-usage.md) · agent đọc [AGENTS.md](AGENTS.md).

## Bảy hạng mục bắt buộc — nằm ở file nào

| # | Hạng mục | File |
|---|---|---|
| 1 | Bằng chứng pain | `evidence/summary.md` · `evidence/data-mining.md` · `evidence/mine_stackexchange.py` |
| 2 | Impact có số | `spec.md` §2 |
| 3 | Thiết kế giải pháp | `spec.md` §4 |
| 4 | Bản chạy thử làm trọn lát cắt | `codebase/` · `ml/` · `data/knowledge_base.json` · lệnh ở trên |
| 5 | Định nghĩa "tốt" + bộ câu thử | `data/DATA_CARD.md` · `eval/benchmark.csv` (30 câu) · `eval/metric_spec.yaml` · `eval/README.md` |
| 6 | Mô phỏng chi phí khi dùng thật | `cost/personas.yaml` · `cost/simulate-N.csv` · `cost/cost-estimate.md` |
| 7 | Slide + demo + video dự phòng | `demo-slides.pdf` · link video: https://drive.google.com/file/d/1UdxZRih6MQq_qQkwUHtvIF-jtcfTa8h6/view?usp=sharing (kịch bản: `docs/VIDEO_SCRIPT.md`) |
| + | *Bonus:* người dùng thử | `validation/log.md` |
