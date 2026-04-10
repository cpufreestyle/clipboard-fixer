#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows 剪贴板修复工具 - GUI 版本
一键修复复制粘贴失效问题
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import os
import sys

class ClipboardFixerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔧 Windows 剪贴板修复工具")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # 设置窗口图标（如果存在）
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        self.setup_ui()
        self.check_status()
    
    def setup_ui(self):
        # 标题
        title_frame = tk.Frame(self.root, bg="#2196F3", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🔧 剪贴板修复工具",
            font=("Microsoft YaHei", 20, "bold"),
            fg="white",
            bg="#2196F3"
        )
        title_label.pack(pady=20)
        
        # 状态显示区域
        status_frame = tk.LabelFrame(self.root, text="📊 服务状态", font=("Microsoft YaHei", 10))
        status_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.status_labels = {}
        for service in ["rdpclip.exe", "explorer.exe"]:
            frame = tk.Frame(status_frame)
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(frame, text=f"• {service}:", font=("Microsoft YaHei", 9)).pack(side=tk.LEFT)
            self.status_labels[service] = tk.Label(
                frame, 
                text="检测中...",
                font=("Microsoft YaHei", 9),
                fg="gray"
            )
            self.status_labels[service].pack(side=tk.RIGHT)
        
        # 操作按钮区域
        button_frame = tk.LabelFrame(self.root, text="🛠️ 修复操作", font=("Microsoft YaHei", 10))
        button_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        buttons = [
            ("🔍 检测状态", self.check_status, "#4CAF50"),
            ("🔄 重启剪贴板服务", self.restart_clipboard, "#2196F3"),
            ("🗑️ 清空剪贴板", self.clear_clipboard, "#FF9800"),
            ("🔁 重启资源管理器", self.restart_explorer, "#9C27B0"),
            ("✨ 一键修复", self.fix_all, "#F44336"),
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=("Microsoft YaHei", 10),
                bg=color,
                fg="white",
                relief=tk.FLAT,
                cursor="hand2",
                height=2
            )
            btn.pack(fill=tk.X, padx=10, pady=5)
            btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(bg=self._lighten_color(c)))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
        
        # 日志区域
        log_frame = tk.LabelFrame(self.root, text="📝 操作日志", font=("Microsoft YaHei", 10))
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.log_text = tk.Text(log_frame, height=6, font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(self.log_text, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        # 版权信息 + 水印
        footer_frame = tk.Frame(self.root)
        footer_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            footer_frame,
            text="Built with ❤️ | v1.0.0",
            font=("Microsoft YaHei", 8),
            fg="gray"
        ).pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            footer_frame,
            text="michaelqiu",
            font=("Microsoft YaHei", 10, "bold"),
            fg="#E91E63",
            cursor="hand2"
        ).pack(side=tk.RIGHT, padx=20)
    
    def _lighten_color(self, color):
        """颜色变亮"""
        colors = {
            "#4CAF50": "#66BB6A",
            "#2196F3": "#42A5F5",
            "#FF9800": "#FFA726",
            "#9C27B0": "#AB47BC",
            "#F44336": "#EF5350"
        }
        return colors.get(color, color)
    
    def log(self, message):
        """添加日志"""
        self.log_text.insert(tk.END, f"[{self._get_time()}] {message}\n")
        self.log_text.see(tk.END)
    
    def _get_time(self):
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def run_command(self, cmd, show_window=True):
        """执行命令"""
        try:
            if show_window:
                subprocess.run(cmd, shell=True, check=True)
            else:
                subprocess.run(
                    cmd, 
                    shell=True, 
                    check=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            return True
        except Exception as e:
            self.log(f"❌ 错误: {e}")
            return False
    
    def check_status(self):
        """检测服务状态"""
        self.log("🔍 检测服务状态...")
        
        for service in ["rdpclip.exe", "explorer.exe"]:
            try:
                result = subprocess.run(
                    f'tasklist /fi "imagename eq {service}"',
                    shell=True,
                    capture_output=True,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                if service.lower() in result.stdout.lower():
                    self.status_labels[service].config(text="✅ 运行中", fg="green")
                else:
                    self.status_labels[service].config(text="❌ 未运行", fg="red")
            except:
                self.status_labels[service].config(text="❓ 未知", fg="gray")
        
        self.log("✅ 状态检测完成")
    
    def restart_clipboard(self):
        """重启剪贴板服务"""
        self.log("🔄 重启剪贴板服务...")
        
        def task():
            # 终止 rdpclip.exe
            subprocess.run(
                "taskkill /f /im rdpclip.exe",
                shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            self.log("  • 已终止 rdpclip.exe")
            
            # 等待
            import time
            time.sleep(1)
            
            # 重新启动
            subprocess.run(
                'start "" "C:\\Windows\\System32\\rdpclip.exe"',
                shell=True
            )
            self.log("  • 已启动 rdpclip.exe")
            self.log("✅ 剪贴板服务重启完成")
        
        threading.Thread(target=task, daemon=True).start()
    
    def clear_clipboard(self):
        """清空剪贴板"""
        self.log("🗑️ 清空剪贴板...")
        
        try:
            # 方法1: 使用 clip 命令
            subprocess.run(
                "echo off | clip",
                shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # 方法2: 使用 PowerShell
            subprocess.run(
                "powershell -command \"[System.Windows.Forms.Clipboard]::Clear()\"",
                shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            self.log("✅ 剪贴板已清空")
        except Exception as e:
            self.log(f"❌ 清空失败: {e}")
    
    def restart_explorer(self):
        """重启资源管理器"""
        self.log("🔁 重启资源管理器...")
        
        def task():
            # 终止 explorer.exe
            subprocess.run(
                "taskkill /f /im explorer.exe",
                shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            self.log("  • 已终止 explorer.exe")
            
            # 等待
            import time
            time.sleep(2)
            
            # 重新启动
            subprocess.run(
                'start "" "C:\\Windows\\explorer.exe"',
                shell=True
            )
            self.log("  • 已启动 explorer.exe")
            self.log("✅ 资源管理器重启完成")
        
        threading.Thread(target=task, daemon=True).start()
    
    def fix_all(self):
        """一键修复"""
        self.log("═════════ ✨ 一键修复开始 ═════════")
        
        def task():
            import time
            
            # 1. 清空剪贴板
            self.log("[1/5] 清空剪贴板...")
            subprocess.run("echo off | clip", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            time.sleep(0.5)
            self.log("      ✅ 完成")
            
            # 2. 终止 rdpclip.exe
            self.log("[2/5] 终止剪贴板服务...")
            subprocess.run("taskkill /f /im rdpclip.exe", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            time.sleep(0.5)
            self.log("      ✅ 完成")
            
            # 3. 终止 explorer.exe
            self.log("[3/5] 终止资源管理器...")
            subprocess.run("taskkill /f /im explorer.exe", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            time.sleep(2)
            self.log("      ✅ 完成")
            
            # 4. 启动 rdpclip.exe
            self.log("[4/5] 启动剪贴板服务...")
            subprocess.run('start "" "C:\\Windows\\System32\\rdpclip.exe"', shell=True)
            time.sleep(1)
            self.log("      ✅ 完成")
            
            # 5. 启动 explorer.exe
            self.log("[5/5] 启动资源管理器...")
            subprocess.run('start "" "C:\\Windows\\explorer.exe"', shell=True)
            time.sleep(1)
            self.log("      ✅ 完成")
            
            self.log("═════════ 🎉 修复完成！ ═════════")
            self.log("请测试复制粘贴功能")
            
            # 刷新状态
            self.check_status()
        
        threading.Thread(target=task, daemon=True).start()


def main():
    root = tk.Tk()
    app = ClipboardFixerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
