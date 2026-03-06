import { useState, useRef, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Send, Loader2, RotateCcw } from 'lucide-react';
import { useApp } from '../lib/store';
import { api } from '../lib/api';
import ChatBubble from '../components/ChatBubble';

export default function Chat() {
  const { user, refreshUser } = useApp();
  const [searchParams] = useSearchParams();
  const cvId = searchParams.get('cv');
  const vacancyId = searchParams.get('vacancy');

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [contextType, setContextType] = useState(cvId ? 'cv_edit' : 'general');
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (user) {
      api.getChatHistory(user.id, contextType).then(history => {
        setMessages(history.map(m => ({ role: m.role, content: m.content })));
      });
    }
  }, [user, contextType]);

  const sendMessage = async () => {
    if (!input.trim() || sending) return;
    const msg = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: msg }]);
    setSending(true);

    try {
      const res = await api.chat({
        user_id: user.id,
        message: msg,
        context_type: contextType,
        cv_id: cvId ? parseInt(cvId) : undefined,
        vacancy_id: vacancyId ? parseInt(vacancyId) : undefined,
      });

      setMessages(prev => [...prev, { role: 'assistant', content: res.reply }]);

      if (res.extracted_data) {
        await refreshUser();
      }
    } catch {
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: 'Sorry, something went wrong. Please try again.' },
      ]);
    }
    setSending(false);
  };

  const clearChat = async () => {
    if (!confirm('Clear chat history?')) return;
    await api.clearChat(user.id, contextType);
    setMessages([]);
  };

  return (
    <div className="h-[calc(100vh-60px)] md:h-[calc(100vh-56px)] flex flex-col max-w-3xl mx-auto">
      {/* Header */}
      <div className="px-4 py-3 border-b border-gray-200 flex items-center justify-between bg-white">
        <div className="flex gap-1 bg-gray-100 rounded-lg p-0.5">
          {[
            { id: 'general', label: 'General' },
            { id: 'cv_edit', label: 'CV Editor' },
          ].map(({ id, label }) => (
            <button
              key={id}
              onClick={() => setContextType(id)}
              className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                contextType === id ? 'bg-white shadow text-blue-600' : 'text-gray-500'
              }`}
            >
              {label}
            </button>
          ))}
        </div>
        <button
          onClick={clearChat}
          className="p-2 rounded-lg hover:bg-gray-100 text-gray-400 hover:text-gray-600"
          title="Clear chat"
        >
          <RotateCcw className="w-4 h-4" />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-4 bg-gray-50">
        {messages.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-400 text-sm">
              {contextType === 'cv_edit'
                ? 'Ask me to edit your CV. Try: "Make my summary more impactful"'
                : 'Ask me anything about your career or CV. Try: "How can I improve my skills section?"'}
            </p>
          </div>
        )}
        {messages.map((msg, i) => (
          <ChatBubble key={i} role={msg.role} content={msg.content} />
        ))}
        {sending && (
          <div className="flex justify-start mb-3">
            <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-md px-4 py-3 shadow-sm">
              <Loader2 className="w-4 h-4 animate-spin text-gray-400" />
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="bg-white border-t border-gray-200 px-4 py-3">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder={contextType === 'cv_edit' ? 'Tell me what to change...' : 'Ask me anything...'}
            className="flex-1 bg-gray-100 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white border border-transparent focus:border-blue-500"
            disabled={sending}
          />
          <button
            onClick={sendMessage}
            disabled={sending || !input.trim()}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white p-2.5 rounded-xl transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
