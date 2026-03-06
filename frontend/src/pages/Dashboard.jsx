import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileText, Download, Trash2, Palette, ChevronDown, Plus } from 'lucide-react';
import { useApp } from '../lib/store';
import { api } from '../lib/api';

export default function Dashboard() {
  const navigate = useNavigate();
  const { user, cvs, selectedCvId, setSelectedCvId, refreshCvs } = useApp();
  const [templates, setTemplates] = useState([]);
  const [selectedCv, setSelectedCv] = useState(null);
  const [loadingCv, setLoadingCv] = useState(false);
  const [showTemplatePicker, setShowTemplatePicker] = useState(false);

  useEffect(() => {
    api.listTemplates().then(setTemplates).catch(() => {});
  }, []);

  // Load selected CV detail
  useEffect(() => {
    if (selectedCvId) {
      setLoadingCv(true);
      api.getCV(selectedCvId)
        .then(setSelectedCv)
        .catch(() => {
          setSelectedCv(null);
          setSelectedCvId(null);
        })
        .finally(() => setLoadingCv(false));
    } else {
      setSelectedCv(null);
    }
  }, [selectedCvId, setSelectedCvId]);

  const downloadPDF = async () => {
    if (!selectedCv) return;
    try {
      const res = await api.exportPDF(selectedCv.id);
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${selectedCv.name}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      alert('PDF export failed: ' + e.message);
    }
  };

  const deleteCv = async () => {
    if (!selectedCv || !confirm('Delete this CV?')) return;
    await api.deleteCV(selectedCv.id);
    setSelectedCvId(null);
    setSelectedCv(null);
    refreshCvs();
  };

  const changeTemplate = async (templateId) => {
    if (!selectedCv) return;
    try {
      await api.changeTemplate(selectedCv.id, templateId);
      const updated = await api.getCV(selectedCv.id);
      setSelectedCv(updated);
      setShowTemplatePicker(false);
    } catch (e) {
      alert(e.message);
    }
  };

  const createCV = async () => {
    try {
      const cv = await api.createCV({
        user_id: user.id,
        name: 'Untitled CV',
        template_id: 'modern',
      });
      await refreshCvs();
      setSelectedCvId(cv.id);
    } catch (e) {
      alert(e.message);
    }
  };

  // Empty state
  if (!selectedCvId) {
    return (
      <div className="h-full flex flex-col items-center justify-center px-4">
        <div className="text-center">
          <div className="w-16 h-16 bg-gray-800 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <FileText className="w-8 h-8 text-gray-600" />
          </div>
          <h2 className="text-xl font-semibold text-white mb-2">No CV selected</h2>
          <p className="text-gray-500 text-sm mb-6">
            {cvs.length === 0
              ? 'Create your first CV to get started.'
              : 'Select a CV from the sidebar to preview it.'}
          </p>
          {cvs.length === 0 && (
            <button
              onClick={createCV}
              className="bg-white hover:bg-gray-100 text-gray-950 font-medium px-6 py-2.5 rounded-xl text-sm transition-colors inline-flex items-center gap-2"
            >
              <Plus className="w-4 h-4" />
              Create Your First CV
            </button>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      {/* Toolbar */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-800 bg-gray-950/50 shrink-0">
        <div className="flex items-center gap-3 min-w-0">
          <h1 className="text-sm font-semibold text-white truncate">
            {selectedCv?.name || 'Loading...'}
          </h1>

          {/* Template picker */}
          <div className="relative">
            <button
              onClick={() => setShowTemplatePicker(!showTemplatePicker)}
              className="flex items-center gap-1 text-xs text-gray-400 hover:text-gray-200 bg-gray-800 px-2.5 py-1.5 rounded-lg transition-colors"
            >
              {selectedCv?.template_id || 'template'}
              <ChevronDown className="w-3 h-3" />
            </button>
            {showTemplatePicker && (
              <div className="absolute top-full left-0 mt-1 bg-gray-800 border border-gray-700 rounded-xl p-1 z-10 min-w-[160px] shadow-lg">
                {templates.map(t => (
                  <button
                    key={t.id}
                    onClick={() => changeTemplate(t.id)}
                    className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${
                      selectedCv?.template_id === t.id
                        ? 'bg-gray-700 text-white'
                        : 'text-gray-400 hover:bg-gray-700 hover:text-white'
                    }`}
                  >
                    <div className="flex items-center gap-2">
                      <div className="w-2.5 h-2.5 rounded-full" style={{ background: t.preview_color }} />
                      {t.name}
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="flex items-center gap-1">
          <button
            onClick={() => navigate(`/chat?cv=${selectedCv?.id}`)}
            className="p-2 rounded-lg text-gray-400 hover:text-blue-400 hover:bg-gray-800 transition-colors"
            title="Edit with AI"
          >
            <Palette className="w-4 h-4" />
          </button>
          <button
            onClick={downloadPDF}
            className="p-2 rounded-lg text-gray-400 hover:text-green-400 hover:bg-gray-800 transition-colors"
            title="Download PDF"
          >
            <Download className="w-4 h-4" />
          </button>
          <button
            onClick={deleteCv}
            className="p-2 rounded-lg text-gray-400 hover:text-red-400 hover:bg-gray-800 transition-colors"
            title="Delete CV"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* CV Preview */}
      <div className="flex-1 bg-gray-800/30 p-4 overflow-auto">
        {loadingCv ? (
          <div className="h-full flex items-center justify-center text-gray-500 text-sm">Loading preview...</div>
        ) : selectedCv?.html_content ? (
          <div className="max-w-[800px] mx-auto h-full">
            <iframe
              srcDoc={selectedCv.html_content}
              className="w-full h-full bg-white rounded-lg shadow-2xl shadow-black/30"
              title="CV Preview"
            />
          </div>
        ) : (
          <div className="h-full flex items-center justify-center text-gray-500 text-sm">No preview available</div>
        )}
      </div>
    </div>
  );
}
