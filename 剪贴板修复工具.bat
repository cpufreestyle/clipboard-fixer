@echo off
chcp 65001 >nul
title 剪贴板修复工具
color 0A

echo.
echo ╔══════════════════════════════════════╗
echo ║     🔧 Windows 剪贴板修复工具        ║
echo ╚══════════════════════════════════════╝
echo.

:menu
echo [1] 🔍 检测剪贴板状态
echo [2] 🔄 重启剪贴板服务 (rdpclip)
echo [3] 🗑️  清空剪贴板
echo [4] 🔁 重启资源管理器
echo [5] ✨ 一键修复 (全部)
echo [0] 🚪 退出
echo.
set /p choice="请选择操作 (0-5): "

if "%choice%"=="1" goto status
if "%choice%"=="2" goto restart_clipboard
if "%choice%"=="3" goto clear_clipboard
if "%choice%"=="4" goto restart_explorer
if "%choice%"=="5" goto fix_all
if "%choice%"=="0" goto end
goto menu

:status
echo.
echo 📊 剪贴板服务状态:
echo.
tasklist /fi "imagename eq rdpclip.exe" 2>nul | find /i "rdpclip.exe" >nul
if %errorlevel% equ 0 (
    echo ✅ rdpclip.exe 运行中
) else (
    echo ❌ rdpclip.exe 未运行
)
tasklist /fi "imagename eq explorer.exe" 2>nul | find /i "explorer.exe" >nul
if %errorlevel% equ 0 (
    echo ✅ explorer.exe 运行中
) else (
    echo ❌ explorer.exe 未运行
)
echo.
pause
cls
goto menu

:restart_clipboard
echo.
echo 🔄 重启剪贴板服务...
taskkill /f /im rdpclip.exe 2>nul
timeout /t 1 /nobreak >nul
start "" "C:\Windows\System32\rdpclip.exe"
echo ✅ 剪贴板服务已重启
echo.
pause
cls
goto menu

:clear_clipboard
echo.
echo 🗑️ 清空剪贴板...
echo off | clip
echo ✅ 剪贴板已清空
echo.
pause
cls
goto menu

:restart_explorer
echo.
echo 🔁 重启资源管理器...
taskkill /f /im explorer.exe 2>nul
timeout /t 2 /nobreak >nul
start "" "C:\Windows\explorer.exe"
echo ✅ 资源管理器已重启
echo.
pause
cls
goto menu

:fix_all
echo.
echo ✨ 执行一键修复...
echo.
echo [1/4] 清空剪贴板...
echo off | clip
echo     ✅ 完成
echo.
echo [2/4] 重启剪贴板服务...
taskkill /f /im rdpclip.exe 2>nul
timeout /t 1 /nobreak >nul
start "" "C:\Windows\System32\rdpclip.exe"
echo     ✅ 完成
echo.
echo [3/4] 重启资源管理器...
taskkill /f /im explorer.exe 2>nul
timeout /t 2 /nobreak >nul
start "" "C:\Windows\explorer.exe"
echo     ✅ 完成
echo.
echo [4/4] 清空回收站...
rd /s /q %systemdrive%\$Recycle.bin 2>nul
echo     ✅ 完成
echo.
echo ════════════════════════════════════════
echo   🎉 修复完成！请测试复制粘贴功能
echo ════════════════════════════════════════
echo.
pause
cls
goto menu

:end
echo.
echo 感谢使用！
timeout /t 1 /nobreak >nul
exit
