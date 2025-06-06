#!/bin/bash

# 假设有多个 category
# all the categories you need is below,you can change it
categories=("tile" "toothbrush" "transistor" "wood" "zipper")

# 原始配置文件路径
# config file path
original_config="./anomalib/anomalib/src/anomalib/models/patchcore/config.yaml"
# you do not need change the code below
for category in "${categories[@]}"; do
    

    # 生成新的配置文件路径
    updated_config="your_updated_config_${category}.yaml"

    # 使用 awk 替换 YAML 文件中的 category 字段值
    awk -v category="$category" '/^ *category:/ {print "  category: " category; next} {print}' "$original_config" > "$updated_config"

    # 执行实验脚本
    powershell -ExecutionPolicy Bypass -File script.ps1 --config "$updated_config"

    sleep 1
    echo "\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"
    echo "Running experiment for category: $category"
done
