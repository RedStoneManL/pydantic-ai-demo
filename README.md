# 智能客服工单系统 Demo

展示 **Pydantic AI 的必要性** + **Langfuse 追踪**

## 🎯 Demo 目的

1. **后端**：展示 Pydantic AI 如何消除 LLM 输出的不确定性
2. **前端**：展示 Langfuse 如何追踪 LLM 调用，查看 call stack

## 📁 项目结构

```
pydantic-ai-demo/
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── models.py          # Pydantic 模型（类型安全）
│   │   ├── agent.py           # Pydantic AI Agent + Langfuse
│   │   └── api.py             # FastAPI 端点
│   ├── main.py                # 入口
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                   # Next.js 前端
│   ├── src/
│   │   ├── components/
│   │   │   ├── TicketForm.tsx
│   │   │   └── TicketResult.tsx
│   │   └── app/
│   │       ├── layout.tsx
│   │       └── page.tsx
│   ├── package.json
│   └── .env.local
│
└── README.md
```

## 🚀 快速启动

### 1. 后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的 API Key

# 启动
python -m uvicorn main:app --reload --port 8000
```

### 2. 前端

```bash
cd frontend

# 安装依赖
npm install

# 启动
npm run dev
```

访问 http://localhost:3000

## 🔄 核心功能

### 后端：Pydantic AI 结构化输出

```python
from pydantic_ai import Agent

class TicketAnalysis(BaseModel):
    category: TicketCategory  # 枚举，只能是特定值
    urgency: UrgencyLevel     # 枚举，只能是 P0-P3
    product: str              # 必填
    summary: str              # 必填
    confidence: float         # 0-1 之间

agent = Agent('openai:gpt-4o', output_type=TicketAnalysis)
result = agent.run_sync(user_input)

# result.output 保证是 TicketAnalysis 类型
# 所有字段都经过验证
```

### 后端：Langfuse 追踪

每次 LLM 调用都被追踪：

```python
from langfuse import Langfuse
from langfuse.decorators import observe

langfuse = Langfuse(...)

@observe(name="analyze_ticket")
async def analyze_ticket(user_input: str):
    result = await agent.run(user_input)
    return result.output
```

### 前端：Call Stack 展示

```tsx
// 获取 Langfuse trace
const response = await axios.get(`/api/trace/${trace_id}`);

// 展示
<TraceViewer trace={response.data} />
```

## 📊 API 端点

| 端点 | 说明 |
|------|------|
| `POST /api/ticket/analyze` | ✅ 用 Pydantic AI 分析 |
| `POST /api/ticket/analyze-bad` | ❌ 不用 Pydantic AI（展示问题）|
| `POST /api/ticket/compare` | 🔄 对比两种方式 |
| `GET /api/trace/{id}` | 获取 Langfuse trace |

## 🧪 测试用例

```bash
# 示例 1：投诉
"我买的智能手表才用了两天就坏了，屏幕闪烁，联系客服也没人回复，订单号是AB12345678，要求退款！"

# 示例 2：咨询
"请问你们的智能手表支持心率监测吗？电池能用多久？"

# 示例 3：故障
"APP登录不上去了，一直提示网络错误，但我网络是正常的。"

# 示例 4：建议
"建议增加一个睡眠分析功能，可以统计深睡浅睡时间。"
```

## 💡 核心演示点

### Pydantic AI 必要性

| 问题 | 不用 Pydantic AI | 用 Pydantic AI |
|------|-----------------|----------------|
| JSON 格式 | ❌ 可能无效 | ✅ 保证有效 |
| 字段名 | ❌ 可能不一致 | ✅ 强制匹配 |
| 类型 | ❌ 可能错误 | ✅ 自动验证 |
| 枚举值 | ❌ 可能 typo | ✅ 编译检查 |
| 错误发现 | ❌ 运行时 | ✅ 编译时 |

### Langfuse 追踪

- 每次 LLM 调用都有 trace ID
- 前端可以查看 call stack
- 显示 token 消耗、耗时
- 便于调试和优化

## 🔗 相关链接

- [Pydantic AI](https://ai.pydantic.dev/)
- [Langfuse](https://langfuse.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
