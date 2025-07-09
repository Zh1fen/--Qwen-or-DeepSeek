#!/usr/bin/env python3
"""
Gradio启动问题诊断和修复工具
解决"When localhost is not accessible, a shareable link must be created"错误
"""

import socket
import subprocess
import sys
import os
from pathlib import Path

def check_port_availability(port=7860):
    """检查端口是否可用"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def check_localhost_connectivity():
    """检查localhost连接性"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect(('127.0.0.1', 80))
        return True
    except:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                s.connect(('localhost', 80))
            return True
        except:
            return False

def check_firewall_status():
    """检查Windows防火墙状态"""
    try:
        result = subprocess.run(
            ['netsh', 'advfirewall', 'show', 'allprofiles', 'state'],
            capture_output=True, text=True, shell=True
        )
        return "ON" in result.stdout
    except:
        return None

def get_running_processes_on_port(port=7860):
    """获取占用指定端口的进程"""
    try:
        result = subprocess.run(
            ['netstat', '-ano', '|', 'findstr', f':{port}'],
            capture_output=True, text=True, shell=True
        )
        return result.stdout.strip()
    except:
        return ""

def diagnose_gradio_issues():
    """诊断Gradio启动问题"""
    print("🔍 正在诊断Gradio启动问题...")
    print("=" * 50)
    
    issues = []
    fixes = []
    
    # 1. 检查端口可用性
    print("1. 检查端口7860可用性...")
    if not check_port_availability(7860):
        issues.append("端口7860被占用")
        processes = get_running_processes_on_port(7860)
        if processes:
            print(f"   ❌ 端口7860被占用:")
            print(f"   {processes}")
            fixes.append("终止占用端口7860的进程，或使用其他端口")
        else:
            print("   ❌ 端口7860不可用")
            fixes.append("尝试使用其他端口（如7861, 7862等）")
    else:
        print("   ✅ 端口7860可用")
    
    # 2. 检查localhost连接性
    print("2. 检查localhost连接性...")
    if not check_localhost_connectivity():
        issues.append("localhost连接失败")
        print("   ❌ 无法连接到localhost")
        fixes.append("检查网络适配器设置，确保loopback接口正常")
    else:
        print("   ✅ localhost连接正常")
    
    # 3. 检查防火墙状态
    print("3. 检查Windows防火墙...")
    firewall_on = check_firewall_status()
    if firewall_on:
        issues.append("防火墙可能阻止连接")
        print("   ⚠️  Windows防火墙已启用")
        fixes.append("添加Python到防火墙例外，或临时关闭防火墙")
    elif firewall_on is None:
        print("   ❓ 无法检查防火墙状态")
    else:
        print("   ✅ 防火墙已关闭")
    
    # 4. 检查Python和Gradio版本
    print("4. 检查Python和Gradio版本...")
    try:
        import gradio
        print(f"   ✅ Gradio版本: {gradio.__version__}")
    except ImportError:
        issues.append("Gradio未安装")
        print("   ❌ Gradio未安装")
        fixes.append("安装Gradio: pip install gradio")
    
    print(f"   ✅ Python版本: {sys.version}")
    
    return issues, fixes

def create_fixed_gradio_launcher():
    """创建修复版的Gradio启动器"""
    launcher_code = '''#!/usr/bin/env python3
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
        print("\\n💡 建议:")
        print("1. 检查防火墙设置")
        print("2. 以管理员权限运行")
        print("3. 使用终端版本: python chat_terminal.py")
'''
    
    with open("gradio_launcher_fixed.py", "w", encoding="utf-8") as f:
        f.write(launcher_code)
    
    print("✅ 已创建修复版启动器: gradio_launcher_fixed.py")

def apply_fixes():
    """应用修复方案"""
    print("\n🔧 正在应用修复方案...")
    
    # 创建修复版启动器
    create_fixed_gradio_launcher()
    
    # 提供修复建议
    print("\n💡 修复建议:")
    print("1. 使用修复版启动器:")
    print("   python gradio_launcher_fixed.py")
    print("\n2. 手动修复方法:")
    print("   - 关闭占用端口7860的程序")
    print("   - 添加Python到防火墙例外")
    print("   - 以管理员权限运行")
    print("\n3. 替代方案:")
    print("   - 使用终端版本: python chat_terminal.py")
    print("   - 使用notebook版本")

def main():
    """主函数"""
    print("🛠️  Gradio启动问题诊断和修复工具")
    print("=" * 50)
    
    # 诊断问题
    issues, fixes = diagnose_gradio_issues()
    
    # 显示结果
    print("\n📋 诊断结果:")
    if issues:
        print("❌ 发现问题:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        
        print("\n🔧 建议修复:")
        for i, fix in enumerate(fixes, 1):
            print(f"   {i}. {fix}")
    else:
        print("✅ 未发现明显问题")
    
    # 应用修复
    apply_fixes()
    
    print("\n🎯 快速启动:")
    print("python gradio_launcher_fixed.py")

if __name__ == "__main__":
    main()
