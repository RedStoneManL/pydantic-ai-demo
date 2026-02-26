"""
幻灯片 2：当前 LLM 应用开发的痛点

这个文件展示传统 LLM 开发的四大痛点
"""

import json
import asyncio
from typing import Optional
from pydantic import BaseModel, Field, ValidationError

# ============================================================
# 痛点 1: 薛定谔的 JSON —— LLM 返回的 JSON 格式不可靠
# ============================================================

async def pain_point_1_schrodinger_json():
    """
    问题: 提示词越写越长，但 LLM 返回的 JSON 依然可能:
    - 少个字段
    - 类型错误 (age 是字符串而不是整数)
    - 格式完全崩坏
    """
    
    # 典型的提示词工程
    prompt = """
    你是一个客服工单分析助手。请分析以下用户输入，返回 JSON 格式:
    {
        "category": "complaint|inquiry|suggestion|bug|refund|other",
        "urgency": "P0|P1|P2|P3",
        "product": "产品名称",
        "order_id": "订单号（可选）",
        "summary": "问题摘要",
        "confidence": 0.0-1.0 之间的浮点数
    }
    
    重要: 
    1. category 必须是上述枚举值之一
    2. confidence 必须是数字，不是字符串
    3. order_id 格式为 2个大写字母+8位数字
    4. 不要返回任何其他内容，只返回 JSON
    """
    
    # 模拟 LLM 可能返回的各种"惊喜"
    bad_responses = [
        # 案例 1: 类型错误
        '{"category": "complaint", "urgency": "P1", "product": "手表", "confidence": "0.8"}',
        
        # 案例 2: 字段缺失
        '{"category": "inquiry", "urgency": "P2", "product": "手表"}',
        
        # 案例 3: 枚举值错误
        '{"category": "投诉", "urgency": "高", "product": "手表", "summary": "坏", "confidence": 0.9}',
        
        # 案例 4: 格式混乱
        '根据分析，这是一个投诉类工单...\n\n```json\n{"category": "complaint"}\n```',
        
        # 案例 5: 完全幻觉
        '{"category": "complaint", "urgency": "P0", "product": null, "summary": "", "confidence": 150}',
    ]
    
    print("=" * 60)
    print("痛点 1: 薛定谔的 JSON")
    print("=" * 60)
    
    for i, response in enumerate(bad_responses, 1):
        print(f"\n❌ 案例 {i}: LLM 返回")
        print(f"   {response[:80]}...")
        
        try:
            data = json.loads(response)
            print(f"   ✓ JSON 解析成功")
            print(f"   ✗ 但数据可能不合法: category={data.get('category')}, confidence={data.get('confidence')}")
        except json.JSONDecodeError:
            print(f"   ✗ JSON 解析失败!")
    
    print("\n💡 后果: 需要写大量防御性代码来处理各种边界情况")


# ============================================================
# 痛点 2: 意大利面条式的上下文
# ============================================================

# 全局变量满天飞 (反模式)
_db_connection = None
_api_key = None
_user_token = None
_cache = {}


def pain_point_2_spaghetti_context():
    """
    问题: 数据库连接、用户 Token、API Keys 在全局变量中满天飞
    """
    
    print("\n" + "=" * 60)
    print("痛点 2: 意大利面条式的上下文")
    print("=" * 60)
    
    # 全局变量导致的耦合问题
    global _db_connection, _api_key, _user_token
    
    def process_ticket(user_input: str):
        """需要访问全局变量"""
        # 依赖全局状态，难以测试
        if not _db_connection:
            raise Exception("数据库未连接")
        if not _api_key:
            raise Exception("API Key 未设置")
        # ... 业务逻辑
    
    def get_user_info(user_id: str):
        """又需要访问全局变量"""
        global _db_connection
        # _db_connection 从哪来？谁知道！
        pass
    
    def call_llm(prompt: str):
        """还是需要全局变量"""
        global _api_key
        # _api_key 又是全局的，难以替换
        pass
    
    print("""
    典型的反模式:
    
    _db_connection = ...  # 全局
    _api_key = ...        # 全局
    _user_token = ...     # 全局
    
    def process_ticket():
        if not _db_connection:  # 耦合全局状态
            ...
    
    def get_user_info():
        # _db_connection 从哪来？谁知道！
        ...
    
    💡 后果:
    - 代码高度耦合
    - 难以测试 (需要 mock 全局变量)
    - 多租户场景难以处理
    - 并发请求可能互相干扰
    """)


# ============================================================
# 痛点 3: 不可测试的黑盒
# ============================================================

def pain_point_3_untestable_blackbox():
    """
    问题: Agent 逻辑依赖真实 LLM API，测试缓慢、烧钱、不可靠
    """
    
    print("\n" + "=" * 60)
    print("痛点 3: 不可测试的黑盒")
    print("=" * 60)
    
    print("""
    传统测试方式:
    
    async def test_analyze_ticket():
        # 必须调用真实 API
        result = await openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[...]
        )
        # 问题:
        # 1. 消耗真实 Token (烧钱)
        # 2. 网络延迟 (慢)
        # 3. 结果不稳定 (LLM 输出可能变化)
        # 4. 无法测试边界情况 (如何模拟特定错误？)
    
    💡 后果:
    - CI/CD 流水线慢且贵
    - 测试覆盖率低
    - 重构时心惊胆战
    """)


# ============================================================
# 痛点 4: 繁琐的错误处理
# ============================================================

class TicketAnalysis(BaseModel):
    category: str
    urgency: str
    confidence: float


async def pain_point_4_manual_retry():
    """
    问题: 需要手写大量的重试和回退逻辑
    """
    
    print("\n" + "=" * 60)
    print("痛点 4: 繁琐的错误处理")
    print("=" * 60)
    
    async def parse_with_retry(llm_response: str, max_retries: int = 3):
        """手写重试逻辑"""
        for attempt in range(max_retries):
            try:
                data = json.loads(llm_response)
                result = TicketAnalysis(**data)
                return result
            except (json.JSONDecodeError, ValidationError) as e:
                if attempt < max_retries - 1:
                    # 手动构造重试提示
                    retry_prompt = f"""
                    之前的输出有错误: {e}
                    
                    请修正并重新返回正确的 JSON。
                    必须包含: category, urgency, confidence
                    confidence 必须是 0-1 的浮点数
                    """
                    # 重新调用 LLM... (需要维护上下文)
                    print(f"   重试 {attempt + 1}/{max_retries}: {e}")
                else:
                    raise
        
        return None
    
    print("""
    手写重试逻辑的痛苦:
    
    1. 捕获 JSON 解析错误
    2. 捕获 Pydantic 校验错误
    3. 构造重试提示词
    4. 维护对话上下文
    5. 设置最大重试次数
    6. 处理最终失败的情况
    7. ... 每个接口都要写一遍
    
    💡 后果:
    - 重复代码多
    - 容易遗漏边界情况
    - 难以统一错误处理策略
    """)


# ============================================================
# 运行演示
# ============================================================

async def main():
    """展示所有痛点"""
    await pain_point_1_schrodinger_json()
    pain_point_2_spaghetti_context()
    pain_point_3_untestable_blackbox()
    await pain_point_4_manual_retry()
    
    print("\n" + "=" * 60)
    print("总结: 这些痛点导致了 LLM 应用开发效率低下")
    print("解决方案: Pydantic AI 🎯")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
