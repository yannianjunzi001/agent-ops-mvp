# Multi-Agent Ops Automation MVP

一个面向 MiMo 100T 申请场景打磨的可运行项目，用来展示我如何使用 AI Agent 构建一个完整的广告运营自动化工作台。

项目聚焦的不是单个脚本，而是一条完整链路：

1. 自动采集广告计划数据
2. 自动分析高 CPA / 低 CTR / 高潜计划
3. 自动生成暂停、降预算、扩量等动作建议
4. 自动执行模拟动作并沉淀日志
5. 自动输出复盘结果并同步飞书

## 项目亮点

- 多 Agent 分工清晰：Coordinator、DataCollector、Analysis、Strategy、Execution、Report、Notify
- 前后端可运行：FastAPI + React + SQLite
- 结果可展示：任务列表、运行结果、Agent 日志、健康分
- 易于扩展：可继续接入真实广告平台 API、LLM 决策层、审批链路

## 目录结构

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

## 本地启动

### 后端

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

### 前端

```bash
cd frontend
npm install
npm run dev
```

页面地址：

```text
http://127.0.0.1:5173
```

## 适合作为申请证明的内容

- GitHub 仓库代码与 README
- 本地运行截图
- Agent 日志截图
- 任务结果页截图
- 若配置了飞书 Webhook，可补充通知截图

## 后续升级方向

- 接入巨量、腾讯、百度等真实投放平台 API
- 在 StrategyAgent / AnalysisAgent 中引入 LLM 推理
- 增加审批流和风险阈值保护
- 增加定时任务与多租户支持
