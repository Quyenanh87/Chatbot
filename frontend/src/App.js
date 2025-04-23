import React from 'react';
import { ChatUI } from './components/ChatUI';

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold text-center mb-4">AI Intern ChatBot</h1>
      <ChatUI />
    </div>
  );
}