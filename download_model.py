import os
import torch
from huggingface_hub import snapshot_download
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import warnings
warnings.filterwarnings("ignore")

class ModelDownloader:
    def __init__(self):
        self.model_dir = "./models"
        os.makedirs(self.model_dir, exist_ok=True)
        
    def download_qwen2_7b(self):
        """下载Qwen2-7B-Instruct模型"""
        model_name = "Qwen/Qwen2-7B-Instruct"
        model_path = os.path.join(self.model_dir, "Qwen2-7B-Instruct")
        
        print(f"开始下载模型: {model_name}")
        print("这可能需要一些时间，请耐心等待...")
        
        try:
            # 下载模型文件
            snapshot_download(
                repo_id=model_name,
                local_dir=model_path,
                local_dir_use_symlinks=False,
                resume_download=True
            )
            print(f"模型下载完成，保存在: {model_path}")
            return model_path
        except Exception as e:
            print(f"下载失败: {e}")
            return None
    
    def download_deepseek_7b(self):
        """下载DeepSeek-Coder-7B-Instruct模型"""
        model_name = "deepseek-ai/deepseek-coder-7b-instruct-v1.5"
        model_path = os.path.join(self.model_dir, "deepseek-coder-7b-instruct")
        
        print(f"开始下载模型: {model_name}")
        print("这可能需要一些时间，请耐心等待...")
        
        try:
            # 下载模型文件
            snapshot_download(
                repo_id=model_name,
                local_dir=model_path,
                local_dir_use_symlinks=False,
                resume_download=True
            )
            print(f"模型下载完成，保存在: {model_path}")
            return model_path
        except Exception as e:
            print(f"下载失败: {e}")
            return None

class LocalLLM:
    def __init__(self, model_path):
        self.model_path = model_path
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.tokenizer = None
        
        print(f"使用设备: {self.device}")
        if self.device == "cuda":
            print(f"GPU显存: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    
    def load_model(self):
        """加载模型和分词器"""
        print("正在加载模型...")
        
        # 配置量化以减少显存占用
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        )
        
        try:
            # 加载分词器
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                trust_remote_code=True
            )
            
            # 加载模型
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype=torch.float16,
                device_map="auto",
                quantization_config=quantization_config if self.device == "cuda" else None,
                trust_remote_code=True
            )
            
            print("模型加载完成!")
            return True
            
        except Exception as e:
            print(f"模型加载失败: {e}")
            return False
    
    def generate_response(self, prompt, max_length=2048, temperature=0.7):
        """生成回复"""
        if self.model is None or self.tokenizer is None:
            return "模型未加载，请先加载模型"
        
        try:
            # 构建对话格式
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
            
            # 应用聊天模板
            text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            
            # 编码输入
            inputs = self.tokenizer(text, return_tensors="pt").to(self.device)
            
            # 生成回复
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_length,
                    temperature=temperature,
                    do_sample=True,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # 解码输出
            response = self.tokenizer.decode(
                outputs[0][inputs['input_ids'].shape[1]:], 
                skip_special_tokens=True
            )
            
            return response.strip()
            
        except Exception as e:
            return f"生成回复时出错: {e}"

def main():
    print("=== 本地大语言模型下载器 ===")
    print("1. 下载 Qwen2-7B-Instruct (推荐)")
    print("2. 下载 DeepSeek-Coder-7B-Instruct")
    print("3. 退出")
    
    choice = input("请选择要下载的模型 (1-3): ").strip()
    
    downloader = ModelDownloader()
    model_path = None
    
    if choice == "1":
        model_path = downloader.download_qwen2_7b()
    elif choice == "2":
        model_path = downloader.download_deepseek_7b()
    elif choice == "3":
        print("退出下载")
        return
    else:
        print("无效选择")
        return
    
    if model_path:
        print(f"\n模型已下载到: {model_path}")
        print("您现在可以运行 chat_terminal.py 或 chat_ui.py 来开始对话")

if __name__ == "__main__":
    main()
