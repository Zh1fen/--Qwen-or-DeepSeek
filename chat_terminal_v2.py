import os
import sys
from pathlib import Path
from local_llm_v2 import LocalLLM

def get_available_models():
    """获取已下载的模型列表"""
    models_dir = Path("./models")
    if not models_dir.exists():
        return []
    
    models = []
    for item in models_dir.iterdir():
        if item.is_dir():
            # 检查是否包含必要的模型文件
            config_file = item / "config.json"
            if config_file.exists():
                models.append(str(item))
    return models

def select_model():
    """选择要使用的模型"""
    models = get_available_models()
    
    if not models:
        print("未找到已下载的模型！")
        print("请先运行以下命令下载模型:")
        print("python download_model_v2.py")
        return None
    
    print("可用的模型:")
    for i, model in enumerate(models, 1):
        model_name = Path(model).name
        print(f"{i}. {model_name}")
    
    while True:
        try:
            choice = int(input(f"请选择模型 (1-{len(models)}): "))
            if 1 <= choice <= len(models):
                return models[choice - 1]
            else:
                print("无效选择，请重新输入")
        except ValueError:
            print("请输入数字")
        except KeyboardInterrupt:
            print("\n用户取消选择")
            return None

def check_model_files(model_path):
    """检查模型文件完整性"""
    required_files = [
        "config.json",
        "tokenizer_config.json"
    ]
    
    model_dir = Path(model_path)
    missing_files = []
    
    for file_name in required_files:
        if not (model_dir / file_name).exists():
            missing_files.append(file_name)
    
    if missing_files:
        print(f"警告：模型文件不完整，缺少: {missing_files}")
        print("建议重新下载模型")
        return False
    return True

def main():
    print("=== 本地大语言模型对话 (改进版) ===")
    print("输入 'quit' 或 'exit' 退出程序")
    print("输入 'clear' 清屏")
    print("输入 'help' 查看帮助")
    print("-" * 50)
    
    # 选择模型
    model_path = select_model()
    if not model_path:
        return
    
    # 检查模型文件
    if not check_model_files(model_path):
        response = input("是否继续尝试加载？(y/n): ")
        if response.lower() not in ['y', 'yes']:
            return
    
    # 初始化模型
    print(f"\n正在初始化模型: {Path(model_path).name}")
    llm = LocalLLM(model_path)
    
    if not llm.load_model():
        print("模型加载失败，程序退出")
        print("\n可能的解决方案:")
        print("1. 检查模型文件是否完整")
        print("2. 确保有足够的GPU/CPU内存")
        print("3. 重新下载模型文件")
        return
    
    # 测试模型
    print("正在测试模型...")
    if not llm.test_model():
        print("模型测试失败，但可以尝试继续使用")
    
    print("\n模型准备就绪！开始对话...")
    print("-" * 50)
    
    # 对话循环
    conversation_history = []
    
    while True:
        try:
            # 获取用户输入
            user_input = input("\n用户: ").strip()
            
            # 处理特殊命令
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("再见！")
                break
            
            if user_input.lower() == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            
            if user_input.lower() == 'help':
                print("\n可用命令:")
                print("quit/exit - 退出程序")
                print("clear - 清屏")
                print("help - 显示此帮助")
                print("history - 显示对话历史")
                continue
            
            if user_input.lower() == 'history':
                print("\n对话历史:")
                for i, (user, assistant) in enumerate(conversation_history, 1):
                    print(f"{i}. 用户: {user}")
                    print(f"   助手: {assistant}")
                continue
            
            if not user_input:
                continue
            
            # 生成回复
            print("助手: ", end="", flush=True)
            response = llm.generate_response(user_input)
            print(response)
            
            # 保存对话历史
            conversation_history.append((user_input, response))
            
            # 限制历史长度
            if len(conversation_history) > 10:
                conversation_history.pop(0)
            
        except KeyboardInterrupt:
            print("\n\n程序被用户中断")
            break
        except Exception as e:
            print(f"\n发生错误: {e}")
            print("程序将继续运行，您可以重试或输入 'quit' 退出")

if __name__ == "__main__":
    main()
