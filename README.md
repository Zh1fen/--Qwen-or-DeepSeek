# 本地大语言模型对话系统

这是一个基于PyTorch和Transformers的本地大语言模型部署方案，专为NVIDIA RTX 4060等中端显卡优化。

## 🚀 特性

- **本地部署**: 完全离线运行，保护隐私
- **显存优化**: 支持4bit量化，适配4060等显卡
- **多模型支持**: 支持Qwen2和DeepSeek系列模型
- **双界面**: 提供终端和Web UI两种交互方式
- **易于使用**: 一键安装和启动

## 💻 系统要求

### 硬件要求
- **显卡**: NVIDIA RTX 4060 或更高（6GB+ 显存）
- **内存**: 16GB+ 系统内存
- **存储**: 20GB+ 可用空间（用于模型文件）

### 软件要求
- Windows 10/11
- Python 3.8-3.11
- CUDA 11.8+ (可选，用于GPU加速)

## 📦 安装步骤

### 1. 克隆或下载项目
```bash
# 如果使用Git
git clone <repository_url>
cd LLM

# 或直接下载解压到此目录
```

### 2. 运行安装脚本
```bash
# Windows用户
install.bat

# 或手动安装
pip install -r requirements.txt
```

### 3. 下载模型
```bash
python download_model.py
```

选择要下载的模型：
- **Qwen2-7B-Instruct**: 通用对话模型，中英文能力强
- **DeepSeek-Coder-7B**: 编程专用模型，代码生成能力强

## 📋 详细文件功能说明

### 核心模块
- **`local_llm_v2.py`**: 本地LLM核心引擎，负责模型加载、推理和生成
- **`config.py`**: 系统配置文件，包含模型参数和路径设置

### 下载工具
- **`download_model_v2.py`**: 增强版下载器（推荐）
  - 支持断点续传和重试机制
  - 文件完整性自动检查
  - 详细的下载进度和错误提示
- **`download_model.py`**: 基础版下载器
  - 支持多模型选择菜单
  - 包含LLM测试功能

### 对话界面
- **`chat_terminal_v2.py`**: 终端对话程序（推荐）
  - 自动模型检测和选择
  - 对话历史记录（最多10轮）
  - 丰富的交互命令（help、clear、history等）
  - 完善的错误处理和恢复
- **`chat_ui.py`**: Web界面核心组件
  - 基于Gradio构建的友好界面
  - 实时对话和参数调节

### 启动和修复工具
- **`gradio_launcher_fixed.py`**: 修复版Web启动器
  - 自动端口检测（7860起）
  - 多种启动方式自动尝试
  - 防火墙和网络问题自动处理
- **`fix_gradio.py`**: Gradio问题诊断工具
  - 端口占用检查
  - 网络连接诊断
  - 防火墙状态检查
  - 自动生成修复建议
- **`launcher.py`** & **`launcher.bat`**: 通用启动脚本
  - 一键启动整个系统
  - Windows用户友好的批处理文件

### 管理工具
- **`model_manager.py`**: 模型管理工具
- **`install.bat`**: Windows自动安装脚本

## 🎯 使用方法

### 1. 下载模型（推荐使用增强版）
```bash
# 增强版下载器（推荐）- 支持重试和断点续传
python download_model_v2.py

# 或使用基础版本 - 支持多模型选择
python download_model.py
```

### 2. 选择对话界面

#### 终端对话模式（推荐 - 稳定可靠）
```bash
python chat_terminal_v2.py
```
- 支持模型自动选择
- 包含对话历史记录
- 多种交互命令（help、clear、history等）

#### Web界面模式（友好界面）
```bash
# 如果遇到启动问题，先运行诊断工具
python fix_gradio.py

# 然后使用修复版启动器
python gradio_launcher_fixed.py
```
浏览器会自动打开对话界面，或手动访问显示的地址

### 3. 快速启动（Windows用户）
```bash
# 双击运行批处理文件
launcher.bat
```

## 📁 项目结构

