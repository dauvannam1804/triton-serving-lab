#!/usr/bin/env python3
# make_onnx_model.py — Sinh model ONNX thật cho bài 0002: y = 2x + 1
#   INPUT0 [batch, 10] float32 → MatMul(W=2I) → Add(b=1) → OUTPUT0 [batch, 10]
#   Batch dimension là ĐỘNG (dim_param "batch") → max_batch_size > 0 dùng được.
# Chạy:  python3 scripts/make_onnx_model.py
import sys
from pathlib import Path

import numpy as np
import onnx
from onnx import TensorProto, helper, numpy_helper

REPO_DIR = Path(__file__).resolve().parent.parent / "model_repository" / "onnx_linear"
OUT_PATH = REPO_DIR / "1" / "model.onnx"
DIM = 10


def build_model() -> onnx.ModelProto:
    x = helper.make_tensor_value_info("INPUT0", TensorProto.FLOAT, ["batch", DIM])
    y = helper.make_tensor_value_info("OUTPUT0", TensorProto.FLOAT, ["batch", DIM])

    w = numpy_helper.from_array((2.0 * np.eye(DIM)).astype(np.float32), "W")
    b = numpy_helper.from_array(np.ones(DIM, dtype=np.float32), "B")

    nodes = [
        helper.make_node("MatMul", ["INPUT0", "W"], ["mm"]),
        helper.make_node("Add", ["mm", "B"], ["OUTPUT0"]),
    ]
    graph = helper.make_graph(nodes, "onnx_linear", [x], [y], initializer=[w, b])
    model = helper.make_model(
        graph,
        opset_imports=[helper.make_opsetid("", 17)],
        producer_name="triton-serving-lab",
    )
    # IR 14 (onnx 1.23 mặc định) mới hơn mức onnxruntime 1.24 hỗ trợ → ghim IR 10
    model.ir_version = 10
    onnx.checker.check_model(model)
    return model


def main() -> int:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    model = build_model()
    onnx.save(model, OUT_PATH)

    print(f"Đã ghi : {OUT_PATH} ({OUT_PATH.stat().st_size} bytes)")
    for inp in model.graph.input:
        shape = [d.dim_param or d.dim_value for d in inp.type.tensor_type.shape.dim]
        print(f"Input  : {inp.name} {shape} {inp.type.tensor_type.elem_type}")
    for out in model.graph.output:
        shape = [d.dim_param or d.dim_value for d in out.type.tensor_type.shape.dim]
        print(f"Output : {out.name} {shape} {out.type.tensor_type.elem_type}")

    try:
        import onnxruntime as ort

        sess = ort.InferenceSession(str(OUT_PATH), providers=["CPUExecutionProvider"])
        sample = np.arange(1, DIM + 1, dtype=np.float32).reshape(1, DIM)
        (got,) = sess.run(None, {"INPUT0": sample})
        expected = 2 * sample + 1
        assert np.allclose(got, expected), f"{got} != {expected}"
        print(f"Verify : onnxruntime OK — [1..10] → {got[0].tolist()}")
    except ImportError:
        print("Verify : bỏ qua (chưa cài onnxruntime — không ảnh hưởng serving)")

    print("OK. Restart server để Triton load model này (./serve.sh).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
