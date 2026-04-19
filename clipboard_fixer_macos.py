#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macOS 剪贴板修复工具 - GUI 版本
一键修复复制粘贴失效问题
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import os
import sys

# ─── 主题配色 ───────────────────────────────────────────────
BG_COLOR      = "#0f0f0f"   # 深黑背景
SURFACE_COLOR = "#1a1a1a"   # 卡片/框架背景
ACCENT_COLOR  = "#ea580c"   # crab-assistant orange
TEXT_COLOR    = "#f5f5f5"   # 主文字（浅灰白）
MUTED_COLOR   = "#888888"   # 次要文字
SUCCESS_COLOR = "#22c55e"   # 绿色
WARN_COLOR    = "#f59e0b"   # 橙色
ERROR_COLOR   = "#ef4444"   # 红色

BUTTON_COLORS = [
    ("🔍 检测状态",           "#4CAF50"),
    ("🔄 重启剪贴板服务",      "#2196F3"),
    ("🗑️ 清空剪贴板",          "#FF9800"),
    ("🔁 重启 Finder",         "#9C27B0"),
    ("✨ 一键修复",            "#ea580c"),
]


class ClipboardFixerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔧 macOS 剪贴板修复工具")
        self.root.geometry("420x540")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.status_labels = {}
        self.setup_ui()
        self.check_status()

    # ── UI ──────────────────────────────────────────────────────

    def setup_ui(self):
        # ── 标题栏 ──
        title_frame = tk.Frame(self.root, bg=ACCENT_COLOR, height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        tk.Label(
            title_frame,
            text="michaelqiu",
            font=("Arial", 16, "bold"),
            fg="#FFD700",
            bg=ACCENT_COLOR,
        ).place(x=8, y=5)

        tk.Label(
            title_frame,
            text="剪贴板修复工具",
            font=("Arial", 18, "bold"),
            fg="white",
            bg=ACCENT_COLOR,
        ).place(x=0, y=35, relwidth=1)

        # ── 状态区 ──
        status_frame = tk.LabelFrame(
            self.root,
            text="📊 服务状态",
            font=("Arial", 10),
            bg=SURFACE_COLOR,
            fg=TEXT_COLOR,
            labelanchor="nw",
        )
        status_frame.pack(fill=tk.X, padx=20, pady=(15, 5))

        for service in ["pboard", "clipboardd", "Finder"]:
            frame = tk.Frame(status_frame, bg=SURFACE_COLOR)
            frame.pack(fill=tk.X, padx=10, pady=4)

            tk.Label(
                frame,
                text=f"• {service}:",
                font=("Arial", 9),
                fg=MUTED_COLOR,
                bg=SURFACE_COLOR,
            ).pack(side=tk.LEFT)

            self.status_labels[service] = tk.Label(
                frame,
                text="检测中...",
                font=("Arial", 9),
                fg=MUTED_COLOR,
                bg=SURFACE_COLOR,
            )
            self.status_labels[service].pack(side=tk.RIGHT)

        # ── 操作按钮区 ──
        button_frame = tk.LabelFrame(
            self.root,
            text="🛠️ 修复操作",
            font=("Arial", 10),
            bg=SURFACE_COLOR,
            fg=TEXT_COLOR,
            labelanchor="nw",
        )
        button_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        commands = [
            (self.check_status,       BUTTON_COLORS[0]),
            (self.restart_clipboard,   BUTTON_COLORS[1]),
            (self.clear_clipboard,     BUTTON_COLORS[2]),
            (self.restart_finder,      BUTTON_COLORS[3]),
            (self.fix_all,             BUTTON_COLORS[4]),
        ]

        for i, (cmd, (text, color)) in enumerate(commands):
            btn = tk.Button(
                button_frame,
                text=text,
                command=cmd,
                font=("Arial", 10),
                bg=color,
                fg="white",
                relief=tk.FLAT,
                cursor="hand2",
                height=2,
            )
            btn.pack(fill=tk.X, padx=10, pady=5)
            btn.bind("<Enter>", self._on_enter(btn, color))
            btn.bind("<Leave>", self._on_leave(btn, color))

        # ── 日志区 ──
        log_frame = tk.LabelFrame(
            self.root,
            text="📝 操作日志",
            font=("Arial", 10),
            bg=SURFACE_COLOR,
            fg=TEXT_COLOR,
            labelanchor="nw",
        )
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(5, 10))

        self.log_text = tk.Text(
            log_frame,
            height=6,
            font=("Menlo", 9),
            bg="#111111",
            fg="#d4d4d4",
            insertbackground="white",
            relief=tk.FLAT,
            highlightthickness=0,
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(self.log_text, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)

        # ── 版权 ──
        tk.Label(
            self.root,
            text="Built with ❤️  |  macOS Edition  |  v1.0.0",
            font=("Arial", 8),
            fg=MUTED_COLOR,
            bg=BG_COLOR,
        ).pack(pady=5)

    # ── 事件绑定辅助 ───────────────────────────────────────────

    @staticmethod
    def _on_enter(btn, color):
        def _handler(_):
            btn.config(bg=ClipboardFixerGUI._lighten_color(color))
        return _handler

    @staticmethod
    def _on_leave(btn, color):
        def _handler(_):
            btn.config(bg=color)
        return _handler

    @staticmethod
    def _lighten_color(color):
        lut = {
            "#4CAF50": "#66BB6A",
            "#2196F3": "#42A5F5",
            "#FF9800": "#FFA726",
            "#9C27B0": "#AB47BC",
            "#ea580c": "#f47216",
        }
        return lut.get(color, color)

    # ── 日志 ───────────────────────────────────────────────────

    def log(self, message):
        self.log_text.insert(tk.END, f"[{self._time()}] {message}\n")
        self.log_text.see(tk.END)

    @staticmethod
    def _time():
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")

    # ── 底层命令 ───────────────────────────────────────────────

    @staticmethod
    def _run(args, **kwargs):
        """执行 shell 命令，吞掉所有异常，返回 True/False。"""
        try:
            subprocess.run(args, **kwargs)
            return True
        except Exception as e:
            print(f"[_run error] {e}")
            return False

    # ── pbpaste / pbcopy 封装 ──────────────────────────────────

    @staticmethod
    def _get_clipboard_content():
        """返回剪贴板内容（字符串），失败返回空。"""
        try:
            r = subprocess.run(
                ["pbpaste"],
                capture_output=True,
            )
            return r.stdout.decode("utf-8", errors="replace")
        except Exception:
            return ""

    @staticmethod
    def _copy_to_clipboard(text: str):
        """写入字符串到剪贴板（通过 pbcopy）。"""
        try:
            subprocess.run(
                ["pbcopy"],
                input=text.encode("utf-8"),
                check=True,
            )
            return True
        except Exception:
            return False

    # ── 检测剪贴板是否为空 ─────────────────────────────────────

    def _clipboard_empty(self):
        return self._get_clipboard_content() == ""

    # ── 操作实现 ───────────────────────────────────────────────

    def check_status(self):
        """检测剪贴板服务状态。"""
        self.log("🔍 检测服务状态...")

        # pboard / clipboardd 进程
        try:
            r = subprocess.run(
                ["pgrep", "-l", "pboard|clipboardd"],
                capture_output=True,
                text=True,
            )
            output = r.stdout.strip()
            if output:
                for line in output.splitlines():
                    proc = line.split(maxsplit=1)[-1]
                    for key in ["pboard", "clipboardd"]:
                        if key in proc:
                            self.status_labels[key].config(
                                text="✅ 运行中", fg=SUCCESS_COLOR
                            )
            else:
                self.status_labels["pboard"].config(
                    text="❌ 未运行", fg=ERROR_COLOR
                )
                self.status_labels["clipboardd"].config(
                    text="❌ 未运行", fg=ERROR_COLOR
                )
        except Exception:
            self.status_labels["pboard"].config(text="❓ 未知", fg=MUTED_COLOR)
            self.status_labels["clipboardd"].config(
                text="❓ 未知", fg=MUTED_COLOR
            )

        # Finder
        try:
            r = subprocess.run(
                ["pgrep", "-x", "Finder"],
                capture_output=True,
            )
            running = r.returncode == 0
            self.status_labels["Finder"].config(
                text="✅ 运行中" if running else "❌ 未运行",
                fg=SUCCESS_COLOR if running else ERROR_COLOR,
            )
        except Exception:
            self.status_labels["Finder"].config(text="❓ 未知", fg=MUTED_COLOR)

        # 剪贴板内容
        content_len = len(self._get_clipboard_content())
        self.log(
            f"  • 剪贴板内容: {content_len} 字符"
            if content_len > 0
            else "  • 剪贴板内容: 空"
        )
        self.log("✅ 状态检测完成")

    def restart_clipboard(self):
        """重启剪贴板服务（launchctl bootout/launch）。"""
        self.log("🔄 重启剪贴板服务...")

        def task():
            import time

            # 杀掉现有 pasteboard 进程
            self.log("  • 终止 pasteboard 进程...")
            self._run(["pkill", "-9", "pboard"])
            self._run(["pkill", "-9", "clipboardd"])
            time.sleep(1)

            # launchctl 重载（尝试多种域）
            for domain in ["gui/$(id -u)", "user/$(id -u)", "system"]:
                # 注意：这里用 shell=True 展开 $(id -u)
                cmd = f'launchctl kickstart -k {domain}'
                subprocess.run(cmd, shell=True)
                self.log(f"  • launchctl kickstart → {domain}")

            time.sleep(1)

            # macOS 13+ clipboardd 由 system 管理，重新 bootstrap
            # 仅在系统域下尝试，无需 sudo（当前用户权限）
            self.log("  • 尝试 launchctl bootstrap...")
            self._run(
                [
                    "sh", "-c",
                    "launchctl bootout gui/$(id -u)/com.apple.pboard 2>/dev/null; "
                    "launchctl bootstrap gui/$(id -u) "
                    "/System/Library/LaunchAgents/com.apple.pboard.plist 2>/dev/null || true"
                ]
            )

            time.sleep(1)
            self.log("✅ 剪贴板服务已重启")

        threading.Thread(target=task, daemon=True).start()

    def clear_clipboard(self):
        """清空剪贴板。"""
        self.log("🗑️ 清空剪贴板...")
        ok = self._run(["pbcopy"], input=b"")
        if ok:
            self.log("✅ 剪贴板已清空")
        else:
            self.log("❌ 清空失败")

    def restart_finder(self):
        """重启 Finder。"""
        self.log("🔁 重启 Finder...")

        def task():
            self.log("  • 终止 Finder...")
            self._run(["pkill", "-9", "Finder"])
            import time
            time.sleep(2)
            self.log("  • 启动 Finder...")
            self._run(["open", "-a", "Finder"])
            self.log("✅ Finder 已重启")
            time.sleep(1)
            self.check_status()

        threading.Thread(target=task, daemon=True).start()

    def fix_all(self):
        """一键修复：清空剪贴板 + 重启 pasteboard + 重启 Finder。"""
        self.log("═════════ ✨ 一键修复开始 ═════════")

        def task():
            import time

            # 1. 清空剪贴板
            self.log("[1/5] 清空剪贴板...")
            self._run(["pbcopy"], input=b"")
            time.sleep(0.5)
            self.log("      ✅ 完成")

            # 2. 终止 pasteboard
            self.log("[2/5] 终止 pasteboard...")
            self._run(["pkill", "-9", "pboard"])
            self._run(["pkill", "-9", "clipboardd"])
            time.sleep(0.5)
            self.log("      ✅ 完成")

            # 3. 终止 Finder
            self.log("[3/5] 终止 Finder...")
            self._run(["pkill", "-9", "Finder"])
            time.sleep(1.5)
            self.log("      ✅ 完成")

            # 4. launchctl 重载
            self.log("[4/5] 重载剪贴板服务...")
            for domain in ["gui/$(id -u)", "user/$(id -u)"]:
                subprocess.run(
                    f"launchctl kickstart -k {domain}", shell=True
                )
            time.sleep(0.5)
            self.log("      ✅ 完成")

            # 5. 启动 Finder
            self.log("[5/5] 启动 Finder...")
            self._run(["open", "-a", "Finder"])
            time.sleep(1)
            self.log("      ✅ 完成")

            self.log("═════════ 🎉 修复完成！ ═════════")
            self.log("请测试复制粘贴功能")
            self.check_status()

        threading.Thread(target=task, daemon=True).start()


# ─── 入口 ─────────────────────────────────────────────────────

def main():
    root = tk.Tk()
    ClipboardFixerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
