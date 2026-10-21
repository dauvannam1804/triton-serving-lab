#!/usr/bin/env bash
# serve.sh — Khởi động Triton Inference Server (CPU-only) với model repository của dự án.
# Cách dùng:  ./serve.sh               → chạy foreground (Ctrl+C để dừng)
#             ./serve.sh --help        → xem mọi option của tritonserver
set -euo pipefail

BASE_DIR="${TRITON_CPU_DIR:-$HOME/.triton-cpu}"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)/model_repository"
BIN="$BASE_DIR/triton_dist/tritonserver/bin/tritonserver"

if [ ! -x "$BIN" ]; then
  echo "Chưa cài Triton. Chạy trước: ./setup_triton_cpu.sh" >&2; exit 1
fi

export LD_LIBRARY_PATH="$BASE_DIR/ssl_extract/usr/lib/x86_64-linux-gnu:$BASE_DIR/triton_dist/tritonserver/lib64:$BASE_DIR/cuda_libs/nvidia/cu13/lib:$BASE_DIR/dcgm_extract/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"

# Trong Triton chuẩn (container) backend mặc định nằm ở /opt/tritonserver/backends.
# Bản cài CPU này đặt ở đây:
EXTRA_ARGS=(--backend-directory="$BASE_DIR/triton_dist/tritonserver/backends")

exec "$BIN" \
  --model-repository="$REPO_DIR" \
  --http-port 8000 \
  --grpc-port 8001 \
  --metrics-port 8002 \
  "${EXTRA_ARGS[@]}" \
  "$@"
