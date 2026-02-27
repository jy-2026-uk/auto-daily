---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 30450220576544cc2418ff8a9955ced57fdfe5ba5b1cfe272f18f12b5afa8088a71a557902210081a40945032ee2327227fa42cb3ad2d4c302e25f554495aa5b26147d2a41ff66
    ReservedCode2: 3045022100bf54b0e32d7e8f8c9ad6f517117bee6be12b57cd3ea2095d5ac85e7170bc32290220655aaee4457b917668409836ab39951436b0ead05a334a75275478e77789efb1
---

# 欧洲汽车新闻早报自动化工具

## 项目结构

```
euro_auto_news/
├── config.py          # 配置文件
├── fetcher.py         # 新闻抓取模块
├── processor.py      # 内容处理模块
├── notifier.py        # 推送模块（飞书/邮件）
├── main.py            # 主程序入口
├── requirements.txt   # Python依赖
└── .github/workflows/
    └── daily_news.yml # GitHub Actions定时任务
```

## 功能特点

- 自动抓取多个欧洲汽车新闻RSS源
- 智能过滤欧洲/德国相关汽车新闻
- 英文新闻标题和摘要直接展示
- 支持飞书群机器人和邮件推送
- 每日自动执行（GitHub Actions）

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置

复制并修改 `config.py` 中的配置：

```python
# 推送配置（选择一种或同时使用）
FEISHU_WEBHOOK = "your飞书Webhook地址"  # 可选
SMTP_CONFIG = {...}  # 可选，邮件配置
```

### 3. 运行测试

```bash
python main.py
```

### 4. 设置定时任务

将项目推送到GitHub仓库，启用GitHub Actions即可每日自动运行。

## 支持的RSS源

- Automotive News Europe
- Autocar
- Just Auto » Europe
- Green Car Reports
- BMW Group PressClub
- Nissan Motor Europe
- MG MOTOR EUROPE
- 等等...
