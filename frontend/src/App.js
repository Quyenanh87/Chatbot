import React from 'react';
import ChatUI from './components/ChatUI';

function App() {
  return (
    <div className="min-h-screen bg-gray-900">
      <header className="bg-gradient-to-r from-green-600 to-emerald-600 text-white p-6 shadow-lg">
        <div className="container mx-auto">
          <h1 className="text-3xl font-bold text-center">Cooking Assistant</h1>
          <p className="text-center text-gray-100 text-sm mt-2">Đầu bếp ảo - Người bạn đồng hành trong bếp của bạn</p>
        </div>
      </header>
      <main className="container mx-auto px-4 py-8 max-w-4xl">
        <ChatUI />
      </main>
    </div>
  );
}

export default App;