const pptxgen = require("pptxgenjs");

// 创建演示文稿
let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.author = 'Monika';
pres.title = 'Pydantic AI 深度解析';

// ============================================================
// 设计规范 (Design System)
// ============================================================
const COLORS = {
  // 核心色
  PRIMARY_RED: "C7000B",      // 主题红 RGB 199/0/11
  BLACK: "231815",            // 黑色 RGB 35/24/21
  DARK_GRAY: "595757",        // 深灰 RGB 89/87/87
  
  // 辅助灰阶
  MED_GRAY: "9FA0A0",         // 中灰 RGB 159/160/160
  LIGHT_GRAY: "DDDDDD",       // 浅灰 RGB 221/221/221
  WHITE: "FFFFFF",            // 纯白
  
  // 背景色
  CARD_BG: "F5F5F5",          // 卡片底色
  PAGE_BG: "FFFFFF",          // 页面背景
};

// 字体规范
const FONTS = {
  mainTitle: { fontFace: "微软雅黑", fontSize: 32, color: COLORS.PRIMARY_RED, bold: true },
  moduleTitle: { fontFace: "微软雅黑", fontSize: 20, color: COLORS.BLACK, bold: true },
  body: { fontFace: "微软雅黑", fontSize: 13, color: COLORS.DARK_GRAY },
  small: { fontFace: "微软雅黑", fontSize: 11, color: COLORS.MED_GRAY },
};

// 通用装饰：红色细线条 (顶部)
function addTopAccentLine(slide, x, y, w) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: x, y: y, w: w, h: 0.02,
    fill: { color: COLORS.PRIMARY_RED },
    line: { color: COLORS.PRIMARY_RED, width: 0 }
  });
}

// 通用装饰：红色竖线 (左侧)
function addLeftAccentLine(slide, x, y, h) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: x, y: y, w: 0.03, h: h,
    fill: { color: COLORS.PRIMARY_RED },
    line: { color: COLORS.PRIMARY_RED, width: 0 }
  });
}

// ============================================================
// Slide 1: 封面
// ============================================================
let slide1 = pres.addSlide();
slide1.background = { color: COLORS.PAGE_BG };

// 左侧红色装饰条
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 0.15, h: 5.625,
  fill: { color: COLORS.PRIMARY_RED }
});

// 主标题
slide1.addText("Pydantic AI 深度解析", {
  x: 0.8, y: 1.8, w: 8.5, h: 1,
  ...FONTS.mainTitle, fontSize: 44
});

// 红色分割线
addTopAccentLine(slide1, 0.8, 2.9, 5);

// 副标题
slide1.addText("类型安全、依赖注入与 Agent 架构选型", {
  x: 0.8, y: 3.1, w: 8.5, h: 0.5,
  fontFace: "微软雅黑", fontSize: 18, color: COLORS.BLACK
});

// 描述
slide1.addText("为什么我们该停止写面条代码，开始用工程化思维构建大模型应用？", {
  x: 0.8, y: 3.7, w: 8.5, h: 0.4,
  fontFace: "微软雅黑", fontSize: 14, color: COLORS.DARK_GRAY, italic: true
});

// 底部信息
slide1.addText("主讲人：[你的名字/Title]", {
  x: 0.8, y: 4.8, w: 8.5, h: 0.3,
  fontFace: "微软雅黑", fontSize: 12, color: COLORS.MED_GRAY
});

// ============================================================
// Slide 2: 当前痛点
// ============================================================
let slide2 = pres.addSlide();
slide2.background = { color: COLORS.PAGE_BG };

// 主标题
slide2.addText("当前 LLM 应用开发的痛点", {
  x: 0.5, y: 0.3, w: 9, h: 0.7,
  ...FONTS.mainTitle
});
addTopAccentLine(slide2, 0.5, 0.85, 9);

// 痛点数据
const painPoints = [
  { num: "01", title: "薛定谔的 JSON", desc: "提示词越写越长，LLM 返回的 JSON 依然少字段或类型错误" },
  { num: "02", title: "意大利面条式的上下文", desc: "数据库连接、Token、API Keys 在全局变量中满天飞" },
  { num: "03", title: "不可测试的黑盒", desc: "Agent 逻辑依赖真实 API，测试缓慢、烧钱且不可靠" },
  { num: "04", title: "繁琐的错误处理", desc: "结构化解析失败后，需要手写大量重试和回退逻辑" },
];

