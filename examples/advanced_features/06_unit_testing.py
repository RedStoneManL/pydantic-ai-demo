"""
幻灯片 8: 核心 Feature V —— 真正的单元测试 (Unit Testing)

展示 Pydantic AI 的 TestModel 和 FunctionModel
"""

import asyncio
from typing import Optional
from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.test import TestModel, FunctionModel


# ============================================================
# 定义模型和 Agent
# ============================================================

@dataclass
class UserDeps:
    """用户依赖"""
    user_id: str
    is_vip: bool


class AnalysisResult(BaseModel):
    """分析结果"""
    category: str
    priority: str
    confidence: float = Field(ge=0.0, le=1.0)


# 创建 Agent
agent = Agent(
    "openai:gpt-4o-mini",
    output_type=AnalysisResult,
    deps_type=UserDeps,
    system_prompt="你是分析助手。",
)


@agent.tool
async def get_user_status(ctx: RunContext[UserDeps]) -> str:
    """获取用户状态"""
    return "vip" if ctx.deps.is_vip else "normal"


# ============================================================
# 痛点: 传统测试依赖真实 API
# ============================================================

def demo_traditional_testing():
    """传统测试方式的问题"""
    
    print("=" * 60)
    print("传统测试: 依赖真实 API")
    print("=" * 60)
    
    print("""
    async def test_analyze_ticket():
        # ❌ 必须调用真实 API
        result = await agent.run("用户输入")
        
        # 问题 1: 消耗 Token (烧钱)
        # 问题 2: 网络延迟 (慢)
        # 问题 3: 结果不稳定 (LLM 输出可能变化)
        # 问题 4: 无法测试边界情况
        
        assert result.output.category in ["complaint", "inquiry", ...]
    
    ❌ 后果:
    - CI/CD 流水线慢且贵
    - 测试不稳定
    - 重构时心惊胆战
    - 无法测试特定场景
    """)


# ============================================================
# Feature 1: TestModel —— 智能 Mock
# ============================================================

async def demo_test_model():
    """TestModel 自动生成 Mock 数据"""
    
    print("\n" + "=" * 60)
    print("Feature 1: TestModel (智能 Mock)")
    print("=" * 60)
    
    # 创建测试用的 Agent (使用 TestModel)
    test_agent = Agent(
        TestModel(),  # 🔑 关键: 使用 TestModel 替代真实 LLM
        output_type=AnalysisResult,
        deps_type=UserDeps,
    )
    
    # 运行测试
    deps = UserDeps(user_id="test_001", is_vip=True)
    result = await test_agent.run("测试输入", deps=deps)
    
    print(f"""
    # 创建测试 Agent
    test_agent = Agent(
        TestModel(),  # 🔑 不消耗 Token
        output_type=AnalysisResult,
    )
    
    # 运行测试
    result = await test_agent.run("测试输入", deps=deps)
    
    # TestModel 自动生成符合 Schema 的数据!
    result.output.category    # -> "c" (自动生成)
    result.output.priority    # -> "a" (自动生成)
    result.output.confidence  # -> 0.5 (自动生成)
    
    实际输出: {result.output}
    
    💡 价值:
    - 零 Token 消耗
    - 零网络延迟
    - 自动符合 Schema
    - 测试速度极快
    """)


# ============================================================
# Feature 2: FunctionModel —— 自定义 Mock 行为
# ============================================================

async def demo_function_model():
    """FunctionModel 允许自定义 Mock 行为"""
    
    print("\n" + "=" * 60)
    print("Feature 2: FunctionModel (自定义 Mock)")
    print("=" * 60)
    
    # 定义自定义 Mock 函数
    def custom_mock(messages, info):
        """自定义 Mock 逻辑"""
        # 可以根据输入返回不同的结果
        last_message = messages[-1] if messages else ""
        
        if "紧急" in str(last_message):
            return AnalysisResult(
                category="complaint",
                priority="high",
                confidence=0.95,
            )
        else:
            return AnalysisResult(
                category="inquiry",
                priority="low",
                confidence=0.7,
            )
    
    # 创建使用 FunctionModel 的 Agent
    test_agent = Agent(
        FunctionModel(custom_mock),  # 🔑 自定义 Mock
        output_type=AnalysisResult,
        deps_type=UserDeps,
    )
    
    # 测试场景 1: 紧急情况
    result1 = await test_agent.run("这是一个紧急问题")
    print(f"\n测试 1: 紧急输入")
    print(f"  输出: {result1.output}")
    
    # 测试场景 2: 普通情况
    result2 = await test_agent.run("普通咨询")
    print(f"\n测试 2: 普通输入")
    print(f"  输出: {result2.output}")
    
    print(f"""
    💡 价值:
    - 可以测试特定场景
    - 可以测试边界情况
    - 可以测试错误处理
    - 完全可控
    """)


