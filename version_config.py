#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本配置文件
在打包时可以修改此文件来更新版本号
"""

# 版本信息
VERSION = "v1.0.5"
AUTHOR = "Nag0mi"

# 版本描述
VERSION_DESCRIPTION = "支持时间偏移"

# 构建信息
BUILD_DATE = "2025-08-02"
BUILD_TYPE = "release"  # release, debug, beta

def get_version_info():
    """获取版本信息"""
    return {
        "version": VERSION,
        "author": AUTHOR,
        "description": VERSION_DESCRIPTION,
        "build_date": BUILD_DATE,
        "build_type": BUILD_TYPE
    }

def get_author_info():
    """获取作者信息字符串"""
    return f"作者:{AUTHOR} 版本:{VERSION}\n严禁倒卖，完全免费，仅供学习交流使用！\nbilibili@平安罗德岛"

if __name__ == "__main__":
    # 测试版本信息
    info = get_version_info()
    print("版本信息:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    print(f"\n作者信息:\n{get_author_info()}") 