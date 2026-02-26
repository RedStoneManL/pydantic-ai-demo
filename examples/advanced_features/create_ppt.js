const pptxgen = require("pptxgenjs");

// 创建演示文稿
let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.author = 'Monika';
pres.title = 'Pydantic AI 深度解析';

// 配色方案 - Midnight Executive + Teal
const COLORS = {
  primary: "1E2761",      // 深藏青
  secondary: "0D9488",    // 青绿
  accent: "14B8A6",       // 亮青
  light: "F8FAFC",        // 浅灰
  white: "FFFFFF",
  text: "1E293B",         // 深灰文字
  textLight: "64748B",    // 浅灰文字
};

// ===== Slide 1: 封面 =====
let slide1 = pres.addSlide();
slide1.background = { color: COLORS.primary };

// 装饰线条
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 2.5, w: 10, h: 0.02, fill: { color: COLORS.accent }
});

slide1.addText("Pydantic AI 深度解析", {
  x: 0.5, y: 1.8, w: 9, h: 1,
  fontSize: 44, fontFace: "Arial", bold: true,
  color: COLORS.white, align: "center"
});

slide1.addText("类型安全、依赖注入与 Agent 架构选型", {
  x: 0.5, y: 2.8, w: 9, h: 0.6,
  fontSize: 22, fontFace: "Arial",
  color: COLORS.accent, align: "center"
});

slide1.addText("为什么我们该停止写面条代码，开始用工程化思维构建大模型应用？", {
  x: 1, y: 3.6, w: 8, h: 0.5,
  fontSize: 16, fontFace: "Arial", italic: true,
  color: COLORS.textLight, align: "center"
});

slide1.addText("主讲人：[你的名字/Title]", {
  x: 0.5, y: 4.8, w: 9, h: 0.4,
  fontSize: 14, fontFace: "Arial",
  color: COLORS.textLight, align: "center"
});

// ===== Slide 2: 当前痛点 =====
let slide2 = pres.addSlide();
slide2.background = { color: COLORS.light };

slide2.addText("当前 LLM 应用开发的痛点", {
  x: 0.5, y: 0.3, w: 9, h: 0.8,
  fontSize: 32, fontFace: "Arial", bold: true,
  color: COLORS.primary
});

const painPoints = [
  { title: "薛定谔的 JSON", desc: "提示词越写越长，LLM 返回的 JSON 依然少字段或类型错误" },
  { title: "意大利面条式的上下文", desc: "数据库连接、Token、API Keys 在全局变量中满天飞" },
  { title: "不可测试的黑盒", desc: "Agent 逻辑依赖真实 API，测试缓慢、烧钱且不可靠" },
  { title: "繁琐的错误处理", desc: "结构化解析失败后，需要手写大量重试和回退逻辑" },
];

painPoints.forEach((item, i) => {
  const y = 1.2 + i * 1.1;
  
  // 数字圆圈
  slide2.addShape(pres.shapes.OVAL, {
    x: 0.5, y: y, w: 0.45, h: 0.45,
    fill: { color: COLORS.secondary }
  });
  slide2.addText(`${i + 1}`, {
    x: 0.5, y: y, w: 0.45, h: 0.45,
    fontSize: 16, fontFace: "Arial", bold: true,
    color: COLORS.white, align: "center", valign: "middle"
  });
  
  // 标题
  slide2.addText(item.title, {
    x: 1.1, y: y, w: 8, h: 0.4,
    fontSize: 18, fontFace: "Arial", bold: true,
    color: COLORS.primary
  });
  
  // 描述
  slide2.addText(item.desc, {
    x: 1.1, y: y + 0.4, w: 8.4, h: 0.5,
    fontSize: 14, fontFace: "Arial",
    color: COLORS.textLight
  });
});

// ===== Slide 3: 什么是 Pydantic AI =====
let slide3 = pres.addSlide();
slide3.background = { color: COLORS.primary };

