# Đề xuất cải tiến — CHỈ GHI, CHƯA LÀM

Mọi lượt đánh giá chạy thêm sau này ghi thành `run-3`, `run-4`… và một dòng mới trong `eval/README.md` mục 5 + `spec.md` §10. **Không thay thế lượt 1, lượt 2.**

## 1. Chính sách trả lời y khoa chặt hơn: diễn giải con số ≠ chẩn đoán người
- **Quy tắc:** chỉ được nói về **kết quả xét nghiệm** ("Kết quả 110 mg/dL lúc đói nằm trong khoảng 100–125 mg/dL mà CDC xếp là tiền tiểu đường [KB01]"), không nói về **người** ("bạn đang ở vùng tiền tiểu đường", "bạn bị…").
- **Cài đặt dự kiến:** thêm luật vào system prompt + `validate_response` chặn mẫu câu "(bạn|anh|chị|bố…) (đang )?(ở|thuộc|nằm trong) (vùng|ngưỡng|nhóm) (tiền )?tiểu đường" → sửa 1 lần → mẫu an toàn.
- **Đo:** chạy thành `run-3` trên cùng 30 câu, chấm theo cách hiểu đã chốt ở `eval/grading/GRADING_DECISIONS.md`.

## 2. Kiểm định an toàn y khoa độc lập
- Một bác sĩ / dược sĩ ngoài nhóm duyệt: 13 đoạn KB (`data/knowledge_base.json`), luật cấp cứu (`check_red_flags`: ngưỡng 250 mg/dL kèm triệu chứng, < 70, < 55), và mẫu an toàn (`agent._template`).
- Ghi người duyệt, ngày, chỗ sửa vào `data/DATA_CARD.md` D2.
- Thêm câu thử cấp cứu nhiều dạng (sai chính tả, kể về người nhà, giấu cuối đoạn dài), theo gợi ý track B.

## 3. Recall và chọn ngưỡng
- Hiện tại: LR recall 0,52 @0,5; 0,83 @0,2 (ngưỡng dải "trung bình" của app); 9/54 ca dương tính rơi vào "thấp" (`FINAL_QA_AUDIT.md` 1.3).
- Đề xuất: chọn ngưỡng dải theo mục tiêu recall đặt trước (vd ≥ 0,90) bằng cross-validation **chỉ trên tập train**, rồi báo trên tập test một lần; cân nhắc Random Forest (AUC 0,819) kèm giải thích; báo calibration (Brier, reliability plot).
- Không đổi model đang dùng cho tới khi có lượt đánh giá mới ghi riêng.

## 4. Đánh giá trên quần thể đại diện
- Pima (phụ nữ gốc Pima, Mỹ, 1960–1980) không đại diện người Việt. Cần dữ liệu người Việt có OGTT/FPG/HbA1c + kết cục (vd hợp tác bệnh viện, có phê duyệt đạo đức), hoặc bỏ điểm ML và chỉ dùng ngưỡng CDC/WHO + mốc BMI châu Á.
- Tối thiểu: báo AUC, recall, precision theo giới và nhóm tuổi.

## 5. Bằng chứng pain mạnh hơn
- Phỏng vấn ≥ 5 người 25–60 tuổi ngoài nhóm vừa có kết quả đường huyết (`evidence/interviews/GUIDE.md`), mỗi người 1 file, đếm x/n.
- Nguồn data tiếng Việt cho phép tư vấn cá nhân: mục hỏi đáp công khai của bệnh viện/nhà thuốc, **chỉ khi điều khoản cho phép**; chốt cách đếm trước, giống `evidence/data-mining.md`.
- Đo số phút thật từ lúc có số đến lúc biết làm gì, để thay các thừa số *(tự ước tính)* trong impact (`spec.md` §2).

## 6. So sánh với ChatGPT (hoặc chatbot tổng quát khác)
- Chạy cùng 30 câu qua một chatbot tổng quát (không system prompt riêng), lưu output nguyên văn thành `eval/baseline-chatgpt.csv`, kèm ngày, model, cách gọi.
- Chấm theo cùng `metric_spec.yaml`, cùng người chấm, không biết output nào của hệ thống nào (làm mù).
- Báo khác biệt Safety, Grounded, Context. Đây là bằng chứng cho §3 "Giải pháp tương tự", hiện ghi "chưa kiểm".
