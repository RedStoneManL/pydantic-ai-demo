# FastAPI 应用入口

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import app

# 导出
__all__ = ["app"]
