# 🔧 Windows 剪贴板修复工具

> 一键修复 Windows 复制粘贴失效问题

---

## 📱 功能特性

| 功能 | 说明 |
|------|------|
| 🔄 重启剪贴板服务 | 重启 `rdpclip.exe` 服务 |
| 🗑️ 清空剪贴板 | 清除剪贴板缓存数据 |
| 🔁 重启资源管理器 | 重启 `explorer.exe` 进程 |
| 📊 状态检测 | 检测剪贴板服务运行状态 |

---

## 🚀 使用方法

### 方式一：图形界面（推荐）

双击运行 `剪贴板修复工具.exe`

### 方式二：命令行

```powershell
# 查看状态
python clipboard_fixer.py --status

# 一键修复
python clipboard_fixer.py --fix

# 重启服务
python clipboard_fixer.py --restart
```

---

## 📦 下载

- **Gitee**: https://gitee.com/cpufreestyle/clipboard-fixer

---

## 🔧 常见问题

**Q: 为什么复制粘贴会失效？**  
A: 通常是因为剪贴板服务（rdpclip.exe）卡死或内存溢出。

**Q: 需要管理员权限吗？**  
A: 部分功能需要，程序会自动请求权限。

**Q: 会丢失剪贴板内容吗？**  
A: 是的，修复会清空当前剪贴板内容。

---

*Built with ❤️ for Windows Users*
