"""
新闻抓取模块
从RSS源获取欧洲汽车新闻
"""

import feedparser
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
import logging

from config import RSS_SOURCES, FILTER_KEYWORDS, EXCLUDE_KEYWORDS, MAX_NEWS_COUNT

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NewsFetcher:
    """新闻抓取器"""

    def __init__(self):
        self.news_list = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def fetch_all(self) -> List[Dict]:
        """从所有启用的RSS源抓取新闻"""
        all_news = []

        for source in RSS_SOURCES:
            if not source.get("enabled", True):
                continue

            logger.info(f"正在抓取: {source['name']}")
            try:
                news_items = self.fetch_rss(source)
                all_news.extend(news_items)
                logger.info(f"  -> 获取到 {len(news_items)} 条新闻")
            except Exception as e:
                logger.error(f"  -> 抓取失败: {str(e)}")

            # 避免请求过快
            time.sleep(1)

        # 去重并排序
        all_news = self.deduplicate(all_news)
        all_news = self.filter_news(all_news)
        all_news = self.sort_by_date(all_news)

        # 限制数量
        return all_news[:MAX_NEWS_COUNT]

    def fetch_rss(self, source: Dict) -> List[Dict]:
        """从单个RSS源抓取新闻"""
        url = source["url"]
        name = source["name"]

        try:
            # 使用requests获取RSS内容
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()

            # 解析RSS
            feed = feedparser.parse(response.content)

            news_items = []
            for entry in feed.entries:
                news_item = self.parse_entry(entry, name)
                if news_item:
                    news_items.append(news_item)

            return news_items

        except requests.RequestException as e:
            logger.error(f"请求失败 [{name}]: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"解析失败 [{name}]: {str(e)}")
            return []

    def parse_entry(self, entry, source_name: str) -> Optional[Dict]:
        """解析单个RSS条目"""
        try:
            # 获取标题
            title = entry.get("title", "").strip()
            if not title:
                return None

            # 获取链接
            link = entry.get("link", "").strip()
            if not link:
                return None

            # 获取摘要/描述
            summary = ""
            if hasattr(entry, "summary"):
                summary = self.clean_html(entry.summary)
            elif hasattr(entry, "description"):
                summary = self.clean_html(entry.description)

            # 获取发布时间
            published = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                try:
                    published = datetime(*entry.published_parsed[:6])
                except:
                    pass

            if hasattr(entry, "updated_parsed") and entry.updated_parsed:
                try:
                    updated = datetime(*entry.updated_parsed[:6])
                    if published is None or updated > published:
                        published = updated
                except:
                    pass

            return {
                "title": title,
                "link": link,
                "summary": summary[:500] if summary else "",  # 限制摘要长度
                "source": source_name,
                "published": published,
                "published_str": self.format_date(published) if published else "未知"
            }

        except Exception as e:
            logger.debug(f"解析条目失败: {str(e)}")
            return None

    def clean_html(self, html_text: str) -> str:
        """清理HTML标签"""
        if not html_text:
            return ""

        import re
        # 移除HTML标签
        text = re.sub(r'<[^>]+>', '', html_text)
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def format_date(self, dt: datetime) -> str:
        """格式化日期"""
        if dt is None:
            return "未知"
        now = datetime.now()
        diff = now - dt

        if diff.days == 0:
            return "今天"
        elif diff.days == 1:
            return "昨天"
        elif diff.days < 7:
            return f"{diff.days}天前"
        else:
            return dt.strftime("%m-%d")

    def deduplicate(self, news_list: List[Dict]) -> List[Dict]:
        """去重 - 基于标题相似度"""
        seen = set()
        result = []

        for news in news_list:
            # 使用链接或标题的简化版作为唯一标识
            key = news.get("link", "") or news.get("title", "")
            key = key.lower().strip()

            # 简单去重：完全相同的链接
            if key and key not in seen:
                seen.add(key)
                result.append(news)

        return result

    def filter_news(self, news_list: List[Dict]) -> List[Dict]:
        """过滤新闻"""
        if not FILTER_KEYWORDS:
            return news_list

        filtered = []
        for news in news_list:
            title = news.get("title", "").lower()
            summary = news.get("summary", "").lower()
            text = title + " " + summary

            # 检查是否包含关键词
            if any(kw.lower() in text for kw in FILTER_KEYWORDS):
                # 检查是否需要排除
                if EXCLUDE_KEYWORDS:
                    if any(excl.lower() in text for excl in EXCLUDE_KEYWORDS):
                        continue
                filtered.append(news)

        return filtered

    def sort_by_date(self, news_list: List[Dict]) -> List[Dict]:
        """按日期排序 - 最新的在前"""
        return sorted(
            news_list,
            key=lambda x: x.get("published") or datetime.min,
            reverse=True
        )


def fetch_news() -> List[Dict]:
    """获取新闻的便捷函数"""
    fetcher = NewsFetcher()
    return fetcher.fetch_all()


if __name__ == "__main__":
    # 测试
    news = fetch_news()
    print(f"\n共获取 {len(news)} 条新闻:\n")
    for i, item in enumerate(news[:5], 1):
        print(f"{i}. {item['title']}")
        print(f"   来源: {item['source']} | {item['published_str']}")
        print(f"   链接: {item['link']}")
        print()
