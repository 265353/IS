import cv2
import numpy as np
import os
from shutil import copyfile
import yaml
import random
from tqdm import tqdm  # 用于进度条显示

def mask_to_polygon(mask):
    # 确保输入为二维数组
    if len(mask.shape) == 3:
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    
    # 寻找轮廓并进行有效性检查
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    valid_contours = [c for c in contours if cv2.contourArea(c) >= 3]
    return [contour.flatten().tolist() for contour in valid_contours]

def normalize_coordinates(polygons, img_width, img_height):
    return [
        [coord / (img_width if i%2==0 else img_height) 
         for i, coord in enumerate(polygon)
        ] for polygon in polygons
    ]

def create_yolo_annotation(labels_file, class_id, polygons):
    content = []
    for polygon in polygons:
        if len(polygon) < 6:  # 至少需要3个点（6个坐标值）
            continue
        content.append(f"{class_id} " + " ".join(map(str, polygon)))
    
    with open(labels_file, 'w') as f:
        f.write("\n".join(content))

def create_dataset_structure(base_path):
    """创建标准化的数据集目录结构"""
    dirs = {
        'images': ['train', 'val', 'test'],
        'labels': ['train', 'val', 'test']
    }
    
    for main_dir, sub_dirs in dirs.items():
        for sub in sub_dirs:
            path = os.path.join(base_path, main_dir, sub)
            os.makedirs(path, exist_ok=True)
            print(f"Created directory: {path}")

def split_indices(total, ratios):
    """精确划分数据集索引"""
    assert abs(sum(ratios)-1.0) < 1e-6, "Ratios must sum to 1.0"
    
    counts = [int(total * r) for r in ratios]
    remainder = total - sum(counts)
    # 将余数分配给最大的分区
    counts[counts.index(max(counts))] += remainder
    return np.cumsum(counts)

if __name__ == '__main__':
    # 配置参数
    train_val_test_split = [0.6, 0.2, 0.2]
    # the path for the file you want to use
    mask_folder = '/home/aistudio/YOLO-main/bottle/ground_truth'
    img_folder = '/home/aistudio/YOLO-main/bottle/test'
    out_folder = os.path.abspath('./dataset/zipper') 
    
    # 创建目录结构
    create_dataset_structure(out_folder)

    # 初始化YOLO配置文件
    dataset_config = {
        'path': out_folder,
        'train': os.path.join('images', 'train'),
        'val': os.path.join('images', 'val'),
        'test': os.path.join('images', 'test'),
        'names': {},
        'nc': 0  # 类别总数
    }

    # 按字母顺序处理类别
    categories = sorted(os.listdir(img_folder))
    dataset_config['nc'] = len(categories)
    
    for class_id, category in enumerate(tqdm(categories, desc="Processing categories")):
        dataset_config['names'][class_id] = category
        
        # 准备路径
        img_dir = os.path.join(img_folder, category)
        mask_dir = os.path.join(mask_folder, category)
        
        # 获取并打乱图像列表
        all_images = [f for f in os.listdir(img_dir) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
        random.shuffle(all_images)
        total_images = len(all_images)
        
        # 精确划分数据集
        split_points = split_indices(total_images, train_val_test_split)
        splits = {
            'train': all_images[:split_points[0]],
            'val': all_images[split_points[0]:split_points[1]],
            'test': all_images[split_points[1]:]
        }

        # 处理每个图像
        for mode, images in splits.items():
            for img_name in tqdm(images, desc=f"{category}->{mode}", leave=False):
                # 处理文件名
                base_name = os.path.splitext(img_name)[0]
                img_path = os.path.join(img_dir, img_name)
                mask_path = os.path.join(mask_dir, f"{base_name}_mask.png")
                
                # 目标路径
                dest_img = os.path.join(out_folder, 'images', mode, f"{class_id}_{img_name}")
                dest_label = os.path.join(out_folder, 'labels', mode, f"{class_id}_{base_name}.txt")

                # 处理掩码文件
                if os.path.exists(mask_path):
                    mask = cv2.imread(mask_path)
                    if mask is None:
                        print(f"Warning: Failed to read mask {mask_path}")
                        continue
                    
                    h, w = mask.shape[:2]
                    polygons = mask_to_polygon(mask)
                    if not polygons:
                        with open(dest_label, 'w') as f:  # 创建空标签文件
                            pass
                    else:
                        normalized = normalize_coordinates(polygons, w, h)
                        create_yolo_annotation(dest_label, class_id, normalized)
                else:
                    open(dest_label, 'w').close()  # 创建空文件
                
                # 复制图像文件
                try:
                    copyfile(img_path, dest_img)
                except FileNotFoundError:
                    print(f"Error: Source image not found {img_path}")
                    continue

    # 保存配置文件
    yaml_path = os.path.join(out_folder, 'dataset.yaml')
    with open(yaml_path, 'w') as f:
        yaml.dump(dataset_config, f, sort_keys=False)
    
    print(f"Dataset preparation complete. Config saved to {yaml_path}")