# Triton Inference Server — Serving & Performance Resources

Nguồn phục vụ mission: vai trò MLOps Engineer — Serving & Performance trong dự án
Cost-Aware GPU Scheduling. Mọi URL dưới đây đã được fetch/xác minh hoạt động (21/10/2026).

## Knowledge

- [Triton Quickstart (official, GitHub)](https://github.com/triton-inference-server/server/blob/main/docs/getting_started/quickstart.md)
  Tạo model repository, launch Triton (GPU lẫn CPU-only cùng 1 image), health check, inference đầu tiên. Use for: bài học smoke test, port 8000/8001/8002, endpoint `/v2/health/ready`.
- [Triton Documentation Home (NVIDIA)](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/index.html)
  Bản đồ toàn bộ docs: kiến trúc, backends, benchmarking. Use for: điểm xuất phát tra cứu mọi chủ đề.
- [Model Repository guide](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_repository.html)
  Cấu trúc thư mục model, version directories, model control API. Use for: dựng model repo chuẩn.
- [Model Configuration guide](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_configuration.html)
  Toàn bộ `config.pbtxt`: input/output dims, datatypes, instance_group, scheduling. Use for: bài về config.pbtxt (bài 2+).
- [Dynamic Batcher](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html)
  Dynamic batching, queue delay, preferred batch sizes. Use for: hiểu cơ chế cốt lõi ảnh hưởng throughput/latency — dữ liệu đầu vào cho scheduling.
- [Metrics guide (Prometheus)](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/metrics.html)
  Endpoint :8002/metrics, GPU metrics, CPU metrics, cách scrape. Use for: thu thập runtime metrics (phần việc chính).
- [Performance Analyzer (perf_analyzer)](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/perf_analyzer/docs/README.html)
  Benchmark tool chính thức: throughput, latency p50/p99, concurrency sweep. Use for: benchmark automation.
  - [Quick Start](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/perf_analyzer/docs/quick_start.html) · [CLI Reference](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/perf_analyzer/docs/cli.html)
- [KServe V2 inference protocol](https://github.com/kserve/kserve/tree/master/docs/predict-api/v2)
  Chuẩn REST/gRPC mà Triton dùng. Use for: hiểu payload JSON nhị phân của request/response.
- [Triton tutorials repo (official)](https://github.com/triton-inference-server/tutorials)
  Quick-deploy PyTorch/ONNX/OpenVINO, feature guides. Use for: ví dụ deploy từng loại backend.
- [`tritonclient` trên PyPI](https://pypi.org/project/tritonclient/)
  Client library chính thức (HTTP + gRPC). Use for: viết smoke test/benchmark bằng Python.
- [GitHub Releases của triton-inference-server/server](https://github.com/triton-inference-server/server/releases)
  Từ ~v2.64.0 có zip server chính thức (không cần Docker). Use for: cài không Docker (đã xác minh v2.73.0 chạy CPU-only).
- [pypi.nvidia.com — wheel CUDA runtime/cupti](https://pypi.nvidia.com)
  `nvidia-cuda-runtime`, `nvidia-cuda-cupti` cho CUDA 13. Use for: phục vụ dependency của bản cài không Docker.

## Wisdom (Communities)

- [Triton Inference Server GitHub Discussions](https://github.com/triton-inference-server/server/discussions)
  Nơi maintainers + users trả lời lỗi load model, config, benchmark. Use for: hỏi lỗi cụ thể không tìm thấy trong docs.
- [NVIDIA Developer Forums](https://forums.developer.nvidia.com/)
  Forum chính thức của NVIDIA (tìm category "Triton Inference Server" hoặc search `triton`). Use for: vấn đề GPU/driver/DCGM nâng cao.
- [Triton + TensorRT newsletter (NVIDIA)](https://www.nvidia.com/en-us/deep-learning-ai/triton-tensorrt-newsletter/)
  Cập nhật release, best practices. Use for: theo dõi bản mới.

## Gaps

- **Chưa có notebook chính thức chạy Triton server ngay trên VM Colab** (đã kiểm tra tutorials repo + server repo: không có). Các hướng khả thi: build từ source `--no-container-build` (một walkthrough CSDN r23.10 đã proven), hoặc zip release (bị chặn nếu driver Colab < r580 vì build CUDA 13). Quyết định sau khi probe `!nvidia-smi` trên Colab.
- **Python backend bản cài CPU này**: stub build cho cp312 (Python 3.12), máy có Python 3.13 → backend python có thể không chạy local. Chưa xác minh. Nếu cần Python backend → dùng Docker CPU hoặc xử lý sau.
- **perf_analyzer**: nằm trong `tritonserver_sdk` zip (0.46GB, cùng releases page) — chưa tải, sẽ tải khi tới bài benchmark.
