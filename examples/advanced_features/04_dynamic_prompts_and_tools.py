"""
幻灯片 6: 核心 Feature III —— 动态提示词与工具挂载

展示 @agent.system_prompt 和 @agent.tool 的高级用法
"""

import asyncio
from typing import Optional
from dataclasses import dataclass
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext


# ============================================================
# 依赖定义
# ============================================================

@dataclass
class AppContext:
    """应用上下文"""
    user_id: str
    is_vip: bool
    language: str  # "zh" | "en"
    timezone: str
    current_time: datetime


# ============================================================
# 输出模型
# ============================================================

class AssistantResponse(BaseModel):
    """助手响应"""
    message: str
    actions: list[str] = Field(default_factory=list)
    language_used: str


# ============================================================
# 创建 Agent
# ============================================================

assistant = Agent(
    "openai:gpt-4o-mini",
    output_type=AssistantResponse,
    deps_type=AppContext,
)


# ============================================================
# Feature 1: 动态系统提示词
# ============================================================

@assistant.system_prompt
async def base_instructions(ctx: RunContext[AppContext]) -> str:
    """基础指令 (所有用户共享)"""
    return "你是一个智能助手，帮助用户解决问题。"


@assistant.system_prompt
async def user_specific_instructions(ctx: RunContext[AppContext]) -> str:
    """
    用户特定指令 (根据上下文动态生成)
    
    不同用户看到的提示词完全不同:
    - VIP 用户: 提供更多特权
    - 普通用户: 标准服务
    """
    deps = ctx.deps
    
    parts = []
    
    # 根据用户角色
    if deps.is_vip:
        parts.append("""
你是 VIP 专属助手。服务标准:
- 优先响应，语气亲切
- 可以提供专属折扣码
- 可以直接升级到人工客服
""")
    else:
        parts.append("""
你是标准助手。服务标准:
- 专业、友好
- 遵循标准处理流程
""")
    
    # 根据语言
    if deps.language == "zh":
        parts.append("请用中文回复用户。")
    else:
        parts.append("Please respond in English.")
    
    # 根据时区
    parts.append(f"\n当前时间: {deps.current_time.strftime('%Y-%m-%d %H:%M')} ({deps.timezone})")
    
    return "\n".join(parts)


@assistant.system_prompt
async def time_aware_instructions(ctx: RunContext[AppContext]) -> str:
    """
    时间感知指令
    
    根据当前时间动态调整行为
    """
    hour = ctx.deps.current_time.hour
    
    if 6 <= hour < 12:
        return "现在是上午，语气可以更积极。"
    elif 12 <= hour < 18:
        return "现在是下午，保持专业。"
    else:
        return "现在是晚上，语气可以更温和，注意用户可能疲劳。"


# ============================================================
# Feature 2: 优雅的工具挂载
# ============================================================

@assistant.tool
async def get_current_time(ctx: RunContext[AppContext]) -> str:
    """
    获取当前时间
    
    (工具描述会自动解析并传给 LLM)
    """
    return ctx.deps.current_time.isoformat()


@assistant.tool
async def get_user_profile(ctx: RunContext[AppContext]) -> dict:
    """
    获取用户资料
    
    自动从 ctx.deps 获取用户信息
    """
    return {
        "user_id": ctx.deps.user_id,
        "is_vip": ctx.deps.is_vip,
        "language": ctx.deps.language,
    }


@assistant.tool
async def generate_discount_code(
    ctx: RunContext[AppContext],
    discount_percent: int,
) -> str:
    """
    生成折扣码
    
    参数:
        discount_percent: 折扣百分比 (1-50)
    
    只有 VIP 用户可以使用此工具
    """
    if not ctx.deps.is_vip:
        return "错误: 只有 VIP 用户可以生成折扣码"
    
    # 模拟生成折扣码
    code = f"VIP{ctx.deps.user_id[:4]}{discount_percent}"
    return f"折扣码: {code} ({discount_percent}% off)"


@assistant.tool
async def translate_text(
    ctx: RunContext[AppContext],
    text: str,
    target_language: str,
) -> str:
    """
    翻译文本
    
    参数:
        text: 要翻译的文本
        target_language: 目标语言 (zh/en)
    """
    # 模拟翻译
    if target_language == "zh":
        return f"[翻译结果] {text}"
    else:
        return f"[Translation] {text}"


# ============================================================
# 演示: 动态提示词
# ============================================================

