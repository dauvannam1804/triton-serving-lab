# NOTES.md — Working notes

## User profile
- Tên: Nam. Vai trò: MLOps Engineer — Serving & Performance trong dự án nhóm (Cost-Aware GPU Scheduling).
- Level: có kinh nghiệm serving/Docker mức nào đó, mới với Triton (self-reported, cần xác minh qua bài đầu).
- Máy cá nhân không GPU. Muốn dùng Google Colab (đã hỏi "có được không?" → cần path xác minh: Docker không chạy chuẩn trên Colab).
- Ngôn ngữ: bài học bằng **Tiếng Việt**, thuật ngữ kỹ thuật giữ tiếng Anh.

## Environment plan
- **VERIFIED 21/10/2026**: Triton 2.73.0 chạy CPU-only không Docker trên máy này. Recipe: zip release + openssl 3.4 deb + dcgm4-core deb + nvidia wheels (cudart, cupti) → `~/.triton-cpu/` (~2.1GB). Scripts: `setup_triton_cpu.sh`, `serve.sh` trong workspace. Chi tiết lỗi từng gặp: REF 0001.
- Lỗi pip: `--upgrade --target` XÓA package khác cùng target dir → luôn cài các wheels NVIDIA cùng một lần gọi pip vào target sạch.
- Colab: chưa có notebook chính thức chạy server trên VM Colab. 3 hướng: build từ source `--no-container-build` (proven 1 lần, CSDN r23.10), extract image layers (chưa ai proven), zip release CUDA 13 (cần driver r580+). → Bài sau probe `!nvidia-smi` trên Colab để quyết định.
- perf_analyzer nằm trong `tritonserver_sdk` zip 0.46GB (cùng releases page) — tải khi tới bài benchmark.

## Preferences
- Bài học tiếng Việt, thuật ngữ kỹ thuật giữ tiếng Anh.

## Open questions cho session sau
- Model cụ thể dự án sẽ serve (PyTorch .pt tự train hay model công khai)? Ảnh hưởng bài ONNX vs PyTorch backend.
- Deadline task?
- Colab probe: driver Colab hiện tại là gì (quyết định path GPU)?