painPoints.forEach((item, i) => {
  const y = 1.1 + i * 1.1;
  
  // 卡片背景
  slide2.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: y, w: 9, h: 0.95,
    fill: { color: COLORS.CARD_BG }
  });
  
  // 红色数字
  slide2.addText(item.num, {
    x: 0.7, y: y + 0.15, w: 0.6, h: 0.65,
    fontFace: "Arial", fontSize: 28, color: COLORS.PRIMARY_RED, bold: true, valign: "middle"
  });
  
  // 标题
  slide2.addText(item.title, {
    x: 1.4, y: y + 0.1, w: 7.8, h: 0.4,
    ...FONTS.moduleTitle, fontSize: 16
  });
  
  // 描述
  slide2.addText(item.desc, {
    x: 1.4, y: y + 0.5, w: 7.8, h: 0.4,
    ...FONTS.body
  });
});

// ============================================================
// Slide 3: 什么是 Pydantic AI
// ============================================================
let slide3 = pres.addSlide();
slide3.background = { color: COLORS.PAGE_BG };

slide3.addText("什么是 Pydantic AI？", {
  x: 0.5, y: 0.3, w: 9, h: 0.7,
  ...FONTS.mainTitle
});
addTopAccentLine(slide3, 0.5, 0.85, 9);

const features = [
  { title: "出身名门", desc: "由 Pydantic 官方团队打造，天生带有 Python 类型系统的正统基因" },
  { title: "核心定位", desc: "不是大而全的生态（不像 LangChain），而是极致优雅的 Agent 节点开发底座" },
  { title: "设计哲学", desc: "让 LLM 的不确定性在底层被消化，暴露出绝对可靠的类型安全对象" },
];

features.forEach((item, i) => {
  const y = 1.1 + i * 1.35;
  
  // 卡片
  slide3.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: y, w: 9, h: 1.2,
    fill: { color: COLORS.WHITE },
    line: { color: COLORS.LIGHT_GRAY, width: 1 }
  });
  
  // 左侧红线
  addLeftAccentLine(slide3, 0.5, y, 1.2);
  
  // 标题
  slide3.addText(item.title, {
    x: 0.8, y: y + 0.15, w: 8.4, h: 0.4,
    ...FONTS.moduleTitle, fontSize: 18, color: COLORS.PRIMARY_RED
  });
  
  // 描述
  slide3.addText(item.desc, {
    x: 0.8, y: y + 0.6, w: 8.4, h: 0.5,
    ...FONTS.body, fontSize: 14
  });
});

// ============================================================
// Slide 4: 类型安全
// ============================================================
let slide4 = pres.addSlide();
slide4.background = { color: COLORS.PAGE_BG };

slide4.addText("核心 Feature I：端到端的极致类型安全", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  ...FONTS.mainTitle, fontSize: 28
});
addTopAccentLine(slide4, 0.5, 0.8, 9);

// 左侧卡片 (1/3)
slide4.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.0, w: 3, h: 4.0,
  fill: { color: COLORS.CARD_BG }
});

slide4.addText("类型安全四层次", {
  x: 0.7, y: 1.15, w: 2.6, h: 0.4,
  ...FONTS.moduleTitle, fontSize: 14
});

slide4.addText([
  { text: "1. 定义时", options: { bold: true, color: COLORS.PRIMARY_RED, breakLine: true } },
  { text: "BaseModel + Field 定义约束", options: { breakLine: true, breakLine: true } },
  { text: "2. 编码时", options: { bold: true, color: COLORS.PRIMARY_RED, breakLine: true } },
  { text: "IDE 自动补全", options: { breakLine: true, breakLine: true } },
  { text: "3. 编译时", options: { bold: true, color: COLORS.PRIMARY_RED, breakLine: true } },
  { text: "MyPy/Pyright 静态检查", options: { breakLine: true, breakLine: true } },
  { text: "4. 运行时", options: { bold: true, color: COLORS.PRIMARY_RED, breakLine: true } },
  { text: "Pydantic 自动校验", options: {} },
], {
  x: 0.7, y: 1.6, w: 2.6, h: 3.2,
  ...FONTS.body, fontSize: 12, valign: "top"
});

