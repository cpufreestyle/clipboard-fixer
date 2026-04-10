# 🔧 Windows 剪贴板修复工具

> 一键修复 Windows 复制粘贴失效问题

[![Gitee](https://img.shields.io/badge/Gitee-cpufreestyle%2Fclipboard--fixer-red?logo=gitee)](https://gitee.com/cpufreestyle/clipboard-fixer)
[![Release](https://img.shields.io/badge/Release-v1.0.0-green?logo=github)](https://gitee.com/cpufreestyle/clipboard-fixer/releases)
[![License](https://img.shields.io/badge/License-MIT-blue)]()

---

## 📥 下载安装

### 直接下载 EXE（推荐）

**[⬇️ 下载 剪贴板修复工具.exe (10.6MB)](https://gitee.com/cpufreestyle/clipboard-fixer/releases/download/v1.0.0/fixer.exe)**

1. 下载后双击运行
2. 点击「一键修复」按钮
3. 测试复制粘贴功能

> 无需安装 Python，独立运行

---

## 📱 功能特性

| 功能 | 说明 |
|------|------|
| 🔄 重启剪贴板服务 | 重启 `rdpclip.exe` 进程 |
| 🗑️ 清空剪贴板 | 清除剪贴板缓存数据 |
| 🔁 重启资源管理器 | 重启 `explorer.exe` 进程 |
| 📊 状态检测 | 检测服务运行状态 |
| ✨ 一键修复 | 自动执行所有修复步骤 |

---

## 🖥️ 界面预览

```
┌────────────────────────────────────┐
│     🔧 Windows 剪贴板修复工具       │
├────────────────────────────────────┤
│  📊 服务状态                       │
│    • rdpclip.exe    ✅ 运行中       │
│    • explorer.exe   ✅ 运行中       │
├────────────────────────────────────┤
│  🛠️ 修复操作                       │
│    [ 🔍 检测状态 ]                  │
│    [ 🔄 重启剪贴板服务 ]            │
│    [ 🗑️ 清空剪贴板 ]               │
│    [ 🔁 重启资源管理器 ]            │
│    [ ✨ 一键修复 ]    ← 推荐使用    │
├────────────────────────────────────┤
│  📝 操作日志                        │
│    [15:08:01] ✨ 一键修复开始       │
│    [15:08:02] ✅ 清空剪贴板         │
│    [15:08:05] ✅ 修复完成           │
└────────────────────────────────────┘
```

---

## 🚀 其他使用方式

### 方式一：批处理脚本（免安装）

下载 `剪贴板修复工具.bat`，双击运行，选择操作。

### 方式二：Python 源码运行

```powershell
# 克隆项目
git clone https://gitee.com/cpufreestyle/clipboard-fixer.git
cd clipboard-fixer

# 运行 GUI 版本
pip install requests
python clipboard_fixer_gui.py

# 或运行命令行版本
python clipboard_fixer.py --fix
```

---

## ❓ 常见问题

**Q: 为什么复制粘贴会失效？**  
A: 通常是因为剪贴板服务（rdpclip.exe）卡死或内存溢出，常见于远程桌面、复制大文件后。

**Q: 需要管理员权限吗？**  
A: 重启服务可能需要，程序会自动请求权限。

**Q: 会丢失剪贴板内容吗？**  
A: 是的，修复会清空当前剪贴板，请提前保存重要内容。

**Q: 支持哪些系统？**  
A: Windows 10/11 均可使用。

**Q: 杀毒软件报警？**  
A: 正常现象，添加信任即可。程序开源透明，可放心使用。

---

## 📁 项目结构

```
clipboard-fixer/
├── clipboard_fixer_gui.py    # GUI 版本主程序
├── clipboard_fixer.py        # 命令行版本
├── 剪贴板修复工具.bat         # 批处理脚本
├── README.md                # 本文件
└── dist/
    └── 剪贴板修复工具.exe     # 打包的可执行文件
```

---

## 🔗 相关链接

- **Gitee 仓库**: https://gitee.com/cpufreestyle/clipboard-fixer
- **下载地址**: https://gitee.com/cpufreestyle/clipboard-fixer/releases

---

<p align="center">
  <b>Windows 剪贴板修复工具</b><br>
  <i>Built with ❤️ for Windows Users</i>
</p>
