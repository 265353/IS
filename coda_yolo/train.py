import os
import json
import torch
import numpy as np
from pathlib import Path


def make_serializable(obj):
    """递归将 metrics 对象转换为 JSON 可序列化的形式"""
    if isinstance(obj, (torch.Tensor, np.ndarray)):
        return obj.tolist()
    elif isinstance(obj, (Path, str)):
        return str(obj)
    elif isinstance(obj, (int, float, bool)) or obj is None:
        return obj
    elif isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_serializable(v) for v in obj]
    elif hasattr(obj, '__dict__'):
        return make_serializable(vars(obj))
    else:
        return str(obj)  # fallback: convert unknown objects to string


def save_metrics_as_json(trainer):
    metrics = getattr(trainer, 'metrics', None)
    if metrics is None:
        print("[Callback] 未获取到 trainer.validator.metrics 对象。")
        return

    metrics_serializable = make_serializable(metrics)

    save_dir = os.path.join(trainer.save_dir, "custom_metrics")
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, "full_metrics.json")

    with open(save_path, "w") as f:
        json.dump(metrics_serializable, f, indent=2)

    print(f"[Callback] 训练验证指标 metrics 已保存至：{save_path}")
from ultralytics import YOLO


if __name__ == "__main__":
    model = YOLO("yolov8m-seg.pt")
    model.add_callback("on_val_end", save_metrics_as_json)

    model.train(
        data="/home/aistudio/dataset/datasetmask/dataset/zipper/dataset.yaml",
        epochs=100,
        imgsz=640,
        device=0,
        workers=4
    )
