#!/usr/bin/env python3
# collect_metrics.py — Thu thập metrics từ Prometheus endpoint của Triton (:8002/metrics)
#   Sample định kỳ trong --duration giây, ghi CSV thô + in tóm tắt (delta counter, avg/max gauge).
#   Counter (chỉ tăng)   : nv_inference_request_success/failure, nv_inference_count/exec_count,
#                          nv_inference_*_duration_us
#   Gauge (lên xuống)    : nv_inference_pending_request_count, nv_cpu_utilization
# Chạy:  python3 scripts/collect_metrics.py --duration 12 --interval 0.5 --out reports/metrics.csv
#        (mở terminal khác chạy perf_analyzer/burst trong lúc này)
import argparse
import csv
import re
import time
import urllib.request
from collections import defaultdict

COUNTERS = {
    "nv_inference_request_success", "nv_inference_request_failure",
    "nv_inference_count", "nv_inference_exec_count",
    "nv_inference_request_duration_us", "nv_inference_queue_duration_us",
    "nv_inference_compute_infer_duration_us",
}
GAUGES = {"nv_inference_pending_request_count", "nv_cpu_utilization"}
LINE_RE = re.compile(r'^(\w+)(?:\{model="([^"]+)")?[^}]*\}?\s+([0-9.eE+-]+)$')

parser = argparse.ArgumentParser()
parser.add_argument("--url", default="http://localhost:8002/metrics")
parser.add_argument("--duration", type=float, default=12, help="số giây thu thập")
parser.add_argument("--interval", type=float, default=0.5, help="chu kỳ sample (giây)")
parser.add_argument("--model", default="onnx_linear", help="model cần theo dõi counters/gauges")
parser.add_argument("--out", default="reports/metrics.csv", help="file CSV ghi raw samples")
args = parser.parse_args()


def scrape() -> dict:
    with urllib.request.urlopen(args.url, timeout=5) as resp:
        text = resp.read().decode()
    out = {}
    for line in text.splitlines():
        m = LINE_RE.match(line)
        if not m:
            continue
        name, model, value = m.group(1), m.group(2), float(m.group(3))
        if name in GAUGES and (model is None or model == args.model):
            out[name] = out.get(name, 0.0) + value
        elif name in COUNTERS and model == args.model:
            out[name] = value
    return out


samples = []
end = time.monotonic() + args.duration
print(f"Đang thu thập {args.duration:.0f}s (mỗi {args.interval}s) — model '{args.model}'…")
print("Mẹo: chạy perf_analyzer / burst_requests.py ở terminal khác trong lúc này.")
while time.monotonic() < end:
    try:
        sample = scrape()
        sample["ts"] = time.time()
        samples.append(sample)
    except Exception as exc:  # server đang restart thì bỏ qua sample hỏng
        print(f"  (bỏ qua sample: {exc})")
    time.sleep(args.interval)

if not samples:
    raise SystemExit("Không sample được điểm nào — server có đang chạy không?")

keys = sorted({k for s in samples for k in s})
with open(args.out, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=keys)
    writer.writeheader()
    writer.writerows(samples)
print(f"\nĐã ghi {len(samples)} samples → {args.out}")

first, last = samples[0], samples[-1]
elapsed = max(last["ts"] - first["ts"], 1e-9)
print(f"\n== TÓM TẮT ({elapsed:.1f}s) ==")
for name in COUNTERS & set(keys):
    delta = last.get(name, 0) - first.get(name, 0)
    print(f"{name:45s} Δ {delta:12.0f}  ({delta / elapsed:10.0f}/s)")
for name in sorted(GAUGES & set(keys)):
    values = [s[name] for s in samples if name in s]
    print(f"{name:45s} avg {sum(values)/len(values):10.3f}  max {max(values):10.3f}")
