# 多代理运维自动化 MVP

一个针对 MiMo 100T 申请场景修复的可运行项目，用于展示如何使用 AI Agent 构建完整的广告运营自动化工作台。

---

# 项目简介

项目重点不是单个脚本，而是一条完整的自动化运营链路：

- 自动采集广告计划数据
- 自动分析高 CPA / 低 CTR / 高潜计划
- 自动生成暂停、降级调度、扩量等动作建议
- 自动执行动作模拟并沉淀日志
- 自动复盘输出结果并同步飞书

---

# 项目亮点

## 多 Agent 协同架构

系统由多个 Agent 分工协作：

- Coordinator Agent（协调器）
- Data Collector Agent（数据采集）
- Analysis Agent（数据分析）
- Strategy Agent（策略生成）
- Execution Agent（动作执行）
- Report Agent（报告生成）
- Notification Agent（通知同步）

---

## 技术栈

### Backend

- FastAPI
- SQLite
- SQLAlchemy
- Pydantic

### Frontend

- React
- Vite

---

## 功能特性

- 可运行的前后端完整项目
- Agent 日志可视化
- 任务执行结果展示
- 健康分统计
- SQLite 本地持久化
- 易于扩展真实广告平台 API
- 支持后续接入 LLM 决策层

---

# 项目结构

```text
agent_ops_mvp/
├─ backend/
│  ├─ app/
│  │  ├─ agent_orchestrator.py
│  │  ├─ database.py
│  │  ├─ integrations.py
│  │  ├─ main.py
│  │  ├─ models.py
│  │  ├─ schemas.py
│  │  └─ seed.py
│  ├─ .env.example
│  └─ requirements.txt
├─ frontend/
│  ├─ index.html
│  ├─ package.json
│  ├─ vite.config.js
│  └─ src/
│     ├─ main.jsx
│     └─ style.css
└─ PROJECT_OVERVIEW.md
```

---

# 本地启动

## Backend

```bash
cd backend

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

copy .env.example .env

python -m app.seed

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

接口文档：

```text
http://127.0.0.1:8000/docs
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

页面地址：

```text
http://127.0.0.1:5173
```

---

# 适合作为申请证明的内容

- GitHub 仓库代码与 README
- 本地运行截图
- Agent 日志截图
- 任务结果页截图
- 飞书通知截图（若配置 Webhook）

---

# 后续升级方向

- 接入巨量、腾讯、百度等真实广告平台 API
- 在 StrategyAgent / AnalysisAgent 中引入 LLM 推理
- 增加流量与风险阈值保护
- 增加定时任务系统
- 增加多机场支持
- 增加 Redis / Celery 异步调度
- 接入真实数据监控系统

---

# License

MIT License
