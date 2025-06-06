#!/usr/bin/env pwsh

# 定义要进行网格搜索的字段及其可能取值
$paramGrid = @{
    "train_batch_size" = @(16, 32, 64)          # 批大小可能取值
    "eval_batch_size" = @(0.001, 0.01)      # 学习率可能取值
}
#!/usr/bin/env pwsh


# 2. 原始配置文件
$originalConfig = "F:\\ML\\anomalib\\src\\anomalib\\src\\anomalib\\models\\patchcore\\config.yaml"
$templateContent = Get-Content $originalConfig -Raw

# 3. 生成所有参数组合
$combinations = @(@{})
foreach ($param in $paramGrid.GetEnumerator()) {
    $newCombinations = @()
    foreach ($value in $param.Value) {
        foreach ($combination in $combinations) {
            $newCombination = $combination.Clone()
            $newCombination[$param.Key] = $value
            $newCombinations += $newCombination
        }
    }
    $combinations = $newCombinations
}

# 4. 执行网格搜索
foreach ($params in $combinations) {
    # 创建临时配置文件内容
    $tempConfig = $templateContent
    
    # 动态替换所有参数
    foreach ($param in $params.GetEnumerator()) {
        $pattern = "(?<=$($param.Key):\s*)[\w.-]+"
        $tempConfig = $tempConfig -replace $pattern, $param.Value
    }

    # 生成临时文件路径（使用GUID避免冲突）
    $tempFile = [System.IO.Path]::GetTempFileName() -replace '\.tmp$','.yaml'
    
    try {
        # 保存临时配置
        $tempConfig | Out-File $tempFile -Encoding utf8 -Force
        
        # 执行训练命令（示例）
        Write-Host "▶ Running with parameters:"
        $params.GetEnumerator() | Sort-Object Key | ForEach-Object {
            Write-Host ("  {0,-20} = {1}" -f $_.Key, $_.Value)
        }
        
        # 实际执行命令（取消注释使用）
        & .\\jiaoben\\total.ps1
        
        # 模拟执行延迟
        Start-Sleep -Milliseconds 500
    }
    finally {
        # 确保临时文件被删除
        if (Test-Path $tempFile) {
            Remove-Item $tempFile -Force
            Write-Host "✓ Temp file removed: $tempFile`n"
        }
    }
}

Write-Host "✅ Grid search completed! Total combinations tested: $($combinations.Count)"