import os
import shutil
from pathlib import Path
import json

class ModelManager:
    def __init__(self):
        self.models_dir = Path("./models")
        self.models_dir.mkdir(exist_ok=True)
        self.info_file = self.models_dir / "models_info.json"
    
    def get_model_info(self):
        """获取模型信息"""
        if self.info_file.exists():
            with open(self.info_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_model_info(self, info):
        """保存模型信息"""
        with open(self.info_file, 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=2)
    
    def list_models(self):
        """列出所有已下载的模型"""
        models = []
        for item in self.models_dir.iterdir():
            if item.is_dir() and item.name != "__pycache__":
                size = self.get_folder_size(item)
                models.append({
                    "name": item.name,
                    "path": str(item),
                    "size": self.format_size(size),
                    "size_bytes": size
                })
        return models
    
    def get_folder_size(self, folder_path):
        """计算文件夹大小"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(folder_path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except (OSError, FileNotFoundError):
                        pass
        except (OSError, FileNotFoundError):
            pass
        return total_size
    
    def format_size(self, size_bytes):
        """格式化文件大小显示"""
        if size_bytes == 0:
            return "0 B"
        
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        unit_index = 0
        size = float(size_bytes)
        
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        
        return f"{size:.1f} {units[unit_index]}"
    
    def delete_model(self, model_name):
        """删除指定模型"""
        model_path = self.models_dir / model_name
        if model_path.exists():
            try:
                shutil.rmtree(model_path)
                print(f"模型 {model_name} 删除成功")
                return True
            except Exception as e:
                print(f"删除模型失败: {e}")
                return False
        else:
            print(f"模型 {model_name} 不存在")
            return False
    
    def get_disk_usage(self):
        """获取磁盘使用情况"""
        total_size = 0
        for model in self.list_models():
            total_size += model["size_bytes"]
        
        return {
            "total_models": len(self.list_models()),
            "total_size": self.format_size(total_size),
            "total_size_bytes": total_size
        }

def main():
    manager = ModelManager()
    
    while True:
        print("\n" + "="*50)
        print("           模型管理工具")
        print("="*50)
        
        models = manager.list_models()
        disk_usage = manager.get_disk_usage()
        
        print(f"\n当前状态:")
        print(f"已下载模型: {disk_usage['total_models']} 个")
        print(f"占用空间: {disk_usage['total_size']}")
        
        if models:
            print(f"\n已下载的模型:")
            for i, model in enumerate(models, 1):
                print(f"{i}. {model['name']} ({model['size']})")
        else:
            print("\n暂无已下载的模型")
        
        print(f"\n操作选项:")
        print("1. 刷新列表")
        print("2. 删除模型")
        print("3. 查看详细信息")
        print("4. 返回主程序")
        
        choice = input("\n请选择操作 (1-4): ").strip()
        
        if choice == "1":
            continue
        elif choice == "2":
            if not models:
                print("没有可删除的模型")
                continue
            
            print("\n选择要删除的模型:")
            for i, model in enumerate(models, 1):
                print(f"{i}. {model['name']}")
            
            try:
                model_idx = int(input("请输入模型编号: ")) - 1
                if 0 <= model_idx < len(models):
                    model_name = models[model_idx]['name']
                    confirm = input(f"确认删除模型 {model_name}? (y/N): ").lower()
                    if confirm == 'y':
                        manager.delete_model(model_name)
                    else:
                        print("取消删除")
                else:
                    print("无效的模型编号")
            except ValueError:
                print("请输入有效的数字")
        
        elif choice == "3":
            if not models:
                print("没有可查看的模型")
                continue
            
            print("\n模型详细信息:")
            for model in models:
                print(f"\n模型名称: {model['name']}")
                print(f"存储路径: {model['path']}")
                print(f"文件大小: {model['size']}")
                
                # 检查模型文件
                model_path = Path(model['path'])
                config_file = model_path / "config.json"
                if config_file.exists():
                    try:
                        with open(config_file, 'r', encoding='utf-8') as f:
                            config = json.load(f)
                        print(f"模型类型: {config.get('model_type', 'Unknown')}")
                        print(f"架构: {config.get('architectures', ['Unknown'])[0]}")
                    except:
                        print("无法读取配置文件")
        
        elif choice == "4":
            break
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    main()
