import { useNavigate } from 'react-router-dom';
import { useApp } from '../lib/store';
import { FileText, Zap, Briefcase, Sparkles, ArrowRight, CheckCircle } from 'lucide-react';

export default function Landing() {
  const navigate = useNavigate();
  const { createUser } = useApp();

  const handleStart = async () => {
    await createUser();
    navigate('/onboarding');
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Hero */}
      <section className="min-h-screen flex flex-col items-center justify-center px-4 relative overflow-hidden">
        {/* Subtle gradient glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-blue-500/10 rounded-full blur-[120px] pointer-events-none" />

        <div className="relative z-10 text-center max-w-3xl mx-auto">
          <div className="animate-fade-up">
            <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-6">
              Your resume.
              <br />
              <span className="text-gray-400">Perfected by AI.</span>
            </h1>
            <p className="text-lg md:text-xl text-gray-400 max-w-lg mx-auto mb-10">
              Tailored to every job. Built in minutes.
              Land interviews, not rejections.
            </p>
          </div>

          <div className="animate-fade-up" style={{ animationDelay: '0.15s' }}>
            <button
              onClick={handleStart}
              className="bg-white hover:bg-gray-100 text-gray-950 font-semibold px-8 py-4 rounded-xl text-lg transition-all hover:shadow-lg hover:shadow-white/10 active:scale-95 inline-flex items-center gap-2"
            >
              Start Building — Free
              <ArrowRight className="w-5 h-5" />
            </button>
          </div>

          {/* Social proof */}
          <div className="flex items-center justify-center gap-6 mt-12 text-sm text-gray-500 animate-fade-in" style={{ animationDelay: '0.3s' }}>
            <span className="flex items-center gap-1.5">
              <span className="text-white font-semibold">2,400+</span> CVs created
            </span>
            <span className="w-1 h-1 rounded-full bg-gray-700" />
            <span className="flex items-center gap-1.5">
              <span className="text-white font-semibold">8</span> templates
            </span>
            <span className="w-1 h-1 rounded-full bg-gray-700" />
            <span className="flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-blue-400" /> AI-powered
            </span>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-24 px-4">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-4">
            Everything you need to land the job
          </h2>
          <p className="text-gray-400 text-center mb-16 max-w-lg mx-auto">
            No more generic resumes. Every CV is crafted for the role you want.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              {
                icon: Sparkles,
                title: 'AI-Powered Editing',
                desc: 'Smart suggestions that rewrite bullets, optimize keywords, and make your experience shine.',
                color: 'text-blue-400 bg-blue-400/10',
              },
              {
                icon: Briefcase,
                title: 'Job-Tailored CVs',
                desc: 'Paste a job link. Get a CV rewritten to match — skills reordered, summary reframed.',
                color: 'text-purple-400 bg-purple-400/10',
              },
              {
                icon: Zap,
                title: '8+ Pro Templates',
                desc: 'Modern, executive, minimal — pick a style and switch anytime. ATS-friendly guaranteed.',
                color: 'text-amber-400 bg-amber-400/10',
              },
            ].map(({ icon: Icon, title, desc, color }) => (
              <div
                key={title}
                className="bg-gray-900 border border-gray-800 rounded-2xl p-6 hover:-translate-y-0.5 transition-all duration-300"
              >
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center mb-4 ${color}`}>
                  <Icon className="w-5 h-5" />
                </div>
                <h3 className="font-semibold text-white text-lg mb-2">{title}</h3>
                <p className="text-sm text-gray-400 leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-24 px-4 border-t border-gray-800/50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-16">
            Three steps to your perfect CV
          </h2>

          <div className="space-y-12">
            {[
              { num: '01', title: 'Tell us about yourself', desc: 'Quick guided onboarding — name, skills, experience. No chat needed.' },
              { num: '02', title: 'Pick a template', desc: 'Choose from 8+ professional designs. Switch anytime, your data stays.' },
              { num: '03', title: 'Tailor & download', desc: 'Paste a job link, AI rewrites your CV. Export as PDF in one click.' },
            ].map(({ num, title, desc }) => (
              <div key={num} className="flex gap-6 items-start">
                <span className="text-3xl font-bold text-gray-700 shrink-0">{num}</span>
                <div>
                  <h3 className="text-lg font-semibold text-white mb-1">{title}</h3>
                  <p className="text-gray-400">{desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-24 px-4 border-t border-gray-800/50">
        <div className="max-w-2xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to build your resume?
          </h2>
          <p className="text-gray-400 mb-8">Free to use. No credit card. Takes 3 minutes.</p>
          <button
            onClick={handleStart}
            className="bg-white hover:bg-gray-100 text-gray-950 font-semibold px-8 py-4 rounded-xl text-lg transition-all hover:shadow-lg hover:shadow-white/10 active:scale-95 inline-flex items-center gap-2"
          >
            Get Started
            <ArrowRight className="w-5 h-5" />
          </button>

          <div className="flex items-center justify-center gap-4 mt-8 text-sm text-gray-500">
            {['No sign-up required', 'ATS-friendly', 'Export as PDF'].map(text => (
              <span key={text} className="flex items-center gap-1.5">
                <CheckCircle className="w-3.5 h-3.5 text-green-500" />
                {text}
              </span>
            ))}
          </div>
        </div>
      </section>

      <footer className="text-center text-xs text-gray-600 py-6 border-t border-gray-800/50">
        Built with AI. Your data stays private.
      </footer>
    </div>
  );
}
