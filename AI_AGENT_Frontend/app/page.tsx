'use client';
import { useState } from 'react';
import Sidebar from '@/components/Sidebar'; 
import ChatInput from '@/components/ChatInput'; 
import ChatBubble from '@/components/ChatBubble'; 
import React from 'react';


export default function Home() {
  type Message = {
    text: string;
    type: "user" | "bot";
  };
  
  interface ApiResponse {
      response: string;
  }

  const [messages, setMessages] = useState<Message[]>([
    { text: '你好！我是你的 AI 助手，有什么我可以帮忙的吗？', type: 'bot' } // Initial bot message
  ]);

  const [isLoading, setIsLoading] = useState<boolean>(false);


  const handleSend = async (text: string) => {
    if (!text.trim() || isLoading) return;

    //add user message
    const userMessage: Message = {
      text,
      type: 'user',
    };

    //send user message and set loading
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    const apiUrl = 'http://localhost:8000/query/';

    //send JSON to POST through API
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },

      body: JSON.stringify({
        query_text: text,
      }),
    });

    //get bot response
    const data: ApiResponse = await response.json();

    //send bot message 
    const botMessage: Message = {
      text: data.response, 
      type: 'bot',        
    }
    setMessages(prev => [...prev, botMessage]);
    setIsLoading(false);
  };

//return everything
  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex flex-col flex-1 bg-white">
        <main className="flex-1 overflow-y-auto p-6">
          {messages.map((msg, index) => (
            <ChatBubble key={index} text={msg.text} type={msg.type} />
          ))}
          {isLoading && (
            <ChatBubble key="loading" text="AI is thinking..." type="bot" />
          )}
        </main>
        <ChatInput onSend={handleSend} />
      </div>
    </div>
  );
}