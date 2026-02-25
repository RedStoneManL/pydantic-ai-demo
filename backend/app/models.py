# Pydantic 模型定义

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from enum import Enum


class TicketCategory(str, Enum):
    """工单分类"""
    COMPLAINT = "complaint"      # 投诉
    INQUIRY = "inquiry"          # 咨询
    SUGGESTION = "suggestion"    # 建议
    BUG = "bug"                  # 故障
    REFUND = "refund"            # 退款
    OTHER = "other"              # 其他


class UrgencyLevel(str, Enum):
    """紧急程度"""
    P0 = "P0"  # 紧急，需要立即处理
    P1 = "P1"  # 高优先级
    P2 = "P2"  # 中等优先级
    P3 = "P3"  # 低优先级


class TicketAnalysis(BaseModel):
    """
    工单分析结果 - Pydantic AI 结构化输出
    
    所有字段都有严格的类型和验证
    """
    # 分类（必填，枚举值）
    category: TicketCategory = Field(
        ...,
        description="工单分类"
    )
    
    # 紧急程度（必填，枚举值）
    urgency: UrgencyLevel = Field(
        ...,
        description="紧急程度 P0-P3"
    )
    
    # 产品名称（必填）
    product: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="涉及的产品名称"
    )
    
    # 订单号（可选）
    order_id: Optional[str] = Field(
        None,
        pattern=r"^[A-Z]{2}\d{8}$",
        description="订单号，格式如 AB12345678"
    )
    
    # 联系方式
    contact_phone: Optional[str] = Field(
        None,
        description="联系电话"
    )
    
    contact_email: Optional[str] = Field(
        None,
        description="联系邮箱"
    )
    
    # 摘要（必填）
    summary: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="工单摘要，10-500字"
    )
    
    # 关键问题列表
    key_issues: List[str] = Field(
        default_factory=list,
        description="关键问题列表"
    )
    
    # 建议处理方式
    suggested_action: str = Field(
        ...,
        description="建议处理方式"
    )
    
    # 置信度（0-1）
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="分类置信度，0-1之间"
    )
    
    @field_validator('contact_phone')
    @classmethod
    def validate_phone(cls, v):
        if v is None:
            return v
        # 简单验证：只保留数字
        digits = ''.join(c for c in v if c.isdigit())
        if len(digits) < 10 or len(digits) > 15:
            raise ValueError(f"无效的电话号码: {v}")
        return v
    
    @field_validator('contact_email')
    @classmethod
    def validate_email(cls, v):
        if v is None:
            return v
        if '@' not in v:
            raise ValueError(f"无效的邮箱地址: {v}")
        return v


class TicketAnalysisRequest(BaseModel):
    """API 请求"""
    user_input: str = Field(..., description="用户输入的问题描述")
    context: Optional[dict] = Field(default=None, description="额外上下文")


class TicketAnalysisResponse(BaseModel):
    """API 响应"""
    success: bool
    status: str  # "success" | "validation_error" | "llm_error"
    
    # 成功时的结果
    result: Optional[TicketAnalysis] = None
    
    # 错误信息
    error: Optional[str] = None
    validation_errors: Optional[List[str]] = None
    
    # Langfuse trace ID
    trace_id: Optional[str] = None
    
    # 耗时
    duration_ms: int = 0
