from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from .agent_orchestrator import AgentOrchestrator
from .database import Base, engine, get_db
from .models import AgentLog, Task, TaskRun
from .schemas import AgentLogOut, TaskCreate, TaskOut, TaskRunOut

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Multi-Agent Ops Automation MVP", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Multi-Agent Ops Automation MVP is running"}


@app.get("/api/dashboard")
def dashboard(db: Session = Depends(get_db)):
    tasks = db.scalars(select(Task).order_by(Task.created_at.desc())).all()
    runs = db.scalars(select(TaskRun).order_by(TaskRun.created_at.desc())).all()
    latest_score = runs[0].score if runs else 0
    return {
        "task_count": len(tasks),
        "run_count": len(runs),
        "latest_score": latest_score,
        "highlights": [
            {
                "title": "完整闭环",
                "detail": "从拉取广告数据、识别异常、生成动作建议到飞书通知，全链路可直接演示。",
            },
            {
                "title": "多 Agent 协同",
                "detail": "任务被拆分为 7 个角色节点，支持日志留痕、复盘和后续接入 LLM 推理层。",
            },
            {
                "title": "工程化可扩展",
                "detail": "前端采用 React，后端采用 FastAPI + SQLite，便于继续接入真实广告平台 API。",
            },
        ],
    }


@app.post("/api/tasks", response_model=TaskOut)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = Task(title=payload.title, objective=payload.objective, priority=payload.priority)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.get("/api/tasks", response_model=list[TaskOut])
def list_tasks(db: Session = Depends(get_db)):
    stmt = select(Task).order_by(Task.created_at.desc())
    return db.scalars(stmt).all()


@app.get("/api/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/api/tasks/{task_id}/run", response_model=TaskRunOut)
def run_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    orchestrator = AgentOrchestrator(db)
    return orchestrator.run_task(task)


@app.get("/api/tasks/{task_id}/runs", response_model=list[TaskRunOut])
def list_task_runs(task_id: int, db: Session = Depends(get_db)):
    stmt = (
        select(TaskRun)
        .where(TaskRun.task_id == task_id)
        .options(selectinload(TaskRun.logs))
        .order_by(TaskRun.created_at.desc())
    )
    return db.scalars(stmt).all()


@app.get("/api/runs/{run_id}", response_model=TaskRunOut)
def get_run(run_id: int, db: Session = Depends(get_db)):
    stmt = select(TaskRun).where(TaskRun.id == run_id).options(selectinload(TaskRun.logs))
    run = db.scalars(stmt).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@app.get("/api/logs", response_model=list[AgentLogOut])
def list_logs(db: Session = Depends(get_db)):
    stmt = select(AgentLog).order_by(AgentLog.created_at.desc()).limit(100)
    return db.scalars(stmt).all()


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"ok": True}
