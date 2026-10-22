#!/usr/bin/env python3
# make_report.py — Tổng hợp benchmark (CSV từ perf_analyzer -f) + metrics (CSV từ collect_metrics.py)
#   thành 1 báo cáo Markdown gửi team. Không dependency ngoài stdlib.
# Chạy:  python3 scripts/make_report.py \
#          --title "CPU baseline — onnx_linear (8 core)" \
#          --perf reports/bench_c1.csv reports/bench_c8.csv \
#          --metrics reports/metrics_c4.csv \
#          --out reports/0001-cpu-baseline-onnx-linear.md
import argparse
import csv
import platform
from datetime import datetime
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--title", required=True)
parser.add_argument("--perf", nargs="*", default=[], help="CSV report của perf_analyzer")
parser.add_argument("--metrics", help="CSV raw của collect_metrics.py")
parser.add_argument("--model", default="onnx_linear")
parser.add_argument("--conclusion", default="_(điền kết luận của bạn tại đây)_")
parser.add_argument("--out", required=True)
args = parser.parse_args()


def fmt(v: str) -> str:
    try:
        f = float(v)
        return f"{f:,.0f}" if f >= 100 else f"{f:.1f}"
    except ValueError:
        return v


lines = [f"# {args.title}", ""]
lines.append(f"*Ngày đo: {datetime.now().strftime('%Y-%m-%d %H:%M')} · host: {platform.node()} · "
             f"{platform.machine()} · Python/py: {platform.python_version()}*")
lines.append("\n**Model:** `" + args.model + "` · **Server:** Triton 2.73.0 CPU-only (không Docker)")
lines.append("\n## Benchmark (perf_analyzer)")
lines.append("\n| Kịch bản | Concurrency | Throughput (infer/s) | p50 (µs) | p90 (µs) | p95 (µs) | p99 (µs) |")
lines.append("|---|---|---|---|---|---|---|")
for path in args.perf:
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        if "Concurrency" not in (reader.fieldnames or []):
            raise SystemExit(f"{path} không phải CSV report của perf_analyzer (thiếu cột 'Concurrency'). "
                             f"Bạn có đang truyền nhầm file metrics?")
        rows = list(reader)
    for row in rows:
        label = Path(path).stem
        lines.append(f"| {label} | {row['Concurrency']} | {fmt(row['Inferences/Second'])} "
                     f"| {fmt(row['p50 latency'])} | {fmt(row['p90 latency'])} "
                     f"| {fmt(row['p95 latency'])} | {fmt(row['p99 latency'])} |")

if args.metrics:
    with open(args.metrics, newline="") as f:
        samples = list(csv.DictReader(f))
    def vals(name):
        return [float(s[name]) for s in samples if s.get(name)]
    first, last = samples[0], samples[-1]
    elapsed = max(float(last["ts"]) - float(first["ts"]), 1e-9)
    lines.append(f"\n## Runtime metrics ({len(samples)} samples / {elapsed:.0f}s, trong lúc có tải)")
    lines.append("\n| Metric | Loại | Giá trị |")
    lines.append("|---|---|---|")
    for name in ["nv_inference_request_success", "nv_inference_exec_count", "nv_inference_queue_duration_us",
                 "nv_inference_compute_infer_duration_us"]:
        if name in first:
            delta = float(last[name]) - float(first[name])
            lines.append(f"| `{name}` | counter | Δ {delta:,.0f} ({delta / elapsed:,.0f}/s) |")
    for name in ["nv_inference_pending_request_count", "nv_cpu_utilization"]:
        if name in first:
            vs = vals(name)
            lines.append(f"| `{name}` | gauge | avg {sum(vs)/len(vs):.3f} · max {max(vs):.3f} |")

lines += [
    "\n## Cách tái hiện",
    "", "```bash",
    "./serve.sh   # terminal 1",
    "./scripts/bench.sh -m onnx_linear -c 8 --measurement-interval 3000 -f reports/bench_c8.csv",
    "python3 scripts/collect_metrics.py --duration 15 --out reports/metrics_c4.csv  # terminal 2, song song lúc có tải",
    "python3 scripts/make_report.py --title '...' --perf reports/bench_c8.csv --metrics reports/metrics_c4.csv --out reports/report.md",
    "```",
    f"\n## Kết luận\n\n{args.conclusion}",
]

out = Path(args.out)
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Đã ghi báo cáo: {out} ({out.stat().st_size} bytes)")
