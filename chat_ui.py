import os
import gradio as gr
from download_model import LocalLLM

class ChatUI:
    def __init__(self):
        self.llm = None
        self.model_loaded = False
        
    def get_available_models(self):
        """获取已下载的模型列表"""
        models_dir = "./models"
        if not os.path.exists(models_dir):
            return []
        
        models = []
        for item in os.listdir(models_dir):
            model_path = os.path.join(models_dir, item)
            if os.path.isdir(model_path):
                models.append(os.path.basename(model_path))
        return models
    
    def load_model(self, model_name, progress=gr.Progress()):
        """加载选定的模型"""
        if not model_name:
            return "请选择一个模型"
        
        model_path = os.path.join("./models", model_name)
        if not os.path.exists(model_path):
            return f"模型路径不存在: {model_path}"
        
        progress(0.1, desc="初始化模型...")
        self.llm = LocalLLM(model_path)
        
        progress(0.5, desc="加载模型文件...")
        success = self.llm.load_model()
        
        if success:
            self.model_loaded = True
            progress(1.0, desc="加载完成！")
            return f"模型 {model_name} 加载成功！"
        else:
            self.model_loaded = False
            return f"模型 {model_name} 加载失败"
    
    def chat_response(self, message, history, temperature, max_length):
        """生成聊天回复"""
        if not self.model_loaded or self.llm is None:
            return history + [("请先加载模型", "")]
        
        if not message.strip():
            return history + [("", "请输入有效的消息")]
        
        # 生成回复
        response = self.llm.generate_response(
            message, 
            max_length=max_length, 
            temperature=temperature
        )
        
        # 更新历史记录
        history.append((message, response))
        return history
    
    def clear_chat(self):
        """清空聊天记录"""
        return []

def create_interface():
    """创建Gradio界面"""
    chat_ui = ChatUI()
    
    with gr.Blocks(title="本地大语言模型对话", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🤖 本地大语言模型对话系统")
        gr.Markdown("基于Qwen2或DeepSeek的本地部署方案")
        
        with gr.Row():
            with gr.Column(scale=2):
                # 模型选择和加载
                with gr.Group():
                    gr.Markdown("### 📂 模型管理")
                    model_dropdown = gr.Dropdown(
                        choices=chat_ui.get_available_models(),
                        label="选择模型",
                        info="请先下载模型"
                    )
                    refresh_btn = gr.Button("🔄 刷新模型列表", size="sm")
                    load_btn = gr.Button("🚀 加载模型", variant="primary")
                    load_status = gr.Textbox(
                        label="加载状态",
                        interactive=False,
                        placeholder="请选择并加载模型"
                    )
                
                # 参数设置
                with gr.Group():
                    gr.Markdown("### ⚙️ 生成参数")
                    temperature = gr.Slider(
                        minimum=0.1, 
                        maximum=2.0, 
                        value=0.7, 
                        step=0.1,
                        label="Temperature (创造性)",
                        info="值越高回复越有创造性"
                    )
                    max_length = gr.Slider(
                        minimum=128, 
                        maximum=4096, 
                        value=2048, 
                        step=128,
                        label="最大回复长度",
                        info="生成回复的最大token数"
                    )
            
            with gr.Column(scale=3):
                # 聊天界面
                gr.Markdown("### 💬 对话区域")
                chatbot = gr.Chatbot(
                    height=500,
                    show_label=False,
                    container=True,
                    bubble_full_width=False
                )
                
                with gr.Row():
                    msg_input = gr.Textbox(
                        placeholder="在这里输入您的消息...",
                        show_label=False,
                        scale=4,
                        container=False
                    )
                    send_btn = gr.Button("📤 发送", variant="primary", scale=1)
                
                with gr.Row():
                    clear_btn = gr.Button("🗑️ 清空对话", variant="secondary")
                    stop_btn = gr.Button("⏹️ 停止生成", variant="stop")
        
        # 使用说明
        with gr.Accordion("📋 使用说明", open=False):
            gr.Markdown("""
            **使用步骤:**
            1. 确保已运行 `python download_model.py` 下载模型
            2. 在模型管理区域选择要使用的模型
            3. 点击"加载模型"按钮，等待加载完成
            4. 在对话区域输入消息并发送
            
            **参数说明:**
            - **Temperature**: 控制回复的随机性和创造性，0.1-2.0
            - **最大回复长度**: 限制每次回复的最大长度
            
            **注意事项:**
            - 首次加载模型需要较长时间，请耐心等待
            - 建议根据显卡性能调整参数
            - 4060显卡建议使用4bit量化降低显存占用
            """)
        
        # 事件绑定
        refresh_btn.click(
            fn=lambda: gr.Dropdown(choices=chat_ui.get_available_models()),
            outputs=model_dropdown
        )
        
        load_btn.click(
            fn=chat_ui.load_model,
            inputs=model_dropdown,
            outputs=load_status
        )
        
        msg_input.submit(
            fn=chat_ui.chat_response,
            inputs=[msg_input, chatbot, temperature, max_length],
            outputs=chatbot
        ).then(
            lambda: "",
            outputs=msg_input
        )
        
        send_btn.click(
            fn=chat_ui.chat_response,
            inputs=[msg_input, chatbot, temperature, max_length],
            outputs=chatbot
        ).then(
            lambda: "",
            outputs=msg_input
        )
        
        clear_btn.click(
            fn=chat_ui.clear_chat,
            outputs=chatbot
        )
    
    return interface

def main():
    """启动Web界面"""
    print("正在启动Web界面...")
    interface = create_interface()
    
    # 启动服务器
    interface.launch(
        server_name="127.0.0.1",
        server_port=7860,
        show_api=False,
        share=False,
        inbrowser=True
    )

if __name__ == "__main__":
    main()
