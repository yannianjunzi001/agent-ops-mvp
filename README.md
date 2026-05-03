多代理运维自动化MVP
一个针对 MiMo 100T 申请场景修复的可运行项目，用于展示我如何使用 AI Agent 构建一个完整的广告运营自动化工作台。

项目重点不是单个脚本，而是一条完整的顺序：

自动采集广告计划数据
自动分析高CPA /低CTR /高潜计划
自动生成暂停、降级调度、扩量等动作建议
自动执行动作模拟并沉淀日志
自动复输出盘结果并同步飞书
项目亮点
多Agent分工指令：协调器、数据收集器、分析、策略、执行、报告、通知
前遥控器可运行：FastAPI + React + SQLite
结果可展示：任务列表、运行结果、Agent日志、健康分
易于扩展：可继续接入真实广告平台API、LLM决策层、渠道货架
目录结构
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
本地启动
的
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -m app.seed
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
接口文档：

http://127.0.0.1:8000/docs
前端
cd frontend
npm install
npm run dev
页面地址：

http://127.0.0.1:5173
适合作为申请证明的内容
GitHub 仓库代码与 README
本地运行截图
特工日志截图
任务结果页截图
若配置了飞书Webhook，可补充通知截图
后续升级方向
接入巨量、腾讯、百度等真实投放平台API
在 StrategyAgent / AnalysisAgent 中引入 LLM 推理
增加增加流量和风险阈值保护
增加定时任务与多机场支持
