"""
LangGraph + Pydantic AI 结合示例

基于 pydantic-ai-demo 工单分析场景

架构:
┌─────────────────────────────────────────────────────────────┐
│                    LangGraph (编排层)                        │
│                                                             │
│  ┌─────────┐   ┌──────────┐   ┌────────┐   ┌──────────┐    │
│  │ analyze │──▶│ enrich   │──▶│ respond│──▶| escalate │    │
│  │ (工单)  │   │ (补充)   │   │ (回复) │   │ (升级)   │    │
│  └─────────┘   └──────────┘   └────────┘   └──────────┘    │
│       │              │                          │          │
│       │         有订单号?                   需人工?        │
│       └──────────────┴──────────────────────────┘          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  Pydantic AI (执行层)                        │
│                                                             │
│  每个 Node 内部是一个 PydanticAI Agent:                     │
│  - 结构化输入/输出                                          │
│  - 自动类型校验                                             │
│  - 内置重试机制                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
"""

from typing import Annotated, Optional
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
import operator
import time

# 导入现有模型
from .models import TicketCategory, UrgencyLevel


# ============================================================
# Part 1: LangGraph 全局状态 (Pydantic 定义)
# ============================================================

class GraphState(BaseModel):
    """
    LangGraph 全局状态
    
    使用 Pydantic BaseModel 确保类型安全
    """
    # 原始用户输入
    user_input: str = Field(default="")
    
    # 解析后的工单信息 (来自 Pydantic AI)
    category: Optional[TicketCategory] = None
    urgency: Optional[UrgencyLevel] = None
    product: Optional[str] = None
    order_id: Optional[str] = None
    summary: Optional[str] = None
    confidence: float = 0.0
    
    # 补充信息
    order_status: Optional[str] = None
    order_product: Optional[str] = None
    
    # 生成的回复
    suggested_response: Optional[str] = None
    
    # 是否需要人工介入
    needs_escalation: bool = False
    escalation_reason: Optional[str] = None
    
    # 流程追踪
    messages: Annotated[list, add_messages] = Field(default_factory=list)
    current_node: str = Field(default="")
    iteration: Annotated[int, operator.add] = Field(default=0)


# ============================================================
# Part 2: Pydantic AI Agents (每个 Node 对应一个 Agent)
# ============================================================

# --- Agent 1: 工单分析 ---

class AnalyzeOutput(BaseModel):
    """工单分析结果"""
    category: TicketCategory = Field(description="工单分类")
    urgency: UrgencyLevel = Field(description="紧急程度")
    product: str = Field(description="产品名称", min_length=1)
    order_id: Optional[str] = Field(
        None, 
        pattern=r"^[A-Z]{2}\d{8}$",
        description="订单号（如果有）"
    )
    summary: str = Field(description="问题摘要", min_length=10)
    confidence: float = Field(description="置信度", ge=0.0, le=1.0)


analyze_agent = Agent(
    "openai:gpt-4o-mini",
    name="ticket_analyzer",
    output_type=AnalyzeOutput,
    system_prompt="""你是工单分析专家。
分析用户的问题描述，提取：
- category: complaint/inquiry/suggestion/bug/refund/other
- urgency: P0(紧急)/P1(高)/P2(中)/P3(低)
- product: 涉及的产品
- order_id: 订单号（格式如 AB12345678，没有则为 null）
- summary: 10-100字摘要
- confidence: 0-1 置信度"""
)


# --- Agent 2: 订单信息补充 ---

class EnrichInput(BaseModel):
    """补充信息输入"""
    order_id: str = Field(description="订单号")


class EnrichOutput(BaseModel):
    """补充信息输出"""
    order_status: str = Field(description="订单状态")
    order_product: str = Field(description="订单产品")
    days_since_order: int = Field(description="距下单天数", ge=0)


enrich_agent = Agent(
    "openai:gpt-4o-mini",
    name="order_enricher",
    output_type=EnrichOutput,
    system_prompt="""你是订单查询助手。
根据订单号，返回：
- order_status: 订单状态
- order_product: 订单产品
- days_since_order: 距下单天数

（实际场景中会调用真实数据库/API）"""
)


