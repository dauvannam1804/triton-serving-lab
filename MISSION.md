# Mission: Triton Inference Server cho MLOps Engineer — Serving & Performance

## Why
Nam đang đảm nhận vai trò **MLOps Engineer — Serving & Performance** trong dự án
*"Cost-Aware GPU Scheduling for Deep Learning"* (xem `Project-Description-1.docx`).
Phần việc của Nam là lớp phục vụ (serving layer) mà bộ lập lịch GPU sẽ điều phối:
chạy model bằng Triton Inference Server, benchmark, thu thập runtime metrics,
và tổng hợp kết quả để các thành viên khác (scheduling/optimization) dùng làm dữ liệu đầu vào.
Làm tốt phần này = có kết quả benchmark/metrics đáng tin cậy để cả team tối ưu chi phí GPU.

## Success looks like
- Tự tay dựng được model repository chuẩn (`config.pbtxt`, version, backend) cho model PyTorch/ONNX
- Khởi động Triton bằng script, chạy inference smoke test pass được
- Chạy `perf_analyzer` tự động, đọc hiểu kết quả throughput/latency (p50/p95/p99)
- Thu thập runtime metrics từ Prometheus endpoint của Triton (GPU util, latency, queue, batch size…)
- Đóng gói logs + tổng hợp kết quả benchmark thành báo cáo cho team
- Hiểu đủ về batching/concurrency/instances để giải thích vì sao hệ thống chậm/nhanh — knowledge cần cho cả dự án Cost-Aware Scheduling

## Constraints
- Máy cá nhân **không có GPU**; môi trường thực hành chính là **Google Colab (GPU T4 free)** hoặc CPU-only Docker cục bộ
- Chưa có cluster Kubernetes ở giai đoạn học — K8s/Kueue chỉ là bối cảnh dự án, chưa cần depth
- Ngôn ngữ bài học: **Tiếng Việt** (thuật ngữ kỹ thuật giữ tiếng Anh)

## Out of scope (tạm thời)
- Tự viết scheduling/optimization algorithm (phần của thành viên khác)
- Kubernetes, Kueue, Helm — chỉ tìm hiểu mức khái niệm khi cần liên kết
- TensorRT optimization sâu, multi-model ensemble phức tạp — chừng nào mission đòi hỏi mới mở rộng