slide3.addText("什么是 Pydantic AI？", {
  x: 0.5, y: 0.3, w: 9, h: 0.8,
  fontSize: 32, fontFace: "Arial", bold: true,
  color: COLORS.white
});

const features = [
  { title: "出身名门", desc: "由 Pydantic 官方团队打造，天生带有 Python 类型系统的正统基因" },
  { title: "核心定位", desc: "不是大而全的生态，而是极致优雅的 Agent 节点开发底座" },
  { title: "设计哲学", desc: "让 LLM 的不确定性在底层被消化，暴露出绝对可靠的类型安全对象" },
];

features.forEach((item, i) => {
  const y = 1.3 + i * 1.3;
  
  slide3.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: y, w: 9, h: 1.1,
    fill: { color: "FFFFFF", transparency: 10 },
    line: { color: COLORS.accent, width: 1 }
  });
  
  slide3.addText(item.title, {
    x: 0.8, y: y + 0.15, w: 8.4, h: 0.4,
    fontSize: 18, fontFace: "Arial", bold: true,
    color: COLORS.accent
  });
  
  slide3.addText(item.desc, {
    x: 0.8, y: y + 0.55, w: 8.4, h: 0.5,
    fontSize: 14, fontFace: "Arial",
    color: COLORS.white
  });
});

// ===== Slide 4: 类型安全 =====
let slide4 = pres.addSlide();
slide4.background = { color: COLORS.light };

slide4.addText("核心 Feature I：端到端的极致类型安全", {
  x: 0.5, y: 0.3, w: 9, h: 0.7,
  fontSize: 28, fontFace: "Arial", bold: true,
  color: COLORS.primary
});

// 左侧说明
slide4.addText([
  { text: "机制说明", options: { bold: true, breakLine: true } },
  { text: "从输入依赖 (deps_type) 到输出结果 (result_type) 全链路泛型支持", options: { breakLine: true, breakLine: true } },
  { text: "工程价值", options: { bold: true, breakLine: true } },
  { text: "• IDE 完美护航：参数补全、方法提示", options: { breakLine: true } },
  { text: "• 静态检查：MyPy/Pyright 运行前报错", options: { breakLine: true } },
  { text: "• 运行时校验：Pydantic 自动验证", options: {} },
], {
  x: 0.5, y: 1.1, w: 4.5, h: 3,
  fontSize: 14, fontFace: "Arial",
  color: COLORS.text, valign: "top"
});

// 右侧代码框
slide4.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 5.2, y: 1.1, w: 4.3, h: 3.5,
  fill: { color: "1E293B" }
});

slide4.addText([
  { text: "class ", options: { color: "F472B6" } },
  { text: "TicketAnalysis", options: { color: "22D3EE" } },
  { text: "(BaseModel):", options: { breakLine: true } },
  { text: "    category: ", options: { color: "F8FAFC" } },
  { text: "TicketCategory", options: { breakLine: true } },
  { text: "    urgency: ", options: { color: "F8FAFC" } },
  { text: "UrgencyLevel", options: { breakLine: true } },
  { text: "    confidence: ", options: { color: "F8FAFC" } },
  { text: "float", options: { breakLine: true, breakLine: true } },
  { text: "agent = ", options: { color: "F8FAFC" } },
  { text: "Agent", options: { color: "22D3EE" } },
  { text: "(", options: { breakLine: true } },
  { text: '    "openai:gpt-4o",', options: { color: "A3E635", breakLine: true } },
  { text: "    output_type=", options: { color: "F8FAFC" } },
  { text: "TicketAnalysis", options: { color: "22D3EE" } },
  { text: ",", options: { breakLine: true } },
  { text: ")", options: {} },
], {
  x: 5.4, y: 1.3, w: 4, h: 3.2,
  fontSize: 11, fontFace: "Consolas",
  color: COLORS.white, valign: "top"
});

// ===== Slide 5: 依赖注入 =====
let slide5 = pres.addSlide();
slide5.background = { color: COLORS.light };

