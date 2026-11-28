# HUMAN ACTIONS — việc cần thành viên làm (agent không tự làm được / không được làm)

| ID | Việc | Ai | Gỡ blocker khi | Hạn | Trạng thái |
|---|---|---|---|---|---|
| H1 | `git push origin LufkyMama` để chốt CP2 (metric_spec, benchmark, §7) | Đội trưởng | Commit `98024ba` có trên GitHub trước 19:30 ICT 27/11 | 19:30 27/11 | DONE (push lên main 19:25 ICT) |
| H2 | Nộp form CP2 (nội dung ở `docs/CP2_READINESS.md`) | Đội trưởng | Có xác nhận nộp | 19:30 27/11 | OPEN |
| H3 | **API key model thật**: tạo `.env` từ `.env.example` (`MODEL_PROVIDER=gemini`/`openai`/`anthropic`, `MODEL_NAME`, `API_KEY`). Không commit `.env` | Minh / Tú | `python run.py eval --try` báo "Nối model được", token > 0 | Trước CP3 10:00 28/11 | DONE — key Gemini đã có 28/11; MODEL_NAME=gemini-3.1-flash-lite |
| H4 | Xác nhận phân công trong `TEAMS.md` + `canvas.md` dòng 7 | Cả nhóm | Mỗi người đồng ý dòng của mình | CP3 | OPEN |
| H5 | Hai người chấm độc lập 5 output (phiếu `eval/grading/`), ghi kết quả vào `eval/README.md` mục 3 | 2 thành viên | Khớp ≥4/5 | CP4 | OPEN (phiếu: eval/grading/GRADING_SHEET.md) |
| H6 | Duyệt bản chấm sơ bộ của agent (`eval/grading/run-N-agent-prelim.csv`) rồi chấm cột `pass` cho `eval/run-1.csv`, `run-2.csv` theo `eval/metric_spec.yaml` | Minh + Mạnh | `python run.py score` in % | CP3 / CP4 | DONE (28/30 · 29/30, Hồ Đức Mạnh xác nhận, commit `3c75b97`) |
| H7 | Đọc tay nhãn data mining (`evidence/mining_labels.csv`) | Thế Anh / Mạnh | Sửa nhãn xong, số cuối cập nhật | CP3 | OPEN |
| H8 | (Tuỳ chọn, R1 nguồn thứ 2) Phỏng vấn ≥3 người 25–60 tuổi ngoài nhóm, mỗi người 1 file `evidence/interviews/P1.md`… | Mạnh | Có ghi chép thật | CP3–CP4 | OPEN |
| H9 | Quay video 30 giây chạy AI thật, upload "Không công khai", dán link vào README | Mạnh | Link mở được ở cửa sổ ẩn danh | CP3 10:00 28/11 | DONE (https://drive.google.com/file/d/1UdxZRih6MQq_qQkwUHtvIF-jtcfTa8h6/view?usp=sharing) |
| H10 | (Bonus) ≥2 người ngoài nhóm dùng thử, ghi `validation/log.md` | Mạnh | Log đủ cột | CP4 | OPEN |
| H11 | Mỗi người viết `reflection/<ten>.md` | Cả nhóm | 4 file | 23:59 28/11 | OPEN |
| H12 | Nộp CP3, CP4 | Đội trưởng | Xác nhận nộp | 10:00 / 14:30 28/11 | OPEN |
| H13 | **Push** các commit local lên GitHub | Đội trưởng / Mạnh | Push lên `main` | Trước 10:00 28/11 | DONE (`3c75b97` trên `origin/main`) |
| H14 | **Quyết định chấm D1**: câu "bạn đang ở vùng tiền tiểu đường" có là "khẳng định chẩn đoán"? Ghi `eval/grading/GRADING_DECISIONS.md` | Cả nhóm / Mạnh | Có quyết định + lý do | Trước khi chấm | DONE — chọn R0 (Hồ Đức Mạnh, 28/11 09:42 ICT) |
| H15 | Chấm 60 output → `final_run-N.csv` → `import_verdicts.py --apply` → `python eval/finalize_results.py` | Mạnh | `eval/finalize_results.py` in "Chế độ CONFIRMED" | CP3 (lượt 1) / CP4 (lượt 2) | DONE — CONFIRMED (`28/30` · `29/30`, còn in lại `demo-slides.pdf` từ `slides/slides.html` trước CP4) |
