import React, { useEffect, useMemo, useState } from 'react'
import { createRoot } from 'react-dom/client'
import {
  Activity,
  Bot,
  ChevronRight,
  ClipboardList,
  Gauge,
  Play,
  Plus,
  RefreshCw,
  ShieldCheck,
  Sparkles,
  Trash2,
  Waypoints
} from 'lucide-react'
import './style.css'

const API = 'http://127.0.0.1:8000/api'

const AGENT_STEPS = [
  { name: 'CoordinatorAgent', detail: '拆解任务、分配链路、兜底异常' },
  { name: 'DataCollectorAgent', detail: '拉取广告计划与账户指标' },
  { name: 'AnalysisAgent', detail: '识别高 CPA、低 CTR、潜力计划' },
  { name: 'StrategyAgent', detail: '生成降预算、暂停、扩量建议' },
  { name: 'ExecutionAgent', detail: '调用执行层完成动作回写' },
  { name: 'ReportAgent', detail: '输出总结、健康分与复盘' },
  { name: 'NotifyAgent', detail: '同步飞书结果，沉淀留痕' }
]

function App() {
  const [tasks, setTasks] = useState([])
  const [logs, setLogs] = useState([])
  const [dashboard, setDashboard] = useState(null)
  const [selectedRun, setSelectedRun] = useState(null)
  const [form, setForm] = useState({
    title: '晚高峰广告巡检',
    objective: '分析计划消耗、转化与 CPA，自动识别异常计划并给出预算调整建议',
    priority: 3
  })
  const [loading, setLoading] = useState(false)
  const [submitting, setSubmitting] = useState(false)

  async function load() {
    const [taskRes, logRes, dashboardRes] = await Promise.all([
      fetch(`${API}/tasks`),
      fetch(`${API}/logs`),
      fetch(`${API}/dashboard`)
    ])

    const taskJson = await taskRes.json()
    const logJson = await logRes.json()
    const dashboardJson = await dashboardRes.json()

    setTasks(taskJson)
    setLogs(logJson)
    setDashboard(dashboardJson)
  }

  useEffect(() => {
    load()
  }, [])

  const successRate = useMemo(() => {
    const completed = tasks.filter((task) => task.status === 'success').length
    if (!tasks.length) return 0
    return Math.round((completed / tasks.length) * 100)
  }, [tasks])

  async function createTask(event) {
    event.preventDefault()
    if (!form.title.trim() || !form.objective.trim()) return
    setSubmitting(true)
    try {
      await fetch(`${API}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form, priority: Number(form.priority) })
      })
      setForm({
        title: '新建广告巡检任务',
        objective: '检查异常消耗与高风险计划，并自动生成飞书通知草案',
        priority: 3
      })
      await load()
    } finally {
      setSubmitting(false)
    }
  }

  async function runTask(taskId) {
    setLoading(true)
    try {
      const response = await fetch(`${API}/tasks/${taskId}/run`, { method: 'POST' })
      const run = await response.json()
      setSelectedRun(run)
      await load()
    } finally {
      setLoading(false)
    }
  }

  async function deleteTask(taskId) {
    await fetch(`${API}/tasks/${taskId}`, { method: 'DELETE' })
    if (selectedRun?.task_id === taskId) {
      setSelectedRun(null)
    }
    await load()
  }

  return (
    <div className="appShell">
      <main className="page">
        <section className="hero">
          <div>
            <span className="eyebrow">
              <Sparkles size={14} />
              MiMo 100T Application Demo
            </span>
            <h1>多 Agent 广告运营自动化工作台</h1>
            <p className="heroCopy">
              用一个可运行的 MVP 展示从数据采集、异常分析、策略生成、动作执行到飞书同步的完整闭环。
            </p>
          </div>
          <div className="heroActions">
            <button className="ghostButton" onClick={load}>
              <RefreshCw size={16} />
              刷新数据
            </button>
            <div className="heroHint">
              <ShieldCheck size={16} />
              适合提交 GitHub 链接、运行截图和项目说明
            </div>
          </div>
        </section>

        <section className="statsGrid">
          <StatCard icon={<ClipboardList size={18} />} label="任务总数" value={String(tasks.length)} note="支持新建、运行、删除" />
          <StatCard icon={<Gauge size={18} />} label="运行成功率" value={`${successRate}%`} note="反映流程可用性" />
          <StatCard icon={<Bot size={18} />} label="Agent 节点" value="7" note="覆盖采集到通知全链路" />
          <StatCard
            icon={<Activity size={18} />}
            label="最近健康分"
            value={dashboard ? String(dashboard.latest_score) : '--'}
            note="基于风险计划数量计算"
          />
        </section>

        <section className="panelGrid">
          <section className="panel">
            <div className="panelHeader">
              <div>
                <h2>项目亮点</h2>
                <p>这部分可以直接拿来支撑申请表中的成果描述。</p>
              </div>
            </div>
            <div className="highlightList">
              {dashboard?.highlights?.map((item) => (
                <article className="highlightItem" key={item.title}>
                  <h3>{item.title}</h3>
                  <p>{item.detail}</p>
                </article>
              ))}
            </div>
          </section>

          <section className="panel">
            <div className="panelHeader">
              <div>
                <h2>多 Agent 链路</h2>
                <p>展示核心逻辑，方便评审理解不是单点脚本。</p>
              </div>
            </div>
            <div className="flowList">
              {AGENT_STEPS.map((step, index) => (
                <div className="flowItem" key={step.name}>
                  <div className="flowIndex">{index + 1}</div>
                  <div>
                    <strong>{step.name}</strong>
                    <p>{step.detail}</p>
                  </div>
                  {index < AGENT_STEPS.length - 1 ? <ChevronRight size={16} className="flowArrow" /> : null}
                </div>
              ))}
            </div>
          </section>
        </section>

        <section className="workspaceGrid">
          <section className="panel">
            <div className="panelHeader">
              <div>
                <h2>新建任务</h2>
                <p>通过不同巡检目标演示 Agent 的复用能力。</p>
              </div>
            </div>
            <form className="taskForm" onSubmit={createTask}>
              <label>
                <span>任务标题</span>
                <input
                  placeholder="例如：夜间预算守护"
                  value={form.title}
                  onChange={(event) => setForm({ ...form, title: event.target.value })}
                />
              </label>
              <label>
                <span>任务目标</span>
                <textarea
                  placeholder="例如：关注高 CPA 和低 CTR 计划，自动给出暂停或降预算建议"
                  value={form.objective}
                  onChange={(event) => setForm({ ...form, objective: event.target.value })}
                />
              </label>
              <label>
                <span>优先级：P{form.priority}</span>
                <input
                  type="range"
                  min="1"
                  max="5"
                  value={form.priority}
                  onChange={(event) => setForm({ ...form, priority: event.target.value })}
                />
              </label>
              <button disabled={submitting}>
                <Plus size={16} />
                创建任务
              </button>
            </form>
          </section>

          <section className="panel">
            <div className="panelHeader">
              <div>
                <h2>任务列表</h2>
                <p>点击运行后可立即看到日志、总结和健康分。</p>
              </div>
            </div>
            <div className="taskList">
              {tasks.map((task) => (
                <article className="taskRow" key={task.id}>
                  <div className="taskMeta">
                    <strong>{task.title}</strong>
                    <p>{task.objective}</p>
                    <div className="tagRow">
                      <span className={`statusTag ${task.status}`}>{task.status}</span>
                      <span className="softTag">P{task.priority}</span>
                    </div>
                  </div>
                  <div className="taskActions">
                    <button disabled={loading} onClick={() => runTask(task.id)}>
                      <Play size={16} />
                      运行
                    </button>
                    <button className="dangerButton" onClick={() => deleteTask(task.id)}>
                      <Trash2 size={16} />
                    </button>
                  </div>
                </article>
              ))}
            </div>
          </section>
        </section>

        <section className="workspaceGrid">
          <section className="panel">
            <div className="panelHeader">
              <div>
                <h2>最近一次结果</h2>
                <p>这里是最适合截图给评审看的区域之一。</p>
              </div>
            </div>
            {selectedRun ? (
              <div className="resultPanel">
                <div className="scoreRing">{selectedRun.score}</div>
                <div className="resultCopy">
                  <span className={`statusTag ${selectedRun.status}`}>{selectedRun.status}</span>
                  <p>{selectedRun.summary}</p>
                </div>
              </div>
            ) : (
              <EmptyState text="运行任意任务后，这里会显示 Agent 输出的总结与健康分。" />
            )}

            <div className="evidenceBlock">
              <div className="evidenceTitle">
                <Waypoints size={16} />
                申请表可强调的证明点
              </div>
              <ul>
                <li>完整前后端项目，可在本地直接运行和演示。</li>
                <li>包含多 Agent 分工、日志留痕、结果汇总与通知链路。</li>
                <li>支持扩展真实广告平台 API 与 LLM 决策层。</li>
              </ul>
            </div>
          </section>

          <section className="panel">
            <div className="panelHeader">
              <div>
                <h2>Agent 日志</h2>
                <p>建议申请时附上这一块截图，能证明流程是真跑起来的。</p>
              </div>
            </div>
            <div className="logList">
              {logs.length ? (
                logs.map((log) => (
                  <article className="logRow" key={log.id}>
                    <div className="logTop">
                      <strong>{log.agent_name}</strong>
                      <span className={`levelTag ${log.level}`}>{log.level}</span>
                    </div>
                    <span className="timestamp">{new Date(log.created_at).toLocaleString()}</span>
                    <p>{log.message}</p>
                  </article>
                ))
              ) : (
                <EmptyState text="还没有日志。先运行一个任务，我们就能得到完整的链路记录。" />
              )}
            </div>
          </section>
        </section>
      </main>
    </div>
  )
}

function StatCard({ icon, label, value, note }) {
  return (
    <article className="statCard">
      <div className="statIcon">{icon}</div>
      <div>
        <span className="statLabel">{label}</span>
        <strong className="statValue">{value}</strong>
        <p>{note}</p>
      </div>
    </article>
  )
}

function EmptyState({ text }) {
  return (
    <div className="emptyState">
      <Bot size={18} />
      <p>{text}</p>
    </div>
  )
}

createRoot(document.getElementById('root')).render(<App />)
