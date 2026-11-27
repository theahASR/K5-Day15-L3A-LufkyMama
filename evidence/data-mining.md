# Đào data — cách đếm và kết quả

> Repo chỉ chứa số đã tổng hợp và vài trích đoạn ngắn đã bỏ tên — không chép nguyên data.

## 1. Cách đếm — viết TRƯỚC khi chạy (chốt 27/11/2026 ~19:15 ICT, trước khi tải và đếm)

- **Data dùng:** toàn bộ câu hỏi công khai trên Medical Sciences Stack Exchange (`medicalsciences.stackexchange.com`) có tag `diabetes` hoặc `blood-sugar`, mọi thời điểm đến ngày tải. Lấy qua Stack Exchange API 2.3 (công khai, không cần đăng nhập; nội dung giấy phép CC BY-SA). Lúc chốt cách đếm, API báo `diabetes` có 110 câu hỏi và `blood-sugar` có 23 câu (có trùng).
- **Vì sao chọn nguồn này:** đây là chỗ người thường tự hỏi về chỉ số của mình khi chưa gặp bác sĩ, toàn bộ tập lấy lại được bằng một script, và không cần cào dữ liệu cá nhân. Giới hạn: người hỏi chủ yếu dùng tiếng Anh và không phải người Việt (xem mục 5).
- **Mẫu số N:** số câu hỏi *duy nhất* (theo `question_id`) trong hợp của hai tag.
- **Đếm gì (nhãn định nghĩa trước, một câu có thể nhiều nhãn):**
  - `L1_so_cua_minh`: người hỏi nêu **chỉ số đo cụ thể của chính mình hoặc người thân** (đường huyết, HbA1c, BMI/cân nặng) kèm con số.
  - `L2_hoi_dien_giai`: hỏi số đó **có nghĩa là gì / có bình thường / có đáng lo / có phải tiểu đường hay tiền tiểu đường**.
  - `L3_hoi_buoc_tiep`: hỏi **nên làm gì tiếp** (ăn gì, vận động, có cần đi khám / xét nghiệm gì).
  - `L4_boi_canh_do`: câu hỏi **không nói rõ hoặc nhầm** bối cảnh đo (lúc đói / sau ăn / ngẫu nhiên / đơn vị mg/dL vs mmol/L).
  - Câu hỏi thuần kiến thức chung, cơ chế sinh học, nghiên cứu, thuốc cho người đã chẩn đoán: không gắn L1–L4.
- **Số chính cần báo:** `L2 ∪ L3` trên N (tỉ lệ câu hỏi thể hiện đúng pain "không biết chỉ số nghĩa là gì / làm gì tiếp"), và `L1 ∩ (L2 ∪ L3)` trên `L1`.
- **Cách gắn nhãn:** (a) script `evidence/mine_stackexchange.py` gắn nhãn sơ bộ bằng luật từ khoá cố định, viết trước khi xem kết quả; (b) một người đọc tay toàn bộ để sửa nhãn và ghi lại từng chỗ sửa vào `evidence/mining_labels.csv`; (c) báo cả số theo luật và số sau khi đọc tay.
- **Script:** `evidence/mine_stackexchange.py` (CP3). Chạy lại: `python evidence/mine_stackexchange.py`.
- **Riêng tư:** chỉ lưu `question_id`, ngày tạo, tiêu đề, nhãn và trích đoạn ≤ 200 ký tự; không lưu tên tài khoản, ảnh đại diện hay link hồ sơ.

## 2. Đọc trước, đếm sau
*(CP3: điền sau khi tải.)*

## 3. Kết quả
*(CP3: chưa chạy.)*

## 4. ≥5 ví dụ cụ thể
*(CP3.)*

## 5. Giới hạn của data
- Người hỏi tự chọn (chỉ người chủ động đăng câu hỏi), phần lớn nói tiếng Anh, không phải người Việt 25–60 tuổi.
- Data cho biết người ta hỏi gì, không cho biết họ làm gì sau đó.
→ Kiểm lại bằng: nghiên cứu đã công bố tại Việt Nam (Miyakawa 2017, Khánh Hòa: 254/376 = 67,6% không hiểu hoặc chưa từng nghe về tiểu đường; xem `evidence/summary.md`) và phỏng vấn bổ sung (`evidence/interviews/`), nếu nhóm hẹn được người.
