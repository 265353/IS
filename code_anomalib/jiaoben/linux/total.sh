#!/bin/bash

# 假设有多个 category
categories=("tile" "toothbrush" "transistor" "wood" "zipper")

# 原始配置文件路径
original_config="/mnt/Disk8T/zmh/anomalib/anomalib/src/anomalib/models/patchcore/config.yaml"

for category in "${categories[@]}"; do
    

    # 生成新的配置文件路径
    updated_config="your_updated_config_${category}.yaml"

    # 使用 awk 替换 YAML 文件中的 category 字段值
    awk -v category="$category" '/^ *category:/ {print "  category: " category; next} {print}' "$original_config" > "$updated_config"

    # 执行实验脚本
    powershell -ExecutionPolicy Bypass -File script.ps1 --config "$updated_config"

    # 在每个实验之间添加适当的延迟（可选）
    sleep 1
    echo "\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"
    echo "Running experiment for category: $category"
done
