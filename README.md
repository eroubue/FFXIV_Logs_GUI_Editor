# FFXIV 日志编辑器

一个用于编辑《最终幻想14》(FFXIV) 战斗日志的图形界面工具。

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-v1.0.3-orange.svg)](https://github.com/eroubue/FFXIV_Logs_GUI_Editor/releases)

## 功能特性

- **文件加载**: 支持加载FFXIV战斗日志文件（.log格式）
- **日志解析**: 自动解析21|开头的战斗日志行
- **数据筛选**: 按来源、技能、目标进行筛选
- **条目编辑**: 支持编辑时间戳、来源、技能、目标、标志、伤害等字段
- **批量操作**: 支持对选中条目应用伤害倍率
- **数据保存**: 保存修改后的日志文件，自动创建备份
- **校验码更新**: 自动更新修改后的校验码（基于FFXIV日志修改器算法）

## 系统要求

- Python 3.6+
- tkinter (通常随Python一起安装)

## 安装和运行

### 方法1: 直接运行
1. 确保已安装Python 3.6或更高版本
2. 克隆仓库：
   ```bash
   git clone https://github.com/eroubue/FFXIV_Logs_GUI_Editor.git
   cd FFXIV_Logs_GUI_Editor
   ```
3. 运行程序：
   ```bash
   python main.py
   ```

### 方法2: 下载可执行文件
从 [Releases](https://github.com/eroubue/FFXIV_Logs_GUI_Editor/releases) 页面下载最新版本的可执行文件。

## 使用说明

### 1. 加载日志文件
-点击"选择日志文件"按钮，选择FFXIV战斗日志文件（.log格式）
### 2. 筛选数据
- 使用顶部的筛选下拉框按来源、技能、目标进行筛选
- 点击"清除筛选"按钮显示所有条目

### 3. 编辑条目
- 在左侧列表中选择要编辑的条目
- 右侧编辑区域会显示该条目的详细信息
- 修改相应字段后点击"更新条目"按钮

### 4. 批量操作
- 选择要修改的条目
- 在"伤害倍率"字段输入倍率值
- 点击"应用倍率"按钮

### 5. 保存文件
- 点击"保存修改"按钮
- 程序会自动创建备份文件（.backup后缀）
- 修改后的内容会保存到原文件

## 日志格式说明

程序支持FFXIV标准的战斗日志格式：
```
21|时间戳|来源ID|来源名称|技能ID|技能名称|目标ID|目标名称|标志|伤害|校验码
```

## 注意事项
- 目标伤害统计显示为当前选中日志内所有战斗叠加，若仅需查看一场战斗，请分割日志。https://github.com/MnFeN/FFXIVLogSeparate/releases
- 程序会自动备份原始文件，备份文件名为原文件名+.backup
- 修改后的条目会自动更新校验码（使用SHA256算法）
- 建议在编辑前备份重要文件
- 程序仅支持21|开头的战斗日志行
- 校验码算法参考：[FFXIV日志修改器](https://github.com/innovationb1ue/FFXIV_logs_modifier)

## 错误处理

- 如果加载文件时出错，会显示错误对话框
- 如果保存文件时出错，会显示错误信息
- 程序会验证输入数据的有效性

## 开发信息

- **开发语言**: Python 3
- **GUI框架**: tkinter
- **编码**: UTF-8
- **支持平台**: Windows, macOS, Linux
- **作者**: [Nag0mi](https://space.bilibili.com/your-bilibili-id)
- **反馈**: 
  - Bilibili: @平安罗德岛
  - 爱发电: https://afdian.com/a/Nag0mi/plan

## 构建和发布

### 版本更新
```bash
# 更新版本号
python update_version.py v1.0.4

# 带版本更新的简化混淆打包
python build_with_version.py v1.0.4
```

### 构建可执行文件
```bash
# 简化混淆打包
python build_simple_obfuscated.py
```

详细说明请参考 [版本更新说明.md](版本更新说明.md)

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。