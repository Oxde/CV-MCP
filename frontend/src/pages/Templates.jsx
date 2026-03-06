import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Eye, Plus } from 'lucide-react';
import { useApp } from '../lib/store';
import { api } from '../lib/api';

const SAMPLE_DATA = {
  full_name: 'Alex Johnson',
  title: 'Senior Software Engineer',
  email: 'alex@example.com',
  phone: '+1 (555) 123-4567',
  location: 'San Francisco, CA',
  linkedin: 'linkedin.com/in/alexj',
  github: 'github.com/alexj',
  portfolio: '',
  summary: 'Results-driven software engineer with 6+ years of experience building scalable web applications. Passionate about clean code, system design, and mentoring junior developers. Led teams delivering products used by 2M+ users.',
  experience: [
    {
      title: 'Senior Software Engineer',
      company: 'TechCorp',
      start: 'Jan 2022',
      end: 'Present',
      bullets: [
        'Led redesign of core API, reducing latency by 40% and improving uptime to 99.95%',
        'Mentored 4 junior engineers, with 2 promoted within 12 months',
        'Implemented CI/CD pipeline reducing deployment time from 2 hours to 15 minutes',
      ],
    },
    {
      title: 'Software Engineer',
      company: 'StartupXYZ',
      start: 'Mar 2019',
      end: 'Dec 2021',
      bullets: [
        'Built real-time notification system serving 500K+ daily active users',
        'Migrated monolith to microservices architecture, improving team velocity by 60%',
      ],
    },
  ],
  education: [
    { degree: 'B.S. Computer Science', school: 'UC Berkeley', year: '2019', gpa: '3.8' },
  ],
  skills: ['Python', 'TypeScript', 'React', 'Node.js', 'PostgreSQL', 'AWS', 'Docker', 'Kubernetes', 'GraphQL', 'Redis'],
  languages: [
    { language: 'English', level: 'Native' },
    { language: 'Spanish', level: 'Conversational' },
  ],
  certifications: [
    { name: 'AWS Solutions Architect', issuer: 'Amazon', year: '2023' },
  ],
  projects: [
    { name: 'OpenTracer', description: 'Open-source distributed tracing tool with 2K+ GitHub stars', tech: ['Go', 'gRPC', 'Jaeger'] },
    { name: 'DevDash', description: 'Developer productivity dashboard with GitHub/Jira integration', tech: ['React', 'Node.js', 'D3.js'] },
  ],
};

export default function Templates() {
  const navigate = useNavigate();
  const { user } = useApp();
  const [templates, setTemplates] = useState([]);
  const [previewId, setPreviewId] = useState(null);
  const [previewHtml, setPreviewHtml] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.listTemplates().then(setTemplates).finally(() => setLoading(false));
  }, []);

  const previewTemplate = async (templateId) => {
    setPreviewId(templateId);
    // Generate preview HTML by creating a temp CV
    try {
      const cv = await api.createCV({
        user_id: user.id,
        name: `Preview - ${templateId}`,
        template_id: templateId,
      });
      setPreviewHtml(cv.html_content);
      // Clean up - delete the preview CV
      await api.deleteCV(cv.id);
    } catch {
      setPreviewHtml('<p style="padding:40px;color:#999">Preview not available - add your profile info first</p>');
    }
  };

  const createWithTemplate = async (templateId) => {
    try {
      const cv = await api.createCV({
        user_id: user.id,
        name: `CV - ${templateId}`,
        template_id: templateId,
      });
      navigate('/dashboard');
    } catch (e) {
      alert(e.message);
    }
  };

  if (loading) {
    return <div className="flex items-center justify-center h-64 text-gray-400">Loading...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">CV Templates</h1>
        <p className="text-sm text-gray-500">Choose a template for your next CV</p>
      </div>

      {/* Preview modal */}
      {previewId && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl w-full max-w-4xl h-[90vh] flex flex-col">
            <div className="flex items-center justify-between p-4 border-b">
              <h2 className="font-bold capitalize">{previewId} Template Preview</h2>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => { createWithTemplate(previewId); setPreviewId(null); }}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-1.5 rounded-lg text-sm font-medium flex items-center gap-1"
                >
                  <Plus className="w-3.5 h-3.5" /> Use Template
                </button>
                <button onClick={() => setPreviewId(null)} className="text-gray-400 hover:text-gray-600 text-xl px-2">✕</button>
              </div>
            </div>
            <iframe
              srcDoc={previewHtml}
              className="flex-1 w-full"
              title="Template Preview"
            />
          </div>
        </div>
      )}

      {/* Template grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {templates.map(t => (
          <div
            key={t.id}
            className="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-md transition-shadow group cursor-pointer"
            onClick={() => previewTemplate(t.id)}
          >
            <div className="flex items-center gap-3 mb-3">
              <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ background: t.preview_color + '15' }}>
                <div className="w-5 h-5 rounded-md" style={{ background: t.preview_color }} />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">{t.name}</h3>
                <p className="text-xs text-gray-500">{t.description}</p>
              </div>
            </div>

            {/* Mini preview bars */}
            <div className="bg-gray-50 rounded-lg p-3 space-y-2">
              <div className="h-4 rounded" style={{ background: t.preview_color, width: '60%' }} />
              <div className="h-2 bg-gray-200 rounded w-full" />
              <div className="h-2 bg-gray-200 rounded w-4/5" />
              <div className="h-2 bg-gray-200 rounded w-3/5" />
              <div className="flex gap-1 mt-1">
                {[...Array(4)].map((_, i) => (
                  <div key={i} className="h-2 rounded-full px-3" style={{ background: t.preview_color + '30' }} />
                ))}
              </div>
            </div>

            <div className="flex items-center justify-between mt-3">
              <button
                onClick={(e) => { e.stopPropagation(); previewTemplate(t.id); }}
                className="text-sm text-gray-400 hover:text-gray-600 flex items-center gap-1"
              >
                <Eye className="w-3.5 h-3.5" /> Preview
              </button>
              <button
                onClick={(e) => { e.stopPropagation(); createWithTemplate(t.id); }}
                className="text-sm font-medium text-blue-600 hover:text-blue-700 flex items-center gap-1"
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
