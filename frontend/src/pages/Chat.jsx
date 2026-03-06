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
      if (res.extracted_data) await refreshUser();
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
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="px-4 py-3 border-b border-gray-800 flex items-center justify-between bg-gray-950/50 shrink-0">
        <div className="flex gap-1 bg-gray-800 rounded-lg p-0.5">
          {[
            { id: 'general', label: 'General' },
            { id: 'cv_edit', label: 'CV Editor' },
          ].map(({ id, label }) => (
            <button
              key={id}
              onClick={() => setContextType(id)}
              className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                contextType === id ? 'bg-gray-700 text-white' : 'text-gray-500'
              }`}
            >
              {label}
            </button>
          ))}
        </div>
        <button
          onClick={clearChat}
          className="p-2 rounded-lg hover:bg-gray-800 text-gray-500 hover:text-gray-300"
          title="Clear chat"
        >
          <RotateCcw className="w-4 h-4" />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-4">
        {messages.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-sm">
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
            <div className="bg-gray-800 border border-gray-700 rounded-2xl rounded-bl-md px-4 py-3">
              <Loader2 className="w-4 h-4 animate-spin text-gray-400" />
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="border-t border-gray-800 px-4 py-3 bg-gray-950/50 shrink-0">
        <div className="flex gap-2 max-w-3xl mx-auto">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder={contextType === 'cv_edit' ? 'Tell me what to change...' : 'Ask me anything...'}
            className="flex-1 bg-gray-800 border border-gray-700 rounded-xl px-4 py-2.5 text-sm text-white placeholder:text-gray-600 focus:outline-none focus:border-gray-500"
            disabled={sending}
          />
          <button
            onClick={sendMessage}
            disabled={sending || !input.trim()}
            className="bg-white hover:bg-gray-100 disabled:bg-gray-700 disabled:text-gray-500 text-gray-950 p-2.5 rounded-xl transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
