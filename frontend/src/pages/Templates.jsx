import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Eye, Plus } from 'lucide-react';
import { useApp } from '../lib/store';
import { api } from '../lib/api';

export default function Templates() {
  const navigate = useNavigate();
  const { user, setSelectedCvId, refreshCvs } = useApp();
  const [templates, setTemplates] = useState([]);
  const [previewId, setPreviewId] = useState(null);
  const [previewHtml, setPreviewHtml] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.listTemplates().then(setTemplates).finally(() => setLoading(false));
  }, []);

  const previewTemplate = async (templateId) => {
    setPreviewId(templateId);
    try {
      const cv = await api.createCV({
        user_id: user.id,
        name: `Preview - ${templateId}`,
        template_id: templateId,
      });
      setPreviewHtml(cv.html_content);
      await api.deleteCV(cv.id);
    } catch {
      setPreviewHtml('<p style="padding:40px;color:#666">Preview not available</p>');
    }
  };

  const createWithTemplate = async (templateId) => {
    try {
      const cv = await api.createCV({
        user_id: user.id,
        name: `CV - ${templateId}`,
        template_id: templateId,
      });
      await refreshCvs();
      setSelectedCvId(cv.id);
      navigate('/dashboard');
    } catch (e) {
      alert(e.message);
    }
  };

  if (loading) {
    return <div className="flex items-center justify-center h-64 text-gray-500">Loading...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-6">
      <div className="mb-6">
        <h1 className="text-xl font-bold text-white">Templates</h1>
        <p className="text-sm text-gray-500">Choose a template for your next CV</p>
      </div>

      {/* Preview modal */}
      {previewId && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 border border-gray-800 rounded-2xl w-full max-w-4xl h-[90vh] flex flex-col">
            <div className="flex items-center justify-between p-4 border-b border-gray-800">
              <h2 className="font-bold text-white capitalize">{previewId} Template</h2>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => { createWithTemplate(previewId); setPreviewId(null); }}
                  className="bg-white hover:bg-gray-100 text-gray-950 px-4 py-1.5 rounded-lg text-sm font-medium flex items-center gap-1"
                >
                  <Plus className="w-3.5 h-3.5" /> Use Template
                </button>
                <button onClick={() => setPreviewId(null)} className="text-gray-500 hover:text-white text-xl px-2">✕</button>
              </div>
            </div>
            <iframe srcDoc={previewHtml} className="flex-1 w-full bg-white" title="Template Preview" />
          </div>
        </div>
      )}

      {/* Template grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {templates.map(t => (
          <div
            key={t.id}
            className="bg-gray-900 rounded-xl border border-gray-800 p-5 hover:border-gray-700 transition-all cursor-pointer"
            onClick={() => previewTemplate(t.id)}
          >
            <div className="flex items-center gap-3 mb-3">
              <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ background: t.preview_color + '20' }}>
                <div className="w-5 h-5 rounded-md" style={{ background: t.preview_color }} />
              </div>
              <div>
                <h3 className="font-semibold text-white">{t.name}</h3>
                <p className="text-xs text-gray-500">{t.description}</p>
              </div>
            </div>

            {/* Mini preview */}
            <div className="bg-gray-800 rounded-lg p-3 space-y-2">
              <div className="h-4 rounded" style={{ background: t.preview_color, width: '60%' }} />
              <div className="h-2 bg-gray-700 rounded w-full" />
              <div className="h-2 bg-gray-700 rounded w-4/5" />
              <div className="h-2 bg-gray-700 rounded w-3/5" />
              <div className="flex gap-1 mt-1">
                {[...Array(4)].map((_, i) => (
                  <div key={i} className="h-2 rounded-full px-3" style={{ background: t.preview_color + '30' }} />
                ))}
              </div>
            </div>

            <div className="flex items-center justify-between mt-3">
              <button
                onClick={(e) => { e.stopPropagation(); previewTemplate(t.id); }}
                className="text-sm text-gray-500 hover:text-gray-300 flex items-center gap-1"
              >
                <Eye className="w-3.5 h-3.5" /> Preview
              </button>
              <button
                onClick={(e) => { e.stopPropagation(); createWithTemplate(t.id); }}
                className="text-sm font-medium text-white hover:text-gray-300 flex items-center gap-1"
              >
                <Plus className="w-3.5 h-3.5" /> Use
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
