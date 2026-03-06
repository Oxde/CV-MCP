import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Send, Loader2 } from 'lucide-react';
import { useApp } from '../lib/store';
import { api } from '../lib/api';
import ChatBubble from '../components/ChatBubble';

export default function Onboarding() {
  const navigate = useNavigate();
  const { user, refreshUser } = useApp();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [started, setStarted] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const startChat = async () => {
    setStarted(true);
    setSending(true);
    try {
      const res = await api.chat({
        user_id: user.id,
        message: "Hi! I'm new here and want to create my CV.",
        context_type: 'onboarding',
      });
      setMessages([
        { role: 'user', content: "Hi! I'm new here and want to create my CV." },
        { role: 'assistant', content: res.reply },
      ]);
    } catch {
      setMessages([{
        role: 'assistant',
        content: "Welcome to CV Craft! I'm here to help you build an amazing resume. Let's start with the basics — what's your name?",
      }]);
    }
    setSending(false);
  };

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
        context_type: 'onboarding',
      });

      setMessages(prev => [...prev, { role: 'assistant', content: res.reply }]);

      if (res.extracted_data) {
        await refreshUser();
      }

      if (res.onboarding_complete) {
        setTimeout(() => navigate('/dashboard'), 1500);
      }
    } catch {
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: "Sorry, something went wrong. Could you try again?" },
      ]);
    }
    setSending(false);
  };

  const skipOnboarding = async () => {
    await api.updateUser(user.id, { onboarding_complete: true });
    await refreshUser();
    navigate('/dashboard');
  };

  if (!started) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex flex-col items-center justify-center px-4">
        <div className="text-center max-w-md">
          <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <span className="text-3xl">👋</span>
          </div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Let's build your CV!</h1>
          <p className="text-gray-500 mb-8">
            I'll ask you a few questions to get started. It takes about 3 minutes.
          </p>
          <button
            onClick={startChat}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-3 rounded-xl transition-all w-full mb-3"
          >
            Start Conversation
          </button>
          <button
            onClick={skipOnboarding}
            className="text-sm text-gray-400 hover:text-gray-600"
          >
            Skip for now, I'll fill in details manually
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between">
        <div>
          <h1 className="font-semibold text-gray-900">Setting up your profile</h1>
          <p className="text-xs text-gray-400">Tell me about yourself</p>
        </div>
        <button
          onClick={skipOnboarding}
          className="text-sm text-gray-400 hover:text-gray-600"
        >
          Skip
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-4">
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
        <div className="flex gap-2 max-w-2xl mx-auto">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Type your answer..."
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
