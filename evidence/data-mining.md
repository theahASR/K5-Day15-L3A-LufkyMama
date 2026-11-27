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
- Lần tải: 28/11/2026 00:48 ICT, API trả **N = 125** câu hỏi duy nhất (hợp tag `diabetes` + `blood-sugar`), câu sớm nhất 2015. File nhãn: `evidence/mining_labels.csv` (chỉ id, ngày, tiêu đề, nhãn, trích đoạn ≤ 200 ký tự, link câu hỏi; không có tên tài khoản).
- Đọc qua các câu được luật gắn nhãn, thấy các *kiểu* câu hỏi: (a) người tự đo và không hiểu số của mình (5533, 3032, 23845); (b) hỏi nguy cơ vì tiền sử gia đình (866); (c) người đã chẩn đoán hỏi mẹo/thực phẩm chức năng (1595); (d) phần lớn là câu hỏi kiến thức, cơ chế, nghiên cứu.
- **Đặc điểm của nguồn:** Medical Sciences SE đóng các câu xin tư vấn y tế cá nhân (personal medical advice). Vì vậy tập này **lọc bỏ đúng kiểu câu hỏi** mà pain mô tả. Đây là lệch chọn mẫu lớn nhất của nguồn.

## 3. Kết quả (luật từ khoá chốt trước — commit `79b647b`, chạy lại: `python evidence/mine_stackexchange.py`)

| Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|
| L1 nêu chỉ số đo của mình/người thân kèm số | 4/125 | 3,2% | 1/4 là dương tính giả (31377: mô tả nghiệm pháp, không phải số của mình) |
| L2 hỏi số đó có nghĩa gì / bình thường không | 7/125 | 5,6% | Có dương tính giả rõ (9261 xét nghiệm H. pylori; 20931 câu về cơ sở dữ liệu; 31204) |
| L3 hỏi bước tiếp theo | 1/125 | 0,8% | |
| L4 không rõ bối cảnh đo / đơn vị | 1/125 | 0,8% | 13169 là dương tính giả (hỏi về ăn đường, không phải đo) |
| **L2 ∪ L3 (pain "không biết số nghĩa gì / làm gì tiếp")** | **8/125** | **6,4%** | Số chính, theo luật đã chốt |
| L1 ∩ (L2 ∪ L3) | 0/4 | — | Luật bỏ sót: 5533 nêu "fasting glucose (110mg/dl)" và hỏi vì sao cao sau khi ngủ dậy nhưng không khớp mẫu câu L2 |

**Độ tin cậy của luật:** agent đọc lại 13 câu được gắn nhãn và thấy ít nhất 5 câu gắn sai (9261, 20931, 31204, 31377, 13169), đồng thời luật bỏ sót ít nhất một câu đúng (5533). Đây là agent đọc lại, **không phải người đọc tay**. Việc đọc tay cả 125 câu theo mục 1(b) vẫn chờ thành viên (HUMAN_ACTIONS H7). Đọc xong thì điền cột `*_tay` rồi chạy `python evidence/mine_stackexchange.py --offline`.

**Kết luận trung thực:** trên nguồn này, tỉ lệ câu hỏi mang đúng pain là **thấp (8/125 = 6,4% theo luật)**. Số này **không ủng hộ** giả thuyết CP1 "≥60% người tự tra cứu không biết bước tiếp theo". Lý do chính có lẽ là nguồn cấm câu xin tư vấn cá nhân, nên số này không ước lượng được tỉ lệ ở người dùng mục tiêu. Nó chỉ cho thấy pain có xuất hiện, với ví dụ thật bên dưới.

## 4. ≥5 ví dụ nguyên văn (trích ≤ 200 ký tự, bỏ tên; nội dung CC BY-SA 4.0, nguồn là link câu hỏi)

1. "After a recent blood test that showed elevated fasting glucose (110mg/dl) and elevated triglycerides (~335mg/Dl), I got myself an Accu-check glucose tester and started regular testing to try to figure…" — https://medicalsciences.stackexchange.com/q/5533 (2016)
2. "I bought myself a $15 blood sugar testing kit the other day because I've been experiencing some health things that are rare for me…" — https://medicalsciences.stackexchange.com/q/3032 (2015)
3. "As part of military and other physicals, I have had blood glucose levels come back several times with high levels…" — https://medicalsciences.stackexchange.com/q/91 (2015)
4. "Almost everytime I measure the blood glucose levels in both right and left hands there's always a difference of 10-20mg/dL." — https://medicalsciences.stackexchange.com/q/23845 (2020)
5. "My grandmother has has type 1 diabetes for more than 25 years… My mother died when I was a kid, so I don't have any information about her health. I want to know my what are my…" — https://medicalsciences.stackexchange.com/q/866 (2015)
6. "My A1C has gone down from 13% to 9%, I noticed these cinnamon pills in a local store that claime[d]…" — https://medicalsciences.stackexchange.com/q/1595 (2015)

Ví dụ 1–4: người tự đo đường huyết bằng máy tại nhà rồi không biết đọc kết quả (lúc đo, sai số máy, ngưỡng). Đây đúng là bước "tự đọc chỉ số tại nhà" trong pain. Ví dụ 6 khớp với câu thử B09 (mẹo/thực phẩm chức năng).

## 5. Giới hạn của data
- Nguồn **cấm câu xin tư vấn cá nhân** → đánh giá thấp tỉ lệ pain; người hỏi tự chọn, chủ yếu nói tiếng Anh, không phải người Việt 25–60 tuổi.
- Luật từ khoá có cả dương tính giả lẫn âm tính giả (mục 3); chưa có người đọc tay.
- Data cho biết người ta hỏi gì, không cho biết họ làm gì sau đó.
→ Kiểm lại bằng: phỏng vấn ≥3 người 25–60 tuổi ngoài nhóm (bộ câu hỏi `evidence/interviews/GUIDE.md`); đối chiếu nghiên cứu công bố tại Việt Nam (Miyakawa 2017, `evidence/summary.md`).
