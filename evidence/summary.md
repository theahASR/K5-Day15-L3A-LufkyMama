# Tổng hợp bằng chứng pain

> Cập nhật 28/11/2026. Chấm ở rubric R1. Chỉ ghi số đã có; phần chưa làm ghi rõ.

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data: 125 câu hỏi công khai Medical Sciences Stack Exchange, cách đếm chốt trước, script chạy lại được, 6 ví dụ nguyên văn | **Đạt về cách làm** (x/N, chọn mẫu và đếm ghi trước, script trong repo, ≥5 ví dụ). Kết quả **ngược giả thuyết** (mục 2). Chưa có người đọc tay | `evidence/data-mining.md` · `evidence/mine_stackexchange.py` · `evidence/mining_labels.csv` |
| Phỏng vấn (≥3 người ngoài nhóm) | ☐ Chưa làm. Đã có bộ câu hỏi | `evidence/interviews/GUIDE.md` |
| Khảo sát (≥20 người) | ☐ Không làm | — |
| *Tham khảo (không phải nguồn của nhóm):* nghiên cứu công bố tại Việt Nam | — | mục 4 |

## 2. Số chính
- **Đào data:** 8/125 câu hỏi (6,4%) hỏi chỉ số có nghĩa gì hoặc bước tiếp theo, theo luật từ khoá chốt trước. 4/125 (3,2%) nêu chỉ số đo của chính mình. Luật có ≥5 dương tính giả và ≥1 âm tính giả theo lần agent đọc lại (chưa có người đọc tay). Nguồn cấm câu xin tư vấn cá nhân nên tỉ lệ này **không** đại diện cho người dùng mục tiêu.
- **Phỏng vấn:** chưa có.

## 3. ≥5 ví dụ nguyên văn (nguồn: Medical Sciences SE, CC BY-SA 4.0, đã bỏ tên)
1. "After a recent blood test that showed elevated fasting glucose (110mg/dl)… I got myself an Accu-check glucose tester and started regular testing to try to figure…" — q/5533
2. "I bought myself a $15 blood sugar testing kit the other day because I've been experiencing some health things that are rare for me…" — q/3032
3. "I have had blood glucose levels come back several times with high levels…" — q/91
4. "Almost everytime I measure the blood glucose levels in both right and left hands there's always a difference of 10-20mg/dL." — q/23845
5. "My mother died when I was a kid, so I don't have any information about her health. I want to know my what are my…" — q/866
6. "My A1C has gone down from 13% to 9%, I noticed these cinnamon pills in a local store that claime[d]…" — q/1595

## 4. Các nguồn có khớp nhau không
- **Nghiên cứu tham khảo (không phải nguồn của nhóm):** Miyakawa et al., *BMC Public Health* 2017;17:298 (doi:10.1186/s12889-017-4208-9). Khảo sát dân cư 20–70 tuổi tại Khánh Hòa, tháng 12/2014, N = 376: **254/376 (67,6%)** không hiểu hoặc chưa từng nghe về tiểu đường, chỉ **12/27 (44%)** người mắc biết mình mắc. Giới hạn: một tỉnh, tự báo cáo, đo hiểu biết chung chứ không đo việc đọc chỉ số.
- **Lệch:** nghiên cứu Việt Nam cho thấy thiếu hiểu biết phổ biến (67,6%), trong khi đào data chỉ thấy 6,4%. Giải thích: nguồn data là diễn đàn tiếng Anh, cấm câu tư vấn cá nhân, người hỏi tự chọn và có hiểu biết y khoa cao hơn. Hai số đo hai thứ khác nhau và trên hai quần thể khác nhau, nên **chưa có nguồn thứ hai của nhóm kiểm lại được**.

## 5. Kết luận
- Pain "tự đọc chỉ số tại nhà mà không biết nghĩa và bước tiếp theo" **có xuất hiện thật** (ví dụ 1–4) nhưng **chưa được định lượng ở người dùng mục tiêu**. Số đào data thấp và đi ngược giả thuyết CP1 (≥60%).
- Quyết định: giữ lát cắt, nhưng **không dùng 6,4% hay 67,6% làm "số người gặp pain"** trong công thức impact; impact ở `spec.md` §2 ghi rõ phần *(tự ước tính)*.
- Việc cần làm để mạnh hơn: phỏng vấn ≥3 người 25–60 tuổi ngoài nhóm (HUMAN_ACTIONS H8); đọc tay 125 nhãn (H7).
