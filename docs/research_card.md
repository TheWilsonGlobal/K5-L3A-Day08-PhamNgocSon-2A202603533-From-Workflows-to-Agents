# Research card

Phần này nối tiếp phần mini research ở buổi lý thuyết (slide 62–63). Chọn **một** câu R1–R4, điền 6 dòng, rồi biến nó thành **một ablation** chạy được trong lab: giữ nguyên model (MockLLM), tool, seed, corpus và giá, chỉ thay đổi một biến.

| Câu | Nguồn (thư viện tham khảo, slide 68–69) | Câu hỏi gợi ý cho lab |
| --- | --- | --- |
| R1 · Scaling | Google Research 2026, *Towards a Science of Scaling Agent Systems* | Task claims chủ yếu tuần tự hay song song được? Dự đoán thêm investigator sẽ làm pass rate và cost/success thay đổi thế nào. |
| R2 · Failure taxonomy | MAST, NeurIPS 2025, *Why Do Multi-Agent LLM Systems Fail?* | Các trial fail của swarm (seed 55) thuộc nhóm nào: lỗi giao việc, lệch mục tiêu, hay lỗi kiểm chứng? |
| R3 · Architecture choices | AgentArch, AACL 2026 | Nếu đổi topology mà giữ nguyên mọi thứ khác, biến nào phải cố định để kết luận còn đúng? |
| R4 · Evaluation confounders | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency* | Làm sao chứng minh chênh lệch giữa A/B/C/D là do topology, không phải do prompt, tool hay seed? |

## Phiếu của nhóm

Điền vào cột cuối. Không xóa hai cột đầu.

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R3 · Architecture choices |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | AgentArch, AACL 2026 (benchmark kiến trúc agent); chưa xác minh URL trực tiếp |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | Khác biệt hiệu năng giữa các kiến trúc agent phụ thuộc vào việc kiểm soát biến nhiễu (prompt, tool, retrieval); đổi topology mà không cố định các biến khác thì kết luận không đáng tin |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | Benchmark của paper, model thật; ở đây chỉ MockLLM + 14 claim public + 5 seed, nghiệp vụ luật cứng trên dữ liệu có cấu trúc |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Đổi A(workflow)->D(swarm): pass giữ hoặc giảm, cost/success tăng, variance từ 0 lên >0 (do tin ticket ở seed 55) |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | Cố định: MockLLM, tool, seed 11/22/33/44/55, corpus public_claims, pricing.yaml, evaluator. Thay đổi duy nhất: topology (workflow/single/orchestrator/swarm) |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | Lỗi dự kiến: swarm tin số ngày trong ticket ở seed 55 (T02). Đo: pass rate, pass^5, variance, cost/success |

## Kết quả ablation

- Lệnh đã chạy (copy nguyên văn): `python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json`
- Run id / file report: reports/benchmark.json (vd R-swarm-C-002-s55 vs R-workflow-C-002-s55)
- Kết quả so với hypothesis: ĐÚNG. workflow 1.000/1.000/var 0/cost 28.79; single 1.000/1.000/0/46.66; orchestrator 1.000/1.000/0/56.99; swarm 0.986/0.929/0.000816/49.57. Chênh lệch chỉ đến từ topology vì mọi biến khác cố định; single và orchestrator đắt hơn workflow mà không tăng pass.
- Giới hạn: MockLLM không phải model sản xuất, latency là `unavailable`.

Muốn đi xa hơn một ablation để lấy điểm cộng thì xem `docs/bonus_topics.md`.

