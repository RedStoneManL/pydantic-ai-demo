'use client';

import { useState } from 'react';
import TicketForm from '@/components/TicketForm';
import TicketResult from '@/components/TicketResult';

export default function Home() {
  const [result, setResult] = useState<any>(null);

  return (
    <main className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            智能客服工单系统 Demo
          </h1>
          <p className="text-gray-600">
            展示 Pydantic AI 的必要性 + Langfuse 追踪
          </p>
        </div>

        {/* 为什么需要 Pydantic AI */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-bold mb-4">🎯 为什么需要 Pydantic AI？</h2>
          
          <div className="grid grid-cols-2 gap-6">
            <div>
              <h3 className="font-bold text-red-600 mb-2">❌ 不用 Pydantic AI</h3>
              <ul className="text-sm space-y-2 text-gray-600">
                <li>• LLM 返回格式不确定</li>
                <li>• JSON 可能解析失败</li>
                <li>• 字段名可能不一致</li>
                <li>• 没有类型验证</li>
                <li>• 枚举值可能错误</li>
                <li>• 错误只能运行时发现</li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-green-600 mb-2">✅ 用 Pydantic AI</h3>
              <ul className="text-sm space-y-2 text-gray-600">
                <li>• 结构化输出保证</li>
                <li>• JSON 格式自动处理</li>
                <li>• 字段名强制匹配</li>
                <li>• 类型自动验证</li>
                <li>• 枚举值强制</li>
                <li>• 编译时 + 运行时检查</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Form */}
        <TicketForm onResult={setResult} />

        {/* Result */}
        {result && <TicketResult result={result} />}

        {/* Footer */}
        <div className="text-center mt-8 text-gray-500 text-sm">
          <p>Pydantic AI Demo | 技术分享</p>
        </div>
      </div>
    </main>
  );
}
