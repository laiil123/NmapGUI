## 🕵️‍♂️ GUI Nmap 类网络扫描器

一个基于 Python 和 PyQt5 的图形化网络扫描工具，具备 IP 段扫描、端口扫描、操作系统识别、服务识别、进度条、动画提示、多线程加速、导出结果等完整功能。

![image](https://github.com/user-attachments/assets/e758efa4-0597-4b50-81eb-003122329ac7)



---

### ✨ 功能特色

| 功能 | 描述 |
|------|------|
| 🔍 主机存活扫描 | 检测 IP 是否在线（Ping） |
| 🌐 端口扫描 | 扫描指定端口范围，支持自定义 1~65535 |
| ⚙️ 服务识别 | 根据端口映射常见服务（如 HTTP, SSH, MySQL） |
| 🖥️ 操作系统识别 | 基于 TTL 值猜测 OS 类型 |
| 🧵 多线程扫描 | 可调线程数，加速扫描过程 |
| 📊 扫描进度条 | 动态显示扫描进度 |
| 🔄 加载动画 | 扫描中展示旋转 loading 动画 |
| 🧾 导出结果 | 一键导出扫描结果为 TXT 文件 |
| 🎨 美观界面 | PyQt5 界面美观，支持 logo、自定义颜色 |

---

### 📦 环境依赖

- Python 3.7+
- PyQt5
- `ping3`（用于 ping 检测）

安装依赖：

```bash
pip install pyqt5 ping3
```

---

### 🚀 使用方法

1. 克隆项目：

```bash
git clone https://github.com/laiil123/NmapGUI.git
cd NmapGUI
```

2. 运行主程序：

```bash
cd nmap_scanner
python main.py
```

3. 设置 IP 段、端口范围、线程数后点击“开始扫描”。

---

### 📁 项目结构

```
NmapGUI/nmap_scanner/
├── main.py              # GUI 主界面
├── scanner.py           # 核心扫描逻辑
├── resources
  ├── logo.png            # 程序 Logo（可选）
  ├── loading.gif         # 动画加载图
├── README.md
```

---



### 🧠 TODO & 可拓展功能

- [ ] Banner 抓取识别服务版本
- [ ] 导出为 HTML/PDF 报告
- [ ] 支持多 IP 同时 Ping
- [ ] 扫描结果可视化图表

---

### 🛡️ 免责声明

本工具仅用于学习与授权测试环境，**请勿用于非法用途**。作者不对任何非法使用造成的后果负责。

---

### 📮 作者

**南邮信安Czech** – 信息安全本科 / 安全开发方向  
GitHub: [@laiil123](https://github.com/laiil123)
