#!/usr/bin/env bash
# bench.sh — Wrapper perf_analyzer: không cần nhớ đường dẫn binary.
# Cách dùng:
#   ./scripts/bench.sh -m onnx_linear --concurrency-range 1 --measurement-interval 3000
#   ./scripts/bench.sh -m onnx_linear -c 8 -f reports/bench.csv    # -f ghi CSV report
set -euo pipefail

BASE_DIR="${TRITON_CPU_DIR:-$HOME/.triton-cpu}"
PA_BIN="$BASE_DIR/sdk/tritonserver_sdk/install/bin/perf_analyzer"

if [ ! -x "$PA_BIN" ]; then
  echo "Chưa cài perf_analyzer. Chạy trước: ./setup_perf_analyzer.sh" >&2; exit 1
fi

exec "$PA_BIN" -i http -u localhost:8000 "$@"
