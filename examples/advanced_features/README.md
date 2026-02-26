# Pydantic AI 高级特性示例

本目录包含 Pydantic AI 深度解析的示例代码和演示幻灯片。

## 文件说明

| 文件 | 说明 |
|------|------|
| `01_pain_points.py` | 当前 LLM 开发的四大痛点 |
| `02_type_safety.py` | 端到端类型安全特性 |
| `03_dependency_injection.py` | 依赖注入机制 (RunContext) |
| `04_dynamic_prompts_and_tools.py` | 动态提示词与工具挂载 |
| `05_auto_correction.py` | 自动错误纠正机制 |
| `06_unit_testing.py` | 单元测试 (TestModel/FunctionModel) |
| `Pydantic_AI_Deep_Dive.pptx` | 演示幻灯片 (12 页) |

## 运行示例

```bash
# 痛点演示
python 01_pain_points.py

# 类型安全演示
python 02_type_safety.py

# 依赖注入演示
python 03_dependency_injection.py

# 动态提示词演示
python 04_dynamic_prompts_and_tools.py

# 自动纠正演示
python 05_auto_correction.py

# 单元测试演示
python 06_unit_testing.py
```

## 查看幻灯片

```bash
# macOS
open Pydantic_AI_Deep_Dive.pptx

# Linux
libreoffice Pydantic_AI_Deep_Dive.pptx
```

## 幻灯片大纲

1. **封面** - Pydantic AI 深度解析
2. **当前痛点** - 四大痛点分析
3. **什么是 Pydantic AI** - 出身、定位、哲学
4. **类型安全** - 端到端类型安全
5. **依赖注入** - RunContext 机制
6. **动态提示词** - @agent.system_prompt & @agent.tool
7. **自动纠正** - 零代码重试机制
8. **单元测试** - TestModel & FunctionModel
9. **优势总结** - 为什么选它
10. **局限性** - 它不能做什么
11. **黄金组合** - LangGraph + Pydantic AI
12. **总结与 Q&A** - 参考资料
