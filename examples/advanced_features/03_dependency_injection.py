"""
幻灯片 5: 核心 Feature II —— 依赖注入机制 (Dependency Injection)

展示 Pydantic AI 的 RunContext 依赖注入
"""

import asyncio
from typing import Optional, Annotated
from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext, Depends


# ============================================================
# 对比: 传统方式 vs 依赖注入
# ============================================================

print("=" * 60)
print("传统方式: 全局变量 (反模式)")
print("=" * 60)

# ❌ 反模式: 全局变量
_db_connection_global = {"connected": True}
_api_key_global = "sk-xxx"
_user_id_global = "user_123"


def bad_approach():
    """传统方式: 依赖全局变量"""
    
    def get_user_info():
        # 从全局变量获取，难以测试，难以替换
        global _db_connection_global, _user_id_global
        return f"User {_user_id_global} from DB"
    
    def call_external_api():
        global _api_key_global
        return f"Calling API with {_api_key_global}"
    
    print("""
    ❌ 反模式:
    
    _db = ...  # 全局
    _api_key = ...  # 全局
    
    def get_user_info():
        global _db  # 耦合全局状态
        ...
    
    问题:
    1. 难以测试 (需要 mock 全局变量)
    2. 多租户难以处理
    3. 并发请求可能冲突
    4. 依赖关系不明确
    """)


# ============================================================
# Pydantic AI 方式: 依赖注入
# ============================================================

@dataclass
class UserContext:
    """
    用户上下文 (依赖)
    
    包含当前请求所需的所有依赖:
    - 用户信息
    - 数据库连接
    - API Keys
    - 配置项
    """
    user_id: str
    user_role: str  # "vip" | "normal" | "admin"
    db_connection: dict
    api_key: str
    request_id: str


@dataclass
class OrderContext:
    """订单上下文 (另一种依赖)"""
    order_id: str
    user_id: str
    db_connection: dict


# ============================================================
# 定义输出模型
# ============================================================

class SupportResponse(BaseModel):
    """客服响应"""
    message: str = Field(description="回复内容")
    tone: str = Field(description="语气: professional/friendly")
    escalated: bool = Field(default=False, description="是否升级")
    vip_perks: Optional[str] = Field(None, description="VIP 特权说明")


class OrderStatus(BaseModel):
    """订单状态"""
    order_id: str
    status: str
    can_refund: bool
    estimated_delivery: Optional[str] = None


# ============================================================
# 创建 Agent (使用依赖注入)
# ============================================================

support_agent = Agent(
    "openai:gpt-4o-mini",
    output_type=SupportResponse,
    deps_type=UserContext,  # 🔑 关键: 指定依赖类型
    system_prompt="""你是客服助手。根据用户角色提供相应服务。""",
)


# ============================================================
# 动态系统提示词 (使用依赖)
# ============================================================

@support_agent.system_prompt
async def dynamic_system_prompt(ctx: RunContext[UserContext]) -> str:
    """
    动态系统提示词
    
    根据 ctx.deps 中的用户信息，动态生成不同的提示词
    """
    deps = ctx.deps
    
    if deps.user_role == "vip":
        return f"""你是专属 VIP 客服。

当前用户: {deps.user_id} (VIP)
请求ID: {deps.request_id}

服务标准:
- 优先响应，语气亲切
- 可以提供额外优惠
- 问题复杂时可直接升级到高级客服
"""
    
    elif deps.user_role == "admin":
        return f"""你是管理员支持助手。

当前用户: {deps.user_id} (管理员)
请求ID: {deps.request_id}

服务标准:
- 提供技术细节
- 可以执行管理操作
- 直接报告系统状态
"""
    
    else:
        return f"""你是标准客服助手。

当前用户: {deps.user_id}
请求ID: {deps.request_id}

服务标准:
- 专业、友好
- 标准处理流程
"""


# ============================================================
# 工具挂载 (使用依赖)
# ============================================================

@support_agent.tool
async def get_user_orders(ctx: RunContext[UserContext]) -> list[str]:
    """
    获取用户订单列表
    
    自动从 ctx.deps 获取数据库连接
    """
    db = ctx.deps.db_connection
    user_id = ctx.deps.user_id
    
    # 模拟数据库查询
    print(f"   [Tool] 查询用户订单: {user_id}")
    return ["ORD001", "ORD002", "ORD003"]


