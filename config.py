# 模型配置
MODEL_CONFIG = {
    "qwen2_7b": {
        "repo_id": "Qwen/Qwen2-7B-Instruct",
        "model_name": "Qwen2-7B-Instruct",
        "description": "Qwen2 7B模型，通用对话能力强",
        "memory_required": "6-8GB"
    },
    "deepseek_7b": {
        "repo_id": "deepseek-ai/deepseek-coder-7b-instruct-v1.5",
        "model_name": "deepseek-coder-7b-instruct",
        "description": "DeepSeek编程专用模型",
        "memory_required": "6-8GB"
    }
}

# 生成参数配置
GENERATION_CONFIG = {
    "temperature": 0.7,
    "top_p": 0.9,
    "max_new_tokens": 2048,
    "do_sample": True,
    "repetition_penalty": 1.1
}

# 量化配置
QUANTIZATION_CONFIG = {
    "load_in_4bit": True,
    "bnb_4bit_compute_dtype": "float16",
    "bnb_4bit_use_double_quant": True,
    "bnb_4bit_quant_type": "nf4"
}
