@echo off
echo ===================================
echo  本地大语言模型环境安装脚本
echo ===================================
echo.

echo 正在检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo 错误: 未找到Python环境，请先安装Python 3.8+
    pause
    exit /b 1
)

echo.
echo 正在检查CUDA环境...
python -c "import torch; print(f'PyTorch版本: {torch.__version__}'); print(f'CUDA可用: {torch.cuda.is_available()}')" 2>nul
if %errorlevel% neq 0 (
    echo 警告: PyTorch未安装或CUDA不可用
    echo 将安装CPU版本，性能可能较慢
)

echo.
echo 正在安装依赖包...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
if %errorlevel% neq 0 (
    echo 安装CUDA版本失败，尝试安装CPU版本...
    pip install torch torchvision torchaudio
)

pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 错误: 依赖包安装失败
    pause
    exit /b 1
)

echo.
echo ===================================
echo  安装完成！
echo ===================================
echo.
echo 使用方法:
echo 1. 下载模型: python download_model.py
echo 2. 终端对话: python chat_terminal.py
echo 3. Web界面: python chat_ui.py
echo.
pause
