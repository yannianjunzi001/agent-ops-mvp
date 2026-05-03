from datetime import datetime

from sqlalchemy.orm import Session

from .integrations import AdvertisingClient, FeishuNotifier
from .models import AgentLog, Task, TaskRun


class AgentOrchestrator:
    def __init__(self, db: Session):
        self.db = db
        self.ads = AdvertisingClient()
        self.feishu = FeishuNotifier()

    def _log(self, run: TaskRun, agent: str, message: str, level: str = "info"):
        item = AgentLog(run_id=run.id, agent_name=agent, level=level, message=message)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def run_task(self, task: Task) -> TaskRun:
        task.status = "running"
        task.updated_at = datetime.utcnow()
        run = TaskRun(task_id=task.id, status="running")
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)

        try:
            self._log(run, "CoordinatorAgent", f"开始执行任务：{task.title}")

            campaigns = self.ads.fetch_campaigns()
            total_cost = sum(item.cost for item in campaigns)
            self._log(
                run,
                "DataCollectorAgent",
                f"已拉取 {len(campaigns)} 条广告计划，累计消耗 {total_cost:.1f} 元。",
            )

            risky = []
            good = []
            for campaign in campaigns:
                if campaign.cpa > 60 or campaign.ctr < 0.025:
                    risky.append(campaign)
                else:
                    good.append(campaign)

            self._log(
                run,
                "AnalysisAgent",
                f"识别高风险计划 {len(risky)} 个，稳定或潜力计划 {len(good)} 个。",
            )

            actions = []
            for campaign in risky:
                if campaign.cpa > 80:
                    result = self.ads.pause_campaign(campaign.campaign_id)
                    actions.append(f"暂停 {campaign.name}，CPA={campaign.cpa:.2f}")
                    self._log(
                        run,
                        "StrategyAgent",
                        f"策略建议：暂停 {campaign.name}，优先止损。",
                        "warning",
                    )
                    self._log(run, "ExecutionAgent", f"执行暂停：{result}", "warning")
                else:
                    result = self.ads.adjust_budget(campaign.campaign_id, -20)
                    actions.append(f"下调 {campaign.name} 预算 20%，CPA={campaign.cpa:.2f}")
                    self._log(
                        run,
                        "StrategyAgent",
                        f"策略建议：降低 {campaign.name} 预算 20%。",
                        "warning",
                    )
                    self._log(run, "ExecutionAgent", f"执行调预算：{result}", "warning")

            for campaign in good:
                if campaign.conversions >= 30 and campaign.cpa < 30:
                    result = self.ads.adjust_budget(campaign.campaign_id, 15)
                    actions.append(f"提升 {campaign.name} 预算 15%，CPA={campaign.cpa:.2f}")
                    self._log(
                        run,
                        "StrategyAgent",
                        f"策略建议：为 {campaign.name} 扩量，预算提升 15%。",
                    )
                    self._log(run, "ExecutionAgent", f"执行扩量：{result}")

            if not actions:
                actions.append("当前没有需要调整的广告计划")

            summary = "；".join(actions)
            score = max(0, 100 - len(risky) * 18)
            self._log(run, "ReportAgent", f"生成运营报告：{summary}；健康分={score}")

            notify_text = (
                "【Agent 运营自动化】\n"
                f"任务：{task.title}\n"
                f"结论：{summary}\n"
                f"健康分：{score}"
            )
            sent = self.feishu.send_text(notify_text)
            self._log(
                run,
                "NotifyAgent",
                "飞书通知已发送。" if sent else "飞书 Webhook 未配置，已跳过真实发送。",
            )

            run.status = "success"
            run.summary = summary
            run.score = score
            run.finished_at = datetime.utcnow()
            task.status = "success"
            task.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(run)
            return run

        except Exception as exc:
            self._log(run, "CoordinatorAgent", f"任务失败：{exc}", "error")
            run.status = "failed"
            run.summary = str(exc)
            run.finished_at = datetime.utcnow()
            task.status = "failed"
            task.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(run)
            return run
