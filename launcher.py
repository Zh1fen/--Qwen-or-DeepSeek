#!/usr/bin/env python3
"""
本地大语言模型启动器
"""
import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """检查必要的依赖"""
    try:
        import torch
        import transformers
        import gradio
        return True
    except ImportError as e:
        print(f"缺少必要的依赖: {e}")
        print("请运行: pip install torch transformers gradio")
        return False

def check_model_exists():
    """检查是否有已下载的模型"""
    models_dir = Path("./models")
    if not models_dir.exists():
        return False
    
    for item in models_dir.iterdir():
        if item.is_dir():
            config_file = item / "config.json"
            if config_file.exists():
                return True
    return False

def main():
    print("=== 本地大语言模型启动器 ===")
    print()
    
    # 检查依赖
    if not check_requirements():
        return
    
    # 检查模型
    if not check_model_exists():
        print("未发现已下载的模型！")
        print("是否现在下载模型？")
        print("1. 是，下载Qwen2-7B-Instruct模型")
        print("2. 否，退出程序")
        
        choice = input("请选择 (1-2): ").strip()
        if choice == "1":
            print("开始下载模型...")
            try:
                subprocess.run([sys.executable, "download_model_v2.py"], check=True)
            except subprocess.CalledProcessError:
                print("模型下载失败，请手动运行: python download_model_v2.py")
                return
            except FileNotFoundError:
                print("找不到下载脚本，请手动运行: python download_model.py")
                return
        else:
            return
    
    # 选择界面类型
    print("\n请选择界面类型:")
    print("1. Web界面 (推荐) - 图形化界面，功能丰富")
    print("2. 终端界面 - 命令行界面，占用资源少")
    print("3. 退出")
    
    while True:
        choice = input("请选择 (1-3): ").strip()
        
        if choice == "1":
            print("正在启动Web界面...")
            try:
                subprocess.run([sys.executable, "chat_ui.py"], check=True)
            except subprocess.CalledProcessError:
                print("Web界面启动失败，尝试启动终端界面...")
                subprocess.run([sys.executable, "chat_terminal.py"])
            except KeyboardInterrupt:
                print("用户取消启动")
            break
            
        elif choice == "2":
            print("正在启动终端界面...")
            try:
                subprocess.run([sys.executable, "chat_terminal.py"], check=True)
            except subprocess.CalledProcessError:
                print("终端界面启动失败")
            except KeyboardInterrupt:
                print("用户取消启动")
            break
            
        elif choice == "3":
            print("退出程序")
            break
            
        else:
            print("无效选择，请输入1、2或3")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"发生错误: {e}")