slide5.addText("核心 Feature II：依赖注入机制", {
  x: 0.5, y: 0.3, w: 9, h: 0.7,
  fontSize: 28, fontFace: "Arial", bold: true,
  color: COLORS.primary
});

slide5.addText([
  { text: "机制说明", options: { bold: true, breakLine: true } },
  { text: "首创的 RunContext 概念，告别全局变量，按需注入", options: { breakLine: true, breakLine: true } },
  { text: "实战场景", options: { bold: true, breakLine: true } },
  { text: "• 外部将 user_id + db_connection 丢给 Agent", options: { breakLine: true } },
  { text: "• Tools 和 Prompts 通过 ctx.deps 安全获取", options: { breakLine: true, breakLine: true } },
  { text: "工程价值", options: { bold: true, breakLine: true } },
  { text: "• 高内聚低耦合，多租户友好", options: { breakLine: true } },
  { text: "• 测试时可轻松注入 Mock 依赖", options: {} },
], {
  x: 0.5, y: 1.1, w: 4.5, h: 3.5,
  fontSize: 14, fontFace: "Arial",
  color: COLORS.text, valign: "top"
});

// 右侧图示
slide5.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 5.2, y: 1.1, w: 4.3, h: 3.5,
  fill: { color: COLORS.primary }
});

slide5.addText([
  { text: "UserContext", options: { bold: true, color: COLORS.accent, breakLine: true } },
  { text: "├── user_id: str", options: { breakLine: true } },
  { text: "├── db_connection", options: { breakLine: true } },
  { text: "└── api_key", options: { breakLine: true, breakLine: true } },
  { text: "        ↓", options: { breakLine: true, breakLine: true } },
  { text: "ctx.deps.user_id", options: { color: COLORS.accent, breakLine: true } },
  { text: "ctx.deps.db_connection", options: { color: COLORS.accent } },
], {
  x: 5.5, y: 1.3, w: 4, h: 3,
  fontSize: 13, fontFace: "Consolas",
  color: COLORS.white, valign: "top"
});

// ===== Slide 6: 动态提示词与工具 =====
let slide6 = pres.addSlide();
slide6.background = { color: COLORS.light };

slide6.addText("核心 Feature III：动态提示词与工具挂载", {
  x: 0.5, y: 0.3, w: 9, h: 0.7,
  fontSize: 28, fontFace: "Arial", bold: true,
  color: COLORS.primary
});

// 左侧
slide6.addText([
  { text: "@agent.system_prompt", options: { bold: true, color: COLORS.secondary, breakLine: true } },
  { text: "• 运行时执行的 Python 函数", options: { breakLine: true } },
  { text: "• 根据 ctx.deps 动态生成", options: { breakLine: true } },
  { text: "• VIP 用户 → 专属提示词", options: { breakLine: true, breakLine: true } },
  { text: "@agent.tool", options: { bold: true, color: COLORS.secondary, breakLine: true } },
  { text: "• 无缝获取注入的依赖", options: { breakLine: true } },
  { text: "• Docstring → JSON Schema", options: { breakLine: true } },
  { text: "• 类型注解自动解析", options: {} },
], {
  x: 0.5, y: 1.1, w: 4.5, h: 3.5,
  fontSize: 14, fontFace: "Arial",
  color: COLORS.text, valign: "top"
});

// 右侧代码
slide6.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 5.2, y: 1.1, w: 4.3, h: 3.5,
  fill: { color: "1E293B" }
});

