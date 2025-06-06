#!/usr/bin/env pwsh

# 定义类别数组
$categories = @("tile", "toothbrush", "transistor", "wood", "zipper")

# 原始配置文件路径
$originalConfig = "F:\\ML\\anomalib\\src\\anomalib\\src\\anomalib\\models\\patchcore\\config.yaml"

foreach ($category in $categories) {
    # 生成新的配置文件路径
    $updatedConfig = "updated_config_${category}.yaml"
    
    # 替换YAML文件中的category字段
    # PowerShell原生处理YAML需要第三方模块，这里使用文本替换作为简单方案
    (Get-Content $originalConfig) -replace '(?<=category:).*', " $category" | Set-Content $updatedConfig
    
    # 执行实验脚本
    # 注意：如果script.ps1就在当前目录，需要加上.\前缀
    & .\\jiaoben\\single.ps1 -config $updatedConfig
    
    # 添加延迟（单位：秒）
    Start-Sleep -Seconds 1
    
    # 输出分隔线
    "\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"
    "Running experiment for category: $category"
}