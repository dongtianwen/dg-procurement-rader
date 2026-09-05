# 东莞采购雷达

自动抓取东莞市政府采购公告，使用 AI 筛选适合 AI 应用开发公司承接的项目。

## 本地运行方案（推荐）

由于广东省政府采购网屏蔽了国外 IP，GitHub Actions 无法直接访问，建议改为本地运行。

### 快速开始

#### 1. 配置环境变量

复制 `.env.example` 为 `.env`，填入您的智谱 AI API Key：

```bash
ZHIPUAI_API_KEY=your_key_here
```

#### 2. 手动运行

双击运行 `run-local.bat` 即可手动执行爬虫并更新页面。

#### 3. 设置自动定时任务

1. 右键点击 PowerShell，选择"**以管理员身份运行**"
2. 执行命令：
   ```powershell
   cd d:\dg-procurement-radar
   .\setup-scheduled-task.ps1
   ```
3. 按提示完成设置

设置完成后，系统会每天早上 8:00 自动运行爬虫并更新 GitHub Pages。

### 查看结果

- GitHub Pages: https://dongtianwen.github.io/dg-procurement-rader
- 本地文件: `index.html`

## 项目结构

```
dg-procurement-radar/
├── scraper.py              # 数据抓取模块
├── processor.py            # AI 筛选模块（智谱 GLM）
├── writer.py               # HTML 页面生成
├── main.py                 # 主程序入口
├── run-local.bat           # 本地运行脚本
├── setup-scheduled-task.ps1 # 定时任务设置脚本
├── requirements.txt        # Python 依赖
└── .env.example            # 环境变量示例
```

## 技术栈

- Python 3.10+
- requests + BeautifulSoup4
- 智谱 GLM-4.7-Flash AI 模型
- GitHub Pages 静态托管

## 数据来源

广东省政府采购网：https://gdgpo.czt.gd.gov.cn

## License

MIT
