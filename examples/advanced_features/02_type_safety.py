"""
幻灯片 4: 核心 Feature I —— 端到端的极致类型安全 (Type Safety)

展示 Pydantic AI 的类型安全特性
"""

import asyncio
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext


# ============================================================
# 定义强类型的输入/输出模型
# ============================================================

class TicketCategory(str, Enum):
    """工单分类 (枚举确保值的有效性)"""
    COMPLAINT = "complaint"
    INQUIRY = "inquiry"
    SUGGESTION = "suggestion"
    BUG = "bug"
    REFUND = "refund"
    OTHER = "other"


class UrgencyLevel(str, Enum):
    """紧急程度 (枚举 + 校验)"""
    P0 = "P0"  # 紧急
    P1 = "P1"  # 高
    P2 = "P2"  # 中
    P3 = "P3"  # 低


class TicketAnalysis(BaseModel):
    """
    结构化输出模型
    
    所有字段都有严格的类型约束:
    - 枚举值限制可选范围
    - Field() 定义约束条件
    - Optional 明确可选性
    """
    category: TicketCategory = Field(
        description="工单分类，必须是枚举值之一"
    )
    
    urgency: UrgencyLevel = Field(
        description="紧急程度 P0-P3"
    )
    
    product: str = Field(
        min_length=1,
        max_length=100,
        description="产品名称，1-100字符"
    )
    
    order_id: Optional[str] = Field(
        None,
        pattern=r"^[A-Z]{2}\d{8}$",
        description="订单号，格式 AB12345678"
    )
    
    summary: str = Field(
        min_length=10,
        max_length=500,
        description="问题摘要，10-500字符"
    )
    
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="置信度，0-1之间"
    )
    
    key_issues: list[str] = Field(
        default_factory=list,
        description="关键问题列表"
    )


# ============================================================
# 创建 Pydantic AI Agent (类型安全核心)
# ============================================================

agent = Agent(
    "openai:gpt-4o-mini",
    output_type=TicketAnalysis,  # 🔑 关键: 指定输出类型
    system_prompt="""你是工单分析专家。分析用户输入，返回结构化信息。
    
    注意:
    - category 必须是: complaint/inquiry/suggestion/bug/refund/other
    - urgency 必须是: P0/P1/P2/P3
    - confidence 必须是 0-1 之间的浮点数
    """,
)


# ============================================================
# 类型安全演示 1: IDE 自动补全
# ============================================================

def demo_ide_autocomplete():
    """
    IDE 完美护航:
    - 参数补全
    - 方法提示
    - 类型检查
    """
    
    print("=" * 60)
    print("Feature 1: IDE 自动补全与类型提示")
    print("=" * 60)
    
    # 创建实例时，IDE 知道所有字段
    analysis = TicketAnalysis(
        category=TicketCategory.COMPLAINT,  # IDE 会提示所有枚举值
        urgency=UrgencyLevel.P1,
        product="智能手表",
        summary="收到的手表无法开机",
        confidence=0.95,
    )
    
    # 访问字段时，IDE 知道类型
    # analysis.category  -> IDE 知道是 TicketCategory
    # analysis.confidence -> IDE 知道是 float
    
    print(f"""
    ✅ IDE 完整支持:
    
    analysis = TicketAnalysis(
        category=TicketCategory.COMPLAINT,  # 枚举值自动补全
        urgency=UrgencyLevel.P1,            # 枚举值自动补全
        product="智能手表",                  # str 类型
        summary="...",                       # str 类型
        confidence=0.95,                     # float 类型
    )
    
    # 访问字段时，IDE 知道确切类型
    analysis.category    # -> TicketCategory (不是 str!)
    analysis.confidence  # -> float
    analysis.order_id    # -> Optional[str]
    """)


# ============================================================
# 类型安全演示 2: 静态类型检查
# ============================================================

def demo_static_type_checking():
    """
    MyPy/Pyright 静态检查
    
    如果把 TicketAnalysis 当成其他类型使用，运行前就会报错
    """
    
    print("\n" + "=" * 60)
    print("Feature 2: 静态类型检查 (MyPy/Pyright)")
    print("=" * 60)
    
    # 这段代码在静态检查时会报错 (注释掉以避免运行时错误)
    
    # analysis: TicketAnalysis = analyze_ticket("...")
    
    # ❌ 类型错误: 尝试把 TicketAnalysis 当成 dict
    # analysis["category"]  # MyPy/Pyright 会报错
    
    # ❌ 类型错误: 尝试访问不存在的字段
    # analysis.unknown_field  # MyPy/Pyright 会报错
    
    # ❌ 类型错误: 尝试把 TicketAnalysis 赋值给不兼容类型
    # wrong: str = analysis  # MyPy/Pyright 会报错
    
    print("""
    静态检查会捕获这些错误:
    
    analysis: TicketAnalysis = ...
    
    # ❌ 类型错误: TicketAnalysis 不是 dict
    analysis["category"]
    
    # ❌ 类型错误: 没有 unknown_field 属性
    analysis.unknown_field
    
    # ❌ 类型错误: 不能把 TicketAnalysis 赋值给 str
    wrong: str = analysis
    
    💡 价值: 代码在运行前就会被检查，避免运行时崩溃
    """)


