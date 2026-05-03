from .database import Base, SessionLocal, engine
from .models import Task

Base.metadata.create_all(bind=engine)


def main():
    db = SessionLocal()
    try:
        if db.query(Task).count() == 0:
            db.add_all(
                [
                    Task(
                        title="每日广告巡检",
                        objective="拉取广告数据，分析 CPA 和 CTR，自动生成优化建议并同步飞书。",
                        priority=2,
                    ),
                    Task(
                        title="异常成本告警",
                        objective="发现 CPA 过高或 CTR 过低的计划，并给出暂停或降预算建议。",
                        priority=1,
                    ),
                    Task(
                        title="优质计划扩量",
                        objective="识别高转化低 CPA 计划，自动生成扩量动作与复盘结论。",
                        priority=3,
                    ),
                ]
            )
            db.commit()
            print("Seed data inserted")
        else:
            print("Seed data already exists")
    finally:
        db.close()


if __name__ == "__main__":
    main()
