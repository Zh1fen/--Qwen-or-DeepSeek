import os
import sys
import time
import logging
from pathlib import Path
from huggingface_hub import snapshot_download

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_model_with_retry(model_name="Qwen/Qwen2-7B-Instruct", max_retries=3):
    """使用重试机制下载模型"""
    model_dir = Path("./models") / model_name.split("/")[-1]
    
    for attempt in range(max_retries):
        try:
            logger.info(f"开始下载模型 {model_name} (尝试 {attempt + 1}/{max_retries})")
            
            # 创建模型目录
            model_dir.mkdir(parents=True, exist_ok=True)
            
            # 下载模型
            snapshot_download(
                repo_id=model_name,
                local_dir=str(model_dir),
                resume_download=True,  # 启用断点续传
                max_workers=1,  # 限制并发数
                token=None,  # 如果需要认证，可以添加token
            )
            
            logger.info(f"模型下载成功: {model_dir}")
            return str(model_dir)
            
        except Exception as e:
            logger.error(f"下载失败 (尝试 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                wait_time = 30 * (attempt + 1)  # 递增等待时间
                logger.info(f"等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
            else:
                logger.error("所有下载尝试均失败")
                return None

def check_model_integrity(model_dir):
    """检查模型文件完整性"""
    required_files = [
        "config.json",
        "generation_config.json", 
        "model.safetensors.index.json",
        "tokenizer.json",
        "tokenizer_config.json"
    ]
    
    model_path = Path(model_dir)
    missing_files = []
    
    for file_name in required_files:
        if not (model_path / file_name).exists():
            missing_files.append(file_name)
    
    if missing_files:
        logger.warning(f"缺少文件: {missing_files}")
        return False
    else:
        logger.info("模型文件检查完整")
        return True

def main():
    print("=== 稳定模型下载工具 ===")
    
    # 检查现有模型
    model_dir = "./models/Qwen2-7B-Instruct"
    if os.path.exists(model_dir):
        print(f"发现现有模型目录: {model_dir}")
        if check_model_integrity(model_dir):
            print("模型文件完整，可以直接使用")
            return model_dir
        else:
            print("模型文件不完整，将重新下载")
    
    # 下载模型
    downloaded_path = download_model_with_retry()
    
    if downloaded_path:
        if check_model_integrity(downloaded_path):
            print(f"模型下载并验证成功: {downloaded_path}")
            return downloaded_path
        else:
            print("模型下载完成但文件不完整，请重新运行脚本")
            return None
    else:
        print("模型下载失败")
        print("建议:")
        print("1. 检查网络连接")
        print("2. 尝试使用代理或VPN")
        print("3. 手动从 https://huggingface.co/Qwen/Qwen2-7B-Instruct 下载")
        return None

if __name__ == "__main__":
    main()
