# backend/app/services - AGENTS.md

**Generated:** 2026-03-11

核心业务逻辑层：图谱构建、多Agent仿真、报告生成的服务实现。

## OVERVIEW

13个服务模块，封装OASIS仿真引擎与Zep知识图谱的所有交互逻辑。职责：图谱构建 → 人设生成 → 仿真执行 → 报告生成。

## STRUCTURE

```
services/
├── ontology_generator.py      # LLM本体定义生成
├── graph_builder.py           # Zep图谱构建
├── text_processor.py          # 文档分块处理
├── zep_entity_reader.py       # 实体/边读取
├── zep_tools.py               # 检索工具 (InsightForge/PanoramaSearch)
├── zep_graph_memory_updater.py # 动态记忆更新
├── oasis_profile_generator.py # Agent人设生成 (Twitter/Reddit)
├── simulation_manager.py      # 仿真状态管理
├── simulation_config_generator.py # 仿真参数配置
├── simulation_runner.py       # OASIS执行引擎
├── simulation_ipc.py          # 进程间通信
└── report_agent.py            # ReACT报告生成
```

## WHERE TO LOOK

| Task | File | Key Class/Function |
|------|------|-------------------|
| 添加新检索工具 | `zep_tools.py` | `ZepToolsService` |
| 修改Agent行为逻辑 | `simulation_runner.py` | `SimulationRunner._run_round()` |
| 调整人设模板 | `oasis_profile_generator.py` | `OasisProfileGenerator` |
| 新增报告章节 | `report_agent.py` | `ReportAgent._generate_section()` |
| 添加IPC命令 | `simulation_ipc.py` | `CommandType` Enum |
| 修改图谱记忆更新 | `zep_graph_memory_updater.py` | `ZepGraphMemoryManager` |

## KEY SERVICES

### ZepToolsService (zep_tools.py)
核心检索工具集：
- `insight_forge(query)` — 深度混合检索，自动生成子问题
- `panorama_search(query)` — 广度搜索，含过期内容
- `quick_search(query)` — 快速检索
- `interview_agent(agent_name)` — Agent访谈

### SimulationRunner (simulation_runner.py)
OASIS执行引擎：
- 双平台并行 (Twitter + Reddit)
- IPC进程控制 (start/pause/stop)
- 实时状态监控
- 每轮动作记录 → `RoundSummary`

### ReportAgent (report_agent.py)
ReACT模式报告生成：
- 目录规划 → 分段生成
- 多轮思考与反思
- 自主调用检索工具
- 日志记录 → `agent_log.jsonl`

### OasisProfileGenerator (oasis_profile_generator.py)
Agent人设生成：
- Twitter CSV格式 (`user_id, username, bio, ...`)
- Reddit JSON格式 (`user_id, user_name, bio, ...`)
- 从图谱实体自动提取

## CONVENTIONS

**数据模型**: 所有类使用`@dataclass`
```python
@dataclass
class AgentAction:
    round_num: int
    platform: str
    agent_id: int
    action_type: str
    ...
```

**日志**: 统一使用 `get_logger('mirofish.service_name')`

**Zep客户端**: 从Config获取API Key
```python
from ..config import Config
client = Zep(api_key=Config.ZEP_API_KEY)
```

**LLM调用**: 使用`LLMClient`封装
```python
from ..utils.llm_client import LLMClient
llm = LLMClient()
response = llm.chat(messages)
```

## NOTES

- **仿真数据**: 存储在 `backend/uploads/simulations/{simulation_id}/`
- **报告日志**: `agent_log.jsonl` 记录每步详细动作
- **IPC协议**: JSON消息，支持start/pause/stop/query命令
- **Zep分页**: 使用 `zep_paging.fetch_all_nodes/edges` 处理大量数据