// 右侧代码 (2/3)
slide4.addShape(pres.shapes.RECTANGLE, {
  x: 3.7, y: 1.0, w: 5.8, h: 4.0,
  fill: { color: COLORS.BLACK }
});

slide4.addText([
  { text: "class ", options: { color: COLORS.PRIMARY_RED } },
  { text: "TicketAnalysis", options: { color: COLORS.LIGHT_GRAY } },
  { text: "(BaseModel):", options: { breakLine: true } },
  { text: "    category: ", options: { color: COLORS.WHITE } },
  { text: "TicketCategory", options: { color: "22D3EE", breakLine: true } },
  { text: "    urgency: ", options: { color: COLORS.WHITE } },
  { text: "UrgencyLevel", options: { color: "22D3EE", breakLine: true } },
  { text: "    confidence: ", options: { color: COLORS.WHITE } },
  { text: "float", options: { color: "22D3EE", breakLine: true, breakLine: true } },
  { text: "agent = ", options: { color: COLORS.WHITE } },
  { text: "Agent", options: { color: "22D3EE" } },
  { text: "(", options: { breakLine: true } },
  { text: '    "openai:gpt-4o",', options: { color: COLORS.MED_GRAY, breakLine: true } },
  { text: "    output_type=", options: { color: COLORS.WHITE } },
  { text: "TicketAnalysis", options: { color: "22D3EE" } },
  { text: ",", options: { breakLine: true } },
  { text: ")", options: {} },
], {
  x: 3.9, y: 1.2, w: 5.4, h: 3.6,
  fontFace: "Consolas", fontSize: 12,
  color: COLORS.WHITE, valign: "top"
});

// ============================================================
// Slide 5: 依赖注入
// ============================================================
let slide5 = pres.addSlide();
slide5.background = { color: COLORS.PAGE_BG };

slide5.addText("核心 Feature II：依赖注入机制", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  ...FONTS.mainTitle, fontSize: 28
});
addTopAccentLine(slide5, 0.5, 0.8, 9);

// 左侧说明
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.0, w: 4.2, h: 4.0,
  fill: { color: COLORS.CARD_BG }
});

slide5.addText([
  { text: "机制说明", options: { bold: true, color: COLORS.PRIMARY_RED, breakLine: true } },
  { text: "首创的 RunContext 概念", options: { breakLine: true } },
  { text: "告别全局变量，按需注入", options: { breakLine: true, breakLine: true } },
  { text: "工程价值", options: { bold: true, color: COLORS.PRIMARY_RED, breakLine: true } },
  { text: "• 高内聚低耦合", options: { breakLine: true } },
  { text: "• 多租户友好", options: { breakLine: true } },
  { text: "• 测试时可注入 Mock", options: {} },
], {
  x: 0.7, y: 1.2, w: 3.8, h: 3.6,
  ...FONTS.body, fontSize: 13, valign: "top"
});

// 右侧图示
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 4.9, y: 1.0, w: 4.6, h: 4.0,
  fill: { color: COLORS.WHITE },
  line: { color: COLORS.LIGHT_GRAY, width: 1 }
});

slide5.addText("UserContext", {
  x: 5.1, y: 1.2, w: 4.2, h: 0.4,
  ...FONTS.moduleTitle, fontSize: 16, color: COLORS.PRIMARY_RED
});

slide5.addText([
  { text: "├── user_id: str", options: { breakLine: true } },
  { text: "├── db_connection", options: { breakLine: true } },
  { text: "└── api_key", options: { breakLine: true, breakLine: true } },
  { text: "        ↓", options: { breakLine: true, breakLine: true } },
  { text: "ctx.deps.user_id", options: { color: COLORS.PRIMARY_RED, breakLine: true } },
  { text: "ctx.deps.db_connection", options: { color: COLORS.PRIMARY_RED } },
], {
  x: 5.1, y: 1.7, w: 4.2, h: 3.0,
  fontFace: "Consolas", fontSize: 12,
  color: COLORS.BLACK, valign: "top"
});

