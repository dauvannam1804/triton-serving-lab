# NOTES.md — Working notes

## User profile
- Tên: Nam. Vai trò: MLOps Engineer — Serving & Performance trong dự án nhóm (Cost-Aware GPU Scheduling).
- Level: có kinh nghiệm serving/Docker mức nào đó, mới với Triton (self-reported, cần xác minh qua bài đầu).
- Máy cá nhân không GPU. Muốn dùng Google Colab (đã hỏi "có được không?" → cần path xác minh: Docker không chạy chuẩn trên Colab).
- Ngôn ngữ: bài học bằng **Tiếng Việt**, thuật ngữ kỹ thuật giữ tiếng Anh.

## Environment plan
- **VERIFIED 21/10/2026**: Triton 2.73.0 chạy CPU-only không Docker trên máy này. Recipe: zip release + openssl 3.4 deb + dcgm4-core deb + nvidia wheels (cudart, cupti) → `~/.triton-cpu/` (~2.1GB). Scripts: `setup_triton_cpu.sh`, `serve.sh` trong workspace. Chi tiết lỗi từng gặp: REF 0001.
- Lỗi pip: `--upgrade --target` XÓA package khác cùng target dir → luôn cài các wheels NVIDIA cùng một lần gọi pip vào target sạch.
- Colab: chưa có notebook chính thức chạy server trên VM Colab. 3 hướng: build từ source `--no-container-build` (proven 1 lần, CSDN r23.10), extract image layers (chưa ai proven), zip release CUDA 13 (cần driver r580+). → Notebook probe-ready `colab/0005-triton-gpu-t4.ipynb` (bước 0 probe driver) — Nam chạy probe là ra path.
- **VERIFIED 22/10/2026 (khi soạn bài 2–5)**: perf_analyzer 2.73.0 chạy được CPU-only (SDK zip, binary link tĩnh). Phát hiện ghi vào bài học: `-f` chỉ xuất CSV; `-c N` deprecated = quét 1→N (khác `--concurrency-range N` fixed); mode polling chặn API load/unload (`explicit model load ... not allowed if polling is enabled`); `nv_cpu_utilization` có trên CPU; model siêu nhỏ (10×10) tắt dynamic batching còn NHANH hơn (14.5k vs 11.3k infer/s tại c=8) — dùng làm bài học "đo trước khi tin lời khuyên".
- Cảnh cáo thao tác: `pkill -f tritonserver` TỰ KHỚP command line của shell đang chạy lệnh (đã dính 1 lần) → dùng `pkill -x tritonserver`.

## Preferences
- Bài học tiếng Việt, thuật ngữ kỹ thuật giữ tiếng Anh.
- Repo GitHub public: https://github.com/dauvannam1804/triton-serving-lab (tên do tôi đặt, Nam认可). docx nhóm bị .gitignore. Lessons từ giờ phải đạt chất lượng "public portfolio".

## Open questions cho session sau
- Model cụ thể dự án sẽ serve (PyTorch .pt tự train hay model công khai)? Ảnh hưởng bài ONNX vs PyTorch backend.
- Deadline task?
- Colab probe: driver Colab hiện tại là gì (quyết định path GPU)?
