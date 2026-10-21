# triton-serving-lab

Workspace học + thực hành **NVIDIA Triton Inference Server** cho vai trò
*MLOps Engineer — Serving & Performance* (serving, benchmark, runtime metrics)
trong dự án **Cost-Aware GPU Scheduling for Deep Learning**.

> Học trong công khai: mỗi bài học là một HTML tựContain trong `lessons/`,
> kèm quiz tự chấm, gắn với nguồn chính thức của NVIDIA.

## Điểm hay nhất của repo

**`setup_triton_cpu.sh`** — công thức đã xác minh (21/10/2026) chạy Triton Inference
Server **CPU-only, không cần Docker, không cần GPU**, chỉ ~2.1GB disk, trên Ubuntu 24.04:

| Thành phần | Vai trò |
|---|---|
| `tritonserver-2.73.0` (zip từ GitHub Releases) | Server + backends |
| OpenSSL ≥ 3.4 (deb) | Build 26.09 cần symbol `OPENSSL_3.4.0` |
| DCGM 4.6.1-core (deb) | Triton link `libdcgm.so.4` |
| `nvidia-cuda-runtime` + `nvidia-cuda-cupti` (wheels, pypi.nvidia.com) | `libcudart.so.13`, `libcupti.so.13` |

Chi tiết đầy đủ + bảng xử lý lỗi từng gặp: [`reference/0001-triton-cpu-no-docker.html`](reference/0001-triton-cpu-no-docker.html)

## Quickstart

```bash
./setup_triton_cpu.sh     # tải + cài vào ~/.triton-cpu (idempotent)
./serve.sh                # khởi động server với model_repository/
```

Smoke test (terminal thứ hai):

```bash
curl -s -o /dev/null -w "%{http_code}\n" localhost:8000/v2/health/ready
# → 200

curl -s -X POST localhost:8000/v2/models/identity_cpu/infer \
  -H "Content-Type: application/json" \
  -d '{"inputs":[{"name":"INPUT0","shape":[1,4],"datatype":"FP32","data":[1,2,3,4]}],"outputs":[{"name":"OUTPUT0"}]}'
# → data:[1.0,2.0,3.0,4.0]

curl -s localhost:8002/metrics | grep nv_inference_request_success
```

Ba cổng chuẩn: **8000** HTTP · **8001** gRPC · **8002** Prometheus metrics.

## Cấu trúc

```
├── lessons/          # bài học (HTML, quiz tương tác)
├── reference/        # cheat sheet in được
├── assets/           # stylesheet + quiz widget dùng chung
├── model_repository/ # model repo của Triton (config.pbtxt + version dirs)
├── serve.sh          # startup script
├── setup_triton_cpu.sh
├── MISSION.md        # mục tiêu học tập
└── RESOURCES.md      # nguồn đã xác minh
```

## Lộ trình

- [x] **0001** — Kiến trúc Triton + smoke test đầu tiên (CPU, không Docker)
- [ ] **0002** — ONNX thật + `config.pbtxt` (dynamic batching, instances)
- [ ] **0003** — `perf_analyzer`: benchmark throughput/latency (p50/p99)
- [ ] **0004** — Thu thập Prometheus metrics + tổng hợp báo cáo
- [ ] **0005** — Path GPU (Colab/cloud) + benchmark GPU thật

## Nguồn chính

- [Triton Quickstart](https://github.com/triton-inference-server/server/blob/main/docs/getting_started/quickstart.md)
- [Triton Documentation](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/index.html)
- [Triton tutorials](https://github.com/triton-inference-server/tutorials)