// ============================================================
// Slide 6: 动态提示词与工具
// ============================================================
let slide6 = pres.addSlide();
slide6.background = { color: COLORS.PAGE_BG };

slide6.addText("核心 Feature III：动态提示词与工具挂载", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  ...FONTS.mainTitle, fontSize: 28
});
addTopAccentLine(slide6, 0.5, 0.8, 9);

// 左侧 @agent.system_prompt
slide6.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.0, w: 4.2, h: 1.8,
  fill: { color: COLORS.CARD_BG }
});

addLeftAccentLine(slide6, 0.5, 1.0, 1.8);

slide6.addText("@agent.system_prompt", {
  x: 0.7, y: 1.15, w: 3.8, h: 0.35,
  ...FONTS.moduleTitle, fontSize: 14, color: COLORS.PRIMARY_RED
});

slide6.addText([
  { text: "• 运行时执行的 Python 函数", options: { breakLine: true } },
  { text: "• 根据 ctx.deps 动态生成", options: { breakLine: true } },
  { text: "• VIP 用户 → 专属提示词", options: {} },
], {
  x: 0.7, y: 1.55, w: 3.8, h: 1.1,
  ...FONTS.body, fontSize: 12, valign: "top"
});

// 左侧 @agent.tool
slide6.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.0, w: 4.2, h: 2.0,
  fill: { color: COLORS.CARD_BG }
});

addLeftAccentLine(slide6, 0.5, 3.0, 2.0);

slide6.addText("@agent.tool", {
  x: 0.7, y: 3.15, w: 3.8, h: 0.35,
  ...FONTS.moduleTitle, fontSize: 14, color: COLORS.PRIMARY_RED
});

slide6.addText([
  { text: "• 无缝获取注入的依赖", options: { breakLine: true } },
  { text: "• Docstring → JSON Schema", options: { breakLine: true } },
  { text: "• 类型注解自动解析", options: {} },
], {
  x: 0.7, y: 3.55, w: 3.8, h: 1.3,
  ...FONTS.body, fontSize: 12, valign: "top"
});

// 右侧代码
slide6.addShape(pres.shapes.RECTANGLE, {
  x: 4.9, y: 1.0, w: 4.6, h: 4.0,
  fill: { color: COLORS.BLACK }
});

slide6.addText([
  { text: "@agent.system_prompt", options: { color: COLORS.PRIMARY_RED, breakLine: true } },
  { text: "async def ", options: { color: COLORS.PRIMARY_RED } },
  { text: "prompt(ctx):", options: { color: COLORS.WHITE, breakLine: true } },
  { text: '    if ctx.deps.is_vip:', options: { color: COLORS.WHITE, breakLine: true } },
  { text: '        return "VIP专属..."', options: { color: COLORS.MED_GRAY, breakLine: true, breakLine: true } },
  { text: "@agent.tool", options: { color: COLORS.PRIMARY_RED, breakLine: true } },
  { text: "async def ", options: { color: COLORS.PRIMARY_RED } },
  { text: "query(ctx, id):", options: { color: COLORS.WHITE, breakLine: true } },
  { text: "    db = ctx.deps.db", options: { color: COLORS.WHITE, breakLine: true } },
  { text: "    return db.query(id)", options: { color: COLORS.WHITE } },
], {
  x: 5.1, y: 1.2, w: 4.2, h: 3.6,
  fontFace: "Consolas", fontSize: 11,
  color: COLORS.WHITE, valign: "top"
});

// ============================================================
// Slide 7: 自动错误纠正
// ============================================================
let slide7 = pres.addSlide();
slide7.background = { color: COLORS.PAGE_BG };

slide7.addText("核心 Feature IV：自动错误纠正机制", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  ...FONTS.mainTitle, fontSize: 28
});
addTopAccentLine(slide7, 0.5, 0.8, 9);

