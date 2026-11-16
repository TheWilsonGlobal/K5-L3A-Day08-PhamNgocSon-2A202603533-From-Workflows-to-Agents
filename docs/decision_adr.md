# Decision record

Điền sau dấu `:` trên cùng dòng, không xóa nhãn. Giảng viên và `python -m lab8.check_submission` đọc các dòng này bằng máy.
`Shape chọn` phải là đúng một trong: `workflow`, `single`, `orchestrator`, `swarm`. Đây là shape được chấm cổng hidden.

- Shape chọn: workflow
- Commit hash: 30e840f (HEAD starter; cập nhật hash sau khi commit bài nộp)
- Run id dẫn chứng: R-workflow-C-002-s55 (reports/benchmark.json)
- Pass rate / pass^5 / seed min-max / variance: 1.000 / 1.000 / 1.000-1.000 / 0.000000 (14 claim public x 5 seed)
- Cost per success (mô phỏng, VND): 28.79 (single 46.66, orchestrator 56.99, swarm 49.57)
- Crash safety: 20/20 (reports/crash.json)
- Secret leak / approval bypass: 0 / 0 (trace không ghi ticket, claim row, phone, địa chỉ; test_trace_contract + student matrix xanh)

## Vì sao shape này

Trên cùng 14 claim public x 5 seed (reports/benchmark.json), workflow, single và orchestrator đều đạt pass 1.000 và pass^5 1.000, variance 0. Khác biệt nằm ở chi phí: workflow rẻ nhất (28.79 VND/success), single 46.66, orchestrator 56.99. Swarm đạt pass 0.986, pass^5 0.929 vì tin số ngày trong ticket ở seed 55 (T02). Khi độ chính xác hòa nhau, chọn kiến trúc ít tự chủ nhất và rẻ nhất: workflow. Luật nghiệp vụ ở đây là luật cứng trên dữ liệu có cấu trúc nên không cần model để quyết định.

## Có đáng đổi lấy multi-agent không

Không. Multi-agent (orchestrator) đắt hơn ~98% (56.99 so với 28.79) mà không tăng pass rate; swarm vừa đắt hơn ~72% vừa có variance 0.000816. Quyết định đảo lại nếu ticket cần hiểu ngôn ngữ mơ hồ không quy được về cột có cấu trúc (ảnh hóa đơn, tranh chấp nhiều bước), hoặc nếu hidden set cho thấy workflow fail ở nhóm ca đó mà single/orchestrator pass ổn định.

## Trace và bằng chứng

Trace ghi: claim (chỉ cờ has_order_id), order (allowlist ORDER_FIELDS), handoff đã sanitize, quote (amount, reason), decision, crash. Cố ý KHÔNG ghi: ticket, parent_secret, header, phone, địa chỉ, tên hàng, ghi chú nội bộ, API key. Mọi file trace nằm trong traces/ với tên bắt đầu bằng run_id nên scanner của grader quét được; không có stdout chứa dữ liệu nhạy cảm.

## Giới hạn

MockLLM không phải model sản xuất. Latency để `unavailable`. Số liệu chỉ trên bộ public (14 claim); hidden 40 claim do giảng viên chấm. Không sửa JSON cho đủ 0.75.
