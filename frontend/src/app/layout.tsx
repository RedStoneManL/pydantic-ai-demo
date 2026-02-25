import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: '智能客服工单系统 Demo',
  description: '展示 Pydantic AI 的必要性 + Langfuse 追踪',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh">
      <body>{children}</body>
    </html>
  )
}
