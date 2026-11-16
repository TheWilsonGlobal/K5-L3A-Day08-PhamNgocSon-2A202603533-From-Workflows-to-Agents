# Bonus report: B3

**Nguồn:** Google Research 2026, error amplification (agent độc lập khuếch đại lỗi tới 17,2x, orchestration tập trung 4,4x).

**Claim và boundary:** một bước verify trước khi ghi giảm khuếch đại lỗi trong hệ nhiều agent. Boundary: kết luận của nguồn dựa trên benchmark của họ; ở đây chỉ là MockLLM + 14 claim public, không đại diện model thật.

**Việc đã làm:** `bonus/swarm_verified.py` giữ nguyên chatter và REFERENCE_WEAKNESS của swarm, thêm verifier bằng code đối chiếu `delay_days`, `status`, `damage_verified` với order row; lệch thì quote lại từ dữ liệu có cấu trúc (tối đa 1 vòng) và ghi `verifier_override` vào trace. Test: `tests/test_bonus_b3.py` (2 test pass).

**Lệnh tái lập:**
`python -m lab8.benchmark --shapes workflow,swarm,swarm_verified --extra-shape swarm_verified=bonus.swarm_verified:run_claim --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/bonus_benchmark.json`

**Kết quả (reports/bonus_benchmark.json):**

| shape | pass | pass^5 | variance | cost/success |
| --- | --- | --- | --- | --- |
| workflow | 1.000 | 1.000 | 0.000000 | 28.79 |
| swarm | 0.986 | 0.929 | 0.000816 | 49.57 |
| swarm_verified | 1.000 | 1.000 | 0.000000 | 49.00 |

**Phân tích:** verifier đưa swarm về ngang workflow về độ chính xác, với cost/success vẫn ~70% cao hơn workflow. Vì verifier đã tự quyết định số liệu, phần giá trị còn lại của swarm gần như chỉ là chatter đắt tiền; kết quả ủng hộ hypothesis rằng guardrail bằng code là thứ sửa lỗi, không phải số agent. Kết luận có thể đảo nếu ticket chứa thông tin không có trong order row. Giới hạn: MockLLM, chỉ bộ public, chưa đo trên hidden; chưa tự viết 8 claim đối kháng.