# --- Agent 3: 回复生成 ---

class RespondInput(BaseModel):
    """回复生成输入"""
    category: TicketCategory
    urgency: UrgencyLevel
    product: str
    summary: str
    order_status: Optional[str] = None


class RespondOutput(BaseModel):
    """回复生成输出"""
    response: str = Field(description="客服回复", min_length=20)
    tone: str = Field(description="语气: professional/friendly/apologetic")
    next_steps: list[str] = Field(description="后续步骤", min_length=1)


respond_agent = Agent(
    "openai:gpt-4o-mini",
    name="response_generator",
    output_type=RespondOutput,
    system_prompt="""你是客服回复撰写专家。
根据工单信息，生成：
- response: 专业、有同理心的回复（20-200字）
- tone: professional/friendly/apolothetic
- next_steps: 后续处理步骤列表"""
)


# --- Agent 4: 升级判断 ---

class EscalateInput(BaseModel):
    """升级判断输入"""
    category: TicketCategory
    urgency: UrgencyLevel
    confidence: float
    order_status: Optional[str] = None


class EscalateOutput(BaseModel):
    """升级判断输出"""
    needs_escalation: bool = Field(description="是否需要人工")
    reason: Optional[str] = Field(None, description="升级原因")
    priority: str = Field(description="优先级: low/medium/high")


escalate_agent = Agent(
    "openai:gpt-4o-mini",
    name="escalation_decider",
    output_type=EscalateOutput,
    system_prompt="""你是客服流程决策者。
判断是否需要人工介入：
- P0/P1 紧急 → 需要
- confidence < 0.7 → 需要
- 投诉类 + 订单问题 → 需要
其他情况自动处理。"""
)


# ============================================================
# Part 3: LangGraph Nodes (编排层调用 Pydantic AI)
# ============================================================

async def analyze_node(state: dict) -> dict:
    """
    Node 1: 工单分析
    
    LangGraph 调用 Pydantic AI Agent
    - 输入: 用户原始描述
    - 输出: 结构化工单信息 (AnalyzeOutput)
    """
    user_input = state["user_input"]
    
    # 调用 Pydantic AI Agent
    result = await analyze_agent.run(f"分析工单: {user_input}")
    output: AnalyzeOutput = result.data  # 类型安全!
    
    # 更新 LangGraph 状态
    return {
        "category": output.category,
        "urgency": output.urgency,
        "product": output.product,
        "order_id": output.order_id,
        "summary": output.summary,
        "confidence": output.confidence,
        "messages": [f"✅ 分析完成: {output.category.value} | {output.urgency.value} | 置信度 {output.confidence:.0%}"],
        "current_node": "analyze",
        "iteration": 1,
    }


async def enrich_node(state: dict) -> dict:
    """
    Node 2: 订单信息补充
    
    如果有订单号，查询补充信息
    """
    order_id = state.get("order_id")
    
    if not order_id:
        return {
            "messages": ["⏭️ 无订单号，跳过补充"],
            "current_node": "enrich",
            "iteration": 1,
        }
    
    # 调用 Pydantic AI Agent
    input_data = EnrichInput(order_id=order_id)
    result = await enrich_agent.run(f"查询订单: {input_data.order_id}")
    output: EnrichOutput = result.data
    
    return {
        "order_status": output.order_status,
        "order_product": output.order_product,
        "messages": [f"📦 订单信息: {output.order_status} | {output.order_product}"],
        "current_node": "enrich",
        "iteration": 1,
    }


async def respond_node(state: dict) -> dict:
    """
    Node 3: 生成回复
    
    根据工单信息生成客服回复
    """
    # 构造 Pydantic 输入（自动校验）
    input_data = RespondInput(
        category=state["category"],
        urgency=state["urgency"],
        product=state["product"],
        summary=state["summary"],
        order_status=state.get("order_status"),
    )
    
    # 调用 Agent
    prompt = f"""
    分类: {input_data.category.value}
    紧急: {input_data.urgency.value}
    产品: {input_data.product}
    摘要: {input_data.summary}
    订单状态: {input_data.order_status or '无'}
    """
    result = await respond_agent.run(prompt)
    output: RespondOutput = result.data
    
    return {
        "suggested_response": output.response,
        "messages": [f"💬 生成回复: {output.tone} | {len(output.next_steps)} 个后续步骤"],
        "current_node": "respond",
        "iteration": 1,
    }


