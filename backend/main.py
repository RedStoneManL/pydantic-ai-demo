#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
智能客服工单系统 Demo - 入口

启动方式：
    python -m uvicorn main:app --reload --port 8000
"""
from app.api import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
