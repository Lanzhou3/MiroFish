# MiroFish

基于社交媒体行为模拟的电商爆品预测系统。

## 项目简介

MiroFish 是一个结合 **社交媒体行为模拟** 与 **电商数据分析** 的创新平台。通过 OASIS 框架模拟大量消费者 Agent 在虚拟社交平台上的互动行为，收集行为数据并分析商品的爆款潜力。

### 核心功能

- 🧪 **社交媒体模拟** - 基于 OASIS 框架，模拟 Twitter/Reddit 等平台的消费者行为
- 📊 **消费者画像生成** - 自动生成具有个性化属性的消费者 Agent
- 🔥 **爆品潜力评估** - 基于行为数据预测商品的爆款概率、销量峰值、ROI
- 📈 **可视化报告** - 实时展示模拟进程和数据洞察

## 技术架构

```
┌─────────────────┐     ┌─────────────────┐
│   Frontend      │     │    Backend      │
│   (Vue 3 +      │────▶│    (Flask)      │
│    Vite + D3)   │     │                 │
└─────────────────┘     └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   Zep Cloud   │    │     OASIS     │    │   LLM API     │
│  (记忆存储)    │    │  (社交模拟)    │    │ (OpenAI 格式)  │
└───────────────┘    └───────────────┘    └───────────────┘
```

## 电商化改造内容

本项目在原始 OASIS 社交媒体模拟框架基础上进行了电商化改造：

### 1. 消费者画像模型 (`ConsumerProfile`)

新增消费者属性：
- **消费能力等级** - HIGH/MEDIUM/LOW
- **价格敏感度** - 0.0-1.0 浮点值
- **品牌忠诚度** - 0.0-1.0 浮点值
- **购物频率** - DAILY/WEEKLY/MONTHLY/RARELY
- **品类偏好** - 偏好商品类目列表
- **平台偏好** - 淘宝/京东/拼多多/抖音等
- **决策因素权重** - 价格/品质/品牌/评价/趋势

### 2. 爆品评估系统 (`ViralEvaluator`)

核心评估指标：
- **爆款概率** - 基于参与率、购买意向率、分享率综合计算
- **销量预测** - 模拟 Agent 数量 × 放大系数 → 真实市场销量
- **ROI 预估** - 投资回报率计算
- **峰值时间预测** - 销量爆发时间点
- **分平台销量分布** - 各电商平台销量预测

### 3. 商品评估 API

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/product/evaluate` | POST | 完整爆品评估 |
| `/api/product/evaluate/quick` | POST | 快速评估（无需模拟数据） |

## 安装

### 前置要求

- Python 3.11+
- Node.js 18+
- LLM API（OpenAI 格式兼容）
- Zep Cloud API Key

### 后端安装

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 安装依赖
cd backend
pip install -r requirements.txt
```

### 前端安装

```bash
cd frontend
npm install
```

## 配置

在项目根目录创建 `.env` 文件：

```env
# LLM 配置（支持 OpenAI 格式的 API）
LLM_API_KEY=your-api-key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL_NAME=gpt-4o-mini

# Zep Cloud 配置
ZEP_API_KEY=your-zep-api-key

# Flask 配置
FLASK_HOST=0.0.0.0
FLASK_PORT=5001
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
```

## 运行

### 启动后端

```bash
cd backend
python run.py
```

后端服务运行在 `http://localhost:5001`

### 启动前端

```bash
cd frontend
npm run dev
```

前端服务运行在 `http://localhost:3000`

## API 概览

### 模拟相关

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/simulation/create` | POST | 创建模拟项目 |
| `/api/simulation/start` | POST | 启动模拟运行 |
| `/api/simulation/status` | GET | 获取运行状态 |
| `/api/simulation/stop` | POST | 停止模拟 |

### 图谱相关

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/graph/upload` | POST | 上传知识图谱数据 |
| `/api/graph/query` | GET | 查询图谱信息 |

### 报告相关

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/report/generate` | POST | 生成分析报告 |
| `/api/report/status` | GET | 获取报告生成状态 |

## 项目结构

```
MiroFish/
├── backend/
│   ├── app/
│   │   ├── api/           # API 路由
│   │   │   ├── graph.py
│   │   │   ├── simulation.py
│   │   │   ├── report.py
│   │   │   └── product.py   # 商品评估 API
│   │   ├── models/        # 数据模型
│   │   │   └── consumer_profile.py  # 消费者画像
│   │   ├── services/      # 业务服务
│   │   │   ├── viral_evaluator.py    # 爆品评估器
│   │   │   ├── simulation_manager.py
│   │   │   └── ...
│   │   ├── utils/         # 工具函数
│   │   └── config.py      # 配置管理
│   ├── uploads/           # 上传文件存储
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── views/         # 页面组件
│   │   ├── components/    # 通用组件
│   │   ├── api/           # API 调用
│   │   └── router/        # 路由配置
│   ├── package.json
│   └── vite.config.js
├── .env                   # 环境配置（需创建）
├── .gitignore
└── LICENSE
```

## 依赖说明

### 后端核心依赖

- **Flask** - Web 框架
- **OpenAI SDK** - LLM 调用
- **Zep Cloud** - 记忆存储与知识图谱
- **CAMEL-OASIS** - 社交媒体模拟框架
- **PyMuPDF** - PDF 文件解析

### 前端核心依赖

- **Vue 3** - 前端框架
- **Vue Router** - 路由管理
- **Vite** - 构建工具
- **D3.js** - 数据可视化
- **Axios** - HTTP 客户端

## 开发计划

- [ ] 更多电商平台支持
- [ ] 实时数据接入
- [ ] 用户画像管理界面
- [ ] 报告导出功能
- [ ] 多语言支持

## License

MIT License