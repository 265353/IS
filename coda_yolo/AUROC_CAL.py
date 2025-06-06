import numpy as np
import json
import matplotlib.pyplot as plt
from sklearn.metrics import auc
import os


def compute_aurc(recall_lists, label="unknown"):
    """
    计算每个类别的 AURC（Recall vs Confidence）并绘图
    参数:
        recall_lists: List[List[float]]，每类的 recall 列表
        label: str，指标标签（如 image/pixel）
    返回:
        List[float or None]：每类的 AURC
    """
    aurc_list = []
    num_classes = len(recall_lists)

    plt.figure(figsize=(10, 6))
    for cls_idx, recall in enumerate(recall_lists):
        try:
            recall_array = np.array(recall, dtype=float)
            if recall_array.ndim != 1 or len(recall_array) < 2:
                raise ValueError("格式错误或长度不足")

            # 置信度均匀分布
            confidence = np.linspace(0.0, 1.0, len(recall_array))
            area = auc(confidence, recall_array)
            aurc_list.append(area)

            # 绘制曲线
            plt.plot(confidence, recall_array, label=f"{label} Class {cls_idx}: AURC={area:.4f}")
        except Exception as e:
            print(f"[警告] 跳过 {label} 类别 {cls_idx}：{str(e)}")
            aurc_list.append(None)

    plt.title(f"{label.capitalize()}-level Recall-Confidence Curves")
    plt.xlabel("Confidence")
    plt.ylabel("Recall")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{label}_recall_confidence_curves.png")
    plt.close()
    return aurc_list


def main():
    json_path = "/home/aistudio/YOLO-main/runs/segment/train1/custom_metrics/full_metrics.json"

    if not os.path.exists(json_path):
        print(f"[错误] 文件不存在: {json_path}")
        return

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"[错误] JSON 解析失败: {str(e)}")
            return

    # 根据你提供的字段结构访问
    image_r_curve = data.get("box", {}).get("r_curve", None)
    pixel_r_curve = data.get("seg", {}).get("r_curve", None)

    if not isinstance(image_r_curve, list) or not isinstance(pixel_r_curve, list):
        print("[错误] 无法从 JSON 中正确解析 r_curve（box.r_curve / seg.r_curve）")
        return

    print("计算图像级 AURC（box.r_curve）...")
    image_aurc = compute_aurc(image_r_curve, label="image")

    print("计算像素级 AURC（seg.r_curve）...")
    pixel_aurc = compute_aurc(pixel_r_curve, label="pixel")

    # 输出结果
    for i, (img, px) in enumerate(zip(image_aurc, pixel_aurc)):
        print(f"类别 {i}：Image AURC = {img if img is not None else 'N/A'} | Pixel AURC = {px if px is not None else 'N/A'}")

    # 保存为 CSV 文件
    import pandas as pd
    df = pd.DataFrame({
        "Class": list(range(len(image_aurc))),
        "Image_AURC": image_aurc,
        "Pixel_AURC": pixel_aurc
    })
    df.to_csv("aurc_metrics_1.csv", index=False)
    print("AURC 指标已保存为 aurc_metrics.csv")



if __name__ == "__main__":
    main()
