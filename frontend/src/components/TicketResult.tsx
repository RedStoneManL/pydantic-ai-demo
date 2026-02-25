'use client';

import { useEffect, useState } from 'react';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface TicketResultProps {
  result: any;
}

export default function TicketResult({ result }: TicketResultProps) {
  const [trace, setTrace] = useState<any>(null);

  useEffect(() => {
    // 如果有 trace_id，获取 trace 详情
    if (result?.trace_id) {
      axios.get(`${API_URL}/api/trace/${result.trace_id}`)
        .then(res => setTrace(res.data))
        .catch(err => console.error('Failed to fetch trace:', err));
    }
  }, [result?.trace_id]);

  if (!result) return null;

  const { mode, ...data } = result;

  // 对比模式
  if (mode === 'compare') {
    return (
      <div className="bg-white rounded-lg shadow p-6 mt-6">
        <h2 className="text-xl font-bold mb-4">🔄 对比结果</h2>
        
        <div className="grid grid-cols-2 gap-6">
          {/* 不用 Pydantic AI */}
          <div className="border rounded-lg p-4">
            <h3 className="font-bold text-red-600 mb-2">❌ 不用 Pydantic AI</h3>
            <div className="bg-red-50 p-3 rounded text-sm">
              <pre>{JSON.stringify(data.bad_approach?.result, null, 2)}</pre>
            </div>
            {data.bad_approach?.problems && (
              <ul className="mt-3 text-sm text-red-600">
                {data.bad_approach.problems.map((p: string, i: number) => (
                  <li key={i}>{p}</li>
                ))}
              </ul>
            )}
          </div>

          {/* 用 Pydantic AI */}
          <div className="border rounded-lg p-4">
            <h3 className="font-bold text-green-600 mb-2">✅ 用 Pydantic AI</h3>
            <div className="bg-green-50 p-3 rounded text-sm">
              <pre>{JSON.stringify(data.good_approach?.result, null, 2)}</pre>
            </div>
            {data.good_approach?.benefits && (
              <ul className="mt-3 text-sm text-green-600">
                {data.good_approach.benefits.map((b: string, i: number) => (
                  <li key={i}>{b}</li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </div>
    );
  }

  // 成功
  if (data.success && data.result) {
    return (
      <div className="bg-white rounded-lg shadow p-6 mt-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-green-600">
            {mode === 'bad' ? '❌ 结果（不可靠）' : '✅ 分析结果'}
          </h2>
          <span className="text-sm text-gray-500">{data.duration_ms}ms</span>
        </div>

        {/* 工单信息 */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="bg-gray-50 p-3 rounded">
            <div className="text-sm text-gray-500">分类</div>
            <div className="font-medium">{data.result.category}</div>
          </div>
          <div className="bg-gray-50 p-3 rounded">
            <div className="text-sm text-gray-500">紧急程度</div>
            <div className={`font-medium ${
              data.result.urgency === 'P0' ? 'text-red-600' :
              data.result.urgency === 'P1' ? 'text-orange-600' :
              data.result.urgency === 'P2' ? 'text-yellow-600' :
              'text-green-600'
            }`}>
              {data.result.urgency}
            </div>
          </div>
          <div className="bg-gray-50 p-3 rounded">
            <div className="text-sm text-gray-500">产品</div>
            <div className="font-medium">{data.result.product}</div>
          </div>
          <div className="bg-gray-50 p-3 rounded">
            <div className="text-sm text-gray-500">置信度</div>
            <div className="font-medium">{(data.result.confidence * 100).toFixed(0)}%</div>
          </div>
        </div>

        {/* 摘要 */}
        <div className="mb-4">
          <div className="text-sm text-gray-500 mb-1">摘要</div>
          <div className="bg-blue-50 p-3 rounded">{data.result.summary}</div>
        </div>

        {/* 建议处理 */}
        {data.result.suggested_action && (
          <div className="mb-4">
            <div className="text-sm text-gray-500 mb-1">建议处理</div>
            <div className="bg-yellow-50 p-3 rounded">{data.result.suggested_action}</div>
          </div>
        )}

        {/* Langfuse Trace */}
        {data.trace_id && (
          <div className="mt-4 border-t pt-4">
            <div className="text-sm text-gray-500 mb-2">Langfuse Trace</div>
            <div className="bg-purple-50 p-3 rounded">
              <div className="flex items-center justify-between">
                <span className="font-mono text-sm">{data.trace_id}</span>
                <a 
                  href={`https://cloud.langfuse.com/trace/${data.trace_id}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-500 hover:underline text-sm"
                >
                  在 Langfuse 中查看 →
                </a>
              </div>
            </div>
          </div>
        )}

        {/* 原始 JSON */}
        <details className="mt-4">
          <summary className="cursor-pointer text-sm text-gray-500">查看原始 JSON</summary>
          <pre className="mt-2 bg-gray-100 p-3 rounded text-xs overflow-auto">
            {JSON.stringify(data.result, null, 2)}
          </pre>
        </details>
      </div>
    );
  }

  // 失败
  return (
    <div className="bg-white rounded-lg shadow p-6 mt-6">
      <h2 className="text-xl font-bold text-red-600 mb-4">❌ 分析失败</h2>
      <div className="bg-red-50 p-3 rounded">
        <div className="font-medium">{data.status}</div>
        <div className="text-sm text-gray-600 mt-1">{data.error}</div>
      </div>
      {data.validation_errors && (
        <div className="mt-3">
          <div className="text-sm text-gray-500 mb-1">验证错误</div>
          <ul className="text-sm text-red-600">
            {data.validation_errors.map((err: string, i: number) => (
              <li key={i}>{err}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