@support_agent.tool
async def check_vip_status(ctx: RunContext[UserContext]) -> dict:
    """
    检查 VIP 状态
    
    根据 ctx.deps.user_role 返回不同结果
    """
    role = ctx.deps.user_role
    
    if role == "vip":
        return {
            "is_vip": True,
            "level": "gold",
            "perks": ["优先客服", "专属折扣", "免费退换"],
        }
    else:
        return {
            "is_vip": False,
            "level": None,
            "perks": [],
        }


@support_agent.tool
async def escalate_to_human(ctx: RunContext[UserContext], reason: str) -> str:
    """
    升级到人工客服
    
    使用 ctx.deps.request_id 追踪请求
    """
    request_id = ctx.deps.request_id
    user_id = ctx.deps.user_id
    
    print(f"   [Tool] 升级请求: {request_id}, 用户: {user_id}, 原因: {reason}")
    return f"已升级，请求ID: {request_id}"


# ============================================================
# 演示: 不同用户角色，不同行为
# ============================================================

async def demo_different_users():
    """演示不同用户角色的不同行为"""
    
    print("\n" + "=" * 60)
    print("演示: 依赖注入实现多租户")
    print("=" * 60)
    
    # 模拟数据库
    mock_db = {"connected": True}
    
    # 用户 1: VIP
    vip_context = UserContext(
        user_id="vip_001",
        user_role="vip",
        db_connection=mock_db,
        api_key="vip-api-key",
        request_id="req_vip_001",
    )
    
    # 用户 2: 普通用户
    normal_context = UserContext(
        user_id="user_123",
        user_role="normal",
        db_connection=mock_db,
        api_key="normal-api-key",
        request_id="req_normal_001",
    )
    
    # 用户 3: 管理员
    admin_context = UserContext(
        user_id="admin_001",
        user_role="admin",
        db_connection=mock_db,
        api_key="admin-api-key",
        request_id="req_admin_001",
    )
    
    print("""
    创建三个不同用户上下文:
    
    1. VIP 用户: vip_001
    2. 普通用户: user_123
    3. 管理员: admin_001
    
    Agent 会根据不同上下文生成不同的系统提示词和行为
    """)


# ============================================================
# 演示: 依赖注入的可测试性
# ============================================================

def demo_testability():
    """演示依赖注入带来的可测试性"""
    
    print("\n" + "=" * 60)
    print("演示: 依赖注入的可测试性")
    print("=" * 60)
    
    print("""
    测试时可以轻松注入 Mock 依赖:
    
    # 生产环境
    prod_context = UserContext(
        user_id="real_user",
        db_connection=real_db,  # 真实数据库
        api_key=real_key,
    )
    
    # 测试环境
    test_context = UserContext(
        user_id="test_user",
        db_connection=mock_db,  # Mock 数据库
        api_key="test_key",
    )
    
    # 同一个 Agent，不同依赖
    result = await support_agent.run("帮我查订单", deps=test_context)
    
    💡 价值:
    - 不需要 mock 全局变量
    - 不需要修改 Agent 代码
    - 测试和生产使用同一套逻辑
    """)


# ============================================================
# 总结
# ============================================================

def print_summary():
    """依赖注入总结"""
    
    print("\n" + "=" * 60)
    print("依赖注入总结")
    print("=" * 60)
    
    print("""
    Pydantic AI 依赖注入的核心:
    
    1. 定义依赖类型
       @dataclass
       class UserContext:
           user_id: str
           db_connection: dict
           api_key: str
    
    2. Agent 指定依赖类型
       agent = Agent(
           deps_type=UserContext,  # 🔑
       )
    
    3. 系统提示词使用依赖
       @agent.system_prompt
       async def prompt(ctx: RunContext[UserContext]):
           return f"用户: {ctx.deps.user_id}"
    
    4. 工具使用依赖
       @agent.tool
       async def query_db(ctx: RunContext[UserContext]):
           db = ctx.deps.db_connection  # 自动注入
           ...
    
    5. 运行时传入依赖
       result = await agent.run("...", deps=user_context)
    
    🎯 价值:
    - 高内聚低耦合
    - 易于测试
    - 多租户友好
    - 依赖关系清晰
    """)


# ============================================================
# 运行演示
# ============================================================

async def main():
    bad_approach()
    await demo_different_users()
    demo_testability()
    print_summary()


if __name__ == "__main__":
    asyncio.run(main())
