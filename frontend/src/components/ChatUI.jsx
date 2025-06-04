import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

const ChatUI = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const [suggestions] = useState([
    "Tìm công thức nấu mì Ý",
    "Cách thay thế trứng khi làm bánh",
    "Tính khẩu phần cho 6 người",
    "Hẹn giờ nấu cơm",
    "Thông tin dinh dưỡng món cà ri gà"
  ]);

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
          <div key={index} className="bg-gray-700/50 p-4 rounded-lg mt-3 mb-3 shadow-sm border border-gray-600 animate-slideIn">
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
          <h3 key={index} className="font-semibold text-green-400 mt-6 mb-4 text-lg border-b border-gray-600 pb-2 animate-fadeIn">
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
      const response = await axios.post('http://localhost:8000/chat', {
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

  const handleSuggestionClick = (suggestion) => {
    setInput(suggestion);
  };

  return (
    <div className="flex flex-col h-[700px] bg-gray-900 rounded-xl shadow-2xl border border-gray-700 overflow-hidden">
      {/* Suggestions */}
      <div className="p-6 border-b border-gray-700 bg-gradient-to-r from-gray-900 to-gray-800">
        <h3 className="text-sm font-medium text-gray-300 mb-3">Gợi ý hỗ trợ:</h3>
        <div className="flex flex-wrap gap-2">
          {suggestions.map((suggestion, index) => (
            <button
              key={index}
              onClick={() => handleSuggestionClick(suggestion)}
              className="px-4 py-2 text-sm bg-gray-800 text-green-400 rounded-full hover:bg-gray-700 transition-all duration-200 shadow-sm border border-gray-600 hover:border-green-500 hover:scale-105"
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-gradient-to-b from-gray-900 to-gray-800 custom-scrollbar">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.isUser ? 'justify-end' : 'justify-start'} animate-slideIn`}
          >
            <div
              className={`max-w-[80%] rounded-2xl p-4 ${
                message.isUser
                  ? 'bg-gradient-to-r from-green-500 to-emerald-500 text-white shadow-lg'
                  : 'bg-gray-800 text-gray-200 shadow-md border border-gray-600'
              }`}
            >
              {!message.isUser && (
                <div className="w-10 h-10 rounded-full bg-gradient-to-r from-green-500 to-emerald-500 text-white flex items-center justify-center mb-3 shadow-lg">
                  👩‍🍳
                </div>
              )}
              <div className="whitespace-pre-wrap">
                {message.isUser ? message.text : formatMessage(message.text)}
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start animate-fadeIn">
            <div className="bg-gray-800 rounded-2xl p-4 shadow-md border border-gray-600">
              <div className="flex space-x-2 items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full animate-bounce opacity-75"></div>
                <div className="w-3 h-3 bg-green-500 rounded-full animate-bounce opacity-75" style={{ animationDelay: '0.2s' }}></div>
                <div className="w-3 h-3 bg-green-500 rounded-full animate-bounce opacity-75" style={{ animationDelay: '0.4s' }}></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="p-6 border-t border-gray-700 bg-gray-900">
        <div className="flex space-x-4">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Hỏi về công thức nấu ăn, nguyên liệu hoặc mẹo nấu nướng..."
            className="flex-1 p-4 bg-gray-800 border border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 text-gray-200 placeholder-gray-400"
          />
          <button
            type="submit"
            disabled={isLoading}
            className="px-8 py-4 bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-xl hover:shadow-lg transition-all duration-200 disabled:opacity-70 disabled:cursor-not-allowed hover:scale-105 active:scale-95 font-medium"
          >
            {isLoading ? 'Đang xử lý...' : 'Gửi'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatUI;
