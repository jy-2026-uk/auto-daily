"""
快速测试脚本 - 仅测试飞书推送
"""
import requests
import json
from config import FEISHU_WEBHOOK

# 发送测试消息
test_message = {
    "msg_type": "text",
    "content": {
        "text": "🚗 测试消息\n\n欧洲汽车早报机器人已配置成功！\n\n每天早上7点会自动推送欧洲汽车新闻早报。"
    }
}

print(f"正在发送测试消息到飞书...")
print(f"Webhook: {FEISHU_WEBHOOK}")

try:
    response = requests.post(
        FEISHU_WEBHOOK,
        headers={"Content-Type": "application/json"},
        data=json.dumps(test_message),
        timeout=10
    )

    print(f"\n响应状态码: {response.status_code}")
    print(f"响应内容: {response.text}")

    if response.status_code == 200:
        result = response.json()
        if result.get("code") == 0:
            print("\n✅ 飞书消息发送成功！请查看您的飞书群聊。")
        else:
            print(f"\n❌ 飞书返回错误: {result}")
    else:
        print(f"\n❌ 请求失败")

except Exception as e:
    print(f"\n❌ 发送失败: {str(e)}")
