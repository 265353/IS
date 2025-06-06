import numpy as np
import json
import matplotlib.pyplot as plt
from sklearn.metrics import auc
import os
import pandas as pd

def compute_AUPRC(Precision_lists, label="unknown", prefix="output"):
    AUPRC_list = []
    num_classes = len(Precision_lists)

    plt.figure(figsize=(10, 6))
    for cls_idx, Precision in enumerate(Precision_lists):
        try:
            Precision_array = np.array(Precision, dtype=float)
            if Precision_array.ndim != 1 or len(Precision_array) < 2:
                raise ValueError("格式错误或长度不足")

            confidence = np.linspace(0.0, 1.0, len(Precision_array))
            area = auc(confidence, Precision_array)
            AUPRC_list.append(area)

            plt.plot(confidence, Precision_array, label=f"{label} Class {cls_idx}: AUPRC={area:.4f}")
        except Exception as e:
            print(f"[警告] 跳过 {label} 类别 {cls_idx}：{str(e)}")
            AUPRC_list.append(None)

    plt.title(f"{label.capitalize()}-level Precision-Confidence Curves")
    plt.xlabel("Confidence")
    plt.ylabel("Precision")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{prefix}_{label}_Precision_confidence_curves.png", dpi=300)
    plt.close()
    return AUPRC_list


def process_all_runs():
    base_path = "/home/aistudio/YOLO-main/runs/segment"

    for i in range(1, 16):  # train1 到 train15
        folder = f"train{i}"
        json_path = os.path.join(base_path, folder, "custom_metrics", "full_metrics.json")

        if not os.path.exists(json_path):
            print(f"[跳过] 找不到文件: {json_path}")
            continue

        print(f"\n==> 处理 {folder} 中的 full_metrics.json")

        with open(json_path, "r") as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"[错误] JSON 解析失败: {str(e)}")
                continue

        image_p_curve = data.get("box", {}).get("p_curve", None)
        pixel_p_curve = data.get("seg", {}).get("p_curve", None)

        if not isinstance(image_p_curve, list) or not isinstance(pixel_p_curve, list):
            print(f"[错误] {folder} 的 p_curve 数据格式不正确")
            continue

        prefix = f"auroc{i}"
        image_AUPRC = compute_AUPRC(image_p_curve, label="image", prefix=prefix)
        pixel_AUPRC = compute_AUPRC(pixel_p_curve, label="pixel", prefix=prefix)

        df = pd.DataFrame({
            "Class": list(range(len(image_AUPRC))),
            "Image_AUPRC": image_AUPRC,
            "Pixel_AUPRC": pixel_AUPRC
        })

        csv_path = f"{prefix}.csv"
        df.to_csv(csv_path, index=False)
        print(f"[保存] 指标已保存为 {csv_path}")


if __name__ == "__main__":
    process_all_runs()
