# Pydantic AI Agent + Langfuse 集成

import os
from typing import Optional
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel

from .models import TicketAnalysis, TicketCategory, UrgencyLevel

# Langfuse 集成
try:
    from langfuse import Langfuse
    from langfuse.decorators import observe, langfuse_context
    HAS_LANGFUSE = True
except ImportError:
    HAS_LANGFUSE = False
    print("Warning: Langfuse not installed, tracing disabled")


# 初始化 Langfuse
def init_langfuse():
    """初始化 Langfuse 客户端"""
    if not HAS_LANGFUSE:
        return None
    
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
    
    if not public_key or not secret_key:
        print("Warning: Langfuse keys not set, tracing disabled")
        return None
    
    return Langfuse(
        public_key=public_key,
        secret_key=secret_key,
        host=host,
    )


# 全局 Langfuse 客户端
langfuse_client = init_langfuse()


# 创建 Pydantic AI Agent
def create_ticket_agent() -> Agent:
    """
    创建工单分析 Agent
    
    关键：output_type=TicketAnalysis 确保输出是结构化的
    """
    
    # 配置模型
    model = OpenAIModel(
        model_name=os.getenv("OPENAI_MODEL_NAME", "gpt-4o"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    agent = Agent(
        model,
        output_type=TicketAnalysis,  # 🔑 关键：结构化输出
        system_prompt="""你是一个专业的客服工单分析助手。

你的任务是分析用户的问题描述，提取结构化信息：

1. **分类** (category)：
   - complaint: 投诉（对服务/产品不满）
   - inquiry: 咨询（询问产品/服务信息）
   - suggestion: 建议（改进意见）
   - bug: 故障（产品功能异常）
   - refund: 退款（申请退款）
   - other: 其他

2. **紧急程度** (urgency)：
   - P0: 紧急，需要立即处理（如系统崩溃、资金问题）
   - P1: 高优先级（如功能无法使用）
   - P2: 中等优先级（如功能异常但有替代方案）
   - P3: 低优先级（如小问题、咨询）

3. **必填字段**：
   - category: 分类
   - urgency: 紧急程度
   - product: 产品名称
   - summary: 工单摘要（10-500字）
   - suggested_action: 建议处理方式
   - confidence: 置信度（0-1）

4. **可选字段**：
   - order_id: 订单号（格式如 AB12345678）
   - contact_phone: 联系电话
   - contact_email: 联系邮箱
   - key_issues: 关键问题列表

注意：
- 必须严格按照 TicketAnalysis 格式返回
- 所有枚举值必须精确匹配
- confidence 反映你对分类的确定程度
""",
    )
    
    @agent.tool
    async def get_current_time(ctx: RunContext) -> str:
        """获取当前时间（工具示例）"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    @agent.tool
    async def check_order_status(ctx: RunContext, order_id: str) -> dict:
        """查询订单状态（模拟）"""
        # 模拟数据库查询
        return {
            "order_id": order_id,
            "status": "delivered",
            "product": "智能手表",
            "created_at": "2024-01-15",
        }
    
    return agent


# 全局 Agent 实例
ticket_agent = create_ticket_agent()


@observe(name="analyze_ticket")
async def analyze_ticket_with_langfuse(
    user_input: str,
    context: Optional[dict] = None,
) -> tuple[TicketAnalysis, str]:
    """
    分析工单（带 Langfuse 追踪）
    
    Returns:
        (result, trace_id)
    """
    import time
    start_time = time.time()
    
    # 创建 Langfuse trace
    trace_id = None
    if langfuse_client:
        trace = langfuse_client.trace(
            name="ticket_analysis",
            metadata={"context": context},
        )
        trace_id = trace.id
        
        # 记录输入
        trace.event(
            name="user_input",
            output={"user_input": user_input},
        )
    
    # 调用 Pydantic AI Agent
    try:
        result = await ticket_agent.run(user_input)
        analysis = result.output
        
        # 记录输出
        if langfuse_client and trace_id:
            trace.event(
                name="analysis_result",
                output=analysis.model_dump(),
            )
            trace.event(
                name="duration_ms",
                output={"duration_ms": int((time.time() - start_time) * 1000)},
            )
        
        return analysis, trace_id
        
    except Exception as e:
        # 记录错误
        if langfuse_client and trace_id:
            trace.event(
                name="error",
                output={"error": str(e)},
            )
        raise


async def analyze_ticket(
    user_input: str,
    context: Optional[dict] = None,
) -> TicketAnalysis:
    """
    分析工单（不带追踪）
    
    简单版本，用于测试
    """
    result = await ticket_agent.run(user_input)
    return result.output
