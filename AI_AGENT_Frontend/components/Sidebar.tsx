'use client'
import { useState } from "react"
import { MessageCircle, FolderOpen } from "lucide-react"

export default function Sidebar() {
  const [active, setActive] = useState("new")

  return (
    <div className="w-64 h-screen bg-[#1e1e2f] text-white flex flex-col p-4 space-y-4 shadow-md">
      <h2 className="text-xl font-semibold mb-6 tracking-wide">💬 对话列表</h2>

      <button
        onClick={() => setActive("new")}
        className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all hover:bg-[#2e2e4f] ${
          active === "new" ? "bg-[#3e3e6f]" : ""
        }`}
      >
        <MessageCircle className="w-5 h-5" />
        <span className="text-sm">新对话</span>
      </button>

      <button
        onClick={() => setActive("history")}
        className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all hover:bg-[#2e2e4f] ${
          active === "history" ? "bg-[#3e3e6f]" : ""
        }`}
      >
        <FolderOpen className="w-5 h-5" />
        <span className="text-sm">历史记录</span>
      </button>

      <div className="flex-grow" />
      <div className="text-xs text-gray-400 text-center">
        © 2025 YourApp
      </div>
    </div>
  )
}