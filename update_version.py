#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本更新脚本
用于在打包时自动更新版本号
"""

import re
import sys
from datetime import datetime

def update_version_config(new_version, build_type="release"):
    """更新版本配置文件"""
    try:
        # 读取当前版本配置
        with open('version_config.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新版本号
        content = re.sub(r'VERSION = "[^"]*"', f'VERSION = "{new_version}"', content)
        
        # 更新构建类型
        content = re.sub(r'BUILD_TYPE = "[^"]*"', f'BUILD_TYPE = "{build_type}"', content)
        
        # 更新构建日期
        current_date = datetime.now().strftime("%Y-%m-%d")
        content = re.sub(r'BUILD_DATE = "[^"]*"', f'BUILD_DATE = "{current_date}"', content)
        
        # 写回文件
        with open('version_config.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ 版本已更新为: {new_version}")
        print(f"✓ 构建类型: {build_type}")
        print(f"✓ 构建日期: {current_date}")
        return True
        
    except Exception as e:
        print(f"✗ 更新版本失败: {e}")
        return False

def update_main_version(new_version):
    """更新main.py中的版本信息（备用）"""
    try:
        with open('main.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新备用版本信息
        content = re.sub(
            r'return "作者:Nag0mi 版本:[^"]*"',
            f'return "作者:Nag0mi 版本:{new_version}"',
            content
        )
        
        with open('main.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ main.py 备用版本信息已更新")
        return True
        
    except Exception as e:
        print(f"✗ 更新main.py版本信息失败: {e}")
        return False

def get_current_version():
    """获取当前版本号"""
    try:
        from version_config import VERSION
        return VERSION
    except ImportError:
        return "v1.0.1"

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python update_version.py <新版本号> [构建类型]")
        print("示例: python update_version.py v1.0.2")
        print("示例: python update_version.py v1.0.2 beta")
        print(f"\n当前版本: {get_current_version()}")
        return
    
    new_version = sys.argv[1]
    build_type = sys.argv[2] if len(sys.argv) > 2 else "release"
    
    # 验证版本号格式
    if not re.match(r'^v\d+\.\d+\.\d+', new_version):
        print("✗ 版本号格式错误，应为 v主版本.次版本.修订版本")
        print("示例: v1.0.2")
        return
    
    print(f"正在更新版本: {get_current_version()} -> {new_version}")
    print(f"构建类型: {build_type}")
    print("-" * 50)
    
    # 更新版本配置
    if update_version_config(new_version, build_type):
        # 同时更新main.py中的备用版本信息
        update_main_version(new_version)
        print("\n✓ 版本更新完成!")
    else:
        print("\n✗ 版本更新失败!")

if __name__ == "__main__":
    main() 