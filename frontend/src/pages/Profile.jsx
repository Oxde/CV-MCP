import { useState } from 'react';
import { Save, Plus, Trash2, X } from 'lucide-react';
import { useApp } from '../lib/store';

export default function Profile() {
  const { user, updateUser } = useApp();
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState({ ...user });
  const [newSkill, setNewSkill] = useState('');

  const save = async () => {
    setSaving(true);
    try {
      await updateUser({
        full_name: form.full_name,
        email: form.email,
        phone: form.phone,
        location: form.location,
        linkedin: form.linkedin,
        github: form.github,
        portfolio: form.portfolio,
        title: form.title,
        summary: form.summary,
        years_experience: form.years_experience,
        skills: form.skills,
        education: form.education,
        work_experience: form.work_experience,
        target_roles: form.target_roles,
      });
    } catch (e) {
      alert(e.message);
    }
    setSaving(false);
  };

  const addSkill = () => {
    if (!newSkill.trim()) return;
    setForm(f => ({ ...f, skills: [...(f.skills || []), newSkill.trim()] }));
    setNewSkill('');
  };
  const removeSkill = (idx) => setForm(f => ({ ...f, skills: f.skills.filter((_, i) => i !== idx) }));

  const addExperience = () => {
    setForm(f => ({
      ...f,
      work_experience: [...(f.work_experience || []), { company: '', title: '', start: '', end: '', bullets: [] }],
    }));
  };
  const updateExperience = (idx, field, value) => {
    setForm(f => {
      const exp = [...(f.work_experience || [])];
      exp[idx] = { ...exp[idx], [field]: value };
      return { ...f, work_experience: exp };
    });
  };
  const removeExperience = (idx) => setForm(f => ({ ...f, work_experience: f.work_experience.filter((_, i) => i !== idx) }));

  const addEducation = () => {
    setForm(f => ({ ...f, education: [...(f.education || []), { degree: '', school: '', year: '' }] }));
  };
  const updateEducation = (idx, field, value) => {
    setForm(f => {
      const edu = [...(f.education || [])];
      edu[idx] = { ...edu[idx], [field]: value };
      return { ...f, education: edu };
    });
  };
  const removeEducation = (idx) => setForm(f => ({ ...f, education: f.education.filter((_, i) => i !== idx) }));

  const inputClass = "w-full bg-gray-800 border border-gray-700 rounded-xl px-3.5 py-2 text-sm text-white placeholder:text-gray-600 focus:outline-none focus:border-gray-500 transition-colors";

  return (
    <div className="max-w-2xl mx-auto px-4 py-6">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-xl font-bold text-white">Profile</h1>
        <button
          onClick={save}
          disabled={saving}
          className="bg-white hover:bg-gray-100 disabled:bg-gray-700 disabled:text-gray-500 text-gray-950 px-4 py-2 rounded-xl text-sm font-medium flex items-center gap-2 transition-colors"
        >
          <Save className="w-4 h-4" /> {saving ? 'Saving...' : 'Save'}
        </button>
      </div>

      <div className="space-y-6">
        {/* Basic Info */}
        <section className="bg-gray-900 rounded-xl border border-gray-800 p-5">
          <h2 className="font-semibold text-white mb-4 text-sm">Basic Info</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs text-gray-500 mb-1">Full Name</label>
              <input value={form.full_name || ''} onChange={(e) => setForm(f => ({ ...f, full_name: e.target.value }))} placeholder="John Doe" className={inputClass} />
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">Job Title</label>
              <input value={form.title || ''} onChange={(e) => setForm(f => ({ ...f, title: e.target.value }))} placeholder="Software Engineer" className={inputClass} />
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">Email</label>
              <input type="email" value={form.email || ''} onChange={(e) => setForm(f => ({ ...f, email: e.target.value }))} placeholder="john@example.com" className={inputClass} />
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">Phone</label>
              <input value={form.phone || ''} onChange={(e) => setForm(f => ({ ...f, phone: e.target.value }))} placeholder="+1 555-123-4567" className={inputClass} />
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">Location</label>
              <input value={form.location || ''} onChange={(e) => setForm(f => ({ ...f, location: e.target.value }))} placeholder="San Francisco, CA" className={inputClass} />
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">Experience</label>
              <input value={form.years_experience || ''} onChange={(e) => setForm(f => ({ ...f, years_experience: e.target.value }))} placeholder="e.g. 3-5" className={inputClass} />
            </div>
          </div>
        </section>

        {/* Links */}
        <section className="bg-gray-900 rounded-xl border border-gray-800 p-5">
          <h2 className="font-semibold text-white mb-4 text-sm">Links</h2>
          <div className="grid grid-cols-1 gap-3">
            <div>
              <label className="block text-xs text-gray-500 mb-1">LinkedIn</label>
              <input value={form.linkedin || ''} onChange={(e) => setForm(f => ({ ...f, linkedin: e.target.value }))} placeholder="linkedin.com/in/johndoe" className={inputClass} />
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">GitHub</label>
              <input value={form.github || ''} onChange={(e) => setForm(f => ({ ...f, github: e.target.value }))} placeholder="github.com/johndoe" className={inputClass} />
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">Portfolio</label>
              <input value={form.portfolio || ''} onChange={(e) => setForm(f => ({ ...f, portfolio: e.target.value }))} placeholder="johndoe.dev" className={inputClass} />
            </div>
          </div>
        </section>

        {/* Summary */}
        <section className="bg-gray-900 rounded-xl border border-gray-800 p-5">
          <h2 className="font-semibold text-white mb-4 text-sm">Professional Summary</h2>
          <textarea
            value={form.summary || ''}
            onChange={(e) => setForm(f => ({ ...f, summary: e.target.value }))}
            rows={3}
            placeholder="Brief summary of your professional background..."
            className="w-full bg-gray-800 border border-gray-700 rounded-xl px-3.5 py-2 text-sm text-white placeholder:text-gray-600 focus:outline-none focus:border-gray-500 resize-none"
          />
        </section>

        {/* Skills */}
        <section className="bg-gray-900 rounded-xl border border-gray-800 p-5">
          <h2 className="font-semibold text-white mb-4 text-sm">Skills</h2>
          <div className="flex flex-wrap gap-1.5 mb-3">
            {(form.skills || []).map((s, i) => (
              <span key={i} className="bg-gray-800 text-gray-300 text-sm px-3 py-1 rounded-full flex items-center gap-1.5">
                {s}
                <button onClick={() => removeSkill(i)} className="text-gray-500 hover:text-red-400">
                  <X className="w-3 h-3" />
                </button>
              </span>
            ))}
          </div>
          <div className="flex gap-2">
            <input value={newSkill} onChange={(e) => setNewSkill(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && addSkill()}
              placeholder="Add a skill..." className={inputClass + " flex-1"} />
            <button onClick={addSkill} className="bg-gray-800 hover:bg-gray-700 px-3 py-2 rounded-xl">
              <Plus className="w-4 h-4 text-gray-400" />
            </button>
          </div>
        </section>

        {/* Experience */}
        <section className="bg-gray-900 rounded-xl border border-gray-800 p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-white text-sm">Work Experience</h2>
            <button onClick={addExperience} className="text-sm text-gray-400 hover:text-white flex items-center gap-1">
              <Plus className="w-3.5 h-3.5" /> Add
            </button>
          </div>
          <div className="space-y-4">
            {(form.work_experience || []).map((exp, i) => (
              <div key={i} className="bg-gray-800 rounded-xl p-4 relative">
                <button onClick={() => removeExperience(i)} className="absolute top-3 right-3 text-gray-600 hover:text-red-400">
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mb-2">
                  <input value={exp.title || ''} onChange={(e) => updateExperience(i, 'title', e.target.value)} placeholder="Job title"
                    className="bg-gray-900 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-white placeholder:text-gray-600 focus:outline-none focus:border-gray-500" />
                  <input value={exp.company || ''} onChange={(e) => updateExperience(i, 'company', e.target.value)} placeholder="Company"
                    className="bg-gray-900 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-white placeholder:text-gray-600 focus:outline-none focus:border-gray-500" />
                  <input value={exp.start || ''} onChange={(e) => updateExperience(i, 'start', e.target.value)} placeholder="Start date"
                    className="bg-gray-900 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-white placeholder:text-gray-600 focus:outline-none focus:border-gray-500" />
                  <input value={exp.end || ''} onChange={(e) => updateExperience(i, 'end', e.target.value)} placeholder="End date"
                    className="bg-gray-900 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-white placeholder:text-gray-600 focus:outline-none focus:border-gray-500" />
                </div>
                <textarea value={(exp.bullets || []).join('\n')} onChange={(e) => updateExperience(i, 'bullets', e.target.value.split('\n').filter(Boolean))}
                  placeholder="Bullet points (one per line)" rows={3}
                  className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-white placeholder:text-gray-600 focus:outline-none focus:border-gray-500 resize-none" />
              </div>
            ))}
          </div>
        </section>

        {/* Education */}
        <section className="bg-gray-900 rounded-xl border border-gray-800 p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-white text-sm">Education</h2>
            <button onClick={addEducation} className="text-sm text-gray-400 hover:text-white flex items-center gap-1">
              <Plus className="w-3.5 h-3.5" /> Add
            </button>
          </div>
          <div className="space-y-3">
            {(form.education || []).map((edu, i) => (
              <div key={i} className="bg-gray-800 rounded-xl p-3 flex items-center gap-2">
                <div className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-2">
                  <input value={edu.degree || ''} onChange={(e) => updateEducation(i, 'degree', e.target.value)} placeholder="Degree"
                    className="bg-gray-900 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-white placeholder:text-gray-600 focus:outline-none focus:border-gray-500" />
                  <input value={edu.school || ''} onChange={(e) => updateEducation(i, 'school', e.target.value)} placeholder="School"
                    className="bg-gray-900 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-white placeholder:text-gray-600 focus:outline-none focus:border-gray-500" />
                  <input value={edu.year || ''} onChange={(e) => updateEducation(i, 'year', e.target.value)} placeholder="Year"
                    className="bg-gray-900 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-white placeholder:text-gray-600 focus:outline-none focus:border-gray-500" />
                </div>
                <button onClick={() => removeEducation(i)} className="text-gray-600 hover:text-red-400 p-1">
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            ))}
          </div>
        </section>
      </div>

      <div className="mt-6 pb-6">
        <button
          onClick={save}
          disabled={saving}
          className="w-full bg-white hover:bg-gray-100 disabled:bg-gray-700 disabled:text-gray-500 text-gray-950 py-3 rounded-xl text-sm font-medium transition-colors"
        >
          {saving ? 'Saving...' : 'Save Profile'}
        </button>
      </div>
    </div>
  );
}
