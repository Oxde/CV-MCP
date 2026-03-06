import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { X, Loader2 } from 'lucide-react';
import { useApp } from '../lib/store';
import { api } from '../lib/api';
import OnboardingStep from '../components/OnboardingStep';

const TOTAL_STEPS = 11;

const ROLE_SUGGESTIONS = ['Software Engineer', 'Product Manager', 'Designer', 'Data Scientist', 'Marketing', 'Sales', 'Operations', 'Finance'];
const LOCATION_SUGGESTIONS = ['San Francisco', 'New York', 'London', 'Remote', 'Berlin', 'Toronto', 'Singapore'];
const SKILL_SUGGESTIONS = ['JavaScript', 'Python', 'React', 'Node.js', 'SQL', 'AWS', 'TypeScript', 'Java', 'Figma', 'Excel', 'Project Management', 'Communication'];
const TARGET_SUGGESTIONS = ['Frontend Engineer', 'Backend Engineer', 'Full Stack Developer', 'Product Manager', 'Data Analyst', 'UX Designer', 'DevOps Engineer'];

const EXP_OPTIONS = [
  { label: '0–1 years', value: '0-1' },
  { label: '1–3 years', value: '1-3' },
  { label: '3–5 years', value: '3-5' },
  { label: '5–10 years', value: '5-10' },
  { label: '10+ years', value: '10+' },
];

