# Phiếu đọc tay nhãn data mining (HUMAN_ACTIONS H7)

**File cần điền:** `evidence/mining_labels.csv`, 125 dòng. Mỗi dòng có link câu hỏi gốc, 4 cột nhãn theo luật (`L1_…`–`L4_…`, do script gắn) và 4 cột `*_tay` **đang trống**.

> **Giữ nguyên kết quả đã báo:** 8/125 (6,4%) theo luật chốt trước (commit `79b647b`). Đọc tay chỉ **thêm** một số thứ hai "sau đọc tay"; không đổi định nghĩa nhãn, không đổi tag hay khoảng thời gian lấy mẫu để được tỉ lệ cao hơn. Muốn lấy mẫu khác thì ghi thành lần đào mới, chốt cách đếm trước, báo cả hai.

## Cách làm (2 người, đọc độc lập rồi đối chiếu)
1. Mở `link` từng dòng, đọc **tiêu đề + thân câu hỏi** (không đọc câu trả lời).
2. Điền 1/0 vào `L1_so_cua_minh_tay`, `L2_hoi_dien_giai_tay`, `L3_hoi_buoc_tiep_tay`, `L4_boi_canh_do_tay` theo định nghĩa **đã chốt** ở `evidence/data-mining.md` mục 1 (không đổi định nghĩa). Chỗ không chắc ghi vào `ghi_chu_tay`.
3. Không sửa các cột nhãn của luật, không xoá dòng.
4. Chạy `python evidence/mine_stackexchange.py --offline`. Phần "sau đọc tay" in số mới. Ghi **cả hai số** (luật và đọc tay) vào `evidence/data-mining.md` mục 3 và `evidence/summary.md`.
5. Nếu hai người đọc lệch nhau: ghi số câu lệch (x/125) trước khi thống nhất.

## Chỗ agent đã thấy có thể sai (đọc lại, đừng chép theo)
- Có thể dương tính giả: q/9261 (xét nghiệm H. pylori), q/20931 (câu về cơ sở dữ liệu), q/31204, q/31377 (mô tả nghiệm pháp), q/13169 (ăn đường, không phải đo).
- Có thể âm tính giả: q/5533 (nêu fasting 110 mg/dL của mình, hỏi vì sao sáng cao hơn).

## Không làm
- Không lưu tên tài khoản, ảnh hay link hồ sơ người hỏi.
- Không chép nguyên thân câu hỏi vào repo (chỉ trích ≤ 200 ký tự, ghi nguồn CC BY-SA).
