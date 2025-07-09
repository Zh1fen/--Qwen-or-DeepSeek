# Local Large Language Model Chat System

This is a local large language model deployment solution based on PyTorch and Transformers, optimized for mid-range graphics cards like NVIDIA RTX 4060.

## 🚀 Features

- **Local Deployment**: Completely offline operation, protecting privacy
- **Memory Optimization**: Supports 4-bit quantization, compatible with RTX 4060 and similar cards
- **Multi-Model Support**: Supports Qwen2 and DeepSeek series models
- **Dual Interface**: Provides both terminal and Web UI interaction modes
- **Easy to Use**: One-click installation and startup

## 💻 System Requirements

### Hardware Requirements
- **Graphics Card**: NVIDIA RTX 4060 or higher (6GB+ VRAM)
- **Memory**: 16GB+ system memory
- **Storage**: 20GB+ available space (for model files)

### Software Requirements
- Windows 10/11
- Python 3.8-3.11
- CUDA 11.8+ (optional, for GPU acceleration)

## 📦 Installation Steps

### 1. Clone or Download the Project
```bash
# If using Git
git clone <repository_url>
cd LLM

# Or download and extract to this directory
```

### 2. Run Installation Script
```bash
# Windows users
install.bat

# Or manual installation
pip install -r requirements.txt
```

### 3. Download Models
```bash
python download_model.py
```

Choose the model to download:
- **Qwen2-7B-Instruct**: General conversation model, strong Chinese and English capabilities
- **DeepSeek-Coder-7B**: Programming-specific model, strong code generation capabilities

## 📋 Detailed File Function Description

### Core Modules
- **`local_llm_v2.py`**: Local LLM core engine, responsible for model loading, inference, and generation
- **`config.py`**: System configuration file, containing model parameters and path settings

### Download Tools
- **`download_model_v2.py`**: Enhanced downloader (recommended)
  - Supports resume download and retry mechanism
  - Automatic file integrity check
  - Detailed download progress and error prompts
- **`download_model.py`**: Basic downloader
  - Supports multi-model selection menu
  - Includes LLM testing functionality

### Chat Interfaces
- **`chat_terminal_v2.py`**: Terminal chat program (recommended)
  - Automatic model detection and selection
  - Conversation history recording (up to 10 rounds)
  - Rich interactive commands (help, clear, history, etc.)
  - Comprehensive error handling and recovery
- **`chat_ui.py`**: Web interface core component
  - User-friendly interface built with Gradio
  - Real-time conversation and parameter adjustment

### Launch and Repair Tools
- **`gradio_launcher_fixed.py`**: Fixed Web launcher
  - Automatic port detection (starting from 7860)
  - Multiple launch methods automatic retry
  - Automatic handling of firewall and network issues
- **`fix_gradio.py`**: Gradio problem diagnosis tool
  - Port occupancy check
  - Network connection diagnosis
  - Firewall status check
  - Automatic repair suggestions generation
- **`launcher.py`** & **`launcher.bat`**: Universal launch scripts
  - One-click system startup
  - Windows user-friendly batch files

### Management Tools
- **`model_manager.py`**: Model management tool
- **`install.bat`**: Windows automatic installation script

## 🎯 Usage Methods

### 1. Download Models (Recommended to use enhanced version)
```bash
# Enhanced downloader (recommended) - supports retry and resume download
python download_model_v2.py

# Or use basic version - supports multi-model selection
python download_model.py
```

### 2. Choose Chat Interface

#### Terminal Chat Mode (Recommended - Stable and Reliable)
```bash
python chat_terminal_v2.py
```
- Supports automatic model selection
- Includes conversation history recording
- Multiple interactive commands (help, clear, history, etc.)

#### Web Interface Mode (User-friendly Interface)
```bash
# If encountering startup issues, run diagnostic tool first
python fix_gradio.py

# Then use the fixed launcher
python gradio_launcher_fixed.py
```
Browser will automatically open the chat interface, or manually access the displayed address

### 3. Quick Start (Windows Users)
```bash
# Double-click to run batch file
launcher.bat
```

## 📁 Project Structure