// 左侧流程图
const flowItems = [
  { text: "LLM 返回", y: 1.1 },
  { text: "Pydantic 校验", y: 1.9, highlight: true },
  { text: "构造重试提示", y: 2.7 },
  { text: "自动重试", y: 3.5 },
];

flowItems.forEach((item, i) => {
  slide7.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: item.y, w: 2.8, h: 0.65,
    fill: { color: item.highlight ? COLORS.PRIMARY_RED : COLORS.BLACK }
  });
  slide7.addText(item.text, {
    x: 0.5, y: item.y, w: 2.8, h: 0.65,
    fontFace: "微软雅黑", fontSize: 13, bold: true,
    color: COLORS.WHITE, align: "center", valign: "middle"
  });
  
  if (i < flowItems.length - 1) {
    slide7.addText("↓", {
      x: 1.6, y: item.y + 0.6, w: 0.5, h: 0.35,
      fontSize: 14, color: COLORS.MED_GRAY, align: "center"
    });
  }
});

// 循环说明
slide7.addShape(pres.shapes.LINE, {
  x: 3.5, y: 4.0, w: 0, h: -2.6,
  line: { color: COLORS.PRIMARY_RED, width: 2 }
});
slide7.addText("← 重试循环", {
  x: 3.3, y: 2.5, w: 1.0, h: 0.3,
  ...FONTS.small, fontSize: 10, color: COLORS.PRIMARY_RED
});

// 右侧说明
slide7.addShape(pres.shapes.RECTANGLE, {
  x: 4.0, y: 1.1, w: 5.5, h: 3.5,
  fill: { color: COLORS.CARD_BG }
});

slide7.addText([
  { text: "零行代码实现", options: { bold: true, color: COLORS.PRIMARY_RED, breakLine: true, breakLine: true } },
  { text: "1. LLM 返回不符合 Schema", options: { breakLine: true } },
  { text: "2. 自动拦截 ValidationError", options: { breakLine: true } },
  { text: "3. 封装错误为重试 Prompt", options: { breakLine: true } },
  { text: "4. 逼迫模型自行修正", options: { breakLine: true, breakLine: true } },
  { text: "🎯 不可靠的文本 → 可靠的数据", options: { bold: true, color: COLORS.BLACK } },
], {
  x: 4.2, y: 1.3, w: 5.1, h: 3.1,
  ...FONTS.body, fontSize: 13, valign: "top"
});

// ============================================================
// Slide 8: 单元测试
// ============================================================
let slide8 = pres.addSlide();
slide8.background = { color: COLORS.PAGE_BG };

slide8.addText("核心 Feature V：真正的单元测试", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  ...FONTS.mainTitle, fontSize: 28
});
addTopAccentLine(slide8, 0.5, 0.8, 9);

// 左侧说明
slide8.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.0, w: 4.2, h: 4.0,
  fill: { color: COLORS.CARD_BG }
});

slide8.addText([
  { text: "TestModel", options: { bold: true, color: COLORS.PRIMARY_RED, breakLine: true } },
  { text: "• 零 Token 消耗", options: { breakLine: true } },
  { text: "• 自动生成符合 Schema 的数据", options: { breakLine: true, breakLine: true } },
  { text: "FunctionModel", options: { bold: true, color: COLORS.PRIMARY_RED, breakLine: true } },
  { text: "• 自定义 Mock 行为", options: { breakLine: true } },
  { text: "• 可测试特定场景", options: { breakLine: true, breakLine: true } },
  { text: "🎯 测试 Agent 像测试普通函数", options: { bold: true, color: COLORS.BLACK } },
], {
  x: 0.7, y: 1.2, w: 3.8, h: 3.6,
  ...FONTS.body, fontSize: 13, valign: "top"
});

