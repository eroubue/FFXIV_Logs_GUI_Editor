#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FFXIV日志编辑器 - 带版本更新的简化混淆打包脚本
用法: python build_with_version.py <版本号>
示例: python build_with_version.py v1.0.2
"""

import os
import sys
import subprocess
from update_version import update_version_config, update_main_version, get_current_version

def build_with_version(new_version):
    """带版本更新的简化混淆打包"""
    print("=" * 60)
    print("FFXIV日志编辑器 - 带版本更新的简化混淆打包工具")
    print(f"当前版本: {get_current_version()}")
    print(f"目标版本: {new_version}")
    print("=" * 60)
    
    # 1. 更新版本号
    print("\n步骤 1: 更新版本号...")
    if not update_version_config(new_version, "release"):
        print("✗ 版本更新失败")
        return False
    
    if not update_main_version(new_version):
        print("✗ main.py版本更新失败")
        return False
    
    print(f"✓ 版本已更新为: {new_version}")
    
    # 2. 运行简化混淆打包
    print("\n步骤 2: 开始简化混淆打包...")
    try:
        # 调用简化混淆打包脚本
        cmd = [sys.executable, "build_simple_obfuscated.py"]
        subprocess.check_call(cmd)
        print("✓ 简化混淆打包完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 简化混淆打包失败: {e}")
        return False

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python build_with_version.py <新版本号>")
        print("示例: python build_with_version.py v1.0.2")
        print(f"\n当前版本: {get_current_version()}")
        return
    
    new_version = sys.argv[1]
    
    # 验证版本号格式
    import re
    if not re.match(r'^v\d+\.\d+\.\d+', new_version):
        print("✗ 版本号格式错误，应为 v主版本.次版本.修订版本")
        print("示例: v1.0.2")
        return
    
    # 执行带版本更新的简化混淆打包
    if build_with_version(new_version):
        print("\n✅ 带版本更新的简化混淆打包成功完成!")
        print(f"新版本: {new_version}")
    else:
        print("\n❌ 带版本更新的简化混淆打包失败!")

if __name__ == "__main__":
    main() 