slide6.addText([
  { text: "@agent.system_prompt", options: { color: "F472B6", breakLine: true } },
  { text: "async def ", options: { color: "F472B6" } },
  { text: "prompt(ctx):", options: { breakLine: true } },
  { text: '    if ctx.deps.is_vip:', options: { color: "F8FAFC", breakLine: true } },
  { text: '        return "VIP专属..."', options: { color: "A3E635", breakLine: true, breakLine: true } },
  { text: "@agent.tool", options: { color: "F472B6", breakLine: true } },
  { text: "async def ", options: { color: "F472B6" } },
  { text: "query(ctx, id):", options: { breakLine: true } },
  { text: "    db = ctx.deps.db", options: { color: "F8FAFC", breakLine: true } },
  { text: "    return db.query(id)", options: { color: "F8FAFC" } },
], {
  x: 5.4, y: 1.3, w: 4, h: 3,
  fontSize: 11, fontFace: "Consolas",
  color: COLORS.white, valign: "top"
});

// ===== Slide 7: 自动错误纠正 =====
let slide7 = pres.addSlide();
slide7.background = { color: COLORS.light };

slide7.addText("核心 Feature IV：自动错误纠正机制", {
  x: 0.5, y: 0.3, w: 9, h: 0.7,
  fontSize: 28, fontFace: "Arial", bold: true,
  color: COLORS.primary
});

// 流程图
const flowItems = [
  { text: "LLM 返回", y: 1.2 },
  { text: "Pydantic 校验", y: 2.0 },
  { text: "构造重试提示", y: 2.8 },
  { text: "自动重试", y: 3.6 },
];

flowItems.forEach((item, i) => {
  slide7.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: item.y, w: 2.5, h: 0.6,
    fill: { color: i === 1 ? COLORS.secondary : COLORS.primary }
  });
  slide7.addText(item.text, {
    x: 0.5, y: item.y, w: 2.5, h: 0.6,
    fontSize: 13, fontFace: "Arial", bold: true,
    color: COLORS.white, align: "center", valign: "middle"
  });
  
  if (i < flowItems.length - 1) {
    slide7.addText("↓", {
      x: 1.5, y: item.y + 0.55, w: 0.5, h: 0.4,
      fontSize: 18, color: COLORS.textLight, align: "center"
    });
  }
});

// 循环箭头说明
slide7.addShape(pres.shapes.LINE, {
  x: 3.2, y: 4.1, w: 0, h: -2.7,
  line: { color: COLORS.secondary, width: 2 }
});
slide7.addText("← 重试循环", {
  x: 3.0, y: 2.5, w: 1.2, h: 0.4,
  fontSize: 11, fontFace: "Arial",
  color: COLORS.secondary
});

// 右侧说明
slide7.addText([
  { text: "零行代码实现", options: { bold: true, color: COLORS.secondary, breakLine: true, breakLine: true } },
  { text: "1. LLM 返回不符合 Schema", options: { breakLine: true } },
  { text: "2. 自动拦截 ValidationError", options: { breakLine: true } },
  { text: "3. 封装错误为重试 Prompt", options: { breakLine: true } },
  { text: "4. 逼迫模型自行修正", options: { breakLine: true, breakLine: true } },
  { text: "🎯 不可靠的文本 → 可靠的数据", options: { bold: true } },
], {
  x: 4.5, y: 1.2, w: 5, h: 3.5,
  fontSize: 14, fontFace: "Arial",
  color: COLORS.text, valign: "top"
});

// ===== Slide 8: 单元测试 =====
let slide8 = pres.addSlide();
slide8.background = { color: COLORS.light };

slide8.addText("核心 Feature V：真正的单元测试", {
  x: 0.5, y: 0.3, w: 9, h: 0.7,
  fontSize: 28, fontFace: "Arial", bold: true,
  color: COLORS.primary
});

slide8.addText([
  { text: "TestModel", options: { bold: true, color: COLORS.secondary, breakLine: true } },
  { text: "• 零 Token 消耗，零网络延迟", options: { breakLine: true } },
  { text: "• 自动读取 result_type", options: { breakLine: true } },
  { text: "• 反射生成符合 Schema 的假数据", options: { breakLine: true, breakLine: true } },
  { text: "FunctionModel", options: { bold: true, color: COLORS.secondary, breakLine: true } },
  { text: "• 自定义 Mock 行为", options: { breakLine: true } },
  { text: "• 可测试特定场景/边界情况", options: { breakLine: true, breakLine: true } },
  { text: "🎯 测试 Agent 像测试普通函数一样简单", options: { bold: true } },
], {
  x: 0.5, y: 1.1, w: 4.5, h: 3.5,
  fontSize: 14, fontFace: "Arial",
  color: COLORS.text, valign: "top"
});