// 右侧对比表
slide8.addTable([
  [
    { text: "", options: { fill: { color: COLORS.BLACK } } },
    { text: "传统方式", options: { fill: { color: COLORS.BLACK }, color: COLORS.WHITE, bold: true, align: "center" } },
    { text: "Pydantic AI", options: { fill: { color: COLORS.BLACK }, color: COLORS.WHITE, bold: true, align: "center" } }
  ],
  [{ text: "Token 消耗", options: { bold: true } }, "有 (烧钱)", { text: "无", options: { color: COLORS.PRIMARY_RED, bold: true } }],
  [{ text: "网络延迟", options: { bold: true } }, "有 (慢)", { text: "无", options: { color: COLORS.PRIMARY_RED, bold: true } }],
  [{ text: "结果稳定性", options: { bold: true } }, "不稳定", { text: "完全稳定", options: { color: COLORS.PRIMARY_RED, bold: true } }],
  [{ text: "CI/CD 友好", options: { bold: true } }, "否", { text: "是", options: { color: COLORS.PRIMARY_RED, bold: true } }],
], {
  x: 4.9, y: 1.2, w: 4.6, h: 2.8,
  fontFace: "微软雅黑", fontSize: 12,
  color: COLORS.BLACK,
  border: { pt: 0.5, color: COLORS.LIGHT_GRAY },
  align: "center"
});

// ============================================================
// Slide 9: 优势总结
// ============================================================
let slide9 = pres.addSlide();
slide9.background = { color: COLORS.PAGE_BG };

slide9.addText("优势总结 —— 为什么选它？", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  ...FONTS.mainTitle, fontSize: 28
});
addTopAccentLine(slide9, 0.5, 0.8, 9);

const pros = [
  { title: "代码质量极高", desc: "将 LLM 开发拉回现代软件工程标准" },
  { title: "开发者体验碾压", desc: "没有晦涩的 LCEL，纯粹的 Python 代码" },
  { title: "数据可靠性", desc: "Pydantic V2 Rust 核心直接对接 Function Calling" },
  { title: "流式支持强大", desc: "支持结构化模型数据的流式输出" },
];

pros.forEach((item, i) => {
  const y = 1.0 + i * 1.1;
  
  slide9.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: y, w: 9, h: 0.95,
    fill: { color: COLORS.CARD_BG }
  });
  
  addLeftAccentLine(slide9, 0.5, y, 0.95);
  
  slide9.addText(item.title, {
    x: 0.8, y: y + 0.12, w: 8.4, h: 0.35,
    ...FONTS.moduleTitle, fontSize: 15, color: COLORS.PRIMARY_RED
  });
  
  slide9.addText(item.desc, {
    x: 0.8, y: y + 0.5, w: 8.4, h: 0.35,
    ...FONTS.body, fontSize: 13
  });
});

// ============================================================
// Slide 10: 局限性
// ============================================================
let slide10 = pres.addSlide();
slide10.background = { color: COLORS.PAGE_BG };

slide10.addText("局限与不足 —— 它不能做什么？", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  ...FONTS.mainTitle, fontSize: 28
});
addTopAccentLine(slide10, 0.5, 0.8, 9);

const cons = [
  { title: "不是全包圆框架", desc: "没有内置文档加载器、向量数据库开箱即用集成" },
  { title: "缺乏宏观图编排", desc: "不支持 LangGraph 的时间旅行、Checkpointer、人类审批" },
  { title: "小场景略显繁琐", desc: "简单聊天机器人用强类型约束可能过度" },
];

cons.forEach((item, i) => {
  const y = 1.0 + i * 1.4;
  
  slide10.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: y, w: 9, h: 1.2,
    fill: { color: "FEF2F2" },
    line: { color: "FECACA", width: 1 }
  });
  
  slide10.addText("⚠ " + item.title, {
    x: 0.8, y: y + 0.15, w: 8.4, h: 0.4,
    ...FONTS.moduleTitle, fontSize: 16, color: COLORS.PRIMARY_RED
  });
  
  slide10.addText(item.desc, {
    x: 0.8, y: y + 0.6, w: 8.4, h: 0.5,
    ...FONTS.body, fontSize: 13
  });
});

// ============================================================
// Slide 11: 黄金组合
// ============================================================
let slide11 = pres.addSlide();
slide11.background = { color: COLORS.PAGE_BG };

slide11.addText("终极的黄金组合 (The Golden Stack)", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  ...FONTS.mainTitle, fontSize: 28
});
addTopAccentLine(slide11, 0.5, 0.8, 9);

