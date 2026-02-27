"""
推送模块
支持飞书群机器人和邮件推送
"""

import json
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List
import logging

from config import FEISHU_WEBHOOK, EMAIL_CONFIG

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Notifier:
    """消息推送器"""

    def __init__(self):
        self.feishu_webhook = FEISHU_WEBHOOK
        self.email_config = EMAIL_CONFIG

    def send_all(self, processed_news: dict) -> Dict[str, bool]:
        """发送消息到所有配置的渠道"""
        results = {}

        # 飞书推送
        if self.feishu_webhook:
            results["feishu"] = self.send_feishu(processed_news["feishu_card"])
        else:
            results["feishu"] = False

        # 邮件推送
        if self.email_config.get("enabled"):
            results["email"] = self.send_email(
                processed_news["html"],
                processed_news["date"]
            )
        else:
            results["email"] = False

        return results

    def send_feishu(self, card_data: dict) -> bool:
        """发送飞书卡片消息"""
        if not self.feishu_webhook:
            logger.warning("未配置飞书Webhook")
            return False

        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                self.feishu_webhook,
                headers=headers,
                data=json.dumps(card_data),
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    logger.info("飞书消息发送成功")
                    return True
                else:
                    logger.error(f"飞书返回错误: {result}")
                    return False
            else:
                logger.error(f"飞书请求失败: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"飞书发送失败: {str(e)}")
            return False

    def send_email(self, html_content: str, date_str: str) -> bool:
        """发送邮件"""
        config = self.email_config

        if not config.get("enabled"):
            logger.warning("邮件功能未启用")
            return False

        try:
            # 创建邮件
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"{config.get('subject_prefix', '')} {date_str}"
            msg['From'] = config.get("smtp_user")
            msg['To'] = ", ".join(config.get("to_emails", []))

            # 添加HTML内容
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)

            # 连接SMTP服务器并发送
            server = smtplib.SMTP(
                config.get("smtp_server"),
                config.get("smtp_port", 587)
            )
            server.starttls()
            server.login(
                config.get("smtp_user"),
                config.get("smtp_password")
            )
            server.sendmail(
                config.get("smtp_user"),
                config.get("to_emails", []),
                msg.as_string()
            )
            server.quit()

            logger.info("邮件发送成功")
            return True

        except Exception as e:
            logger.error(f"邮件发送失败: {str(e)}")
            return False


def send_notification(processed_news: dict) -> Dict[str, bool]:
    """发送通知的便捷函数"""
    notifier = Notifier()
    return notifier.send_all(processed_news)
