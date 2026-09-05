# 东莞采购雷达 - 设置定时任务脚本
# 每天早上 8:00 自动运行

$TaskName = "东莞采购雷达"
$ScriptPath = Join-Path $PSScriptRoot "run-local.bat"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "设置定时任务: $TaskName" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否以管理员身份运行
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "错误：请以管理员身份运行此脚本！" -ForegroundColor Red
    Write-Host "右键点击 PowerShell，选择'以管理员身份运行'" -ForegroundColor Yellow
    pause
    exit 1
}

# 删除已存在的任务
$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "发现已存在的任务，正在删除..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# 创建任务动作
$Action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$ScriptPath`""

# 创建任务触发器 - 每天早上 8:00
$Trigger = New-ScheduledTaskTrigger -Daily -At "08:00"

# 创建任务设置
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# 创建任务
$Task = New-ScheduledTask -Action $Action -Trigger $Trigger -Settings $Settings

# 注册任务
Register-ScheduledTask -TaskName $TaskName -InputObject $Task -Force

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "定时任务设置成功！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "任务名称: $TaskName" -ForegroundColor Cyan
Write-Host "运行时间: 每天早上 8:00" -ForegroundColor Cyan
Write-Host "执行脚本: $ScriptPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "您可以在'任务计划程序'中查看和管理此任务" -ForegroundColor Yellow
Write-Host ""

# 询问是否立即运行
$runNow = Read-Host "是否立即运行一次测试？(Y/N)"
if ($runNow -eq "Y" -or $runNow -eq "y") {
    Write-Host ""
    Write-Host "正在启动爬虫..." -ForegroundColor Cyan
    Start-Process -FilePath $ScriptPath -Wait
}

pause
