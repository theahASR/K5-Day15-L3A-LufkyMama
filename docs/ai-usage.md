# Khai báo dùng AI

Luật của đề: dùng AI thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó 0 điểm**. Mỗi thành viên phải đọc lại phần có tên mình.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử (`codebase/agent.py`, `tools.py`, `ai.py`) | Claude Code (coding agent) | Viết workflow, 9 công cụ, nối Gemini; sửa lỗi đọc chỉ số trước lượt 1 | **Chưa có người duyệt** — cần đọc lại trước demo | Minh (tích hợp), Tú (prompt) |
| Prompt (`SYSTEM` trong `agent.py`) | Claude Code | Viết bản đầu 7 luật và một lần sửa trước lượt 2 | Chưa duyệt | Tú |
| ML (`ml/train.py`) | Claude Code | Viết script train LR/RF, xuất `model.json` | Chưa duyệt; số liệu ở `ml/metrics.json` do script tính | Thế Anh |
| Knowledge base | Claude Code + agent tra web | Tự viết lại 13 đoạn từ CDC/NIDDK/WHO, agent mở từng URL để đối chiếu (27/11/2026) | Chưa có thành viên kiểm từng đoạn với nguồn | Tú |
| Đào data (script, nhãn) | Claude Code | Viết `evidence/mine_stackexchange.py` với luật từ khoá chốt trước; agent đọc lại 13 câu được gắn nhãn | **Chưa có người đọc tay** 125 nhãn (HUMAN_ACTIONS H7) | Thế Anh |
| Phỏng vấn / khảo sát | — | Chỉ soạn bộ câu hỏi `evidence/interviews/GUIDE.md` | — | Mạnh |
| Câu thử | Claude Code | B01–B15: nhóm viết (CP2); agent sửa B01–B04 vì Glucose Pima là OGTT. B16–B30: agent soạn từ dòng Pima, câu hỏi Stack Exchange (dịch) và kịch bản tự viết | Mỗi câu có `source`; chưa có người duyệt B16–B30 | Minh |
| Chấm cột `pass` | Claude Code | **Chấm sơ bộ** cả hai lượt ở `eval/grading/run-N-agent-prelim.csv` | Cột `pass` trong `eval/run-N.csv` để trống cho người chấm; 2 người chấm độc lập 5 output (`eval/grading/GRADING_SHEET.md`) | Minh + 1 người |
| Mô phỏng chi phí | Claude Code | Điền `cost/personas.yaml` (số *tự ước tính*), chạy `simulate` | Chưa duyệt | Minh |
| Slide, văn bản (spec, README, báo cáo) | Claude Code | Soạn bản đầu từ số trong repo | Chưa duyệt | Mạnh (slide) |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát, người dùng thử; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
