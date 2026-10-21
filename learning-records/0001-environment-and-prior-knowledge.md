# Environment & prior knowledge established (session 1)

Nam có kinh nghiệm serving/Docker cơ bản (self-reported), mới với Triton. Máy cá nhân là Ubuntu 24.04 (glibc 2.39, 8 CPU, 15GB RAM), **không GPU, còn ~17GB disk, có Docker 29.8.2 nhưng không đủ disk cho Triton image (~20GB)**.

Đã xác minh end-to-end (evidence: chạy thật trong session) một đường cài Triton **không Docker, không GPU**: server zip chính thức v2.73.0 (GitHub Releases) + OpenSSL ≥3.4 (deb Ubuntu) + DCGM 4.6.1-core (deb NVIDIA cuda repo) + `nvidia-cuda-runtime`/`nvidia-cuda-cupti` wheels (pypi.nvidia.com). Server chạy CPU-only, smoke test pass: health 200, inference identity trả đúng, Prometheus metrics đếm request. Đóng gói trong `setup_triton_cpu.sh` + `serve.sh`.

**Implications:** (1) mọi lesson hands-on chạy local không tốn tiền cloud; (2) GPU metrics/GPU inference phải chờ path Colab hoặc cloud — Colab cần probe `nvidia-smi` (driver r580+ mới chạy được zip CUDA 13); (3) Python backend local có nguy cơ lỗi vì stub build cp312 vs Python 3.13 của máy — kiểm tra trước khi dạy bài Python backend; (4) ngôn ngữ bài học: tiếng Việt, thuật ngữ giữ tiếng Anh.