async def escalate_node(state: dict) -> dict:
    """
    Node 4: 升级判断
    
    决定是否需要人工介入
    """
    input_data = EscalateInput(
        category=state["category"],
        urgency=state["urgency"],
        confidence=state["confidence"],
        order_status=state.get("order_status"),
    )
    
    prompt = f"""
    分类: {input_data.category.value}
    紧急: {input_data.urgency.value}
    置信度: {input_data.confidence}
    订单状态: {input_data.order_status or '无'}
    """
    result = await escalate_agent.run(prompt)
    output: EscalateOutput = result.data
    
    return {
        "needs_escalation": output.needs_escalation,
        "escalation_reason": output.reason,
        "messages": [f"{'🚨 升级人工' if output.needs_escalation else '✅ 自动处理'} | 优先级: {output.priority}"],
        "current_node": "escalate",
        "iteration": 1,
    }


# ============================================================
# Part 4: LangGraph 路由逻辑 (条件边)
# ============================================================

def should_enrich(state: dict) -> str:
    """
    条件边: 是否需要查询订单
    
    基于 Pydantic 校验后的 state 做决策
    """
    order_id = state.get("order_id")
    if order_id:
        return "enrich"
    return "respond"


# ============================================================
# Part 5: 构建 Graph
# ============================================================

def build_ticket_pipeline() -> StateGraph:
    """构建工单处理流水线"""
    
    # 使用 Pydantic schema 定义 Graph 状态
    graph = StateGraph(GraphState.model_json_schema())
    
    # 添加节点 (每个节点内部是 Pydantic AI Agent)
    graph.add_node("analyze", analyze_node)
    graph.add_node("enrich", enrich_node)
    graph.add_node("respond", respond_node)
    graph.add_node("escalate", escalate_node)
    
    # 入口
    graph.set_entry_point("analyze")
    
    # 条件边: analyze -> enrich (有订单) / respond (无订单)
    graph.add_conditional_edges(
        "analyze",
        should_enrich,
        {
            "enrich": "enrich",
            "respond": "respond",
        }
    )
    
    # 固定边
    graph.add_edge("enrich", "respond")
    graph.add_edge("respond", "escalate")
    graph.add_edge("escalate", END)
    
    return graph.compile()


# ============================================================
# Part 6: 运行示例
# ============================================================

async def process_ticket(user_input: str) -> dict:
    """
    处理工单的完整流程
    
    LangGraph 编排 + Pydantic AI 执行
    """
    app = build_ticket_pipeline()
    
    initial_state = {
        "user_input": user_input,
        "messages": [],
        "iteration": 0,
    }
    
    print("=" * 60)
    print(f"📥 输入: {user_input}")
    print("=" * 60)
    
    # 流式执行
    final_state = None
    async for event in app.astream(initial_state):
        for node_name, node_output in event.items():
            print(f"\n▶ {node_name}: {node_output.get('messages', [])}")
            final_state = node_output
    
    print("\n" + "=" * 60)
    print("📋 最终结果:")
    print(f"  分类: {final_state.get('category')}")
    print(f"  紧急: {final_state.get('urgency')}")
    print(f"  回复: {final_state.get('suggested_response')}")
    print(f"  升级: {final_state.get('needs_escalation')}")
    print("=" * 60)
    
    return final_state


if __name__ == "__main__":
    import asyncio
    
    # 测试用例
    test_cases = [
        "我买的智能手表 AB12345678 收到就坏了，要求退款！",
        "请问你们有儿童手表吗？想给孩子买个",
        "APP 闪退，登录不了，订单号 CD87654321",
    ]
    
    for case in test_cases:
        asyncio.run(process_ticket(case))
        print("\n")
