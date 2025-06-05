import React from 'react';
import ChatUI from './components/ChatUI';

function App() {
  return (
    <div className="h-screen overflow-hidden bg-gray-900">
      <header className="text-white p-6">
        <div className="container mx-auto text-center">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-green-400 to-emerald-500 bg-clip-text text-transparent drop-shadow-lg">
            Cooking Assistant
          </h1>
          <p className="text-gray-300 text-lg mt-3 font-medium tracking-wide">
            Đầu bếp ảo - Người bạn đồng hành trong bếp của bạn
          </p>
        </div>
      </header>
      <main className="container mx-auto px-4 max-w-4xl">
        <ChatUI />
      </main>
    </div>
  );
}

export default App;