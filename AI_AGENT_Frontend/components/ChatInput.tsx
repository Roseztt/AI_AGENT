'use client'
import { useState } from 'react'

type ChatInputProps = {
  onSend: (text: string) => void
}

export default function ChatInput({ onSend }: ChatInputProps) {
  const [input, setInput] = useState('')

  const handleSubmit = () => {
    if (!input.trim()) return
    onSend(input)
    setInput('')
  }

  return (
    <div className="flex p-4 border-t">
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
        placeholder="输入消息并按回车发送..."
        className="flex-1 p-2 border rounded mr-2"
      />
      <button
        onClick={handleSubmit}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        发送
      </button>
    </div>
  )
}