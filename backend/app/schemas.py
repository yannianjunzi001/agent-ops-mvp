from datetime import datetime
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    objective: str = Field(..., min_length=2)
    priority: int = Field(3, ge=1, le=5)

class TaskOut(BaseModel):
    id: int
    title: str
    objective: str
    status: str
    priority: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class AgentLogOut(BaseModel):
    id: int
    run_id: int
    agent_name: str
    level: str
    message: str
    created_at: datetime

    model_config = {"from_attributes": True}

class TaskRunOut(BaseModel):
    id: int
    task_id: int
    status: str
    summary: str
    score: float
    created_at: datetime
    finished_at: datetime | None
    logs: list[AgentLogOut] = []

    model_config = {"from_attributes": True}