# ============================================================
# Feature 3: 测试工具调用
# ============================================================

async def demo_test_tools():
    """测试工具调用逻辑"""
    
    print("\n" + "=" * 60)
    print("Feature 3: 测试工具调用")
    print("=" * 60)
    
    # 创建带工具的 Agent
    tool_agent = Agent(
        TestModel(),  # Mock LLM
        output_type=AnalysisResult,
        deps_type=UserDeps,
    )
    
    @tool_agent.tool
    async def check_inventory(ctx: RunContext[UserDeps], product_id: str) -> dict:
        """检查库存 (测试时会真正调用)"""
        # 这个逻辑会被真实执行!
        return {
            "product_id": product_id,
            "in_stock": True,
            "quantity": 100,
        }
    
    print("""
    创建带工具的测试 Agent:
    
    test_agent = Agent(TestModel(), ...)
    
    @test_agent.tool
    async def check_inventory(ctx, product_id):
        # 工具逻辑会被真实执行
        return {"in_stock": True, "quantity": 100}
    
    💡 价值:
    - 工具逻辑被真实测试
    - 不依赖 LLM 决策
    - 可以验证工具输出格式
    """)


# ============================================================
# Feature 4: 完整的测试示例
# ============================================================

async def demo_complete_test():
    """完整的单元测试示例"""
    
    print("\n" + "=" * 60)
    print("Feature 4: 完整测试示例")
    print("=" * 60)
    
    print("""
    # test_agent.py
    
    import pytest
    from pydantic_ai import Agent
    from pydantic_ai.models.test import TestModel, FunctionModel
    
    # 被测试的 Agent
    agent = Agent(
        "openai:gpt-4o-mini",
        output_type=AnalysisResult,
        deps_type=UserDeps,
    )
    
    # 测试 1: 基本功能
    async def test_basic_analysis():
        test_agent = agent.override(
            model=TestModel()
        )
        
        deps = UserDeps(user_id="test", is_vip=False)
        result = await test_agent.run("输入", deps=deps)
        
        assert isinstance(result.output, AnalysisResult)
        assert 0 <= result.output.confidence <= 1
    
    # 测试 2: VIP 用户行为
    async def test_vip_user():
        def vip_mock(messages, info):
            return AnalysisResult(
                category="inquiry",
                priority="high",  # VIP 优先
                confidence=0.9,
            )
        
        test_agent = agent.override(
            model=FunctionModel(vip_mock)
        )
        
        deps = UserDeps(user_id="vip", is_vip=True)
        result = await test_agent.run("输入", deps=deps)
        
        assert result.output.priority == "high"
    
    # 测试 3: 工具调用
    async def test_tool_call():
        tool_called = False
        
        @agent.tool
        async def test_tool(ctx, param: str):
            nonlocal tool_called
            tool_called = True
            return "result"
        
        test_agent = agent.override(model=TestModel())
        await test_agent.run("输入")
        
        # 验证工具是否被调用
        # (需要更复杂的设置)
    
    # 运行测试: pytest test_agent.py -v
    
    💡 价值:
    - 测试不消耗 Token
    - 测试速度快
    - 测试稳定
    - 可以测试任何场景
    """)


# ============================================================
# 总结
# ============================================================

def print_summary():
    """单元测试总结"""
    
    print("\n" + "=" * 60)
    print("单元测试总结")
    print("=" * 60)
    
    print("""
    Pydantic AI 测试能力:
    
    1. TestModel (智能 Mock)
       - 自动生成符合 Schema 的数据
       - 零 Token 消耗
       - 零网络延迟
       - 适合基本功能测试
    
    2. FunctionModel (自定义 Mock)
       - 自定义 Mock 逻辑
       - 可以测试特定场景
       - 可以测试边界情况
       - 适合复杂逻辑测试
    
    3. 工具测试
       - 工具逻辑被真实执行
       - 可以验证工具输出
       - 不依赖 LLM 决策
    
    4. 对比传统测试
    
       ┌────────────────┬──────────────┬──────────────┐
       │                │ 传统方式     │ Pydantic AI  │
       ├────────────────┼──────────────┼──────────────┤
       │ Token 消耗     │ 有 (烧钱)    │ 无           │
       │ 网络延迟       │ 有 (慢)      │ 无           │
       │ 结果稳定性     │ 不稳定       │ 完全稳定     │
       │ 边界测试       │ 困难         │ 容易         │
       │ CI/CD 友好     │ 否           │ 是           │
       └────────────────┴──────────────┴──────────────┘
    
    🎯 价值: 让测试 Agent 变得像测试普通函数一样简单
    """)


# ============================================================
# 运行演示
# ============================================================

async def main():
    demo_traditional_testing()
    await demo_test_model()
    await demo_function_model()
    await demo_test_tools()
    await demo_complete_test()
    print_summary()


if __name__ == "__main__":
    asyncio.run(main())
