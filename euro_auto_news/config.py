"""
配置文件
请根据您的需求修改以下配置
"""

# ==================== 新闻源配置 ====================
# RSS源列表 - 欧洲/德国汽车新闻
RSS_SOURCES = [
    {
        "name": "Automotive News Europe",
        "url": "https://www.autonews.com/europe/rss.xml",
        "enabled": True
    },
    {
        "name": "Autocar",
        "url": "https://www.autocar.co.uk/rss",
        "enabled": True
    },
    {
        "name": "Just Auto - Europe",
        "url": "https://www.just-auto.com/region/europe/feed/",
        "enabled": True
    },
    {
        "name": "Green Car Reports",
        "url": "https://www.greencarreports.com/rss-feeds",
        "enabled": True
    },
    {
        "name": "Automotive IQ",
        "url": "https://www.automotive-iq.com/rss-feeds",
        "enabled": True
    },
    {
        "name": "Motor Authority",
        "url": "https://www.motorauthority.com/rss-feeds",
        "enabled": True
    },
]

# 关键词过滤 - 只保留包含这些关键词的新闻
# 留空则不过滤
FILTER_KEYWORDS = [
    "Europe", "European", "Germany", "German",
    "Volkswagen", "BMW", "Mercedes", "Audi", "Porsche",
    "VW", "Daimler", "Opel", "Peugeot", "Renault",
    "Tesla", "electric", "EV", "battery", "charging",
    "sales", "market", "launch", "new model",
    "OEM", "automaker", "car industry"
]

# 排除关键词 - 排除包含这些关键词的新闻
EXCLUDE_KEYWORDS = [
    "used car", "review", "test drive", "racing",
    "motorsport", "formula", "rally"
]

# 新闻数量限制
MAX_NEWS_COUNT = 15

# ==================== 推送配置 ====================

# 飞书配置 (二选一)
# 优先级：环境变量 > 硬编码 (GitHub Actions会自动注入环境变量)
import os
FEISHU_WEBHOOK = os.environ.get("FEISHU_WEBHOOK", "https://open.feishu.cn/open-apis/bot/v2/hook/c6f7f47f-c2be-4198-9b08-bc0c37097620")  # 飞书群机器人Webhook地址

# 邮件配置 (二选一)
EMAIL_CONFIG = {
    "enabled": False,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_user": "your_email@gmail.com",
    "smtp_password": "your_app_password",  # 需要使用应用专用密码
    "from_name": "欧洲汽车早报",
    "to_emails": ["recipient@example.com"],  # 接收人列表
    "subject_prefix": "【欧洲汽车早报】"
}

# ==================== 执行时间配置 ====================
# 每日执行时间 (UTC+8时区)
DAILY_HOUR = 7  # 早上7点
DAILY_MINUTE = 0
