---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 30450221009a1af5dd6ff495f45b0e94cb13dae779f59e8bd02be65f62701bd161381de7cd0220528f087c0181d5da332b68084fcc77e4a5949785c87890bf53de0d187c9186bd
    ReservedCode2: 3045022100e1afaca056b6c8036ebb6d4a9416ae5bad4b2f8ea9057027415346b6049bb55e02200be952794b82095997c864d92f11535a50444868d8eaf0f56ee4a08ac0297605
---

# GitHub Actions 部署指南

## 步骤1: 创建GitHub仓库

1. 打开 https://github.com/new
2. 创建新仓库（如 `euro-auto-news`）
3. 选择 **Public** 或 **Private**
4. 点击 **Create repository**

## 步骤2: 上传代码

有两种方式：

### 方式A: 命令行上传

```bash
# 在本地打开终端，进入项目目录
cd euro_auto_news

# 初始化git
git init
git add .
git commit -m "Initial commit"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/euro-auto-news.git

# 推送
git push -u origin main
```

### 方式B: 网页上传

1. 在仓库页面点击 **uploading an existing file**
2. 拖入所有文件
3. 点击 **Commit changes**

## 步骤3: 添加飞书Webhook密钥

1. 进入仓库页面
2. 点击 **Settings**（设置）
3. 点击左侧 **Secrets and variables** → **Actions**
4. 点击 **New repository secret**
5. 添加：
   - **Name**: `FEISHU_WEBHOOK`
   - **Secret**: `https://open.feishu.cn/open-apis/bot/v2/hook/c6f7f47f-c2be-4198-9b08-bc0c37097620`
6. 点击 **Add secret**

## 步骤4: 验证

1. 进入 **Actions** 页面
2. 点击 **Daily Europe Auto News**
3. 点击 **Run workflow** → **Run workflow**
4. 查看运行结果

## 步骤5: 自动运行

- 每天早上7点（北京时间）会自动运行
- 也可以手动触发：在Actions页面点击Run workflow

---

## 文件结构

```
euro_auto_news/
├── .github/
│   └── workflows/
│       └── daily_news.yml    # GitHub Actions配置
├── config.py                  # 配置文件
├── fetcher.py                 # 新闻抓取
├── processor.py              # 内容处理
├── notifier.py               # 飞书推送
├── main.py                   # 主程序
├── requirements.txt          # Python依赖
└── README.md                 # 说明文档
```

## 常见问题

### Q: 为什么推送失败？
A: 检查Secrets中的FEISHU_WEBHOOK是否正确配置

### Q: 如何修改推送时间？
A: 编辑 `.github/workflows/daily_news.yml` 中的cron表达式

### Q: 如何添加更多新闻源？
A: 编辑 `config.py` 中的 `RSS_SOURCES` 列表
