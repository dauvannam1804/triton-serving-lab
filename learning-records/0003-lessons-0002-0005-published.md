# Xuất bản bài 0002–0005 — artifacts đã verify trên máy

Session 3 (22/10/2026): soạn xong toàn bộ 4 bài còn lại của lộ trình, mỗi bài kèm số liệu đo THẬT trên máy Nam (không phải số mô phỏng):

- **0002 ONNX + config.pbtxt**: `scripts/make_onnx_model.py` sinh model 621 bytes (y=2x+1), server load READY, bằng chứng batching qua chênh lệch `request_success` vs `exec_count` (64 req → 43 exec; delay 10ms → 256 req chỉ 42 exec). Phát hiện dạy kèm: polling mode chặn model-control load API.
- **0003 perf_analyzer**: cài được không Docker (`setup_perf_analyzer.sh`); baseline c=1 (2111 infer/s, queue 200µs > compute 12µs); sweep c=1..8 bão hòa ~11–14k infer/s; A/B tắt batching NHANH HƠN (ngược lời khuyên phổ biến) — bài học method "đo trước khi tin".
- **0004 metrics + báo cáo**: `scripts/collect_metrics.py` + `make_report.py` chạy thật; báo cáo mẫu `reports/0001-cpu-baseline-onnx-linear.md` đã có trong repo; cross-validation perf_analyzer ↔ Prometheus khớp (~190µs queue/request).
- **0005 GPU path**: notebook probe-ready `colab/0005-triton-gpu-t4.ipynb` (8 bước, tái dùng recipe + clone lab repo); CHƯA verify trên Colab — vấp vát của Nam chính là dữ liệu bài học.

**Implications:** ZPD: bài 2–4 nằm hoàn toàn trong vùng gần (tái dùng kỹ năng bài 1 + script có sẵn), bài 5 là vùng phát triển (môi trường lạ + path chưa verify). Khi Nam học lại từng bài: mở đầu bằng 2 câu retrieval từ bài trước (record 0002), sau mỗi bài xem quiz score trong chính widget (tự chấm). Roadmap README vẫn để `[ ]` cho 0002–0005 — tick khi Nam tự làm pass hands-on, không tick vì "đã có bài".
