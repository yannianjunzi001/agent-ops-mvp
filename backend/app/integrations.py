import os
from dataclasses import dataclass

import requests
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Campaign:
    campaign_id: str
    name: str
    cost: float
    conversions: int
    ctr: float
    cpa: float


class FeishuNotifier:
    def __init__(self):
        self.webhook_url = os.getenv("FEISHU_WEBHOOK_URL", "").strip()

    def send_text(self, text: str) -> bool:
        if not self.webhook_url:
            print("[Feishu skipped]", text)
            return False
        response = requests.post(
            self.webhook_url,
            json={"msg_type": "text", "content": {"text": text}},
            timeout=8,
        )
        response.raise_for_status()
        return True


class AdvertisingClient:
    """广告平台 API 占位客户端，后续可替换为真实平台 SDK 或 HTTP API。"""

    def __init__(self):
        self.base_url = os.getenv("AD_API_BASE_URL", "")
        self.token = os.getenv("AD_API_TOKEN", "")

    def fetch_campaigns(self) -> list[Campaign]:
        return [
            Campaign("cmp_001", "搜索词-品牌防守", 320.5, 18, 0.081, 17.8),
            Campaign("cmp_002", "信息流-新客测试", 1880.0, 22, 0.019, 85.45),
            Campaign("cmp_003", "再营销-老客召回", 690.0, 41, 0.064, 16.82),
            Campaign("cmp_004", "短视频-活动爆量", 1150.0, 39, 0.058, 29.48),
        ]

    def pause_campaign(self, campaign_id: str) -> dict:
        return {"campaign_id": campaign_id, "action": "pause", "ok": True}

    def adjust_budget(self, campaign_id: str, percent: int) -> dict:
        return {
            "campaign_id": campaign_id,
            "action": "adjust_budget",
            "percent": percent,
            "ok": True,
        }
