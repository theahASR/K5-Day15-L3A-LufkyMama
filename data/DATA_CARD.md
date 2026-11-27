# DATA CARD — LufkyMama · Track B

> Bản đầu CP2 (27/11/2026). Cập nhật ở CP3 khi train model và xây knowledge base.

## D1 · Pima Indians Diabetes Database

| Mục | Nội dung |
|---|---|
| Nguồn gốc | National Institute of Diabetes and Digestive and Kidney Diseases (NIDDK), công bố trong Smith J.W. et al. (1988), *Using the ADAP learning algorithm to forecast the onset of diabetes mellitus*, Proc. Symp. Computer Applications in Medical Care, 261–265. Từng phân phối qua UCI ML Repository; bản Kaggle "Pima Indians Diabetes Database" (UCI ML, giấy phép CC0). |
| Bản nhóm tải | `https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv` (không có dòng tiêu đề), tải 27/11/2026. SHA-256 `6bfe5d0f379d17a0e0819b996407e3c09bf80febd4287f2ed212190dfff154af`. **Không commit nguyên file**; `ml/train.py` (CP3) tải lại và kiểm hash. |
| Kích thước | 768 dòng × 9 cột; 268 dòng `Outcome = 1` (34,9%), 500 dòng `Outcome = 0` — nhóm tự đếm trên file đã tải. |
| Đối tượng | Phụ nữ ≥21 tuổi, gốc Pima (Arizona, Mỹ). Cộng đồng có tỉ lệ tiểu đường type 2 rất cao. |
| Loại | Dữ liệu thật, đã ẩn danh từ nguồn; không có định danh cá nhân. |
| Mục đích dùng | (1) Train mô hình sàng lọc nguy cơ tham khảo (CP3). (2) Nguồn `data_that` cho câu thử B01–B05, B07 (số dòng = thứ tự dòng trong file, đếm từ 1). |

### Từ điển dữ liệu

| Cột | Ý nghĩa (theo mô tả gốc UCI) | Đơn vị | Số ô = 0 (thực chất là thiếu) |
|---|---|---|---|
| Pregnancies | Số lần mang thai | lần | 111 (0 là giá trị hợp lệ) |
| Glucose | **Nồng độ glucose huyết tương 2 giờ sau nghiệm pháp dung nạp glucose đường uống (OGTT)**. KHÔNG phải đường huyết lúc đói | mg/dL | 5 |
| BloodPressure | Huyết áp tâm trương | mmHg | 35 |
| SkinThickness | Độ dày nếp gấp da cơ tam đầu | mm | 227 |
| Insulin | Insulin huyết thanh 2 giờ | µU/mL | 374 |
| BMI | Cân nặng (kg) / chiều cao (m)² | kg/m² | 11 |
| DiabetesPedigreeFunction | Điểm tiền sử gia đình | không đơn vị | 0 |
| Age | Tuổi | năm | 0 |
| Outcome | Có tiểu đường trong 5 năm theo dõi (1) hay không (0) | nhãn | — |

### Làm sạch (kế hoạch CP3, chi tiết ở `ml/README.md`)
- Giá trị 0 ở Glucose, BloodPressure, BMI coi là thiếu; điền trung vị **chỉ tính trên tập train**.
- Không dùng SkinThickness, Insulin (thiếu 30–49%, người dùng tại nhà không có).
- Chia train/test 80/20, phân tầng theo Outcome, seed = 42.

### Bias và giới hạn — đọc trước khi dùng
1. **Không đại diện cho người Việt Nam**: chỉ phụ nữ gốc Pima, ≥21 tuổi; không có nam giới. Điểm mô hình **không** phải xác suất mắc bệnh cho người Việt và chưa được kiểm định ngoài mẫu.
2. Glucose là chỉ số OGTT 2 giờ. Người dùng nhập đường huyết lúc đói hoặc ngẫu nhiên thì **không** đưa vào mô hình như nhau; hệ thống hỏi lại bối cảnh đo (G10).
3. Dữ liệu thu thập từ thập niên 1960–1980, nhãn theo tiêu chuẩn WHO thời điểm đó.
4. Nam giới, thai kỳ, người <21 tuổi: ngoài phạm vi mô hình → hệ thống chỉ giải thích chung, không cho điểm.

### Quyền sử dụng
Bộ dữ liệu được phân phối công khai cho nghiên cứu qua UCI ML Repository; bản Kaggle ghi giấy phép CC0. Nhóm chỉ dùng cho mục đích học tập trong hackathon.

### Người kiểm nội dung
Bùi Thế Anh (Data/ML) — *chưa xác nhận, chờ thành viên kiểm.* Agent đã đối chiếu 6 dòng dùng trong benchmark với file gốc (27/11/2026).

## D2 · Knowledge base y khoa (CP3)
Kế hoạch: `data/knowledge_base.json`, 15–25 đoạn ngắn do nhóm tự viết lại (không chép nguyên văn), mỗi đoạn có `source_id, title, content, source_url, version_or_date, applicability, limitations`. Nguồn: ADA Standards of Care, CDC, NIDDK, WHO, Bộ Y tế. **Chưa xây.**

## D3 · Câu thử tự viết (`tu_viet`)
9/15 câu ở CP2 do nhóm tự viết dựa trên kịch bản lớp 1–4 (spec §5). Không phải dữ liệu thật và không dùng làm bằng chứng pain.
