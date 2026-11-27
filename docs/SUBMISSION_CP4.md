# Gói nộp CP4 — 14:30 Thứ Bảy 28/11/2026

Đối chiếu README BTC mục CP4 + guide 4.4 + rubric Phần 0.

| # | Yêu cầu BTC | Bằng chứng | Trạng thái |
|---|---|---|---|
| 1 | Phòng demo + link repo | `spec.md` dòng 1 còn `Phòng __ · Zone __` | Đội trưởng điền |
| 2 | Tích 7 hạng mục bắt buộc | `README.md` bảng 7 hạng mục | 6/7 đủ file; mục 7 thiếu link video |
| 3 | Kết quả lượt 1 → lượt 2 | `run-1@20261128-010841` (commit `4eb2c01`) → `run-2@20261128-011951` (commit `0349cb1`), cùng 30 câu, cùng model; cải tiến commit `23013c6` | **SƠ BỘ**: 28/30 → 29/30 (cách hiểu nới) hoặc 26/30 → 25/30 (cách hiểu chặt, KHÔNG ĐẠT). Chờ người chấm |
| 4 | Chi phí / task thành công ở kịch bản cơ sở + tên model | `cost/cost-estimate.md`, `cost/simulate-1.csv` (50 phiên, seed 42, 0 lỗi, `simulate-1@20261128-012440`, commit `94b783d`) | $0,0021 (`gemini-3.1-flash-lite`, **tỉ lệ đạt sơ bộ**; cách hiểu chặt → $0,0025). `gemini-3.8-flash` $0,0116 là **ước tính** |
| 5 | `demo-slides.pdf` ở gốc + link video dự phòng | `demo-slides.pdf` 8 trang (slide 5–7 ghi rõ SƠ BỘ + cách hiểu chặt) | PDF **ĐỦ**; video **THIẾU** |
| 6 | Lượt 2 + `eval/report.md` + `eval/README.md` | có | Số sơ bộ, đã dán nhãn |
| 7 | `spec.md` đủ §0–§9 | có §0–§10; §7 không đổi | **ĐỦ** |
| 8 | Tự khai phần chưa xong | mục dưới | — |
| B | *(Bonus)* `validation/log.md` | trống; kịch bản `validation/SCRIPT.md` | Không có người thử |

## Điều kiện cứng (rubric Phần 0)
| # | Điều kiện | Trạng thái |
|---|---|---|
| 1 | AI thật ở quyết định trung tâm | Đạt |
| 2 | Bằng chứng pain ≥1 nguồn đạt ngưỡng | Có rủi ro (xem CP3 #1) |
| 3 | ≥20 câu + % đạt | 30 câu; **% đạt chỉ là sơ bộ** cho tới khi người chấm điền `pass` |
| 4 | `demo-slides.pdf` | Đạt |

## Sau khi người chấm xong (trước 14:30)
```
python eval/grading/import_verdicts.py --run 2 --final eval/grading/final_run-2.csv --apply
python eval/finalize_results.py                    # cập nhật report, spec §8 (khối tự sinh), cost, slide 5–7, demo-slides.pdf
python run.py simulate --rate-from eval/run-2.csv --wait 4   # chỉ khi tỉ lệ đạt lượt 2 đổi; ra simulate-2, giữ simulate-1
python run.py check
```

## Git — lệnh an toàn (remote lúc kiểm: `origin/main` = `origin/LufkyMama` = `f2c61c6`)
```
git fetch origin
git status                                     # phải sạch
git rev-list --count LufkyMama..origin/main    # phải in 0 — nếu > 0: DỪNG, xem dưới
git log --oneline origin/main..LufkyMama       # xem lại các commit sẽ đẩy
git push origin LufkyMama
git push origin LufkyMama:main                 # chỉ fast-forward; bị từ chối nếu main đã đổi
```
Nếu `main` đã có commit mới: **không** dùng `--force`. Mở PR: `gh pr create --base main --head LufkyMama --title "CP3/CP4"`, xử lý xung đột trong PR, rồi merge.

## Điền form CP4
- Phòng + link repo · 7 hạng mục (ghi rõ video nếu chưa có).
- Lượt 1 → lượt 2: số **sau khi người chấm** (nếu chưa: ghi "sơ bộ 28/30 → 29/30; cách hiểu chặt 26/30 → 25/30, chưa chốt").
- Chi phí / task thành công cơ sở: $0,0021, `gemini-3.1-flash-lite` (ghi "theo tỉ lệ đạt sơ bộ" nếu chưa chấm).
- `demo-slides.pdf` · link video dự phòng.
- Phần chưa xong: người chấm, 2 người chấm độc lập, đọc tay nhãn, phỏng vấn, người dùng thử, kiểm định y khoa độc lập.