```
LLM/
├── download_model.py          # Basic model download script (supports multi-model selection)
├── download_model_v2.py       # Enhanced model download script (retry mechanism, resume download, integrity check)
├── chat_terminal_v2.py        # Terminal chat interface (improved version, supports model selection, history recording)
├── chat_ui.py                # Web chat interface core component
├── local_llm_v2.py           # Local LLM core class (model loading, inference engine)
├── gradio_launcher_fixed.py   # Fixed Web interface launcher (multiple launch methods, automatic port detection)
├── fix_gradio.py             # Gradio problem diagnosis and repair tool
├── model_manager.py          # Model management tool
├── config.py                 # Configuration file
├── launcher.py               # Universal launcher
├── launcher.bat             # Windows batch launch script
├── install.bat              # Windows automatic installation script
├── requirements.txt         # Python dependency list
├── README.md               # Project documentation
└── models/                 # Model files directory (automatically created)
    ├── Qwen2-7B-Instruct/  # Qwen2-7B model files
    └── __pycache__/        # Python cache files
```

## ⚙️ Configuration Description

### Generation Parameters
- **Temperature**: Controls reply randomness (0.1-2.0)
- **Top-p**: Nucleus sampling parameter (recommended 0.9)
- **Max tokens**: Maximum generation length (recommended 2048)

### Quantization Configuration
- **4-bit quantization**: Significantly reduces VRAM usage
- **Double quantization**: Further optimizes memory usage
- **NF4 format**: Balances performance and precision

## 🔧 Troubleshooting

### Quick Diagnosis
```bash
# Web interface startup problem diagnosis
python fix_gradio.py
```

### Common Issues

1. **Insufficient VRAM**
   ```
   Error: CUDA out of memory
   ```
   Solutions:
   - Reduce max_new_tokens parameter
   - Ensure 4-bit quantization is enabled
   - Close other GPU programs
   - Use CPU mode

2. **Model Loading Failed**
   ```
   Error: Model loading failed
   ```
   Solutions:
   - Use `download_model_v2.py` to re-download (supports integrity check)
   - Check model file integrity
   - Check if disk space is sufficient

3. **Network Download Issues**
   ```
   Error: Connection timeout
   ```
   Solutions:
   - Use `download_model_v2.py`'s retry mechanism
   - Configure proxy or VPN
   - Manually download model files from HuggingFace

4. **Web Interface Inaccessible**
   ```
   Error: localhost is not accessible
   ```
   Solutions:
   - Run `fix_gradio.py` for diagnosis
   - Use `gradio_launcher_fixed.py` to launch
   - Check firewall settings
   - Try using terminal version `chat_terminal_v2.py`

5. **Port Already in Use**
   ```
   Error: Port 7860 is already in use
   ```
   Solutions:
   - `gradio_launcher_fixed.py` will automatically find available ports
   - Or manually specify other ports

### Performance Optimization

1. **VRAM Optimization**
   - Enable 4-bit quantization
   - Use gradient checkpointing
   - Reduce batch size

2. **Speed Optimization**
   - Use GPU inference
   - Enable CUDA cache
   - Choose appropriate precision

## 📊 Model Comparison

| Model | Parameters | VRAM Requirement | Features | Recommended Use |
|-------|------------|------------------|----------|-----------------|
| Qwen2-7B | 7B | 6-8GB | General conversation | Daily chat, Q&A |
| DeepSeek-7B | 7B | 6-8GB | Code generation | Programming assistance |

## 🛡️ Security Notes

- All computations are performed locally, no data uploaded
- Model files are stored locally, can be used offline
- Recommend regularly updating dependency packages for security patches

## 📝 Changelog

### v1.0.0 (2024-07-06)
- Initial version release
- Support for Qwen2 and DeepSeek models
- Provides terminal and Web interfaces
- 4-bit quantization optimization

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

This project is licensed under the MIT License.

## 🔗 Related Links

- [Qwen2 Model](https://huggingface.co/Qwen/Qwen2-7B-Instruct)
- [DeepSeek Model](https://huggingface.co/deepseek-ai/deepseek-coder-7b-instruct-v1.5)
- [Transformers Documentation](https://huggingface.co/docs/transformers)
- [PyTorch Documentation](https://pytorch.org/docs/)
