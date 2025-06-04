import React from 'react';
import ChatUI from './components/ChatUI';

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-green-600 text-white p-4 shadow-md">
        <h1 className="text-2xl font-bold text-center">Cooking Assistant</h1>
        <p className="text-center text-sm mt-1">Đầu bếp ảo - Người bạn đồng hành trong bếp của bạn</p>
      </header>
      <main className="container mx-auto px-4 py-8">
        <ChatUI />
      </main>
    </div>
  );
}

export default App;