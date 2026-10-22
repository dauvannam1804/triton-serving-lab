#!/usr/bin/env python3
# burst_requests.py — Bắn N request song song vào 1 model (dùng cho bài 0002/0004).
# Mục đích: tạo tải đồng thời để quan sát Dynamic Batching qua metrics
#   (nv_inference_request_success tăng = N, nhưng nv_inference_exec_count tăng ít hơn).
# Chạy:  python3 scripts/burst_requests.py --model onnx_linear --requests 64 --batch 1
import argparse
import json
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser()
parser.add_argument("--url", default="http://localhost:8000")
parser.add_argument("--model", default="onnx_linear")
parser.add_argument("--requests", type=int, default=64, help="số request bắn ra")
parser.add_argument("--batch", type=int, default=1, help="số hàng (batch size) mỗi request")
parser.add_argument("--workers", type=int, default=16, help="số thread song song")
args = parser.parse_args()

payload = json.dumps({
    "inputs": [{
        "name": "INPUT0",
        "shape": [args.batch, 10],
        "datatype": "FP32",
        "data": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0] * args.batch,
    }],
    "outputs": [{"name": "OUTPUT0"}],
}).encode()


def send(_: int) -> int:
    req = urllib.request.Request(
        f"{args.url}/v2/models/{args.model}/infer",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status


start = time.perf_counter()
with ThreadPoolExecutor(max_workers=args.workers) as pool:
    codes = list(pool.map(send, range(args.requests)))
elapsed = time.perf_counter() - start

ok = sum(1 for c in codes if c == 200)
print(f"Đã bắn  : {len(codes)} request (mỗi request batch {args.batch} hàng, {args.workers} threads)")
print(f"Thành công: {ok}/{len(codes)}")
print(f"Wall time : {elapsed * 1000:.0f} ms ({len(codes) / elapsed:.0f} req/s)")
