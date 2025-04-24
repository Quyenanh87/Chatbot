import React, { useState } from 'react';
import axios from 'axios';

export function ChatUI() {
  const [input, setInput] = useState('');
  const [chat, setChat] = useState([]);
  const [filename, setFilename] = useState('');

  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;
  console.log(API_BASE_URL);

  const handleSend = async () => {
    if (!input.trim()) return;

    try {
      if (filename) {
        const formData = new FormData();
        formData.append('filename', filename);
        formData.append('question', input);
        const res = await axios.post(`${API_BASE_URL}/ask-pdf`, formData);
        setChat((prev) => [
          ...prev,
          { type: 'user', text: input },
          { type: 'bot', text: res.data.answer },
        ]);
      } else {
        const res = await axios.post(`${API_BASE_URL}/chat`, { message: input });
        setChat((prev) => [
          ...prev,
          { type: 'user', text: input },
          { type: 'bot', text: res.data.reply },
        ]);
      }
    } catch (err) {
      setChat((prev) => [...prev, { type: 'bot', text: '❌ Có lỗi xảy ra.' }]);
    }

    setInput('');
  };

  const handlePdfUpload = async (selectedFile) => {
    const formData = new FormData();
    formData.append('pdf', selectedFile);
    try {
      const res = await axios.post(`${API_BASE_URL}/upload-pdf`, formData);
      setFilename(res.data.filename);
      setChat((prev) => [...prev, { type: 'bot', text: `📎 Đã tải lên file: ${res.data.filename}` }]);
    } catch {
      setChat((prev) => [...prev, { type: 'bot', text: '❌ Tải file thất bại.' }]);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-4 bg-gray-900 text-white rounded-xl shadow-md">
      <div className="h-[400px] overflow-y-auto border border-gray-700 p-4 mb-4 rounded bg-gray-800 space-y-4">
        {chat.map((c, idx) => (
          <div key={idx} className={`flex ${c.type === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`max-w-[75%] p-3 rounded-lg shadow text-sm whitespace-pre-line
                ${c.type === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-100 border border-gray-600'}`}
            >
              <div className="mb-1 text-xs font-semibold">
                {c.type === 'user' ? '👤 Bạn' : '🤖 Bot'}
              </div>
              {c.text}
            </div>
          </div>
        ))}
      </div>

      <div className="flex gap-2 mb-2 items-center">
        <input
          type="text"
          className="flex-grow border border-gray-600 bg-gray-800 text-white rounded px-3 py-2"
          placeholder={filename ? 'Bạn muốn hỏi gì?...' : 'Nhập câu hỏi...'}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        />
        <button onClick={handleSend} className="bg-blue-600 text-white px-4 py-2 rounded">
          Gửi
        </button>
      </div>

      <div className="mt-3">
        <label className="block w-full cursor-pointer">
          <input
            type="file"
            accept="application/pdf"
            className="hidden"
            onChange={(e) => {
              const selectedFile = e.target.files[0];
              handlePdfUpload(selectedFile);
            }}
          />
          <div className="w-full p-2 text-center border border-dashed border-purple-400 bg-gray-800 rounded hover:bg-purple-800 transition">
            📎 Click để chọn file PDF để hỏi
          </div>
        </label>
      </div>
    </div>
  );
}
