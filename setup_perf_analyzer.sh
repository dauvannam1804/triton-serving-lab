#!/usr/bin/env bash
# setup_perf_analyzer.sh — Cài perf_analyzer (benchmark chính thức của Triton) không cần Docker.
# perf_analyzer nằm trong zip SDK cùng trang GitHub Releases với server zip (~458MB,
# chỉ extract thư mục install/ ≈ 550MB). Đã xác minh v2.73.0 chạy trên máy CPU-only này.
# Cách dùng:  ./setup_perf_analyzer.sh
set -euo pipefail

BASE_DIR="${TRITON_CPU_DIR:-$HOME/.triton-cpu}"
SDK_URL="https://github.com/triton-inference-server/server/releases/download/v2.73.0/tritonserver_sdk-2.73.0%2Bnv26.09-cu132-cp312-manylinux_2_34-x86_64.zip"
PA_BIN="$BASE_DIR/sdk/tritonserver_sdk/install/bin/perf_analyzer"

need_disk() { # $1 = GB cần
  local avail_gb
  avail_gb=$(df --output=avail -BG "$BASE_DIR" | tail -1 | tr -dc '0-9')
  if [ "$avail_gb" -lt "$1" ]; then
    echo "Cần tối thiểu ${1}GB trống ở $BASE_DIR, chỉ còn ${avail_gb}GB." >&2; exit 1
  fi
}

if [ -x "$PA_BIN" ]; then
  echo "perf_analyzer đã có: $PA_BIN"
else
  mkdir -p "$BASE_DIR"
  need_disk 3
  echo "==> Tải SDK zip (~458MB) + extract chỉ thư mục install/"
  tmp_zip="$(mktemp /tmp/triton_sdk_XXXX.zip)"
  curl -L --fail -o "$tmp_zip" "$SDK_URL"
  unzip -q "$tmp_zip" "tritonserver_sdk/install/*" -d "$BASE_DIR/sdk"
  rm "$tmp_zip"
fi

"$PA_BIN" --version
echo "Xong. Dùng qua wrapper: scripts/bench.sh -m onnx_linear ..."
