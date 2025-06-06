import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const ChatUI = () => {
  const welcomeMessages = [
    "Xin chào! Tôi là bếp trưởng AI, rất vui được gặp bạn! Hôm nay bạn muốn nấu món gì nào? 👩‍🍳",
    "Chào mừng đến với nhà bếp thông minh! Để tôi giúp bạn khám phá những công thức nấu ăn tuyệt vời nhé! 🍳",
    "Xin chào đầu bếp! Hãy cùng nhau tạo ra những món ăn ngon cho gia đình bạn nhé! 🥘"
  ];

  const [messages, setMessages] = useState([
    { 
      text: welcomeMessages[Math.floor(Math.random() * welcomeMessages.length)], 
      isUser: false 
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const formatMessage = (text) => {
    const lines = text.split('\n');
    return lines.map((line, index) => {
      // Xóa tất cả dấu * và hiển thị bullet point cho mỗi dòng có nội dung
      if (line.includes('*')) {
        const cleanLine = line.replace(/\*+/g, '').trim();
        if (cleanLine) {
          return (
            <div key={index} className="flex items-start space-x-3 mb-3 animate-fadeIn">
              <span className="text-green-400 text-lg mt-0.5">•</span>
              <span className="text-gray-200">{cleanLine}</span>
            </div>
          );
        }
      }
      
      // Xử lý các dòng bắt đầu bằng "Mẹo:"
      if (line.startsWith('Mẹo:')) {
        return (
          <div key={index} className="bg-gray-700/50 p-4 rounded-lg mt-3 mb-3 shadow-sm border border-gray-600 animate-slideIn backdrop-blur-sm">
            <div className="flex items-center space-x-2">
              <span className="text-2xl">💡</span>
              <span className="font-medium text-green-300">{line}</span>
            </div>
          </div>
        );
      }

      // Xử lý các tiêu đề (Nguyên liệu, Hướng dẫn, v.v.)
      if (line.endsWith(':')) {
        return (
          <h3 key={index} className="font-semibold text-green-400 mt-6 mb-4 text-lg border-b border-gray-600/50 pb-2 animate-fadeIn">
            {line}
          </h3>
        );
      }

      // Xử lý danh sách các bước
      if (line.match(/^\d+\./)) {
        return (
          <div key={index} className="flex items-start space-x-3 mb-4 animate-slideIn">
            <span className="flex-shrink-0 w-6 h-6 rounded-full bg-green-500 text-gray-900 flex items-center justify-center text-sm font-medium">
              {line.split('.')[0]}
            </span>
            <span className="text-gray-200 flex-1">{line.split('.').slice(1).join('.').trim()}</span>
          </div>
        );
      }

      // Các dòng thông thường
      return <p key={index} className="text-gray-200 mb-3 animate-fadeIn">{line}</p>;
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { text: userMessage, isUser: true }]);
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_URL}/chat`, {
        message: userMessage
      });

      setMessages(prev => [...prev, { text: response.data.reply, isUser: false }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, {
        text: "Xin lỗi, hiện tại tôi đang gặp trục trặc kết nối. Vui lòng thử lại sau!",
        isUser: false
      }]);
    }

    setIsLoading(false);
  };

  return (
    <>
      <div 
        className="fixed inset-0"
        style={{
          backgroundImage: "url('/cooking-bg.png')",
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat',
          opacity: 0.2,
          zIndex: 0
        }}
      />
      <div className="min-h-screen relative">
        <div className="relative z-10 p-4 md:p-8">
          <div className="max-w-4xl mx-auto">
            <div className="flex flex-col h-[650px] bg-gray-900/90 backdrop-blur-md rounded-xl shadow-2xl border border-gray-700/50 overflow-hidden">
              {/* Header */}
              <div className="bg-gradient-to-r from-gray-900/80 to-gray-800/80 border-b border-gray-700/50 p-4">
                <h1 className="text-2xl font-semibold text-green-400 text-center">
                  Cooking Assistant
                </h1>
              </div>

              {/* Chat Messages */}
              <div className="flex-1 overflow-y-auto p-6 space-y-6">
                {messages.map((msg, index) => (
                  <div
                    key={index}
                    className={`flex ${msg.isUser ? 'justify-end' : 'justify-start'}`}
                  >
                    {!msg.isUser && (
                      <div className="w-10 h-10 rounded-full bg-green-600 flex items-center justify-center mr-3 flex-shrink-0 shadow-lg border-2 border-green-500/50">
                        <span role="img" aria-label="chef" className="text-xl">👩‍🍳</span>
                      </div>
                    )}
                    <div
                      className={`max-w-[80%] rounded-lg p-4 shadow-lg ${
                        msg.isUser
                          ? 'bg-green-600/90 text-white backdrop-blur-sm'
                          : 'bg-gray-800/90 border border-gray-700/50 backdrop-blur-sm'
                      }`}
                    >
                      {formatMessage(msg.text)}
                    </div>
                    {msg.isUser && (
                      <div className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center ml-3 flex-shrink-0 shadow-lg border-2 border-gray-600/50">
                        <span role="img" aria-label="user" className="text-xl">👤</span>
                      </div>
                    )}
                  </div>
                ))}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="w-10 h-10 rounded-full bg-green-600 flex items-center justify-center mr-3 flex-shrink-0 shadow-lg border-2 border-green-500/50">
                      <span role="img" aria-label="chef" className="text-xl">👩‍🍳</span>
                    </div>
                    <div className="bg-gray-800/90 rounded-lg p-4 border border-gray-700/50 backdrop-blur-sm shadow-lg">
                      <div className="flex space-x-2">
                        <div className="w-2 h-2 bg-green-500 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-green-500 rounded-full animate-bounce delay-100"></div>
                        <div className="w-2 h-2 bg-green-500 rounded-full animate-bounce delay-200"></div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Input Form */}
              <form onSubmit={handleSubmit} className="p-4 border-t border-gray-700/50 bg-gradient-to-r from-gray-900/90 to-gray-800/90 backdrop-blur-md">
                <div className="flex space-x-4">
                  <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Hỏi đầu bếp điều bạn muốn..."
                    className="flex-1 bg-gray-700/50 text-white rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-green-500 border border-gray-600/50 placeholder-gray-400"
                  />
                  <button
                    type="submit"
                    disabled={isLoading}
                    className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors duration-200 disabled:opacity-50 shadow-lg hover:shadow-green-500/20"
                  >
                    Gửi
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ChatUI;