// 对比表格
slide8.addTable([
  [
    { text: "", options: { fill: { color: COLORS.primary } } },
    { text: "传统方式", options: { fill: { color: COLORS.primary }, color: COLORS.white, bold: true } },
    { text: "Pydantic AI", options: { fill: { color: COLORS.primary }, color: COLORS.white, bold: true } }
  ],
  ["Token 消耗", "有 (烧钱)", "无"],
  ["网络延迟", "有 (慢)", "无"],
  ["结果稳定性", "不稳定", "完全稳定"],
  ["CI/CD 友好", "否", "是"],
], {
  x: 5.2, y: 1.2, w: 4.3, h: 2.5,
  fontSize: 11, fontFace: "Arial",
  color: COLORS.text,
  border: { pt: 0.5, color: "CBD5E1" }
});

// ===== Slide 9: 优势总结 =====
let slide9 = pres.addSlide();
slide9.background = { color: COLORS.primary };

slide9.addText("优势总结 —— 为什么选它？", {
  x: 0.5, y: 0.3, w: 9, h: 0.7,
  fontSize: 28, fontFace: "Arial", bold: true,
  color: COLORS.white
});

const pros = [
  { title: "代码质量极高", desc: "将 LLM 开发拉回现代软件工程标准" },
  { title: "开发者体验碾压", desc: "没有晦涩的 LCEL，纯粹的 Python 代码" },
  { title: "数据可靠性", desc: "Pydantic V2 Rust 核心直接对接 Function Calling" },
  { title: "流式支持强大", desc: "支持结构化模型数据的流式输出" },
];

pros.forEach((item, i) => {
  const y = 1.1 + i * 1.0;
  
  slide9.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: y, w: 9, h: 0.85,
    fill: { color: "FFFFFF", transparency: 10 }
  });
  
  slide9.addText(item.title, {
    x: 0.8, y: y + 0.1, w: 4, h: 0.35,
    fontSize: 16, fontFace: "Arial", bold: true,
    color: COLORS.accent
  });
  
  slide9.addText(item.desc, {
    x: 0.8, y: y + 0.45, w: 8.4, h: 0.35,
    fontSize: 13, fontFace: "Arial",
    color: COLORS.white
  });
});

// ===== Slide 10: 局限性 =====
let slide10 = pres.addSlide();
slide10.background = { color: COLORS.light };

slide10.addText("局限与不足 —— 它不能做什么？", {
  x: 0.5, y: 0.3, w: 9, h: 0.7,
  fontSize: 28, fontFace: "Arial", bold: true,
  color: COLORS.primary
});

const cons = [
  { title: "不是全包圆框架", desc: "没有内置文档加载器、向量数据库开箱即用集成" },
  { title: "缺乏宏观图编排", desc: "不支持 LangGraph 的时间旅行、Checkpointer、人类审批" },
  { title: "小场景略显繁琐", desc: "简单聊天机器人用强类型约束可能过度" },
];

cons.forEach((item, i) => {
  const y = 1.1 + i * 1.3;
  
  slide10.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: y, w: 9, h: 1.1,
    fill: { color: "FEF2F2" },
    line: { color: "FECACA", width: 1 }
  });
  
  slide10.addText("⚠ " + item.title, {
    x: 0.8, y: y + 0.15, w: 8.4, h: 0.4,
    fontSize: 16, fontFace: "Arial", bold: true,
    color: "DC2626"
  });
  
  slide10.addText(item.desc, {
    x: 0.8, y: y + 0.55, w: 8.4, h: 0.45,
    fontSize: 13, fontFace: "Arial",
    color: COLORS.text
  });
});

