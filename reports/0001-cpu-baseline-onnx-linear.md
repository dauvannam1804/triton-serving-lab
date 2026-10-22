# CPU baseline — onnx_linear (8 core, không Docker)

*Ngày đo: 2026-10-22 20:19 · host: namdv-Latitude-5490 · x86_64 · Python/py: 3.13.5*

**Model:** `onnx_linear` · **Server:** Triton 2.73.0 CPU-only (không Docker)

## Benchmark (perf_analyzer)

| Kịch bản | Concurrency | Throughput (infer/s) | p50 (µs) | p90 (µs) | p95 (µs) | p99 (µs) |
|---|---|---|---|---|---|---|
| bench_c1 | 1 | 2,266 | 414 | 480 | 508 | 1,032 |
| bench_c8 | 8 | 14,731 | 446 | 747 | 1,017 | 2,144 |

## Runtime metrics (30 samples / 15s, trong lúc có tải)

| Metric | Loại | Giá trị |
|---|---|---|
| `nv_inference_request_success` | counter | Δ 31,936 (2,199/s) |
| `nv_inference_exec_count` | counter | Δ 31,936 (2,199/s) |
| `nv_inference_queue_duration_us` | counter | Δ 6,163,993 (424,400/s) |
| `nv_inference_compute_infer_duration_us` | counter | Δ 316,471 (21,789/s) |
| `nv_inference_pending_request_count` | gauge | avg 0.400 · max 1.000 |
| `nv_cpu_utilization` | gauge | avg 0.282 · max 0.339 |

## Cách tái hiện

```bash
./serve.sh   # terminal 1
./scripts/bench.sh -m onnx_linear -c 8 --measurement-interval 3000 -f reports/bench_c8.csv
python3 scripts/collect_metrics.py --duration 15 --out reports/metrics_c4.csv  # terminal 2, song song lúc có tải
python3 scripts/make_report.py --title '...' --perf reports/bench_c8.csv --metrics reports/metrics_c4.csv --out reports/report.md
```

## Kết luận

_(điền kết luận của bạn tại đây)_
