#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动更新模块
用于检查GitHub仓库的版本并打开发布页面
"""

import os
import sys
import json
import requests
import webbrowser
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
from typing import Optional, Dict

# GitHub仓库信息
GITHUB_REPO = "eroubue/FFXIV_Logs_GUI_Editor"  # 根据搜索结果更新为正确的仓库地址
GITHUB_API_BASE = "https://api.github.com"
RELEASES_URL = f"{GITHUB_API_BASE}/repos/{GITHUB_REPO}/releases/latest"
GITHUB_RELEASES_PAGE = f"https://github.com/{GITHUB_REPO}/releases"

class AutoUpdater:
    """自动更新器"""
    
    def __init__(self, current_version: str):
        self.current_version = current_version
        self.update_window = None
        
    def check_for_updates(self) -> Optional[Dict]:
        """
        检查是否有可用更新
        
        Returns:
            Dict: 更新信息，包含version, body等
            None: 无可用更新或检查失败
        """
        try:
            print("正在检查更新...")
            response = requests.get(RELEASES_URL, timeout=10)
            response.raise_for_status()
            
            release_data = response.json()
            
            # 优先使用name字段作为版本号，如果没有则使用tag_name
            latest_version = release_data.get('name', release_data.get('tag_name', ''))
            
            # 如果name字段为空或不是版本号格式，尝试从tag_name中提取
            if not latest_version or not latest_version.startswith(('v', 'V')):
                tag_name = release_data.get('tag_name', '')
                # 尝试从tag_name中提取版本号
                if tag_name and tag_name != 'Release':
                    latest_version = tag_name
                else:
                    # 如果都没有有效的版本号，使用当前版本
                    latest_version = self.current_version
            
            print(f"当前版本: {self.current_version}")
            print(f"最新版本: {latest_version}")
            
            # 比较版本号
            if self._compare_versions(latest_version, self.current_version) > 0:
                return {
                    'version': latest_version,
                    'body': release_data['body'],
                    'published_at': release_data['published_at']
                }
            else:
                print("当前已是最新版本")
                return None
                
        except requests.RequestException as e:
            print(f"检查更新失败: {e}")
            return None
        except Exception as e:
            print(f"检查更新时出错: {e}")
            return None
    
    def _compare_versions(self, version1: str, version2: str) -> int:
        """
        比较版本号
        
        Returns:
            int: 1 if version1 > version2, -1 if version1 < version2, 0 if equal
        """
        try:
            # 标准化版本号格式
            v1 = version1.upper().lstrip('V')
            v2 = version2.upper().lstrip('V')
            
            # 分割版本号
            parts1 = [int(x) for x in v1.split('.')]
            parts2 = [int(x) for x in v2.split('.')]
            
            # 补齐长度
            max_len = max(len(parts1), len(parts2))
            parts1.extend([0] * (max_len - len(parts1)))
            parts2.extend([0] * (max_len - len(parts2)))
            
            # 比较
            for p1, p2 in zip(parts1, parts2):
                if p1 > p2:
                    return 1
                elif p1 < p2:
                    return -1
            
            return 0
        except (ValueError, AttributeError):
            # 如果版本号格式无效，返回0（认为相等）
            print(f"警告: 无效的版本号格式 - {version1} vs {version2}")
            return 0
    
    def show_update_dialog(self, update_info: Dict) -> bool:
        """
        显示更新对话框
        
        Args:
            update_info: 更新信息
            
        Returns:
            bool: 用户是否同意打开下载页面
        """
        # 创建更新对话框
        self.update_window = tk.Toplevel()
        self.update_window.title("发现新版本")
        self.update_window.geometry("500x400")
        self.update_window.resizable(False, False)
        
        # 居中显示
        self.update_window.transient()
        self.update_window.grab_set()
        
        # 主框架
        main_frame = ttk.Frame(self.update_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="发现新版本", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 版本信息
        version_frame = ttk.Frame(main_frame)
        version_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(version_frame, text=f"当前版本: {self.current_version}").pack(anchor=tk.W)
        ttk.Label(version_frame, text=f"最新版本: {update_info['version']}").pack(anchor=tk.W)
        ttk.Label(version_frame, text=f"发布时间: {update_info['published_at']}").pack(anchor=tk.W)
        
        # 更新说明
        ttk.Label(main_frame, text="更新说明:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        # 创建文本框显示更新说明
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, height=10)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 插入更新说明
        text_widget.insert(tk.END, update_info.get('body', '无更新说明'))
        text_widget.config(state=tk.DISABLED)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # 用户选择结果
        result = {'choice': None}
        
        def on_open_download():
            result['choice'] = True
            self.update_window.destroy()
        
        def on_skip():
            result['choice'] = False
            self.update_window.destroy()
        
        ttk.Button(button_frame, text="打开下载页面", command=on_open_download).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="稍后提醒", command=on_skip).pack(side=tk.LEFT)
        
        # 等待用户选择
        self.update_window.wait_window()
        
        return result['choice']
    
    def open_download_page(self) -> None:
        """打开GitHub下载页面"""
        try:
            print(f"正在打开下载页面: {GITHUB_RELEASES_PAGE}")
            webbrowser.open(GITHUB_RELEASES_PAGE)
            messagebox.showinfo("提示", "已打开GitHub发布页面，请手动下载最新版本。")
        except Exception as e:
            print(f"打开下载页面失败: {e}")
            messagebox.showerror("错误", f"无法打开下载页面: {e}")
    
    def check_and_update(self) -> None:
        """
        检查并执行更新（在后台线程中运行）
        """
        def update_thread():
            try:
                # 检查更新
                update_info = self.check_for_updates()
                if not update_info:
                    return
                
                # 在主线程中显示更新对话框
                def show_dialog():
                    if self.show_update_dialog(update_info):
                        # 用户同意打开下载页面
                        self.open_download_page()
                
                # 确保在主线程中执行GUI操作
                if threading.current_thread() is not threading.main_thread():
                    # 使用after方法在主线程中执行
                    root = tk._default_root
                    if root:
                        root.after(0, show_dialog)
                
            except Exception as e:
                print(f"更新检查失败: {e}")
        
        # 启动后台线程
        thread = threading.Thread(target=update_thread, daemon=True)
        thread.start()

def check_for_updates_on_startup(current_version: str) -> None:
    """
    在程序启动时检查更新
    
    Args:
        current_version: 当前版本号
    """
    updater = AutoUpdater(current_version)
    updater.check_and_update()

if __name__ == "__main__":
    # 测试更新检查
    updater = AutoUpdater("v1.0.3")
    update_info = updater.check_for_updates()
    if update_info:
        print(f"发现新版本: {update_info['version']}")
        print(f"更新说明: {update_info['body']}")
    else:
        print("当前已是最新版本") 