# FastAPI 端点

import time
import json
import asyncio
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from .models import (
    TicketAnalysis,
    TicketAnalysisRequest,
    TicketAnalysisResponse,
)
from .agent import analyze_ticket_with_langfuse, analyze_ticket

app = FastAPI(
    title="智能客服工单系统 Demo",
    description="展示 Pydantic AI 的必要性 + Langfuse 追踪",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# 方式 1：不用 Pydantic AI（展示问题）
# ============================================================

async def analyze_ticket_bad(user_input: str) -> dict:
    """
    ❌ 不用 Pydantic AI 的方式
    
    问题：
    1. LLM 可能返回格式不对的 JSON
    2. 字段名可能不一致
    3. 没有类型验证
    4. 错误只能在运行时发现
    """
    import openai
    
    client = openai.OpenAI(
        api_key="sk-xxx",
        base_url="http://100.102.191.165:1025/v1",
    )
    
    prompt = f"""
    分析以下客服工单，返回 JSON 格式：
    
    用户输入：{user_input}
    
    返回格式：
    {{
        "category": "complaint/inquiry/suggestion/bug/refund/other",
        "urgency": "P0/P1/P2/P3",
        "product": "产品名称",
        "summary": "工单摘要"
    }}
    """
    
    response = client.chat.completions.create(
        model="GLM-4.7-w8a8",
        messages=[{"role": "user", "content": prompt}],
    )
    
    raw_output = response.choices[0].message.content
    
    # 问题 1：可能不是有效 JSON
    try:
        result = json.loads(raw_output)
    except json.JSONDecodeError:
        # 尝试提取 JSON
        import re
        match = re.search(r'\{.*\}', raw_output, re.DOTALL)
        if match:
            try:
                result = json.loads(match.group())
            except:
                return {"error": "无法解析 JSON", "raw": raw_output}
        else:
            return {"error": "没有找到 JSON", "raw": raw_output}
    
    # 问题 2：字段名可能不一致
    category = result.get("category") or result.get("分类") or result.get("type")
    
    # 问题 3：没有验证值是否合法
    # urgency 可能是 "高" 而不是 "P1"
    
    # 问题 4：类型不安全
    # confidence 可能是字符串 "高" 而不是 float
    
    return result


@app.post("/api/ticket/analyze-bad", response_model=dict)
async def api_analyze_bad(request: TicketAnalysisRequest):
    """
    ❌ 不用 Pydantic AI（展示问题）
    
    可能遇到的问题：
    - JSON 解析失败
    - 字段名不一致
    - 值不在枚举范围内
    - 类型错误
    """
    try:
        result = await analyze_ticket_bad(request.user_input)
        return {
            "success": True,
            "result": result,
            "warning": "这种方式不可靠，可能出现各种问题"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "demonstration": "这就是不用 Pydantic AI 的问题"
        }


# ============================================================
# 方式 2：用 Pydantic AI（正确方式）
# ============================================================

@app.post("/api/ticket/analyze", response_model=TicketAnalysisResponse)
async def api_analyze(request: TicketAnalysisRequest):
    """
    ✅ 用 Pydantic AI（正确方式）
    
    优势：
    - 结构化输出保证
    - 类型安全
    - 自动验证
    - Langfuse 追踪
    """
    start_time = time.time()
    
    try:
        # 调用 Agent（带 Langfuse 追踪）
        analysis, trace_id = await analyze_ticket_with_langfuse(
            user_input=request.user_input,
            context=request.context,
        )
        
        return TicketAnalysisResponse(
            success=True,
            status="success",
            result=analysis,
            trace_id=trace_id,
            duration_ms=int((time.time() - start_time) * 1000),
        )
        
    except ValidationError as e:
        # Pydantic 验证错误
        return TicketAnalysisResponse(
            success=False,
            status="validation_error",
            error="输出验证失败",
            validation_errors=[str(err) for err in e.errors()],
            duration_ms=int((time.time() - start_time) * 1000),
        )
        
    except Exception as e:
        # LLM 调用错误
        return TicketAnalysisResponse(
            success=False,
            status="llm_error",
            error=str(e),
            duration_ms=int((time.time() - start_time) * 1000),
        )


# ============================================================
# Langfuse Trace 查询
# ============================================================

@app.get("/api/trace/{trace_id}")
async def get_trace(trace_id: str):
    """
    获取 Langfuse Trace 详情
    
    前端用这个接口展示 call stack
    """
    from .agent import langfuse_client
    
    if not langfuse_client:
        raise HTTPException(503, "Langfuse not configured")
    
    try:
        # 获取 trace
        trace = langfuse_client.get_trace(trace_id)
        return trace
        
    except Exception as e:
        raise HTTPException(404, f"Trace not found: {e}")


@app.get("/api/traces")
async def list_traces(limit: int = 10):
    """获取最近的 traces"""
    from .agent import langfuse_client
    
    if not langfuse_client:
        raise HTTPException(503, "Langfuse not configured")
    
    try:
        traces = langfuse_client.get_traces(limit=limit)
        return traces
    except Exception as e:
        raise HTTPException(500, str(e))


# ============================================================
# 对比演示
# ============================================================

@app.post("/api/ticket/compare")
async def api_compare(request: TicketAnalysisRequest):
    """
    对比演示：同一输入，两种方式的结果
    
    展示 Pydantic AI 的必要性
    """
    import asyncio
    
    # 并行执行两种方式
    bad_task = asyncio.create_task(analyze_ticket_bad(request.user_input))
    good_task = asyncio.create_task(analyze_ticket(request.user_input))
    
    bad_result, good_analysis = await asyncio.gather(
        bad_task, good_task, return_exceptions=True
    )
    
    return {
        "input": request.user_input,
        "bad_approach": {
            "method": "直接调用 LLM，手动解析 JSON",
            "result": bad_result if not isinstance(bad_result, Exception) else {"error": str(bad_result)},
            "problems": [
                "❌ JSON 格式可能无效",
                "❌ 字段名可能不一致",
                "❌ 没有类型验证",
                "❌ 枚举值可能错误",
                "❌ 错误只能运行时发现",
            ]
        },
        "good_approach": {
            "method": "Pydantic AI 结构化输出",
            "result": good_analysis.model_dump() if not isinstance(good_analysis, Exception) else {"error": str(good_analysis)},
            "benefits": [
                "✅ JSON 格式保证",
                "✅ 字段名强制匹配",
                "✅ 类型自动验证",
                "✅ 枚举值强制",
                "✅ 编译时 + 运行时检查",
            ]
        }
    }


# ============================================================
# 健康检查
# ============================================================

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def root():
    return {
        "name": "智能客服工单系统 Demo",
        "features": [
            "Pydantic AI 结构化输出",
            "Langfuse 追踪",
            "对比演示"
        ]
    }
