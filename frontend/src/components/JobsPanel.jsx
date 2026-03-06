import { useState, useEffect } from 'react';
import { Globe, FileText, Plus, Trash2, ExternalLink, Loader2, X, ChevronDown } from 'lucide-react';
import { useApp } from '../lib/store';
import { api } from '../lib/api';

const STATUS_COLORS = {
  saved: 'bg-gray-700 text-gray-300',
  applied: 'bg-blue-900/50 text-blue-300',
  interview: 'bg-yellow-900/50 text-yellow-300',
  offer: 'bg-green-900/50 text-green-300',
  rejected: 'bg-red-900/50 text-red-300',
};

export default function JobsPanel() {
  const { user, jobsPanelOpen, setJobsPanelOpen } = useApp();
  const [vacancies, setVacancies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAdd, setShowAdd] = useState(false);
  const [addMode, setAddMode] = useState('url');
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
    } catch (e) { alert(e.message); }
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
    } catch (e) { alert(e.message); }
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
    } catch (e) { alert(e.message); }
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

  const panelContent = (
    <div className="h-full flex flex-col bg-gray-950 border-l border-gray-800">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-800">
        <h2 className="font-semibold text-white text-sm">Jobs</h2>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowAdd(true)}
            className="text-gray-400 hover:text-white transition-colors"
            title="Add Job"
          >
            <Plus className="w-4 h-4" />
          </button>
          <button
            onClick={() => setJobsPanelOpen(false)}
            className="md:hidden text-gray-400 hover:text-white"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Job list */}
      <div className="flex-1 overflow-y-auto px-3 py-3 space-y-2">
        {loading ? (
          <div className="text-center py-8 text-gray-500 text-sm">Loading...</div>
        ) : vacancies.length === 0 ? (
          <div className="text-center py-8">
            <Globe className="w-8 h-8 text-gray-700 mx-auto mb-2" />
            <p className="text-xs text-gray-500">No jobs tracked yet</p>
            <button
              onClick={() => setShowAdd(true)}
              className="text-xs text-blue-400 hover:text-blue-300 mt-1"
            >
              Add your first job
            </button>
          </div>
        ) : (
          vacancies.map(v => (
            <div key={v.id} className="bg-gray-900 rounded-xl p-3 border border-gray-800 hover:border-gray-700 transition-colors">
              <div className="flex items-start justify-between gap-2">
                <div className="min-w-0 flex-1">
                  <h3 className="text-sm font-medium text-white truncate">{v.title || 'Untitled'}</h3>
                  <p className="text-xs text-gray-500 truncate">{v.company}{v.location ? ` · ${v.location}` : ''}</p>
                </div>
                <div className="flex items-center gap-1 shrink-0">
                  {v.url && (
                    <a href={v.url} target="_blank" rel="noopener noreferrer" className="text-gray-600 hover:text-gray-400 p-1">
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  )}
                  <button onClick={() => deleteVacancy(v.id)} className="text-gray-600 hover:text-red-400 p-1">
                    <Trash2 className="w-3 h-3" />
                  </button>
                </div>
              </div>
              <div className="flex gap-1 mt-2 flex-wrap">
                {Object.keys(STATUS_COLORS).map(s => (
                  <button
                    key={s}
                    onClick={() => updateStatus(v.id, s)}
                    className={`text-[10px] px-2 py-0.5 rounded-full transition-colors ${
                      v.status === s ? STATUS_COLORS[s] : 'text-gray-600 hover:text-gray-400'
                    }`}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          ))
        )}
      </div>

      {/* Add modal */}
      {showAdd && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5 w-full max-w-lg">
            <h2 className="text-lg font-bold text-white mb-4">Add Job</h2>

            <div className="flex gap-1 bg-gray-800 rounded-xl p-1 mb-4">
              {[
                { id: 'url', label: 'Link', icon: Globe },
                { id: 'text', label: 'Paste', icon: FileText },
                { id: 'manual', label: 'Manual', icon: Plus },
              ].map(({ id, label, icon: Icon }) => (
                <button
                  key={id}
                  onClick={() => setAddMode(id)}
                  className={`flex-1 flex items-center justify-center gap-1.5 py-2 rounded-lg text-sm font-medium transition-colors ${
                    addMode === id ? 'bg-gray-700 text-white' : 'text-gray-500'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" /> {label}
                </button>
              ))}
            </div>

            {addMode === 'url' && (
              <div>
                <input type="url" placeholder="https://linkedin.com/jobs/..." value={urlInput} onChange={(e) => setUrlInput(e.target.value)}
                  className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-2.5 text-sm text-white placeholder:text-gray-600 mb-3 focus:outline-none focus:border-gray-500" />
                <button onClick={addFromUrl} disabled={submitting || !urlInput.trim()}
                  className="w-full bg-white hover:bg-gray-100 disabled:bg-gray-700 disabled:text-gray-500 text-gray-950 py-2.5 rounded-xl text-sm font-medium flex items-center justify-center gap-2">
                  {submitting ? <><Loader2 className="w-4 h-4 animate-spin" /> Parsing...</> : 'Parse & Add'}
                </button>
              </div>
            )}

            {addMode === 'text' && (
              <div>
                <textarea placeholder="Paste job description..." value={textInput} onChange={(e) => setTextInput(e.target.value)} rows={5}
                  className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-2.5 text-sm text-white placeholder:text-gray-600 mb-3 focus:outline-none focus:border-gray-500 resize-none" />
                <button onClick={addFromText} disabled={submitting || !textInput.trim()}
                  className="w-full bg-white hover:bg-gray-100 disabled:bg-gray-700 disabled:text-gray-500 text-gray-950 py-2.5 rounded-xl text-sm font-medium flex items-center justify-center gap-2">
                  {submitting ? <><Loader2 className="w-4 h-4 animate-spin" /> Parsing...</> : 'Parse & Add'}
                </button>
              </div>
            )}

            {addMode === 'manual' && (
              <div className="space-y-3">
                <input type="text" placeholder="Job title" value={manualData.title} onChange={(e) => setManualData(p => ({ ...p, title: e.target.value }))}
                  className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-2.5 text-sm text-white placeholder:text-gray-600 focus:outline-none focus:border-gray-500" />
                <input type="text" placeholder="Company" value={manualData.company} onChange={(e) => setManualData(p => ({ ...p, company: e.target.value }))}
                  className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-2.5 text-sm text-white placeholder:text-gray-600 focus:outline-none focus:border-gray-500" />
                <textarea placeholder="Description (optional)" value={manualData.description} onChange={(e) => setManualData(p => ({ ...p, description: e.target.value }))} rows={3}
                  className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-2.5 text-sm text-white placeholder:text-gray-600 focus:outline-none focus:border-gray-500 resize-none" />
                <button onClick={addManual} disabled={submitting || !manualData.title.trim()}
                  className="w-full bg-white hover:bg-gray-100 disabled:bg-gray-700 disabled:text-gray-500 text-gray-950 py-2.5 rounded-xl text-sm font-medium">
                  Add Job
                </button>
              </div>
            )}

            <button onClick={() => setShowAdd(false)} className="w-full mt-2 py-2 text-sm text-gray-500 hover:text-gray-300">Cancel</button>
          </div>
        </div>
      )}
    </div>
  );

  return (
    <>
      {/* Desktop panel */}
      <div className="hidden md:block w-80 shrink-0">
        {panelContent}
      </div>

      {/* Mobile bottom sheet */}
      {jobsPanelOpen && (
        <div className="md:hidden fixed inset-0 z-50 flex flex-col justify-end">
          <div className="flex-1 bg-black/60 animate-fade-in" onClick={() => setJobsPanelOpen(false)} />
          <div className="h-[70vh] animate-slide-right">
            {panelContent}
          </div>
        </div>
      )}
    </>
  );
}
