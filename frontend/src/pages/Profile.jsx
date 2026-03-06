import { useState } from 'react';
import { Save, Plus, Trash2, LogOut } from 'lucide-react';
import { useApp } from '../lib/store';

export default function Profile() {
  const { user, updateUser, logout } = useApp();
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
        projects: form.projects,
        languages: form.languages,
        certifications: form.certifications,
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

  const removeSkill = (idx) => {
    setForm(f => ({ ...f, skills: f.skills.filter((_, i) => i !== idx) }));
  };

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

  const removeExperience = (idx) => {
    setForm(f => ({ ...f, work_experience: f.work_experience.filter((_, i) => i !== idx) }));
  };

  const addEducation = () => {
    setForm(f => ({
      ...f,
      education: [...(f.education || []), { degree: '', school: '', year: '' }],
    }));
  };

  const updateEducation = (idx, field, value) => {
    setForm(f => {
      const edu = [...(f.education || [])];
      edu[idx] = { ...edu[idx], [field]: value };
      return { ...f, education: edu };
    });
  };

  const removeEducation = (idx) => {
    setForm(f => ({ ...f, education: f.education.filter((_, i) => i !== idx) }));
  };

  const Input = ({ label, value, onChange, type = 'text', placeholder }) => (
    <div>
      <label className="block text-xs font-medium text-gray-500 mb-1">{label}</label>
      <input
        type={type}
        value={value || ''}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full bg-gray-50 border border-gray-200 rounded-xl px-3.5 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
      />
    </div>
  );

  return (
    <div className="max-w-2xl mx-auto px-4 py-6">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Profile</h1>
        <div className="flex items-center gap-2">
          <button
            onClick={save}
            disabled={saving}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white px-4 py-2 rounded-xl text-sm font-medium flex items-center gap-2 transition-colors"
          >
            <Save className="w-4 h-4" /> {saving ? 'Saving...' : 'Save'}
          </button>
          <button
            onClick={logout}
            className="p-2 rounded-xl hover:bg-red-50 text-gray-400 hover:text-red-600"
            title="Logout"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="space-y-6">
        {/* Basic Info */}
        <section className="bg-white rounded-xl border border-gray-200 p-5">
          <h2 className="font-semibold text-gray-900 mb-4">Basic Info</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <Input label="Full Name" value={form.full_name} onChange={v => setForm(f => ({ ...f, full_name: v }))} placeholder="John Doe" />
            <Input label="Job Title" value={form.title} onChange={v => setForm(f => ({ ...f, title: v }))} placeholder="Software Engineer" />
            <Input label="Email" value={form.email} onChange={v => setForm(f => ({ ...f, email: v }))} type="email" placeholder="john@example.com" />
            <Input label="Phone" value={form.phone} onChange={v => setForm(f => ({ ...f, phone: v }))} placeholder="+1 555-123-4567" />
            <Input label="Location" value={form.location} onChange={v => setForm(f => ({ ...f, location: v }))} placeholder="San Francisco, CA" />
            <Input label="Years of Experience" value={form.years_experience} onChange={v => setForm(f => ({ ...f, years_experience: parseInt(v) || 0 }))} type="number" />
          </div>
        </section>

        {/* Links */}
        <section className="bg-white rounded-xl border border-gray-200 p-5">
          <h2 className="font-semibold text-gray-900 mb-4">Links</h2>
          <div className="grid grid-cols-1 gap-3">
            <Input label="LinkedIn" value={form.linkedin} onChange={v => setForm(f => ({ ...f, linkedin: v }))} placeholder="linkedin.com/in/johndoe" />
            <Input label="GitHub" value={form.github} onChange={v => setForm(f => ({ ...f, github: v }))} placeholder="github.com/johndoe" />
            <Input label="Portfolio" value={form.portfolio} onChange={v => setForm(f => ({ ...f, portfolio: v }))} placeholder="johndoe.dev" />
          </div>
        </section>

        {/* Summary */}
        <section className="bg-white rounded-xl border border-gray-200 p-5">
          <h2 className="font-semibold text-gray-900 mb-4">Professional Summary</h2>
          <textarea
            value={form.summary || ''}
            onChange={(e) => setForm(f => ({ ...f, summary: e.target.value }))}
            rows={3}
            placeholder="Brief summary of your professional background..."
            className="w-full bg-gray-50 border border-gray-200 rounded-xl px-3.5 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          />
        </section>

        {/* Skills */}
        <section className="bg-white rounded-xl border border-gray-200 p-5">
          <h2 className="font-semibold text-gray-900 mb-4">Skills</h2>
          <div className="flex flex-wrap gap-1.5 mb-3">
            {(form.skills || []).map((s, i) => (
              <span key={i} className="bg-blue-50 text-blue-700 text-sm px-3 py-1 rounded-full flex items-center gap-1.5">
                {s}
                <button onClick={() => removeSkill(i)} className="text-blue-400 hover:text-blue-600">
                  <Trash2 className="w-3 h-3" />
                </button>
              </span>
            ))}
          </div>
          <div className="flex gap-2">
            <input
              value={newSkill}
              onChange={(e) => setNewSkill(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && addSkill()}
              placeholder="Add a skill..."
              className="flex-1 bg-gray-50 border border-gray-200 rounded-xl px-3.5 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button onClick={addSkill} className="bg-gray-100 hover:bg-gray-200 px-3 py-2 rounded-xl">
              <Plus className="w-4 h-4 text-gray-600" />
            </button>
          </div>
        </section>

        {/* Experience */}
        <section className="bg-white rounded-xl border border-gray-200 p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-gray-900">Work Experience</h2>
            <button onClick={addExperience} className="text-sm text-blue-600 hover:text-blue-700 flex items-center gap-1">
              <Plus className="w-3.5 h-3.5" /> Add
            </button>
          </div>
          <div className="space-y-4">
            {(form.work_experience || []).map((exp, i) => (
              <div key={i} className="bg-gray-50 rounded-xl p-4 relative">
                <button
                  onClick={() => removeExperience(i)}
                  className="absolute top-3 right-3 text-gray-400 hover:text-red-500"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mb-2">
                  <input
                    value={exp.title || ''}
                    onChange={(e) => updateExperience(i, 'title', e.target.value)}
                    placeholder="Job title"
                    className="bg-white border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <input
                    value={exp.company || ''}
                    onChange={(e) => updateExperience(i, 'company', e.target.value)}
                    placeholder="Company"
                    className="bg-white border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <input
                    value={exp.start || ''}
                    onChange={(e) => updateExperience(i, 'start', e.target.value)}
                    placeholder="Start (e.g., Jan 2022)"
                    className="bg-white border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <input
                    value={exp.end || ''}
                    onChange={(e) => updateExperience(i, 'end', e.target.value)}
                    placeholder="End (or Present)"
                    className="bg-white border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <textarea
                  value={(exp.bullets || []).join('\n')}
                  onChange={(e) => updateExperience(i, 'bullets', e.target.value.split('\n').filter(Boolean))}
                  placeholder="Bullet points (one per line)"
                  rows={3}
                  className="w-full bg-white border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                />
              </div>
            ))}
          </div>
        </section>

        {/* Education */}
        <section className="bg-white rounded-xl border border-gray-200 p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-gray-900">Education</h2>
            <button onClick={addEducation} className="text-sm text-blue-600 hover:text-blue-700 flex items-center gap-1">
              <Plus className="w-3.5 h-3.5" /> Add
            </button>
          </div>
          <div className="space-y-3">
            {(form.education || []).map((edu, i) => (
              <div key={i} className="bg-gray-50 rounded-xl p-3 flex items-center gap-2">
                <div className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-2">
                  <input
                    value={edu.degree || ''}
                    onChange={(e) => updateEducation(i, 'degree', e.target.value)}
                    placeholder="Degree"
                    className="bg-white border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <input
                    value={edu.school || ''}
                    onChange={(e) => updateEducation(i, 'school', e.target.value)}
                    placeholder="School"
                    className="bg-white border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <input
                    value={edu.year || ''}
                    onChange={(e) => updateEducation(i, 'year', e.target.value)}
                    placeholder="Year"
                    className="bg-white border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <button onClick={() => removeEducation(i)} className="text-gray-400 hover:text-red-500 p-1">
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            ))}
          </div>
        </section>
      </div>

      {/* Bottom save */}
      <div className="mt-6 mb-20 md:mb-6">
        <button
          onClick={save}
          disabled={saving}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white py-3 rounded-xl text-sm font-medium transition-colors"
        >
          {saving ? 'Saving...' : 'Save Profile'}
        </button>
      </div>
    </div>
  );
}
