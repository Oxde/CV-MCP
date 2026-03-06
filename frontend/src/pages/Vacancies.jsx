import { useState, useEffect } from 'react';
import { Link, Globe, FileText, Plus, Trash2, ExternalLink, Loader2 } from 'lucide-react';
import { useApp } from '../lib/store';
import { api } from '../lib/api';

const STATUS_COLORS = {
  saved: 'bg-gray-100 text-gray-600',
  applied: 'bg-blue-100 text-blue-700',
  interview: 'bg-yellow-100 text-yellow-700',
  offer: 'bg-green-100 text-green-700',
  rejected: 'bg-red-100 text-red-600',
};

export default function Vacancies() {
  const { user } = useApp();
  const [vacancies, setVacancies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAdd, setShowAdd] = useState(false);
  const [addMode, setAddMode] = useState('url'); // url, text, manual
  const [urlInput, setUrlInput] = useState('');
  const [textInput, setTextInput] = useState('');
  const [manualData, setManualData] = useState({ title: '', company: '', description: '' });
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (user) {
      api.listVacancies(user.id).then(setVacancies).finally(() => setLoading(false));
    }
  }, [user]);

  const addFromUrl = async () => {
    if (!urlInput.trim()) return;
    setSubmitting(true);
    try {
      const v = await api.createVacancyFromUrl({ user_id: user.id, url: urlInput.trim() });
      setVacancies(prev => [v, ...prev]);
      setShowAdd(false);
      setUrlInput('');
    } catch (e) {
      alert(e.message);
    }
    setSubmitting(false);
  };

  const addFromText = async () => {
    if (!textInput.trim()) return;
    setSubmitting(true);
    try {
      const v = await api.createVacancyFromText({ user_id: user.id, text: textInput.trim() });
      setVacancies(prev => [v, ...prev]);
      setShowAdd(false);
      setTextInput('');
    } catch (e) {
      alert(e.message);
    }
    setSubmitting(false);
  };

  const addManual = async () => {
    if (!manualData.title.trim()) return;
    setSubmitting(true);
    try {
      const v = await api.createVacancy({ user_id: user.id, ...manualData });
      setVacancies(prev => [v, ...prev]);
      setShowAdd(false);
      setManualData({ title: '', company: '', description: '' });
    } catch (e) {
      alert(e.message);
    }
    setSubmitting(false);
  };

  const updateStatus = async (id, status) => {
    await api.updateVacancy(id, { status });
    setVacancies(prev => prev.map(v => v.id === id ? { ...v, status } : v));
  };

  const deleteVacancy = async (id) => {
    if (!confirm('Delete this vacancy?')) return;
    await api.deleteVacancy(id);
    setVacancies(prev => prev.filter(v => v.id !== id));
  };

  if (loading) {
    return <div className="flex items-center justify-center h-64 text-gray-400">Loading...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Job Vacancies</h1>
          <p className="text-sm text-gray-500">{vacancies.length} position{vacancies.length !== 1 ? 's' : ''} tracked</p>
        </div>
        <button
          onClick={() => setShowAdd(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl text-sm font-medium flex items-center gap-2"
        >
          <Plus className="w-4 h-4" /> Add Job
        </button>
      </div>

      {/* Add vacancy modal */}
      {showAdd && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl p-6 w-full max-w-lg">
            <h2 className="text-lg font-bold mb-4">Add Vacancy</h2>

            {/* Mode tabs */}
            <div className="flex gap-1 bg-gray-100 rounded-xl p-1 mb-4">
              {[
                { id: 'url', label: 'From Link', icon: Globe },
                { id: 'text', label: 'Paste Text', icon: FileText },
                { id: 'manual', label: 'Manual', icon: Plus },
              ].map(({ id, label, icon: Icon }) => (
                <button
                  key={id}
                  onClick={() => setAddMode(id)}
                  className={`flex-1 flex items-center justify-center gap-1.5 py-2 rounded-lg text-sm font-medium transition-colors ${
                    addMode === id ? 'bg-white shadow text-blue-600' : 'text-gray-500'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" /> {label}
                </button>
              ))}
            </div>

            {addMode === 'url' && (
              <div>
                <p className="text-sm text-gray-500 mb-2">Paste a job posting URL (LinkedIn, Indeed, etc.)</p>
                <input
                  type="url"
                  placeholder="https://linkedin.com/jobs/..."
                  value={urlInput}
                  onChange={(e) => setUrlInput(e.target.value)}
                  className="w-full bg-gray-100 rounded-xl px-4 py-2.5 text-sm mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                  onClick={addFromUrl}
                  disabled={submitting || !urlInput.trim()}
                  className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white py-2.5 rounded-xl text-sm font-medium flex items-center justify-center gap-2"
                >
                  {submitting ? <><Loader2 className="w-4 h-4 animate-spin" /> Parsing...</> : 'Parse & Add'}
                </button>
              </div>
            )}

            {addMode === 'text' && (
              <div>
                <p className="text-sm text-gray-500 mb-2">Paste the job description text</p>
                <textarea
                  placeholder="Copy and paste the full job posting here..."
                  value={textInput}
                  onChange={(e) => setTextInput(e.target.value)}
                  rows={6}
                  className="w-full bg-gray-100 rounded-xl px-4 py-2.5 text-sm mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                />
                <button
                  onClick={addFromText}
                  disabled={submitting || !textInput.trim()}
                  className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white py-2.5 rounded-xl text-sm font-medium flex items-center justify-center gap-2"
                >
                  {submitting ? <><Loader2 className="w-4 h-4 animate-spin" /> Parsing...</> : 'Parse & Add'}
                </button>
              </div>
            )}

            {addMode === 'manual' && (
              <div className="space-y-3">
                <input
                  type="text"
                  placeholder="Job title"
                  value={manualData.title}
                  onChange={(e) => setManualData(p => ({ ...p, title: e.target.value }))}
                  className="w-full bg-gray-100 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <input
                  type="text"
                  placeholder="Company"
                  value={manualData.company}
                  onChange={(e) => setManualData(p => ({ ...p, company: e.target.value }))}
                  className="w-full bg-gray-100 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <textarea
                  placeholder="Description (optional)"
                  value={manualData.description}
                  onChange={(e) => setManualData(p => ({ ...p, description: e.target.value }))}
                  rows={3}
                  className="w-full bg-gray-100 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                />
                <button
                  onClick={addManual}
                  disabled={submitting || !manualData.title.trim()}
                  className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white py-2.5 rounded-xl text-sm font-medium"
                >
                  Add Vacancy
                </button>
              </div>
            )}

            <button
              onClick={() => setShowAdd(false)}
              className="w-full mt-2 py-2 text-sm text-gray-400 hover:text-gray-600"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {/* Vacancy list */}
      {vacancies.length === 0 ? (
        <div className="text-center py-16">
          <Globe className="w-12 h-12 text-gray-300 mx-auto mb-3" />
          <p className="text-gray-500 mb-1">No vacancies yet</p>
          <p className="text-sm text-gray-400">Add a job posting to start tailoring your CV</p>
        </div>
      ) : (
        <div className="grid gap-3">
          {vacancies.map(v => (
            <div key={v.id} className="bg-white rounded-xl border border-gray-200 p-4 hover:shadow-sm transition-shadow">
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="font-semibold text-gray-900 text-sm truncate">{v.title || 'Untitled'}</h3>
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${STATUS_COLORS[v.status]}`}>
                      {v.status}
                    </span>
                  </div>
                  <p className="text-sm text-gray-500">{v.company}{v.location ? ` · ${v.location}` : ''}</p>
                  {v.description && (
                    <p className="text-xs text-gray-400 mt-1 line-clamp-2">{v.description}</p>
                  )}
                  {v.requirements?.length > 0 && (
                    <div className="flex flex-wrap gap-1 mt-2">
                      {v.requirements.slice(0, 5).map((r, i) => (
                        <span key={i} className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">{r}</span>
                      ))}
                      {v.requirements.length > 5 && (
                        <span className="text-xs text-gray-400">+{v.requirements.length - 5}</span>
                      )}
                    </div>
                  )}
                </div>
                <div className="flex items-center gap-1 ml-2">
                  {v.url && (
                    <a
                      href={v.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="p-2 rounded-lg hover:bg-gray-100 text-gray-400 hover:text-gray-600"
                    >
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  )}
                  <button
                    onClick={() => deleteVacancy(v.id)}
                    className="p-2 rounded-lg hover:bg-red-50 text-gray-400 hover:text-red-600"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Status selector */}
              <div className="flex gap-1 mt-3 flex-wrap">
                {Object.keys(STATUS_COLORS).map(s => (
                  <button
                    key={s}
                    onClick={() => updateStatus(v.id, s)}
                    className={`text-xs px-2.5 py-1 rounded-full border transition-colors ${
                      v.status === s
                        ? STATUS_COLORS[s] + ' border-current'
                        : 'border-gray-200 text-gray-400 hover:border-gray-300'
                    }`}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
