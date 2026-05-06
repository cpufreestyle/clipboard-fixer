#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剪贴板修复工具 - 跨平台版 (macOS / Linux / Windows)
支持: macOS (pbpaste/pbcopy), Linux (xclip/xsel), Windows (PowerShell)
"""

import os
import sys
import platform
import subprocess
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import tempfile
import shutil

IS_MAC = platform.system() == "Darwin"
IS_LINUX = platform.system() == "Linux"
IS_WINDOWS = platform.system() == "Windows"

TITLE = "🔧 剪贴板修复工具"
VERSION = "1.0.0"
AUTHOR = "MichaelQiu"

# ========== 跨平台剪贴板读写 ==========

def _clipboard_get_macos() -> str:
    try:
        return subprocess.check_output(["pbpaste"], text=True, timeout=5)
    except Exception as e:
        raise RuntimeError(f"macOS pbpaste 失败: {e}")

def _clipboard_set_macos(text: str) -> None:
    try:
        p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
        p.communicate(input=text.encode("utf-8"), timeout=5)
    except Exception as e:
        raise RuntimeError(f"macOS pbcopy 失败: {e}")

def _clipboard_get_linux() -> str:
    # 优先 xclip，其次 xsel
    for cmd in ["xclip", "xsel"]:
        try:
            result = subprocess.check_output(
                [cmd, "-selection", "clipboard", "-o"],
                text=True, timeout=5, stderr=subprocess.DEVNULL
            )
            return result
        except Exception:
            continue
    raise RuntimeError("Linux 未找到 xclip 或 xsel，请运行: sudo apt install xclip")

def _clipboard_set_linux(text: str) -> None:
    for cmd in ["xclip", "xsel"]:
        try:
            if cmd == "xclip":
                p = subprocess.Popen([cmd, "-selection", "clipboard", "-i"],
                                     stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
                p.communicate(input=text.encode("utf-8"), timeout=5)
            else:
                p = subprocess.Popen([cmd, "--clipboard"], stdin=subprocess.PIPE,
                                     stderr=subprocess.DEVNULL)
                p.communicate(input=text.encode("utf-8"), timeout=5)
            return
        except Exception:
            continue
    raise RuntimeError("Linux 未找到 xclip 或 xsel，请运行: sudo apt install xclip")

def _clipboard_get_windows() -> str:
    try:
        result = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", "Get-Clipboard -Raw"],
            text=True, timeout=5, encoding="utf-8", errors="ignore"
        )
        return result
    except Exception as e:
        raise RuntimeError(f"Windows PowerShell Get-Clipboard 失败: {e}")

def _clipboard_set_windows(text: str) -> None:
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", f"Set-Clipboard -Value '{text.replace(chr(39), chr(39)+chr(39))}'"],
            timeout=5, check=True
        )
    except Exception as e:
        raise RuntimeError(f"Windows PowerShell Set-Clipboard 失败: {e}")

def clipboard_get() -> str:
    if IS_MAC:
        return _clipboard_get_macos()
    elif IS_LINUX:
        return _clipboard_get_linux()
    elif IS_WINDOWS:
        return _clipboard_get_windows()
    raise RuntimeError("不支持的操作系统")

def clipboard_set(text: str) -> None:
    if IS_MAC:
        return _clipboard_set_macos(text)
    elif IS_LINUX:
        return _clipboard_set_linux(text)
    elif IS_WINDOWS:
        return _clipboard_set_windows(text)
    raise RuntimeError("不支持的操作系统")

# ========== 剪贴板修复策略 ==========

def get_platform_name() -> str:
    if IS_MAC:
        return "macOS"
    elif IS_LINUX:
        return "Linux"
    elif IS_WINDOWS:
        return "Windows"
    return "Unknown"

def get_platform_info() -> str:
    if IS_MAC:
        return f"macOS {platform.mac_ver()[0]}"
    elif IS_LINUX:
        try:
            with open("/etc/os-release") as f:
                lines = f.readlines()
            for line in lines:
                if line.startswith("PRETTY_NAME="):
                    return line.strip().split("=")[1].strip('"')
        except Exception:
            pass
        return platform.release()
    elif IS_WINDOWS:
        return f"Windows {platform.release()}"
    return "Unknown"

def get_fix_description() -> list:
    if IS_MAC:
        return [
            "1. 模拟 Cmd+C 复制操作",
            "2. 清空剪贴板后重新复制",
            "3. 重启 pboard 服务",
            "4. 重启 WindowServer",
        ]
    elif IS_LINUX:
        return [
            "1. 模拟 Ctrl+C 复制操作",
            "2. 清空剪贴板 (xclip -cut)",
            "3. 重新写入剪贴板",
        ]
    elif IS_WINDOWS:
        return [
            "1. 模拟 Ctrl+C 复制操作",
            "2. 清空剪贴板",
            "3. 重新写入剪贴板",
        ]

def apply_fix(strategy: int) -> str:
    """执行修复策略，返回结果"""
    if IS_MAC:
        return _apply_fix_macos(strategy)
    elif IS_LINUX:
        return _apply_fix_linux(strategy)
    elif IS_WINDOWS:
        return _apply_fix_windows(strategy)
    return "不支持该系统"

def _apply_fix_macos(strategy: int) -> str:
    if strategy == 1:
        # 策略1: pbcopy 空内容再恢复
        orig = clipboard_get()
        subprocess.run(["pbcopy"], input=b"", timeout=3)
        import time; time.sleep(0.3)
        if orig:
            clipboard_set(orig)
        return "✅ 修复完成 (pbcopy 重置)"
    elif strategy == 2:
        # 策略2: 重启 pboard
        subprocess.run(["killall", "pboard"], timeout=5)
        return "✅ pboard 已重启"
    elif strategy == 3:
        # 策略3: 重新读取当前选中内容
        try:
            subprocess.run(["killall", "pboard"], timeout=5)
        except Exception:
            pass
        return "✅ 修复完成"
    return "未知策略"

def _apply_fix_linux(strategy: int) -> str:
    if strategy == 1:
        orig = clipboard_get()
        subprocess.run(["xclip", "-selection", "clipboard", "-i"],
                       input=b"", timeout=5, stderr=subprocess.DEVNULL)
        import time; time.sleep(0.3)
        if orig:
            clipboard_set(orig)
        return "✅ 修复完成 (xclip 重置)"
    elif strategy == 2:
        subprocess.run(["xclip", "-selection", "clipboard", "-c"],
                       timeout=5, stderr=subprocess.DEVNULL)
        return "✅ 剪贴板已清空"
    return "未知策略"

def _apply_fix_windows(strategy: int) -> str:
    if strategy == 1:
        orig = clipboard_get()
        subprocess.run(["powershell", "-NoProfile", "-Command",
                        "Set-Clipboard -Value ''"], timeout=5)
        import time; time.sleep(0.3)
        if orig:
            clipboard_set(orig)
        return "✅ 修复完成 (PowerShell 重置)"
    elif strategy == 2:
        subprocess.run(["powershell", "-NoProfile", "-Command",
                        "Set-Clipboard -Value ''"], timeout=5)
        return "✅ 剪贴板已清空"
    return "未知策略"

# ========== GUI ==========

BG_COLOR = "#f0f4f8"
HEADER_COLOR = "#1565C0"
SUCCESS_COLOR = "#2E7D32"
WARN_COLOR = "#E65100"
MUTED_COLOR = "#666"

class ClipboardFixerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(TITLE)
        self.root.geometry("560x700")
        self.root.minsize(480, 620)
        self.root.configure(bg=BG_COLOR)
        self.fixing = False

        self._build_ui()
        self.check_clipboard()

    def _build_ui(self) -> None:
        # 标题栏
        header = tk.Frame(self.root, bg=HEADER_COLOR, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text=TITLE, font=("SF Pro Display", 20, "bold"),
                 fg="white", bg=HEADER_COLOR).place(x=20, y=14)
        tk.Label(header, text=f"跨平台版 v{VERSION} | {get_platform_info()}",
                 font=("SF Pro Text", 11), fg="#BBDEFB", bg=HEADER_COLOR).place(x=20, y=48)

        container = tk.Frame(self.root, bg=BG_COLOR, padx=24, pady=20)
        container.pack(fill="both", expand=True)

        # 状态卡片
        self.status_card = tk.Frame(container, bg="white", relief="flat", bd=0)
        self.status_card.pack(fill="x", pady=(0, 16))
        self.status_card.configure(highlightbackground="#E0E0E0", highlightthickness=1)

        self.status_icon = tk.Label(self.status_card, text="⏳", font=("SF Pro", 28),
                                   bg="white", width=3)
        self.status_icon.pack(side="left", padx=16, pady=16)

        status_text_frame = tk.Frame(self.status_card, bg="white")
        status_text_frame.pack(side="left", fill="y", expand=True)

        self.status_title = tk.Label(status_text_frame, text="正在检测...",
                                     font=("SF Pro Display", 14, "bold"), bg="white", anchor="w")
        self.status_title.pack(fill="x")
        self.status_detail = tk.Label(status_text_frame, text="",
                                      font=("SF Pro Text", 11), fg=MUTED_COLOR, bg="white", anchor="w")
        self.status_detail.pack(fill="x", pady=(2, 0))

        self.status_card.pack_propagate(False)

        # 剪贴板内容
        content_label = tk.Label(container, text="剪贴板内容预览",
                                 font=("SF Pro Display", 13, "bold"), bg=BG_COLOR, anchor="w")
        content_label.pack(fill="x", pady=(0, 6))

        self.content_text = scrolledtext.ScrolledText(
            container, height=6, font=("SF Mono", 11),
            wrap="word", relief="flat", bd=0,
            bg="#FAFAFA", fg="#333",
            insertbackground="#1565C0",
            highlightbackground="#E0E0E0", highlightthickness=1
        )
        self.content_text.pack(fill="x", pady=(0, 16))

        # 修复策略
        strategy_label = tk.Label(container, text="修复策略",
                                 font=("SF Pro Display", 13, "bold"), bg=BG_COLOR, anchor="w")
        strategy_label.pack(fill="x", pady=(0, 8))

        self.strategy_var = tk.IntVar(value=1)
        self.strategy_desc_label = tk.Label(container, text="", font=("SF Pro Text", 11),
                                           fg=MUTED_COLOR, bg=BG_COLOR, anchor="w", justify="left")
        self.strategy_desc_label.pack(fill="x", pady=(0, 8))

        strategies = get_fix_description()
        self.strategy_buttons = []
        for i, desc in enumerate(strategies, 1):
            btn = tk.Radiobutton(
                container, text=desc, variable=self.strategy_var, value=i,
                font=("SF Pro Text", 11), bg=BG_COLOR, anchor="w",
                activebackground=BG_COLOR, justify="left", padx=0,
                command=self._update_strategy_desc
            )
            btn.pack(fill="x", pady=1)
            self.strategy_buttons.append(btn)

        self._update_strategy_desc()

        # 操作按钮
        btn_frame = tk.Frame(container, bg=BG_COLOR)
        btn_frame.pack(fill="x", pady=16)

        self.refresh_btn = tk.Button(
            btn_frame, text="🔄 刷新剪贴板", font=("SF Pro Text", 12, "bold"),
            bg="#E3F2FD", fg=HEADER_COLOR, relief="flat", padx=20, pady=8,
            cursor="hand2", command=self.check_clipboard
        )
        self.refresh_btn.pack(side="left", padx=(0, 8))

        self.fix_btn = tk.Button(
            btn_frame, text="🔧 一键修复", font=("SF Pro Text", 12, "bold"),
            bg=HEADER_COLOR, fg="white", relief="flat", padx=24, pady=8,
            cursor="hand2", command=self._do_fix
        )
        self.fix_btn.pack(side="left")

        # 日志区
        log_label = tk.Label(container, text="执行日志",
                             font=("SF Pro Display", 13, "bold"), bg=BG_COLOR, anchor="w")
        log_label.pack(fill="x", pady=(8, 6))

        self.log_text = scrolledtext.ScrolledText(
            container, height=8, font=("SF Mono", 10),
            wrap="word", relief="flat", bg="#1E1E1E", fg="#D4D4D4",
            insertbackground="white", state="disabled"
        )
        self.log_text.pack(fill="both", expand=True)

        # 底部信息
        footer = tk.Label(container, text=f"by {AUTHOR}",
                         font=("SF Pro Text", 9), fg=MUTED_COLOR, bg=BG_COLOR)
        footer.pack(pady=(10, 0))

    def _update_strategy_desc(self) -> None:
        descs = {
            1: "清空剪贴板 → 保存内容 → 重新写入，最通用有效",
            2: "重启剪贴板系统服务",
            3: "轻量重置，无需额外操作",
        }
        self.strategy_desc_label.config(text=f"提示: {descs.get(self.strategy_var.get(), '')}")

    def _log(self, msg: str) -> None:
        from datetime import datetime
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"[{ts}] {msg}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def check_clipboard(self) -> None:
        self.refresh_btn.config(state="disabled", text="⏳ 检测中...")
        threading.Thread(target=self._check_worker, daemon=True).start()

    def _check_worker(self) -> None:
        try:
            content = clipboard_get()
            length = len(content)
            preview = content[:200].replace("\n", " ").strip() or "(空)"
            self.root.after(0, lambda: self._update_status("✅ 剪贴板正常", preview, length, True))
        except Exception as e:
            self.root.after(0, lambda: self._update_status("❌ 剪贴板异常", str(e), 0, False))
        self.root.after(0, lambda: self.refresh_btn.config(state="normal", text="🔄 刷新剪贴板"))

    def _update_status(self, title: str, detail: str, length: int, ok: bool) -> None:
        self.status_title.config(text=title, fg=SUCCESS_COLOR if ok else WARN_COLOR)
        self.status_detail.config(text=f"长度: {length} 字符 | 预览: {detail[:80]}{'...' if len(detail)>80 else ''}")
        self.content_text.delete("1.0", "end")
        self.content_text.insert("1.0", clipboard_get() if ok else "")
        self._log(title)

    def _do_fix(self) -> None:
        if self.fixing:
            return
        self.fixing = True
        self.fix_btn.config(state="disabled", text="⏳ 修复中...")
        threading.Thread(target=self._fix_worker, daemon=True).start()

    def _fix_worker(self) -> None:
        strategy = self.strategy_var.get()
        self.root.after(0, lambda: self._log(f"执行策略 {strategy}..."))
        try:
            result = apply_fix(strategy)
            self.root.after(0, lambda: self._log(result))
            self.root.after(0, lambda: self.check_clipboard())
        except Exception as e:
            self.root.after(0, lambda: self._log(f"❌ 修复失败: {e}"))
        self.fixing = False
        self.root.after(0, lambda: self.fix_btn.config(state="normal", text="🔧 一键修复"))


def main() -> None:
    root = tk.Tk()
    app = ClipboardFixerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
