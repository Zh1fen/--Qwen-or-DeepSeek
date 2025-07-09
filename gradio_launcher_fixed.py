#!/usr/bin/env python3
"""
修复版Gradio启动器
支持多种启动方式和端口自动检测
"""

import gradio as gr
import socket
from chat_ui import create_interface

def find_available_port(start_port=7860, max_attempts=10):
    """查找可用端口"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def launch_gradio_robust():
    """稳健的Gradio启动方法"""
    print("🚀 启动修复版Gradio界面...")
    
    try:
        interface = create_interface()
    except Exception as e:
        print(f"❌ 创建界面失败: {e}")
        return False
    
    # 查找可用端口
    port = find_available_port()
    if not port:
        print("❌ 找不到可用端口")
        return False
    
    print(f"📡 使用端口: {port}")
    
    # 尝试不同的启动方式
    launch_configs = [
        {
            "name": "本地启动 (127.0.0.1)",
            "config": {
                "server_name": "127.0.0.1",
                "server_port": port,
                "share": False,
                "inbrowser": True
            }
        },
        {
            "name": "本地启动 (localhost)",
            "config": {
                "server_name": "localhost", 
                "server_port": port,
                "share": False,
                "inbrowser": True
            }
        },
        {
            "name": "全网络启动 (0.0.0.0)",
            "config": {
                "server_name": "0.0.0.0",
                "server_port": port,
                "share": False,
                "inbrowser": True
            }
        },
        {
            "name": "公共链接",
            "config": {
                "share": True,
                "inbrowser": True
            }
        }
    ]
    
    for config in launch_configs:
        print(f"🔄 尝试: {config['name']}...")
        try:
            interface.launch(**config['config'])
            print(f"✅ 成功启动: {config['name']}")
            return True
        except Exception as e:
            print(f"❌ {config['name']} 失败: {e}")
            continue
    
    print("❌ 所有启动方式都失败了")
    return False

if __name__ == "__main__":
    if not launch_gradio_robust():
        print("\n💡 建议:")
        print("1. 检查防火墙设置")
        print("2. 以管理员权限运行")
        print("3. 使用终端版本: python chat_terminal.py")