async def demo_dynamic_prompts():
    """演示动态系统提示词"""
    
    print("=" * 60)
    print("Feature 1: 动态系统提示词")
    print("=" * 60)
    
    # VIP 用户 (中文)
    vip_zh_context = AppContext(
        user_id="vip_001",
        is_vip=True,
        language="zh",
        timezone="Asia/Shanghai",
        current_time=datetime.now(timezone.utc),
    )
    
    # 普通用户 (英文)
    normal_en_context = AppContext(
        user_id="user_123",
        is_vip=False,
        language="en",
        timezone="America/New_York",
        current_time=datetime.now(timezone.utc),
    )
    
    print("""
    不同用户，不同系统提示词:
    
    用户 1: VIP + 中文
    ┌─────────────────────────────────────┐
    │ 你是 VIP 专属助手。服务标准:        │
    │ - 优先响应，语气亲切               │
    │ - 可以提供专属折扣码               │
    │ - 可以直接升级到人工客服           │
    │                                     │
    │ 请用中文回复用户。                 │
    │                                     │
    │ 当前时间: 2024-xx-xx (Asia/Shanghai)│
    └─────────────────────────────────────┘
    
    用户 2: 普通用户 + 英文
    ┌─────────────────────────────────────┐
    │ 你是标准助手。服务标准:            │
    │ - 专业、友好                       │
    │ - 遵循标准处理流程                 │
    │                                     │
    │ Please respond in English.          │
    │                                     │
    │ Current time: 2024-xx-xx (EST)      │
    └─────────────────────────────────────┘
    
    💡 价值:
    - 一套代码，多种行为
    - 个性化服务
    - 上下文感知
    """)


# ============================================================
# 演示: 工具自动 Schema 生成
# ============================================================

def demo_tool_schema():
    """演示工具的 JSON Schema 自动生成"""
    
    print("\n" + "=" * 60)
    print("Feature 2: 工具 Schema 自动生成")
    print("=" * 60)
    
    print("""
    定义工具时:
    
    @assistant.tool
    async def generate_discount_code(
        ctx: RunContext[AppContext],
        discount_percent: int,
    ) -> str:
        '''
        生成折扣码
        
        参数:
            discount_percent: 折扣百分比 (1-50)
        '''
        ...
    
    Pydantic AI 自动生成 JSON Schema:
    
    {
        "name": "generate_discount_code",
        "description": "生成折扣码\\n\\n参数:\\n    discount_percent: 折扣百分比 (1-50)",
        "parameters": {
            "type": "object",
            "properties": {
                "discount_percent": {
                    "type": "integer"
                }
            },
            "required": ["discount_percent"]
        }
    }
    
    💡 价值:
    - Docstring → Description
    - Type hints → JSON Schema
    - 自动校验参数类型
    - LLM 知道如何调用
    """)


# ============================================================
# 演示: 工具访问依赖
# ============================================================

def demo_tool_deps():
    """演示工具如何访问注入的依赖"""
    
    print("\n" + "=" * 60)
    print("Feature 3: 工具访问依赖")
    print("=" * 60)
    
    print("""
    工具可以直接访问 ctx.deps:
    
    @assistant.tool
    async def generate_discount_code(
        ctx: RunContext[AppContext],
        discount_percent: int,
    ) -> str:
        # 直接访问依赖
        if not ctx.deps.is_vip:
            return "错误: 只有 VIP 可以使用"
        
        user_id = ctx.deps.user_id
        code = f"VIP{user_id[:4]}{discount_percent}"
        return code
    
    运行时:
    
    result = await agent.run(
        "给我一个 20% 折扣码",
        deps=vip_context  # 注入依赖
    )
    
    # 工具内部可以访问 vip_context.is_vip, vip_context.user_id
    
    💡 价值:
    - 工具逻辑与依赖解耦
    - 测试时可以注入 Mock 依赖
    - 多租户场景自动隔离
    """)


# ============================================================
# 总结
# ============================================================

def print_summary():
    """总结"""
    
    print("\n" + "=" * 60)
    print("动态提示词与工具挂载总结")
    print("=" * 60)
    
    print("""
    Pydantic AI 的动态能力:
    
    1. 动态系统提示词
       - @agent.system_prompt 装饰器
       - 多个提示词函数会自动合并
       - 根据 ctx.deps 动态生成
       - 支持时间/用户/环境感知
    
    2. 工具自动 Schema
       - @agent.tool 装饰器
       - Docstring → Description
       - Type hints → JSON Schema
       - 参数自动校验
    
    3. 工具访问依赖
       - ctx.deps 直接访问注入的依赖
       - 无需全局变量
       - 测试友好
    
    🎯 价值: 
    - 一套代码，多种行为
    - 类型安全的工具调用
    - 高度可定制
    """)


# ============================================================
# 运行演示
# ============================================================

async def main():
    await demo_dynamic_prompts()
    demo_tool_schema()
    demo_tool_deps()
    print_summary()


if __name__ == "__main__":
    asyncio.run(main())