export default function Onboarding() {
  const navigate = useNavigate();
  const { user, updateUser, refreshUser } = useApp();
  const [step, setStep] = useState(0);
  const [saving, setSaving] = useState(false);
  const [finishing, setFinishing] = useState(false);

  const [fullName, setFullName] = useState(user?.full_name || '');
  const [title, setTitle] = useState(user?.title || '');
  const [experience, setExperience] = useState(user?.years_experience || '');
  const [location, setLocation] = useState(user?.location || '');
  const [email, setEmail] = useState(user?.email || '');
  const [phone, setPhone] = useState(user?.phone || '');
  const [linkedin, setLinkedin] = useState(user?.linkedin || '');
  const [skills, setSkills] = useState(user?.skills || []);
  const [skillInput, setSkillInput] = useState('');
  const [workExp, setWorkExp] = useState({
    title: '', company: '', start_date: '', end_date: '', bullets: ['', '', ''],
  });
  const [education, setEducation] = useState({ degree: '', school: '', year: '' });
  const [targetRoles, setTargetRoles] = useState(user?.target_roles || []);
  const [targetInput, setTargetInput] = useState('');

  const saveField = async (data) => {
    setSaving(true);
    try {
      await updateUser(data);
    } catch (e) {
      console.error('Save failed:', e);
    }
    setSaving(false);
  };

  const next = async () => {
    switch (step) {
      case 0: await saveField({ full_name: fullName }); break;
      case 1: await saveField({ title }); break;
      case 2: await saveField({ years_experience: experience }); break;
      case 3: await saveField({ location }); break;
      case 4: await saveField({ email }); break;
      case 5: await saveField({ phone }); break;
      case 6: await saveField({ linkedin }); break;
      case 7: await saveField({ skills }); break;
      case 8: {
        const existing = user?.work_experience || [];
        const entry = {
          ...workExp,
          bullets: workExp.bullets.filter(b => b.trim()),
        };
        if (entry.title) {
          await saveField({ work_experience: [...existing, entry] });
        }
        break;
      }
      case 9: {
        const existing = user?.education || [];
        if (education.degree || education.school) {
          await saveField({ education: [...existing, education] });
        }
        break;
      }
      case 10: {
        await saveField({ target_roles: targetRoles });
        await finishOnboarding();
        return;
      }
    }
    if (step < TOTAL_STEPS - 1) setStep(step + 1);
  };

  const finishOnboarding = async () => {
    setFinishing(true);
    try {
      await api.chat({
        user_id: user.id,
        message: 'Generate a professional summary for my CV based on my profile.',
        context_type: 'onboarding',
      });
      await updateUser({ onboarding_complete: true });
      await refreshUser();
      navigate('/dashboard');
    } catch {
      await updateUser({ onboarding_complete: true });
      await refreshUser();
      navigate('/dashboard');
    }
  };

  const back = () => { if (step > 0) setStep(step - 1); };
  const canContinue = () => {
    switch (step) {
      case 0: return fullName.trim().length > 0;
      case 1: return title.trim().length > 0;
      case 2: return experience !== '';
      case 3: return location.trim().length > 0;
      case 4: return email.trim().length > 0;
      case 7: return skills.length > 0;
      case 8: return workExp.title.trim().length > 0;
      default: return true;
    }
  };
  const isSkippable = () => [5, 6, 9, 10].includes(step);

  const addSkill = (skill) => {
    const s = skill.trim();
    if (s && !skills.includes(s)) setSkills([...skills, s]);
    setSkillInput('');
  };
  const removeSkill = (skill) => setSkills(skills.filter(s => s !== skill));
  const addTargetRole = (role) => {
    const r = role.trim();
    if (r && !targetRoles.includes(r)) setTargetRoles([...targetRoles, r]);
    setTargetInput('');
  };
  const removeTargetRole = (role) => setTargetRoles(targetRoles.filter(r => r !== role));

  if (finishing) {
    return (
      <div className="min-h-screen bg-gray-950 flex flex-col items-center justify-center">
        <Loader2 className="w-8 h-8 text-white animate-spin mb-4" />
        <p className="text-white text-lg font-medium">Building your profile...</p>
        <p className="text-gray-400 text-sm mt-1">AI is crafting your professional summary</p>
      </div>
    );
  }

  const stepConfigs = [
    {
      title: "What's your name?",
      subtitle: "Let's start with the basics.",
      content: (
        <input type="text" value={fullName} onChange={(e) => setFullName(e.target.value)} placeholder="John Doe" autoFocus
          className="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3.5 text-white text-lg placeholder:text-gray-600 focus:outline-none focus:border-white transition-colors" />
      ),
    },
    {
      title: 'What do you do?',
      subtitle: 'Your current or most recent role.',
      content: (
        <div>
          <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="e.g. Software Engineer" autoFocus
            className="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3.5 text-white text-lg placeholder:text-gray-600 focus:outline-none focus:border-white transition-colors mb-4" />
          <div className="flex flex-wrap gap-2">
            {ROLE_SUGGESTIONS.map(r => (
              <button key={r} onClick={() => setTitle(r)}
                className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${title === r ? 'bg-white text-gray-950 font-medium' : 'bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-gray-200'}`}>
                {r}
              </button>
            ))}
          </div>
        </div>
      ),
    },
    {
      title: 'Years of experience?',
      subtitle: 'How long have you been working?',
      content: (
        <div className="grid grid-cols-1 gap-3">
          {EXP_OPTIONS.map(opt => (
            <button key={opt.value} onClick={() => setExperience(opt.value)}
              className={`py-4 px-5 rounded-xl text-left text-lg font-medium transition-all ${experience === opt.value ? 'bg-white text-gray-950' : 'bg-gray-900 text-gray-300 border border-gray-700 hover:border-gray-500'}`}>
              {opt.label}
            </button>
          ))}
        </div>
      ),
    },
    {
      title: 'Where are you based?',
      subtitle: 'City or remote — your call.',
      content: (
        <div>
          <input type="text" value={location} onChange={(e) => setLocation(e.target.value)} placeholder="e.g. San Francisco, CA" autoFocus
            className="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3.5 text-white text-lg placeholder:text-gray-600 focus:outline-none focus:border-white transition-colors mb-4" />
          <div className="flex flex-wrap gap-2">
            {LOCATION_SUGGESTIONS.map(l => (
              <button key={l} onClick={() => setLocation(l)}
                className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${location === l ? 'bg-white text-gray-950 font-medium' : 'bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-gray-200'}`}>
                {l}
              </button>
            ))}
          </div>
        </div>
      ),
    },
    {
      title: 'Your email?',
      subtitle: 'For your CV contact section.',
      content: (
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="john@example.com" autoFocus
          className="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3.5 text-white text-lg placeholder:text-gray-600 focus:outline-none focus:border-white transition-colors" />
      ),
    },
    {
      title: 'Phone number?',
      subtitle: 'Optional — skip if you prefer.',
      content: (
        <input type="tel" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="+1 (555) 123-4567" autoFocus
          className="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3.5 text-white text-lg placeholder:text-gray-600 focus:outline-none focus:border-white transition-colors" />
      ),
    },
    {
      title: 'LinkedIn profile?',
      subtitle: 'Optional — adds credibility to your CV.',
      content: (
        <div className="flex items-center bg-gray-900 border border-gray-700 rounded-xl overflow-hidden focus-within:border-white transition-colors">
          <span className="text-gray-500 text-sm pl-4 shrink-0">linkedin.com/in/</span>
          <input type="text" value={linkedin} onChange={(e) => setLinkedin(e.target.value)} placeholder="johndoe" autoFocus
            className="flex-1 bg-transparent px-2 py-3.5 text-white text-lg placeholder:text-gray-600 focus:outline-none" />
        </div>
      ),
    },
    {
      title: 'Your key skills?',
      subtitle: 'Add at least one. These go on your CV.',
      content: (
        <div>
          <div className="flex gap-2 mb-4">
            <input type="text" value={skillInput} onChange={(e) => setSkillInput(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addSkill(skillInput); } }}
              placeholder="Type a skill and press Enter" autoFocus
              className="flex-1 bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white placeholder:text-gray-600 focus:outline-none focus:border-white transition-colors" />
          </div>
          {skills.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-4">
              {skills.map(s => (
                <span key={s} className="bg-white text-gray-950 px-3 py-1.5 rounded-lg text-sm font-medium flex items-center gap-1.5">
                  {s}
                  <button onClick={() => removeSkill(s)} className="text-gray-400 hover:text-gray-600"><X className="w-3.5 h-3.5" /></button>
                </span>
              ))}
            </div>
          )}
          <div className="flex flex-wrap gap-2">
            {SKILL_SUGGESTIONS.filter(s => !skills.includes(s)).map(s => (
              <button key={s} onClick={() => addSkill(s)}
                className="px-3 py-1.5 rounded-lg text-sm bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-gray-200 transition-colors">
                + {s}
              </button>
            ))}
          </div>
        </div>
      ),
    },
    {
      title: 'Most recent job?',
      subtitle: 'Add your latest role. You can add more later.',
      content: (
        <div className="space-y-3">
          <input type="text" value={workExp.title} onChange={(e) => setWorkExp(p => ({ ...p, title: e.target.value }))} placeholder="Job title" autoFocus
            className="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white placeholder:text-gray-600 focus:outline-none focus:border-white transition-colors" />
          <input type="text" value={workExp.company} onChange={(e) => setWorkExp(p => ({ ...p, company: e.target.value }))} placeholder="Company"
            className="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white placeholder:text-gray-600 focus:outline-none focus:border-white transition-colors" />
          <div className="grid grid-cols-2 gap-3">
            <input type="text" value={workExp.start_date} onChange={(e) => setWorkExp(p => ({ ...p, start_date: e.target.value }))} placeholder="Start (e.g. Jan 2022)"
              className="bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white placeholder:text-gray-600 focus:outline-none focus:border-white transition-colors" />
            <input type="text" value={workExp.end_date} onChange={(e) => setWorkExp(p => ({ ...p, end_date: e.target.value }))} placeholder="End (or Present)"
              className="bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white placeholder:text-gray-600 focus:outline-none focus:border-white transition-colors" />
          </div>
          <p className="text-xs text-gray-500">Key achievements (up to 3 bullet points)</p>
          {workExp.bullets.map((b, i) => (
            <input key={i} type="text" value={b} onChange={(e) => { const bullets = [...workExp.bullets]; bullets[i] = e.target.value; setWorkExp(p => ({ ...p, bullets })); }}
              placeholder={`Achievement ${i + 1}`}
              className="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white placeholder:text-gray-600 focus:outline-none focus:border-white transition-colors" />
          ))}
        </div>
      ),
    },
    {
      title: 'Education?',
      subtitle: 'Optional — skip if not relevant.',
      content: (
        <div className="space-y-3">
          <input type="text" value={education.degree} onChange={(e) => setEducation(p => ({ ...p, degree: e.target.value }))} placeholder="Degree (e.g. B.S. Computer Science)" autoFocus
            className="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white placeholder:text-gray-600 focus:outline-none focus:border-white transition-colors" />
          <input type="text" value={education.school} onChange={(e) => setEducation(p => ({ ...p, school: e.target.value }))} placeholder="School / University"
            className="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white placeholder:text-gray-600 focus:outline-none focus:border-white transition-colors" />
          <input type="text" value={education.year} onChange={(e) => setEducation(p => ({ ...p, year: e.target.value }))} placeholder="Graduation year (e.g. 2023)"
            className="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white placeholder:text-gray-600 focus:outline-none focus:border-white transition-colors" />
        </div>
      ),
    },
    {
      title: 'What roles are you targeting?',
      subtitle: 'Optional — helps AI tailor your CV.',
      content: (
        <div>
          <div className="flex gap-2 mb-4">
            <input type="text" value={targetInput} onChange={(e) => setTargetInput(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addTargetRole(targetInput); } }}
              placeholder="Type a role and press Enter" autoFocus
              className="flex-1 bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white placeholder:text-gray-600 focus:outline-none focus:border-white transition-colors" />
          </div>
          {targetRoles.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-4">
              {targetRoles.map(r => (
                <span key={r} className="bg-white text-gray-950 px-3 py-1.5 rounded-lg text-sm font-medium flex items-center gap-1.5">
                  {r}
                  <button onClick={() => removeTargetRole(r)} className="text-gray-400 hover:text-gray-600"><X className="w-3.5 h-3.5" /></button>
                </span>
              ))}
            </div>
          )}
          <div className="flex flex-wrap gap-2">
            {TARGET_SUGGESTIONS.filter(r => !targetRoles.includes(r)).map(r => (
              <button key={r} onClick={() => addTargetRole(r)}
                className="px-3 py-1.5 rounded-lg text-sm bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-gray-200 transition-colors">
                + {r}
              </button>
            ))}
          </div>
        </div>
      ),
    },
  ];

  const cfg = stepConfigs[step];

  return (
    <OnboardingStep
      step={step}
      totalSteps={TOTAL_STEPS}
      title={cfg.title}
      subtitle={cfg.subtitle}
      onBack={back}
      onNext={next}
      onSkip={isSkippable() ? next : null}
      canContinue={canContinue() && !saving}
    >
      {cfg.content}
    </OnboardingStep>
  );
}
