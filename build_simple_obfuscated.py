#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FFXIV日志编辑器简化混淆打包脚本
使用PyInstaller的基础混淆功能
"""

import os
import sys
import subprocess
import shutil
import random
import string
import re

def install_pyinstaller():
    """安装PyInstaller"""
    print("正在安装PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller==6.3.0"])
        print("PyInstaller安装成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"安装PyInstaller失败: {e}")
        return False

def generate_random_string(length=8):
    """生成随机字符串"""
    # 确保第一个字符是字母
    first_char = random.choice(string.ascii_letters)
    rest_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=length-1))
    return first_char + rest_chars

def obfuscate_code():
    """混淆代码"""
    print("开始混淆代码...")
    
    # 读取原始main.py
    with open("main.py", "r", encoding="utf-8") as f:
        original_code = f.read()
    
    # 创建混淆后的代码
    obfuscated_code = original_code
    
    # 1. 混淆类名和方法名（保护重要类名）
    class_mapping = {}
    method_mapping = {}
    
    # 定义需要保护的类名（这些类名不应该被混淆）
    protected_classes = {
        'object', 'Exception', 'ValueError', 'FFXIVLogEntry', 
        'DamageCalculator', 'LogParser', 'FFXIVLogsGUI'
    }
    
    # 查找类定义
    class_pattern = r'class\s+(\w+)\s*[:\(]'
    classes = re.findall(class_pattern, obfuscated_code)
    
    for class_name in classes:
        if class_name not in protected_classes:
            new_name = generate_random_string(10)
            class_mapping[class_name] = new_name
            obfuscated_code = re.sub(r'\b' + class_name + r'\b', new_name, obfuscated_code)
    
    # 定义需要保护的方法名（这些方法名不应该被混淆）
    protected_methods = {
        '__init__', '__main__', 'main', 'load_file', 'load_file_by_path',
        'save_file', 'parse_file', 'parse_line', 'encode_damage', 'decode_damage',
        'calculate_checksum', 'validate_checksum', 'to_dict', 'update_values',
        'get_decoded_damage', 'set_damage_from_int', 'is_valid_damage',
        'get_modified_line', 'setup_ui', 'apply_filters', 'clear_filters',
        'refresh_tree', 'on_entry_select', 'populate_edit_fields',
        'update_damage_calculation', 'decode_damage', 'encode_damage',
        'clear_edit_fields', 'update_entry', 'apply_damage_multiplier',
        'extract_unique_values', 'update_filter_combos', 'update_dynamic_filters',
        'calculate_target_total_damage', 'get_flags_comment'
    }
    
    # 查找方法定义
    method_pattern = r'def\s+(\w+)\s*\('
    methods = re.findall(method_pattern, obfuscated_code)
    
    for method_name in methods:
        if method_name not in protected_methods:
            new_name = generate_random_string(8)
            method_mapping[method_name] = new_name
            obfuscated_code = re.sub(r'\b' + method_name + r'\b', new_name, obfuscated_code)
    
    # 2. 混淆变量名（保护重要属性名）
    # 定义需要保护的属性名（这些属性名不应该被混淆）
    protected_attributes = {
        'root', 'main_frame', 'tree', 'source', 'target', 'ability', 'damage',
        'flags', 'timestamp', 'checksum', 'line_number', 'raw_line',
        'source_id', 'target_id', 'id', 'log_entries', 'filtered_entries',
        'original_file_path', 'file_label', 'status_var', 'source_var',
        'ability_var', 'target_var', 'target_damage_var', 'sources',
        'abilities', 'targets', 'excluded_abilities'
    }
    
    var_pattern = r'self\.(\w+)\s*='
    variables = re.findall(var_pattern, obfuscated_code)
    
    for var_name in variables:
        if var_name not in protected_attributes:
            new_name = generate_random_string(6)
            obfuscated_code = re.sub(r'self\.' + var_name + r'\b', 'self.' + new_name, obfuscated_code)
    
    # 3. 添加混淆字符串
    obfuscated_code = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
混淆后的FFXIV日志编辑器
作者: Nag0mi
版本: v1.0.0
"""

{obfuscated_code}
'''
    
    # 保存混淆后的代码
    with open("main_obfuscated.py", "w", encoding="utf-8") as f:
        f.write(obfuscated_code)
    
    print("代码混淆完成！")
    return True

def build_obfuscated_exe():
    """构建混淆的exe文件"""
    print("开始构建混淆exe文件...")
    
    # PyInstaller命令参数（增强混淆）
    cmd = [
        "pyinstaller",
        "--onefile",                    # 打包成单个exe文件
        "--windowed",                   # 不显示控制台窗口
        "--name=FFXIV日志编辑器_混淆版",  # 设置exe文件名
        "--icon=icon.ico",              # 图标文件（如果存在）
        "--add-data=checksum_calculator.py;.",  # 包含校验码计算模块
        
        "main_obfuscated.py"           # 混淆后的主程序文件
    ]
    
    # 如果图标文件不存在，移除图标参数
    if not os.path.exists("icon.ico"):
        cmd = [arg for arg in cmd if not arg.startswith("--icon")]
        print("未找到icon.ico文件，将使用默认图标")
    
    try:
        subprocess.check_call(cmd)
        print("混淆exe文件构建成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"构建混淆exe文件失败: {e}")
        return False

def cleanup_obfuscation():
    """清理混淆临时文件"""
    print("清理混淆临时文件...")
    
    files_to_remove = [
        "main_obfuscated.py"
    ]
    
    dirs_to_remove = [
        "build", 
        "__pycache__"
    ]
    
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"已删除文件: {file_name}")
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已删除目录: {dir_name}")
    
    # 删除spec文件
    spec_files = [
        "FFXIV日志编辑器_混淆版.spec",
        "FFXIV日志编辑器.spec"
    ]
    
    for spec_file in spec_files:
        if os.path.exists(spec_file):
            os.remove(spec_file)
            print(f"已删除文件: {spec_file}")

def main():
    """主函数"""
    print("=" * 60)
    print("FFXIV日志编辑器 - 简化混淆打包工具")
    print("作者: Nag0mi")
    print("版本: v1.0.0")
    print("=" * 60)
    
    # 检查当前目录
    if not os.path.exists("main.py"):
        print("错误: 未找到main.py文件，请确保在正确的目录中运行此脚本")
        return
    
    # 安装PyInstaller
    if not install_pyinstaller():
        return
    
    # 混淆代码
    if not obfuscate_code():
        return
    
    # 构建混淆exe文件
    if not build_obfuscated_exe():
        return
    
    # 检查输出文件
    exe_path = os.path.join("dist", "FFXIV日志编辑器_混淆版.exe")
    
    if os.path.exists(exe_path):
        print(f"\n✅ 混淆打包成功！")
        print(f"exe文件位置: {os.path.abspath(exe_path)}")
        print(f"文件大小: {os.path.getsize(exe_path) / 1024 / 1024:.2f} MB")
        print(f"混淆级别: 基础混淆")
        
        # 询问是否清理临时文件
        response = input("\n是否清理临时文件？(y/n): ").lower().strip()
        if response in ['y', 'yes', '是']:
            cleanup_obfuscation()
            print("清理完成！")
    else:
        print("❌ 混淆打包失败: 未找到生成的exe文件")

if __name__ == "__main__":
    main() 