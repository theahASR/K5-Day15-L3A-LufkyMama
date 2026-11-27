# Dàn slide → lấy số từ file nào

Nguồn HTML: `slides/slides.html` → xuất `demo-slides.pdf` (8 trang) bằng Chrome headless:
`"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf=demo-slides.pdf slides/slides.html`

| # | Trang | Có gì | Số lấy từ | Xong |
|---|---|---|---|---|
| 1 | Người dùng & pain | 8/125 (6,4%) ngược giả thuyết · 67,6% (Miyakawa, tham khảo) · 2 trích nguyên văn | `evidence/summary.md` | ☑ |
| 2 | Vì sao chọn bài này | 4 hướng, 3 loại · impact 150.000 phút/tháng *(tự ước tính)* | `spec.md` §2 | ☑ |
| 3 | Giải pháp | luồng chặn trước → căn cứ → AI → chặn sau · không làm · vì sao workflow · G10 · AUC 0,787 | `spec.md` §4, `ml/metrics.json` | ☑ |
| 4 | Demo live | B05 thường · B08 khó · B15 an toàn · câu lạ | `eval/benchmark.csv`, `eval/run-2.csv` | ☑ (link video chờ H9) |
| 5 | Đánh giá | 7 metric lượt 1 → 2 · lỗi B30/B12 · cải tiến · còn B22 | `eval/report.md` | ☑ (chấm sơ bộ) |
| 6 | Chi phí | chi phí / task thành công · 3 kịch bản · 2 model · so impact | `cost/cost-estimate.md`, `cost/simulate-1-summary.md` | ☑ |
| 7 | Kết luận | ITERATE + lý do | trang 1, 5, 6 | ☑ |
| 8 | Thêm 1 tuần | 5 việc trỏ về lỗi còn lại | `eval/report.md` mục 5 | ☑ |

## Ai nói trang nào (đề xuất — nhóm tự chốt)

| Trang | Người nói | Câu giám khảo hay hỏi, phải trả lời được |
|---|---|---|
| 1–2 | Hồ Đức Mạnh | Vì sao 8/125 thấp mà vẫn làm? Impact lấy số ở đâu? |
| 3 | Nguyễn Anh Tú | Vì sao workflow chứ không phải agent? Lỗi nguy hiểm nhất là gì, chặn ở đâu? |
| 3 (ML) | Bùi Thế Anh | Vì sao chỉ cho điểm khi là nữ + OGTT? AUC 0,787 nghĩa là gì, recall 0,52 thì sao? |
| 4–6 | Vũ Nguyễn Hoàng Minh | Chi phí / task thành công tính thế nào? Chấm pass ra sao? |
| 7–8 | Cả nhóm | Go / iterate / stop vì sao? |

## Script nói (~5 phút)
1. "Người có một con số đường huyết trong tay nhưng không biết nó nghĩa là gì. Ví dụ thật trên diễn đàn: tự đo hai tay lệch 10–20 mg/dL, không biết số nào đúng. Đếm 125 câu hỏi công khai, chỉ 8 câu hỏi đúng kiểu này, ngược giả thuyết của nhóm. Lý do: diễn đàn cấm câu tư vấn cá nhân. Nên nhóm ghi rõ pain chưa được định lượng."
2. "Ba hướng bị loại… impact 30 phút/người/tháng, toàn tự ước tính."
3. "Code chặn cấp cứu trước khi AI nói gì. Model ML chỉ cho điểm khi dữ liệu người dùng giống dữ liệu train. AI chỉ được dùng căn cứ có mã nguồn."
4. Demo 3 câu + câu lạ.
5. "Chuẩn đạt chốt từ tối qua, không sửa. Lượt 1: 28/30, lỗi đau nhất là xếp loại đường huyết của người 15 tuổi bằng ngưỡng người lớn. Sửa một chỗ, lượt 2: 29/30."
6. Chi phí.
7. "Iterate: hệ thống an toàn và rẻ, nhưng chưa chứng minh được pain bằng số của người dùng thật."