// 架构图 - 外层
slide11.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.1, w: 9, h: 2.4,
  fill: { color: COLORS.BLACK }
});

slide11.addText("LangGraph (外层管家)", {
  x: 0.8, y: 1.3, w: 8.4, h: 0.4,
  fontFace: "微软雅黑", fontSize: 16, bold: true,
  color: COLORS.PRIMARY_RED
});

slide11.addText("全局图状态维护 | 复杂路由 | 循环 | 持久化记忆 | 人类介入", {
  x: 0.8, y: 1.7, w: 8.4, h: 0.35,
  fontFace: "微软雅黑", fontSize: 12,
  color: COLORS.WHITE
});

// 内层
slide11.addShape(pres.shapes.RECTANGLE, {
  x: 1.2, y: 2.3, w: 7.6, h: 1.0,
  fill: { color: COLORS.PRIMARY_RED }
});

slide11.addText("Pydantic AI (内层打工人)", {
  x: 1.4, y: 2.4, w: 7.2, h: 0.35,
  fontFace: "微软雅黑", fontSize: 14, bold: true,
  color: COLORS.WHITE
});

slide11.addText("结构化数据提取 | 局部工具调用 | 100% 正确输出", {
  x: 1.4, y: 2.8, w: 7.2, h: 0.35,
  fontFace: "微软雅黑", fontSize: 11,
  color: COLORS.WHITE
});

// 结论
slide11.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.7, w: 9, h: 0.7,
  fill: { color: COLORS.CARD_BG }
});

slide11.addText("💡 结论：抛弃非黑即白的站队，组合使用才是最佳实践", {
  x: 0.5, y: 3.7, w: 9, h: 0.7,
  fontFace: "微软雅黑", fontSize: 15, bold: true,
  color: COLORS.BLACK, align: "center", valign: "middle"
});

// Demo 链接
slide11.addText("Demo: github.com/RedStoneManL/pydantic-ai-demo", {
  x: 0.5, y: 4.6, w: 9, h: 0.3,
  fontFace: "微软雅黑", fontSize: 12,
  color: COLORS.MED_GRAY, align: "center"
});

// ============================================================
// Slide 12: 总结与 Q&A
// ============================================================
let slide12 = pres.addSlide();
slide12.background = { color: COLORS.PAGE_BG };

// 左侧红色装饰条
slide12.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 0.15, h: 5.625,
  fill: { color: COLORS.PRIMARY_RED }
});

slide12.addText("总结", {
  x: 0.8, y: 1.2, w: 8.5, h: 0.8,
  ...FONTS.mainTitle, fontSize: 36
});

addTopAccentLine(slide12, 0.8, 1.9, 5);

slide12.addText('"Pydantic AI 把大模型的不确定性，\n用工程化的确定性关进了笼子。"', {
  x: 0.8, y: 2.2, w: 8.5, h: 0.9,
  fontFace: "微软雅黑", fontSize: 18, italic: true,
  color: COLORS.PRIMARY_RED
});

slide12.addText("参考资料与 Demo 源码", {
  x: 0.8, y: 3.3, w: 8.5, h: 0.4,
  fontFace: "微软雅黑", fontSize: 14, bold: true,
  color: COLORS.BLACK
});

slide12.addText("github.com/RedStoneManL/pydantic-ai-demo\nexamples/advanced_features/", {
  x: 0.8, y: 3.7, w: 8.5, h: 0.5,
  fontFace: "微软雅黑", fontSize: 12,
  color: COLORS.MED_GRAY
});

slide12.addText("Q & A", {
  x: 0.8, y: 4.5, w: 8.5, h: 0.6,
  fontFace: "微软雅黑", fontSize: 28, bold: true,
  color: COLORS.PRIMARY_RED
});

// 保存文件
const outputPath = "/root/.openclaw/workspace/pydantic-ai-demo/examples/advanced_features/Pydantic_AI_Deep_Dive_v2.pptx";
pres.writeFile({ fileName: outputPath })
  .then(() => console.log(`✅ PPT v2 已生成: ${outputPath}`))
  .catch(err => console.error("❌ 生成失败:", err));
