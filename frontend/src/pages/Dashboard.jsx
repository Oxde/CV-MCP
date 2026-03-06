import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, FileText, Download, Trash2, Eye, Palette } from 'lucide-react';
import { useApp } from '../lib/store';
import { api } from '../lib/api';

export default function Dashboard() {
  const navigate = useNavigate();
  const { user } = useApp();
  const [cvs, setCvs] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [showCreate, setShowCreate] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState('modern');
  const [cvName, setCvName] = useState('');
  const [previewCv, setPreviewCv] = useState(null);

  useEffect(() => {
    if (user) {
      Promise.all([
        api.listCVs(user.id),
        api.listTemplates(),
      ]).then(([c, t]) => {
        setCvs(c);
        setTemplates(t);
      }).finally(() => setLoading(false));
    }
  }, [user]);

  const createCV = async () => {
    setCreating(true);
    try {
      const cv = await api.createCV({
        user_id: user.id,
        name: cvName || 'My CV',
        template_id: selectedTemplate,
      });
      setCvs(prev => [cv, ...prev]);
      setShowCreate(false);
      setCvName('');
    } catch (e) {
      alert(e.message);
    }
    setCreating(false);
  };

  const downloadPDF = async (cv) => {
    try {
      const res = await api.exportPDF(cv.id);
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${cv.name}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      alert('PDF generation failed: ' + e.message);
    }
  };

  const deleteCV = async (id) => {
    if (!confirm('Delete this CV?')) return;
    await api.deleteCV(id);
    setCvs(prev => prev.filter(c => c.id !== id));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-400">Loading...</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">My CVs</h1>
          <p className="text-sm text-gray-500">{cvs.length} resume{cvs.length !== 1 ? 's' : ''}</p>
        </div>
        <button
          onClick={() => setShowCreate(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl text-sm font-medium flex items-center gap-2 transition-colors"
        >
          <Plus className="w-4 h-4" /> New CV
        </button>
      </div>

      {/* Create CV modal */}
      {showCreate && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl p-6 w-full max-w-lg max-h-[90vh] overflow-y-auto">
            <h2 className="text-lg font-bold mb-4">Create New CV</h2>
            <input
              type="text"
              placeholder="CV name (e.g., 'Google SWE')"
              value={cvName}
              onChange={(e) => setCvName(e.target.value)}
              className="w-full bg-gray-100 rounded-xl px-4 py-2.5 text-sm mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <p className="text-sm font-medium text-gray-700 mb-2">Choose a template:</p>
            <div className="grid grid-cols-2 gap-2 mb-4">
              {templates.map(t => (
                <button
                  key={t.id}
                  onClick={() => setSelectedTemplate(t.id)}
                  className={`text-left p-3 rounded-xl border-2 transition-colors ${
                    selectedTemplate === t.id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-center gap-2 mb-1">
                    <div className="w-3 h-3 rounded-full" style={{ background: t.preview_color }} />
                    <span className="text-sm font-semibold">{t.name}</span>
                  </div>
                  <p className="text-xs text-gray-500">{t.description}</p>
                </button>
              ))}
            </div>
            <div className="flex gap-2">
              <button
                onClick={createCV}
                disabled={creating}
                className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white py-2.5 rounded-xl text-sm font-medium transition-colors"
              >
                {creating ? 'Creating...' : 'Create CV'}
              </button>
              <button
                onClick={() => setShowCreate(false)}
                className="px-4 py-2.5 rounded-xl text-sm text-gray-600 hover:bg-gray-100"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* CV Preview modal */}
      {previewCv && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl w-full max-w-4xl h-[90vh] flex flex-col">
            <div className="flex items-center justify-between p-4 border-b">
              <h2 className="font-bold">{previewCv.name}</h2>
              <button onClick={() => setPreviewCv(null)} className="text-gray-400 hover:text-gray-600 text-xl">✕</button>
            </div>
            <iframe
              srcDoc={previewCv.html_content}
              className="flex-1 w-full"
              title="CV Preview"
            />
          </div>
        </div>
      )}

      {/* CV list */}
      {cvs.length === 0 ? (
        <div className="text-center py-16">
          <FileText className="w-12 h-12 text-gray-300 mx-auto mb-3" />
          <p className="text-gray-500 mb-1">No CVs yet</p>
          <p className="text-sm text-gray-400">Create your first CV to get started</p>
        </div>
      ) : (
        <div className="grid gap-3">
          {cvs.map(cv => (
            <div key={cv.id} className="bg-white rounded-xl border border-gray-200 p-4 flex items-center justify-between hover:shadow-sm transition-shadow">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center">
                  <FileText className="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 text-sm">{cv.name}</h3>
                  <p className="text-xs text-gray-400">Template: {cv.template_id}</p>
                </div>
              </div>
              <div className="flex items-center gap-1">
                <button
                  onClick={() => setPreviewCv(cv)}
                  className="p-2 rounded-lg hover:bg-gray-100 text-gray-400 hover:text-gray-600"
                  title="Preview"
                >
                  <Eye className="w-4 h-4" />
                </button>
                <button
                  onClick={() => navigate(`/chat?cv=${cv.id}`)}
                  className="p-2 rounded-lg hover:bg-blue-50 text-gray-400 hover:text-blue-600"
                  title="Edit with AI"
                >
                  <Palette className="w-4 h-4" />
                </button>
                <button
                  onClick={() => downloadPDF(cv)}
                  className="p-2 rounded-lg hover:bg-green-50 text-gray-400 hover:text-green-600"
                  title="Download PDF"
                >
                  <Download className="w-4 h-4" />
                </button>
                <button
                  onClick={() => deleteCV(cv.id)}
                  className="p-2 rounded-lg hover:bg-red-50 text-gray-400 hover:text-red-600"
                  title="Delete"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
