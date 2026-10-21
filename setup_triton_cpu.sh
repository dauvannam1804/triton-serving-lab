#!/usr/bin/env bash
# setup_triton_cpu.sh — Cài Triton Inference Server chạy CPU-only, KHÔNG cần Docker hay GPU.
# Đã xác minh chạy thành công trên Ubuntu 24.04 (glibc 2.39), Triton 2.73.0 (nv26.09).
# Cách dùng:  ./setup_triton_cpu.sh            (cài vào ~/.triton-cpu)
set -euo pipefail

BASE_DIR="${TRITON_CPU_DIR:-$HOME/.triton-cpu}"
mkdir -p "$BASE_DIR"
cd "$BASE_DIR"

TRITON_URL="https://github.com/triton-inference-server/server/releases/download/v2.73.0/tritonserver-2.73.0%2Bnv26.09-cu132-cp312-manylinux_2_34-x86_64.zip"
OPENSSL_DEB="libssl3t64_3.4.1-1ubuntu4_amd64.deb"
OPENSSL_URL="http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/${OPENSSL_DEB}"
DCGM_DEB="datacenter-gpu-manager-4-core_4.6.1-1_amd64.deb"
DCGM_URL="https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/${DCGM_DEB}"

need_disk() { # $1 = GB cần
  local avail_gb
  avail_gb=$(df --output=avail -BG "$BASE_DIR" | tail -1 | tr -dc '0-9')
  if [ "$avail_gb" -lt "$1" ]; then
    echo "Cần tối thiểu ${1}GB trống ở $BASE_DIR, chỉ còn ${avail_gb}GB." >&2; exit 1
  fi
}

echo "==> [1/4] Triton server (zip chính thức từ GitHub Releases, ~1.1GB)"
if [ ! -d triton_dist/tritonserver ]; then
  need_disk 6
  curl -L --fail -o triton.zip "$TRITON_URL"
  unzip -q triton.zip -d triton_dist
  rm triton.zip
else
  echo "    đã có, bỏ qua"
fi

echo "==> [2/4] OpenSSL >= 3.4 (Ubuntu 24.04 có 3.0 — bản build Triton cần symbol OPENSSL_3.4.0)"
if [ ! -d ssl_extract ]; then
  curl -sSf -O "$OPENSSL_URL"
  dpkg-deb -x "$OPENSSL_DEB" ssl_extract
  rm "$OPENSSL_DEB"
else
  echo "    đã có, bỏ qua"
fi

echo "==> [3/4] DCGM 4.6.1-core (Triton link libdcgm.so.4; không cần GPU driver)"
if [ ! -d dcgm_extract ]; then
  curl -sSf -O "$DCGM_URL"
  dpkg-deb -x "$DCGM_DEB" dcgm_extract
  rm "$DCGM_DEB"
else
  echo "    đã có, bỏ qua"
fi

echo "==> [4/4] CUDA 13 runtime + CUPTI (pip wheels từ index chính thức pypi.nvidia.com)"
if [ ! -f cuda_libs/nvidia/cu13/lib/libcudart.so.13 ] || [ ! -f cuda_libs/nvidia/cu13/lib/libcupti.so.13 ]; then
  pip install --quiet --target "$BASE_DIR/cuda_libs" \
    --index-url https://pypi.nvidia.com nvidia-cuda-runtime nvidia-cuda-cupti
else
  echo "    đã có, bỏ qua"
fi

echo ""
echo "Cài xong. Khởi động server ví dụ:"
echo "  ./serve.sh"
echo ""
echo "Biến môi trường LD_LIBRARY_PATH cần thiết (serve.sh đã set sẵn):"
echo "  $BASE_DIR/ssl_extract/usr/lib/x86_64-linux-gnu"
echo "  $BASE_DIR/triton_dist/tritonserver/lib64"
echo "  $BASE_DIR/cuda_libs/nvidia/cu13/lib"
echo "  $BASE_DIR/dcgm_extract/usr/lib/x86_64-linux-gnu"