// ===== Slide 11: 黄金组合 =====
let slide11 = pres.addSlide();
slide11.background = { color: COLORS.light };

slide11.addText("终极的黄金组合 (The Golden Stack)", {
  x: 0.5, y: 0.3, w: 9, h: 0.7,
  fontSize: 28, fontFace: "Arial", bold: true,
  color: COLORS.primary
});

// 架构图
slide11.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.5, y: 1.2, w: 9, h: 2.2,
  fill: { color: COLORS.primary }
});

slide11.addText("LangGraph (外层管家)", {
  x: 0.8, y: 1.4, w: 8.4, h: 0.4,
  fontSize: 16, fontFace: "Arial", bold: true,
  color: COLORS.accent
});

slide11.addText("全局图状态维护 | 复杂路由 | 循环 | 持久化记忆 | 人类介入", {
  x: 0.8, y: 1.8, w: 8.4, h: 0.35,
  fontSize: 12, fontFace: "Arial",
  color: COLORS.white
});

// 内层
slide11.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 1.5, y: 2.4, w: 7, h: 0.8,
  fill: { color: COLORS.secondary }
});

slide11.addText("Pydantic AI (内层打工人) → 结构化数据提取 | 局部工具调用 | 100% 正确输出", {
  x: 1.7, y: 2.5, w: 6.6, h: 0.6,
  fontSize: 12, fontFace: "Arial", bold: true,
  color: COLORS.white, valign: "middle"
});

// 结论
slide11.addText("💡 结论：抛弃非黑即白的站队，组合使用才是最佳实践", {
  x: 0.5, y: 3.6, w: 9, h: 0.5,
  fontSize: 16, fontFace: "Arial", bold: true,
  color: COLORS.secondary, align: "center"
});

// Demo 链接
slide11.addText("Demo: github.com/RedStoneManL/pydantic-ai-demo", {
  x: 0.5, y: 4.3, w: 9, h: 0.4,
  fontSize: 14, fontFace: "Arial",
  color: COLORS.textLight, align: "center"
});

// ===== Slide 12: 总结与 Q&A =====
let slide12 = pres.addSlide();
slide12.background = { color: COLORS.primary };

slide12.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 2.0, w: 10, h: 0.02, fill: { color: COLORS.accent }
});

slide12.addText("总结", {
  x: 0.5, y: 1.0, w: 9, h: 0.8,
  fontSize: 36, fontFace: "Arial", bold: true,
  color: COLORS.white, align: "center"
});

slide12.addText('"Pydantic AI 把大模型的不确定性，\n用工程化的确定性关进了笼子。"', {
  x: 1, y: 2.3, w: 8, h: 1.0,
  fontSize: 20, fontFace: "Arial", italic: true,
  color: COLORS.accent, align: "center"
});

slide12.addText("参考资料与 Demo 源码", {
  x: 0.5, y: 3.5, w: 9, h: 0.4,
  fontSize: 16, fontFace: "Arial", bold: true,
  color: COLORS.white, align: "center"
});

slide12.addText("github.com/RedStoneManL/pydantic-ai-demo\nexamples/advanced_features/", {
  x: 0.5, y: 3.9, w: 9, h: 0.5,
  fontSize: 14, fontFace: "Arial",
  color: COLORS.textLight, align: "center"
});

slide12.addText("Q & A", {
  x: 0.5, y: 4.6, w: 9, h: 0.6,
  fontSize: 28, fontFace: "Arial", bold: true,
  color: COLORS.white, align: "center"
});

// 保存文件
const outputPath = "/root/.openclaw/workspace/pydantic-ai-demo/examples/advanced_features/Pydantic_AI_Deep_Dive.pptx";
pres.writeFile({ fileName: outputPath })
  .then(() => console.log(`✅ PPT 已生成: ${outputPath}`))
  .catch(err => console.error("❌ 生成失败:", err));