# ============================================================
# 类型安全演示 3: 运行时校验
# ============================================================

def demo_runtime_validation():
    """
    Pydantic 在运行时自动校验数据
    """
    
    print("\n" + "=" * 60)
    print("Feature 3: 运行时自动校验")
    print("=" * 60)
    
    # ✅ 合法数据
    valid_data = {
        "category": "complaint",
        "urgency": "P1",
        "product": "手表",
        "summary": "问题摘要...",
        "confidence": 0.9,
    }
    
    try:
        result = TicketAnalysis(**valid_data)
        print(f"✅ 合法数据: {result.category}, {result.urgency}")
    except Exception as e:
        print(f"❌ 校验失败: {e}")
    
    # ❌ 类型错误: confidence 是字符串
    invalid_data_1 = {
        "category": "complaint",
        "urgency": "P1",
        "product": "手表",
        "summary": "问题摘要...",
        "confidence": "high",  # 应该是 float
    }
    
    print("\n❌ 案例 1: confidence 类型错误")
    try:
        result = TicketAnalysis(**invalid_data_1)
    except Exception as e:
        print(f"   校验失败: {e}")
    
    # ❌ 范围错误: confidence > 1
    invalid_data_2 = {
        "category": "complaint",
        "urgency": "P1",
        "product": "手表",
        "summary": "问题摘要...",
        "confidence": 1.5,  # 超过 1.0
    }
    
    print("\n❌ 案例 2: confidence 超出范围")
    try:
        result = TicketAnalysis(**invalid_data_2)
    except Exception as e:
        print(f"   校验失败: {e}")
    
    # ❌ 枚举错误: category 不在枚举中
    invalid_data_3 = {
        "category": "投诉",  # 应该是英文枚举值
        "urgency": "P1",
        "product": "手表",
        "summary": "问题摘要...",
        "confidence": 0.9,
    }
    
    print("\n❌ 案例 3: category 不是有效枚举值")
    try:
        result = TicketAnalysis(**invalid_data_3)
    except Exception as e:
        print(f"   校验失败: {e}")
    
    # ❌ 格式错误: order_id 格式不对
    invalid_data_4 = {
        "category": "complaint",
        "urgency": "P1",
        "product": "手表",
        "summary": "问题摘要...",
        "confidence": 0.9,
        "order_id": "123",  # 应该是 AB12345678 格式
    }
    
    print("\n❌ 案例 4: order_id 格式错误")
    try:
        result = TicketAnalysis(**invalid_data_4)
    except Exception as e:
        print(f"   校验失败: {e}")


# ============================================================
# 类型安全演示 4: Agent 输出保证
# ============================================================

async def demo_agent_output_guarantee():
    """
    Pydantic AI Agent 的输出保证是正确类型
    """
    
    print("\n" + "=" * 60)
    print("Feature 4: Agent 输出类型保证")
    print("=" * 60)
    
    # 调用 Agent
    # result.output 保证是 TicketAnalysis 类型
    # 如果 LLM 返回不符合的数据，会自动重试
    
    print("""
    agent = Agent(
        "openai:gpt-4o-mini",
        output_type=TicketAnalysis,  # 🔑 关键
    )
    
    result = await agent.run("我买的手表坏了")
    
    # result.output 保证是 TicketAnalysis 类型!
    # 不可能是 dict, str, 或其他类型
    output: TicketAnalysis = result.output
    
    # IDE 知道 output 的所有字段和类型
    output.category     # TicketCategory (枚举)
    output.urgency      # UrgencyLevel (枚举)
    output.confidence   # float (0-1)
    output.order_id     # Optional[str]
    
    💡 价值: 从 LLM 的不确定性到 Python 的确定性
    """)


# ============================================================
# 总结
# ============================================================

def print_summary():
    """类型安全总结"""
    
    print("\n" + "=" * 60)
    print("类型安全总结")
    print("=" * 60)
    
    print("""
    Pydantic AI 类型安全的四个层次:
    
    1. 定义时 (Definition Time)
       - BaseModel + Field 定义约束
       - Enum 限制取值范围
       - Optional 明确可选性
    
    2. 编码时 (Coding Time)
       - IDE 自动补全
       - 类型提示
       - 实时错误检查
    
    3. 编译时 (Compile Time)
       - MyPy/Pyright 静态分析
       - 类型不匹配在运行前被发现
    
    4. 运行时 (Runtime)
       - Pydantic 自动校验
       - 数据不符合 Schema → ValidationError
       - Agent 输出保证类型正确
    
    🎯 结果: LLM 的不确定性被关进了类型安全的笼子
    """)


# ============================================================
# 运行演示
# ============================================================

async def main():
    demo_ide_autocomplete()
    demo_static_type_checking()
    demo_runtime_validation()
    await demo_agent_output_guarantee()
    print_summary()


if __name__ == "__main__":
    asyncio.run(main())
