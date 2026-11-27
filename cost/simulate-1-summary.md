# Tóm tắt mô phỏng simulate-1@20261128-012440

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| mot_lan_sau_kham | 30 | 2 | 3757 | 704 | 2.0 | 14.9 |
| tu_do_tai_nha | 17 | 2 | 3827 | 701 | 2.1 | 14.8 |
| hoi_ho_nguoi_than | 3 | 3 | 5414 | 960 | 3.0 | 21.3 |

Tỉ lệ đạt dùng để tính: 29/30 (97%) — lượt run-2@20261128-011951

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/grading/run-2-agent-prelim.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (1.000 người) | Chi phí / tháng — cơ sở (5.000 người) | Chi phí / tháng — cao (20.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.0020 | $0.0021 | $0.0010 | $4.17 | $20.83 | $83.31 | $0.0042 |
| gemini-3.8-flash (vào 1.5 · ra 7.5 $/1M) | $0.0112 | $0.0116 | $0.0056 | $22.81 | $114.05 | $456.18 | $0.0228 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (2.1) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gemini-3.1-flash-lite. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
