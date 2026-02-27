"""
欧洲汽车新闻早报 - 主程序入口
每日自动抓取欧洲汽车新闻并推送
"""

import sys
import logging
from datetime import datetime

from fetcher import fetch_news
from processor import process_news
from notifier import send_notification

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """主函数"""
    start_time = datetime.now()
    logger.info("=" * 50)
    logger.info("🚗 欧洲汽车新闻早报机器人启动")
    logger.info(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 50)

    try:
        # 1. 抓取新闻
        logger.info("\n📥 Step 1: 抓取新闻...")
        news_list = fetch_news()
        logger.info(f"   共获取 {len(news_list)} 条新闻")

        if not news_list:
            logger.warning("   未获取到任何新闻")

        # 2. 处理新闻
        logger.info("\n📝 Step 2: 处理新闻...")
        processed = process_news(news_list)
        logger.info(f"   处理完成，共 {processed['news_count']} 条")

        # 3. 打印Markdown预览
        logger.info("\n📄 早报预览:")
        logger.info("-" * 50)
        # 只打印前3条预览
        preview_lines = processed["markdown"].split('\n')[:20]
        for line in preview_lines:
            logger.info(f"   {line}")
        logger.info("   ...")

        # 4. 发送通知
        logger.info("\n📤 Step 3: 发送通知...")
        results = send_notification(processed)

        # 5. 输出结果
        logger.info("\n" + "=" * 50)
        logger.info("📊 发送结果:")
        if results.get("feishu"):
            logger.info("   ✅ 飞书推送成功")
        if results.get("email"):
            logger.info("   ✅ 邮件推送成功")
        if not any(results.values()):
            logger.warning("   ⚠️ 未配置任何推送渠道")

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        logger.info(f"\n⏱️ 总耗时: {duration:.1f}秒")
        logger.info("✅ 执行完成!")
        logger.info("=" * 50)

        return True

    except Exception as e:
        logger.error(f"\n❌ 执行失败: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