```
LLM/
├── download_model.py          # 基础模型下载脚本（支持多模型选择）
├── download_model_v2.py       # 增强版模型下载脚本（重试机制、断点续传、完整性检查）
├── chat_terminal_v2.py        # 终端对话界面（改进版，支持模型选择、历史记录）
├── chat_ui.py                # Web对话界面核心组件
├── local_llm_v2.py           # 本地LLM核心类（模型加载、推理引擎）
├── gradio_launcher_fixed.py   # 修复版Web界面启动器（多种启动方式、端口自动检测）
├── fix_gradio.py             # Gradio问题诊断和修复工具
├── model_manager.py          # 模型管理工具
├── config.py                 # 配置文件
├── launcher.py               # 通用启动器
├── launcher.bat             # Windows批处理启动脚本
├── install.bat              # Windows自动安装脚本
├── requirements.txt         # Python依赖包列表
├── README.md               # 项目说明文档
└── models/                 # 模型文件目录（自动创建）
    ├── Qwen2-7B-Instruct/  # Qwen2-7B模型文件
    └── __pycache__/        # Python缓存文件
```

## ⚙️ 配置说明

### 生成参数
- **Temperature**: 控制回复的随机性（0.1-2.0）
- **Top-p**: 核采样参数（建议0.9）
- **Max tokens**: 最大生成长度（建议2048）

### 量化配置
- **4bit量化**: 大幅减少显存占用
- **Double quantization**: 进一步优化内存使用
- **NF4格式**: 平衡性能和精度

## 🔧 故障排除

### 快速诊断
```bash
# Web界面启动问题诊断
python fix_gradio.py
```

### 常见问题

1. **显存不足**
   ```
   错误: CUDA out of memory
   ```
   解决方案：
   - 减少max_new_tokens参数
   - 确保4bit量化已启用
   - 关闭其他GPU程序
   - 使用CPU模式运行

2. **模型加载失败**
   ```
   错误: Model loading failed
   ```
   解决方案：
   - 使用`download_model_v2.py`重新下载（支持完整性检查）
   - 检查模型文件完整性
   - 检查磁盘空间是否充足

3. **网络下载问题**
   ```
   错误: Connection timeout
   ```
   解决方案：
   - 使用`download_model_v2.py`的重试机制
   - 配置代理或VPN
   - 手动从HuggingFace下载模型文件

4. **Web界面无法访问**
   ```
   错误: localhost is not accessible
   ```
   解决方案：
   - 运行`fix_gradio.py`进行诊断
   - 使用`gradio_launcher_fixed.py`启动
   - 检查防火墙设置
   - 尝试使用终端版本`chat_terminal_v2.py`

5. **端口被占用**
   ```
   错误: Port 7860 is already in use
   ```
   解决方案：
   - `gradio_launcher_fixed.py`会自动寻找可用端口
   - 或手动指定其他端口

### 性能优化

1. **显存优化**
   - 启用4bit量化
   - 使用梯度检查点
   - 减少batch size

2. **速度优化**
   - 使用GPU推理
   - 开启CUDA缓存
   - 选择合适的精度

## 📊 模型对比

| 模型 | 参数量 | 显存需求 | 特点 | 推荐用途 |
|------|--------|----------|------|----------|
| Qwen2-7B | 7B | 6-8GB | 通用对话 | 日常聊天、问答 |
| DeepSeek-7B | 7B | 6-8GB | 代码生成 | 编程辅助 |

## 🛡️ 安全说明

- 所有计算在本地进行，不会上传数据
- 模型文件存储在本地，可离线使用
- 建议定期更新依赖包以获得安全补丁

## 📝 更新日志

### v1.0.0 (2024-07-06)
- 初始版本发布
- 支持Qwen2和DeepSeek模型
- 提供终端和Web界面
- 4bit量化优化

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

本项目采用MIT许可证。

## 🔗 相关链接

- [Qwen2模型](https://huggingface.co/Qwen/Qwen2-7B-Instruct)
- [DeepSeek模型](https://huggingface.co/deepseek-ai/deepseek-coder-7b-instruct-v1.5)
- [Transformers文档](https://huggingface.co/docs/transformers)
- [PyTorch文档](https://pytorch.org/docs/)
