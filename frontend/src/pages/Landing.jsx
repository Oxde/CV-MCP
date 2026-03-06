import { useNavigate } from 'react-router-dom';
import { useApp } from '../lib/store';
import { FileText, Zap, Briefcase, Sparkles } from 'lucide-react';

export default function Landing() {
  const navigate = useNavigate();
  const { createUser } = useApp();

  const handleStart = async () => {
    await createUser();
    navigate('/onboarding');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex flex-col">
      <div className="flex-1 flex flex-col items-center justify-center px-4 py-12">
        {/* Logo */}
        <div className="w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center mb-6 shadow-lg shadow-blue-200">
          <FileText className="w-9 h-9 text-white" />
        </div>

        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 text-center mb-3">
          CV Craft
        </h1>
        <p className="text-lg text-gray-500 text-center max-w-md mb-10">
          AI-powered resumes tailored to every job.
          Land interviews, not rejections.
        </p>

        <button
          onClick={handleStart}
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-3.5 rounded-xl text-lg transition-all hover:shadow-lg hover:shadow-blue-200 active:scale-95"
        >
          Get Started — It's Free
        </button>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16 max-w-3xl w-full">
          {[
            { icon: Sparkles, title: 'AI-Powered', desc: 'Smart suggestions that make your CV stand out' },
            { icon: Briefcase, title: 'Job-Tailored', desc: 'Paste a job link, get a CV optimized for it' },
            { icon: Zap, title: '8+ Templates', desc: 'Professional designs from modern to executive' },
          ].map(({ icon: Icon, title, desc }) => (
            <div key={title} className="text-center p-5">
              <div className="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center mx-auto mb-3">
                <Icon className="w-5 h-5 text-blue-600" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-1">{title}</h3>
              <p className="text-sm text-gray-500">{desc}</p>
            </div>
          ))}
        </div>
      </div>

      <footer className="text-center text-xs text-gray-400 py-4">
        Built with AI. Your data stays private.
      </footer>
    </div>
  );
}
