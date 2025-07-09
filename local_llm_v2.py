import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocalLLM:
    def __init__(self, model_path):
        self.model_path = model_path
        self.tokenizer = None
        self.model = None
        self.device = self._get_device()
        
    def _get_device(self):
        """获取可用设备"""
        if torch.cuda.is_available():
            device = "cuda"
            # 获取GPU显存信息
            total_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
            logger.info(f"使用设备: {device}")
            logger.info(f"GPU显存: {total_memory:.1f} GB")
        else:
            device = "cpu"
            logger.info(f"使用设备: {device}")
        return device
    
    def load_model(self):
        """加载模型和分词器"""
        try:
            logger.info("正在加载模型...")
            
            # 检查模型路径
            if not os.path.exists(self.model_path):
                logger.error(f"模型路径不存在: {self.model_path}")
                return False
            
            # 检查必要文件
            required_files = ["config.json", "tokenizer_config.json"]
            for file_name in required_files:
                file_path = os.path.join(self.model_path, file_name)
                if not os.path.exists(file_path):
                    logger.error(f"缺少必要文件: {file_path}")
                    return False
            
            # 加载分词器
            logger.info("正在加载分词器...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                trust_remote_code=True,
                local_files_only=True
            )
            
            # 设置模型加载参数
            model_kwargs = {
                "torch_dtype": torch.bfloat16 if self.device == "cuda" else torch.float32,
                "device_map": "auto" if self.device == "cuda" else None,
                "trust_remote_code": True,
                "local_files_only": True
            }
            
            # 如果GPU显存不足，启用量化模式
            if self.device == "cuda":
                total_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
                if total_memory < 12:  # 如果显存小于12GB
                    logger.info("GPU显存较小，启用4bit量化模式")
                    
                    # 配置4bit量化（推荐）
                    quantization_config = BitsAndBytesConfig(
                        load_in_4bit=True,
                        bnb_4bit_compute_dtype=torch.float16,
                        bnb_4bit_use_double_quant=True,
                        bnb_4bit_quant_type="nf4",
                        llm_int8_enable_fp32_cpu_offload=True  # 允许CPU卸载
                    )
                    
                    model_kwargs.update({
                        "quantization_config": quantization_config,
                        "torch_dtype": torch.float16,
                        "low_cpu_mem_usage": True
                    })
            
            # 加载模型
            logger.info("正在加载模型...")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                **model_kwargs
            )
            
            # 如果使用CPU，移动模型到CPU
            if self.device == "cpu":
                self.model = self.model.to("cpu")
            
            logger.info("模型加载完成！")
            return True
            
        except Exception as e:
            logger.error(f"模型加载失败: {e}")
            
            # 如果是显存相关错误，尝试CPU模式
            if any(keyword in str(e).lower() for keyword in ["out of memory", "dispatch", "cpu", "disk"]):
                logger.warning("GPU加载失败，尝试使用CPU模式（速度较慢）...")
                try:
                    # CPU模式重新加载
                    cpu_kwargs = {
                        "torch_dtype": torch.float32,
                        "device_map": "cpu",
                        "trust_remote_code": True,
                        "local_files_only": True,
                        "low_cpu_mem_usage": True
                    }
                    
                    self.model = AutoModelForCausalLM.from_pretrained(
                        self.model_path,
                        **cpu_kwargs
                    )
                    self.device = "cpu"
                    logger.info("成功使用CPU模式加载模型")
                    return True
                    
                except Exception as cpu_error:
                    logger.error(f"CPU模式也失败了: {cpu_error}")
            
            # 提供解决建议
            if "out of memory" in str(e).lower():
                logger.error("GPU显存不足！建议:")
                logger.error("1. 关闭其他占用GPU的程序")
                logger.error("2. 重启程序再试")
                logger.error("3. 使用更小的模型")
            return False
    
    def generate_response(self, user_input, max_length=512, temperature=0.7):
        """生成回复"""
        if not self.model or not self.tokenizer:
            return "错误：模型未加载"
        
        try:
            # 构建对话格式
            messages = [
                {"role": "system", "content": "你是一个有用的AI助手。"},
                {"role": "user", "content": user_input}
            ]
            
            # 应用聊天模板
            text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            
            # 编码输入
            model_inputs = self.tokenizer([text], return_tensors="pt")
            
            # 确保输入在正确的设备上
            if self.device == "cuda" and torch.cuda.is_available():
                model_inputs = model_inputs.to("cuda")
            else:
                model_inputs = model_inputs.to("cpu")
            
            # 生成回复
            with torch.no_grad():
                generated_ids = self.model.generate(
                    model_inputs.input_ids,
                    max_new_tokens=max_length,
                    temperature=temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    attention_mask=model_inputs.attention_mask
                )
            
            # 解码回复
            generated_ids = [
                output_ids[len(input_ids):] for input_ids, output_ids in 
                zip(model_inputs.input_ids, generated_ids)
            ]
            
            response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
            return response.strip()
            
        except Exception as e:
            logger.error(f"生成回复时出错: {e}")
            if "out of memory" in str(e).lower():
                return "错误：GPU显存不足，请减少输入长度或重启程序"
            return f"错误：{e}"
    
    def test_model(self):
        """测试模型是否正常工作"""
        if not self.model or not self.tokenizer:
            return False
        
        try:
            test_response = self.generate_response("你好", max_length=50)
            logger.info(f"模型测试成功，回复: {test_response}")
            return True
        except Exception as e:
            logger.error(f"模型测试失败: {e}")
            return False
