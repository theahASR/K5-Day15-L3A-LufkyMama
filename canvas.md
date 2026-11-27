# Canvas — LufkyMama · Track B

> Điền ở guide bước 1.4. CP1 17:00 Thứ Sáu 27/11: nộp bản đầu, đủ 7 dòng (dòng 4 được ghi giả thuyết + nguồn sẽ kiểm).
> CP2 19:30 Thứ Sáu 27/11: cập nhật (số bằng chứng đầu, lát cắt đã chốt) và điền dòng "Đã đổi gì so với CP1".
> Track F: chép thêm thẻ đề của nhóm (khung trong file track F) xuống dưới bảng này.

| # | Dòng | Nhóm điền |
|---|---|---|
| 1 | Track + lát cắt | Track B (Y tế) — Dự đoán nguy cơ bệnh tiểu đường từ các chỉ số sức khỏe đầu vào và tích hợp chatbot AI tư vấn dinh dưỡng, lối sống ngay sau khi có kết quả. |
| 2 | Người dùng chính | Người trưởng thành (25–60 tuổi) có chỉ số sức khỏe/xét nghiệm đường huyết cơ bản hoặc thuộc nhóm nguy cơ muốn tự sàng lọc sớm tiểu đường tại nhà. |
| 3 | Pain: ai — đang làm gì — vướng đâu — hậu quả | Người trưởng thành có nguy cơ tiểu đường đang tự đọc các chỉ số sức khỏe tại nhà nhưng khó đánh giá mức độ rủi ro và thiếu hướng dẫn ăn uống, sinh hoạt cụ thể, dẫn đến chủ quan và bỏ lỡ giai đoạn phòng ngừa sớm. |
| 4 | Bằng chứng đầu — CP1: giả thuyết + nguồn sẽ kiểm · CP2: số đầu tiên + 1 trích dẫn | Số đầu (nghiên cứu công bố, chưa phải data của nhóm): khảo sát dân cư người lớn 20–70 tuổi tại Khánh Hòa, tháng 12/2014 — **254/376 (67,6%)** "either did not understand or had never heard of DM", và chỉ **12/27 (44%)** người mắc tiểu đường biết mình mắc (Miyakawa et al., *BMC Public Health* 2017;17:298, doi:10.1186/s12889-017-4208-9). Giới hạn: một tỉnh, tự báo cáo, đo hiểu biết chung chứ chưa đo trực tiếp việc đọc chỉ số. Giả thuyết CP1 (≥60% người tự tra chỉ số không biết bước tiếp theo) **chưa kiểm**; đang làm data mining câu hỏi công khai (evidence/data-mining.md) để có x/N riêng ở CP3. |
| 5 | **Lát cắt** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả) | Người dùng trưởng thành nhập các chỉ số sức khỏe cơ bản để sàng lọc nguy cơ tiểu đường, hệ thống dự đoán mức độ nguy cơ và kích hoạt chatbot AI tư vấn cá nhân hóa chế độ ăn uống, vận động kèm khuyến nghị thăm khám ngay sau khi trả kết quả. |
| 6 | AI tự làm đến đâu + 1 dòng lý do: sai thì ai chịu gì | AI chỉ sàng lọc nguy cơ tham khảo và tư vấn lối sống/dinh dưỡng, KHÔNG chẩn đoán thay bác sĩ hay kê đơn thuốc — lý do: nếu dự đoán âm tính giả hoặc tư vấn sai thuốc, người bệnh có thể chậm trễ điều trị và gặp biến chứng nguy hiểm. |
| 7 | Phân công có tên | Vũ Nguyễn Hoàng Minh (đội trưởng): Tech Lead, backend, tích hợp, evaluation · Bùi Thế Anh: data mining, mô hình ML · Nguyễn Anh Tú: chatbot AI, knowledge base, prompt · Hồ Đức Mạnh: nghiên cứu người dùng, giao diện, demo |
| — | *(CP2)* Đã đổi gì so với CP1 | (1) Chốt lát cắt: workflow cố định Kiểm hồ sơ → ML sàng lọc → tra kiến thức có nguồn → LLM tư vấn → kiểm an toàn (spec §4). (2) Đọc lại Pima: cột Glucose là đường huyết 2 giờ sau nghiệm pháp dung nạp glucose (OGTT), không phải lúc đói → sửa B01–B04 trong benchmark và giới hạn phạm vi model (data/DATA_CARD.md). (3) Bằng chứng: đổi từ "phỏng vấn 5–10 người" sang ưu tiên data mining câu hỏi công khai + nghiên cứu đã công bố, phỏng vấn làm bổ sung (evidence/). |
