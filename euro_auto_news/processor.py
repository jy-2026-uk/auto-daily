"""
内容处理模块
生成早报格式
"""

from typing import List, Dict
from datetime import datetime


class NewsProcessor:
    """新闻处理器 - 生成早报格式"""

    def __init__(self):
        self.today = datetime.now().strftime("%Y年%m月%d日")

    def generate_markdown(self, news_list: List[Dict]) -> str:
        """生成Markdown格式早报"""
        if not news_list:
            return self._generate_empty_report()

        report = []
        report.append(f"# 🚗 欧洲汽车早报 - {self.today}")
        report.append("")
        report.append(f"**今日要闻 ({len(news_list)}条)**")
        report.append("")

        for i, item in enumerate(news_list, 1):
            # 标题
            report.append(f"### {i}. {item['title']}")
            report.append("")

            # 来源和时间
            meta = f"📰 {item['source']} | 🕐 {item['published_str']}"
            report.append(meta)
            report.append("")

            # 摘要
            if item.get("summary"):
                report.append(f"> {item['summary']}")
                report.append("")

            # 链接
            report.append(f"🔗 [查看原文]({item['link']})")
            report.append("")
            report.append("---")
            report.append("")

        # 底部信息
        report.append("")
        report.append("---")
        report.append(f"*数据来源: Automotive News Europe, Autocar, Just Auto等*")
        report.append(f"*生成时间: {datetime.now().strftime('%H:%M:%S')}*")

        return "\n".join(report)

    def generate_html(self, news_list: List[Dict]) -> str:
        """生成HTML格式早报"""
        if not news_list:
            return self._generate_empty_report_html()

        html_parts = []
        html_parts.append(f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>欧洲汽车早报 - {self.today}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
        .header {{ background: linear-gradient(135deg, #1a73e8, #4285f4); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
        .header h1 {{ margin: 0; font-size: 24px; }}
        .header .date {{ opacity: 0.9; margin-top: 5px; }}
        .news-card {{ background: white; border-radius: 8px; padding: 20px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .news-title {{ font-size: 18px; font-weight: 6001a73e; color: #8; margin-bottom: 10px; }}
        .news-meta {{ font-size: 13px; color: #666; margin-bottom: 10px; }}
        .news-summary {{ font-size: 14px; color: #333; line-height: 1.6; }}
        .news-link {{ display: inline-block; margin-top: 10px; color: #1a73e8; text-decoration: none; }}
        .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚗 欧洲汽车早报</h1>
        <div class="date">{self.today} | 今日要闻 ({len(news_list)}条)</div>
    </div>
""")

        for i, item in enumerate(news_list, 1):
            html_parts.append(f"""
    <div class="news-card">
        <div class="news-title">{i}. {self._escape_html(item['title'])}</div>
        <div class="news-meta">📰 {self._escape_html(item['source'])} | 🕐 {item['published_str']}</div>
        <div class="news-summary">{self._escape_html(item.get('summary', ''))}</div>
        <a class="news-link" href="{self._escape_html(item['link'])}" target="_blank">🔗 查看原文 →</a>
    </div>
""")

        html_parts.append(f"""
    <div class="footer">
        <p>数据来源: Automotive News Europe, Autocar, Just Auto等</p>
        <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
</body>
</html>
""")

        return "\n".join(html_parts)

    def generate_feishu_card(self, news_list: List[Dict]) -> dict:
        """生成飞书卡片消息格式"""
        if not news_list:
            return self._generate_empty_feishu_card()

        # 构建新闻列表
        news_elements = []
        for i, item in enumerate(news_list[:10], 1):  # 飞书卡片限制
            news_elements.append({
                "tag": "div",
                "text": {
                    "tag": "text",
                    "content": f"**{i}. {self._escape_md(item['title'])}**\n📰 {item['source']} | 🕐 {item['published_str']}\n{item.get('summary', '')[:100]}...\n[查看原文]({item['link']})"
                }
            })

        card = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": f"🚗 欧洲汽车早报 - {self.today}"
                    },
                    "template": "blue"
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "text",
                            "content": f"📊 今日要闻 ({len(news_list)}条)\n\n"
                        }
                    },
                    *news_elements,
                    {
                        "tag": "div",
                        "text": {
                            "tag": "text",
                            "content": f"\n---\n*数据来源: Automotive News Europe, Autocar, Just Auto*\n*生成时间: {datetime.now().strftime('%H:%M')}*"
                        }
                    }
                ]
            }
        }

        return card

    def _generate_empty_report(self) -> str:
        """生成空报告"""
        return f"""# 🚗 欧洲汽车早报 - {self.today}

今日暂无汽车行业重大新闻。

---
*数据来源: Automotive News Europe, Autocar, Just Auto等*
*生成时间: {datetime.now().strftime('%H:%M:%S')}*
"""

    def _generate_empty_report_html(self) -> str:
        """生成空报告HTML"""
        return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>欧洲汽车早报</title></head>
<body>
    <h1>欧洲汽车早报 - {self.today}</h1>
    <p>今日暂无汽车行业重大新闻。</p>
</body>
</html>
"""

    def _generate_empty_feishu_card(self) -> dict:
        """生成空飞书卡片"""
        return {
            "msg_type": "text",
            "content": f"🚗 欧洲汽车早报 - {self.today}\n\n今日暂无汽车行业重大新闻。"
        }

    def _escape_html(self, text: str) -> str:
        """HTML转义"""
        return (text
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;"))

    def _escape_md(self, text: str) -> str:
        """Markdown转义"""
        return text.replace("[", "\\[").replace("]", "\\]")


def process_news(news_list: List[Dict]) -> dict:
    """处理新闻的便捷函数"""
    processor = NewsProcessor()
    return {
        "markdown": processor.generate_markdown(news_list),
        "html": processor.generate_html(news_list),
        "feishu_card": processor.generate_feishu_card(news_list),
        "news_count": len(news_list),
        "date": processor.today
    }
