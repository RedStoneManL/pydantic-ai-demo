'use client';

import { useState } from 'react';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// 示例输入
const EXAMPLES = [
  {
    title: "投诉",
    input: "我买的智能手表才用了两天就坏了，屏幕闪烁，联系客服也没人回复，订单号是AB12345678，要求退款！"
  },
  {
    title: "咨询",
    input: "请问你们的智能手表支持心率监测吗？电池能用多久？防水吗？"
  },
  {
    title: "故障",
    input: "APP登录不上去了，一直提示网络错误，但我网络是正常的，其他APP都能用。"
  },
  {
    title: "建议",
    input: "建议增加一个睡眠分析功能，可以统计深睡浅睡时间，这样更有价值。"
  }
];

export default function TicketForm({ onResult }: { onResult: (result: any) => void }) {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState<'good' | 'bad' | 'compare'>('good');

  const handleSubmit = async () => {
    if (!input.trim()) return;
    
    setLoading(true);
    try {
      let endpoint = '/api/ticket/analyze';
      if (mode === 'bad') endpoint = '/api/ticket/analyze-bad';
      if (mode === 'compare') endpoint = '/api/ticket/compare';
      
      const response = await axios.post(`${API_URL}${endpoint}`, {
        user_input: input
      });
      
      onResult({ ...response.data, mode });
    } catch (error: any) {
      onResult({ error: error.message, mode });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-bold mb-4">智能客服工单分析</h2>
      
      {/* 模式选择 */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">分析模式</label>
        <div className="flex gap-2">
          <button
            onClick={() => setMode('good')}
            className={`px-4 py-2 rounded ${
              mode === 'good' 
                ? 'bg-green-500 text-white' 
                : 'bg-gray-200 hover:bg-gray-300'
            }`}
          >
            ✅ Pydantic AI
          </button>
          <button
            onClick={() => setMode('bad')}
            className={`px-4 py-2 rounded ${
              mode === 'bad' 
                ? 'bg-red-500 text-white' 
                : 'bg-gray-200 hover:bg-gray-300'
            }`}
          >
            ❌ 不用 Pydantic AI
          </button>
          <button
            onClick={() => setMode('compare')}
            className={`px-4 py-2 rounded ${
              mode === 'compare' 
                ? 'bg-blue-500 text-white' 
                : 'bg-gray-200 hover:bg-gray-300'
            }`}
          >
            🔄 对比演示
          </button>
        </div>
      </div>

      {/* 示例按钮 */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">示例</label>
        <div className="flex flex-wrap gap-2">
          {EXAMPLES.map((ex, i) => (
            <button
              key={i}
              onClick={() => setInput(ex.input)}
              className="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded"
            >
              {ex.title}
            </button>
          ))}
        </div>
      </div>

      {/* 输入框 */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">用户输入</label>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="w-full h-32 p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
          placeholder="输入用户的问题描述..."
        />
      </div>

      {/* 提交按钮 */}
      <button
        onClick={handleSubmit}
        disabled={loading || !input.trim()}
        className={`w-full py-3 rounded-lg font-medium ${
          loading || !input.trim()
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
            : 'bg-blue-500 hover:bg-blue-600 text-white'
        }`}
      >
        {loading ? '分析中...' : '开始分析'}
      </button>
    </div>
  );
}
