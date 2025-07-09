@echo off
title 本地大语言模型对话系统
color 0A

:MAIN_MENU
cls
echo ========================================
echo    本地大语言模型对话系统
echo ========================================
echo.
echo 请选择操作:
echo.
echo [1] 下载模型
echo [2] 启动终端对话
echo [3] 启动Web界面
echo [4] 检查环境
echo [5] 退出
echo.
set /p choice="请输入选择 (1-5): "

if "%choice%"=="1" goto DOWNLOAD_MODEL
if "%choice%"=="2" goto START_TERMINAL
if "%choice%"=="3" goto START_WEB
if "%choice%"=="4" goto CHECK_ENV
if "%choice%"=="5" goto EXIT
goto MAIN_MENU

:DOWNLOAD_MODEL
cls
echo 正在启动模型下载...
python download_model.py
echo.
echo 按任意键返回主菜单...
pause >nul
goto MAIN_MENU

:START_TERMINAL
cls
echo 正在启动终端对话界面...
python chat_terminal.py
echo.
echo 按任意键返回主菜单...
pause >nul
goto MAIN_MENU

:START_WEB
cls
echo 正在启动Web界面...
echo 浏览器将自动打开 http://127.0.0.1:7860
python chat_ui.py
echo.
echo 按任意键返回主菜单...
pause >nul
goto MAIN_MENU

:CHECK_ENV
cls
echo ========================================
echo           环境检查
echo ========================================
echo.
echo 检查Python版本:
python --version
echo.
echo 检查PyTorch和CUDA:
python -c "import torch; print(f'PyTorch版本: {torch.__version__}'); print(f'CUDA可用: {torch.cuda.is_available()}'); print(f'CUDA版本: {torch.version.cuda if torch.cuda.is_available() else \"N/A\"}')"
echo.
echo 检查GPU信息:
python -c "import torch; print(f'GPU数量: {torch.cuda.device_count()}'); [print(f'GPU {i}: {torch.cuda.get_device_name(i)}') for i in range(torch.cuda.device_count())] if torch.cuda.is_available() else print('无可用GPU')"
echo.
echo 检查已安装的关键包:
python -c "import transformers, gradio; print(f'Transformers版本: {transformers.__version__}'); print(f'Gradio版本: {gradio.__version__}')"
echo.
echo 检查模型文件:
if exist "models" (
    echo 模型目录存在
    dir models /B
) else (
    echo 模型目录不存在，请先下载模型
)
echo.
echo 按任意键返回主菜单...
pause >nul
goto MAIN_MENU

:EXIT
echo 感谢使用！
timeout /t 2 >nul
exit /b 0
