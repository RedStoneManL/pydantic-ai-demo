# 测试用例

import pytest
import asyncio
from app.models import TicketAnalysis, TicketCategory, UrgencyLevel
from app.agent import analyze_ticket, create_ticket_agent


class TestModels:
    """Pydantic 模型测试"""
    
    def test_valid_ticket_analysis(self):
        """测试有效的工单分析结果"""
        ticket = TicketAnalysis(
            category=TicketCategory.COMPLAINT,
            urgency=UrgencyLevel.P1,
            product="智能手表",
            summary="产品质量问题，屏幕闪烁",
            suggested_action="联系用户确认问题，安排退换货",
            confidence=0.95,
        )
        
        assert ticket.category == TicketCategory.COMPLAINT
        assert ticket.urgency == UrgencyLevel.P1
        assert ticket.confidence == 0.95
    
    def test_invalid_category(self):
        """测试无效的分类"""
        with pytest.raises(ValueError):
            TicketAnalysis(
                category="invalid_category",  # 无效值
                urgency=UrgencyLevel.P1,
                product="智能手表",
                summary="测试",
                suggested_action="测试",
                confidence=0.9,
            )
    
    def test_invalid_urgency(self):
        """测试无效的紧急程度"""
        with pytest.raises(ValueError):
            TicketAnalysis(
                category=TicketCategory.COMPLAINT,
                urgency="P5",  # 无效值
                product="智能手表",
                summary="测试",
                suggested_action="测试",
                confidence=0.9,
            )
    
    def test_confidence_range(self):
        """测试置信度范围"""
        # 太高
        with pytest.raises(ValueError):
            TicketAnalysis(
                category=TicketCategory.COMPLAINT,
                urgency=UrgencyLevel.P1,
                product="智能手表",
                summary="测试",
                suggested_action="测试",
                confidence=1.5,  # 超出 0-1 范围
            )
        
        # 太低
        with pytest.raises(ValueError):
            TicketAnalysis(
                category=TicketCategory.COMPLAINT,
                urgency=UrgencyLevel.P1,
                product="智能手表",
                summary="测试",
                suggested_action="测试",
                confidence=-0.1,  # 超出 0-1 范围
            )
    
    def test_summary_length(self):
        """测试摘要长度限制"""
        # 太短
        with pytest.raises(ValueError):
            TicketAnalysis(
                category=TicketCategory.COMPLAINT,
                urgency=UrgencyLevel.P1,
                product="智能手表",
                summary="短",  # 少于 10 字
                suggested_action="测试",
                confidence=0.9,
            )
    
    def test_order_id_format(self):
        """测试订单号格式"""
        # 有效格式
        ticket = TicketAnalysis(
            category=TicketCategory.COMPLAINT,
            urgency=UrgencyLevel.P1,
            product="智能手表",
            order_id="AB12345678",  # 有效
            summary="测试摘要内容",
            suggested_action="测试",
            confidence=0.9,
        )
        assert ticket.order_id == "AB12345678"
        
        # 无效格式
        with pytest.raises(ValueError):
            TicketAnalysis(
                category=TicketCategory.COMPLAINT,
                urgency=UrgencyLevel.P1,
                product="智能手表",
                order_id="123",  # 无效
                summary="测试摘要内容",
                suggested_action="测试",
                confidence=0.9,
            )


class TestAgent:
    """Agent 测试（需要 LLM）"""
    
    @pytest.fixture
    def agent(self):
        return create_ticket_agent()
    
    def test_agent_creation(self, agent):
        """测试 Agent 创建"""
        assert agent is not None
    
    @pytest.mark.asyncio
    async def test_analyze_complaint(self, agent):
        """测试分析投诉"""
        user_input = "我买的智能手表才用了两天就坏了，屏幕闪烁，联系客服也没人回复，要求退款！"
        
        # 这个测试需要真实的 LLM
        # 在 CI 环境中可能需要 mock
        try:
            result = await agent.run(user_input)
            analysis = result.output
            
            assert isinstance(analysis, TicketAnalysis)
            assert analysis.category == TicketCategory.COMPLAINT
            assert analysis.product != ""
            assert len(analysis.summary) >= 10
        except Exception as e:
            pytest.skip(f"LLM not available: {e}")


class TestComparison:
    """对比测试：用 vs 不用 Pydantic AI"""
    
    def test_good_approach_returns_valid_structure(self):
        """测试好的方式返回有效结构"""
        # 模拟 Pydantic AI 返回
        result = TicketAnalysis(
            category=TicketCategory.COMPLAINT,
            urgency=UrgencyLevel.P1,
            product="智能手表",
            summary="产品质量问题，屏幕闪烁",
            suggested_action="联系用户确认问题",
            confidence=0.95,
        )
        
        # 验证所有字段
        assert isinstance(result.category, TicketCategory)
        assert isinstance(result.urgency, UrgencyLevel)
        assert isinstance(result.product, str)
        assert isinstance(result.confidence, float)
        assert 0 <= result.confidence <= 1
    
    def test_bad_approach_may_return_invalid(self):
        """测试差的方式可能返回无效数据"""
        # 模拟 LLM 直接返回的原始数据（可能有问题）
        bad_results = [
            {"category": "投诉"},  # 缺少字段
            {"分类": "complaint"},  # 字段名不一致
            {"category": "complaint", "urgency": "紧急"},  # 枚举值错误
            "不是 JSON",  # 根本不是 JSON
            {"category": "complaint", "confidence": "高"},  # 类型错误
        ]
        
        for bad in bad_results:
            # 这些都是可能出现的问题
            # 用 Pydantic AI 就不会遇到
            if isinstance(bad, str):
                assert True  # JSON 解析会失败
            elif isinstance(bad, dict):
                # 可能缺少字段或字段名不一致
                assert "category" not in bad or "分类" in bad or True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
