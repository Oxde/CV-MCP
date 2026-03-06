import { NavLink, useNavigate } from 'react-router-dom';
import { FileText, Plus, MessageSquare, LayoutTemplate, User, LogOut, X } from 'lucide-react';
import { useApp } from '../lib/store';
import { api } from '../lib/api';

export default function Sidebar() {
  const navigate = useNavigate();
  const { user, cvs, selectedCvId, setSelectedCvId, refreshCvs, sidebarOpen, setSidebarOpen, logout } = useApp();

  const createCV = async () => {
    try {
      const cv = await api.createCV({
        user_id: user.id,
        name: 'Untitled CV',
        template_id: 'modern',
      });
      await refreshCvs();
      setSelectedCvId(cv.id);
      navigate('/dashboard');
    } catch (e) {
      alert(e.message);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const sidebar = (
    <div className="h-full flex flex-col bg-gray-950 border-r border-gray-800 w-60">
      {/* Logo */}
      <div className="flex items-center justify-between px-4 py-4 border-b border-gray-800">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-white rounded-lg flex items-center justify-center">
            <FileText className="w-4.5 h-4.5 text-gray-950" />
          </div>
          <span className="font-bold text-white text-lg">CV Craft</span>
        </div>
        {/* Mobile close */}
        <button
          onClick={() => setSidebarOpen(false)}
          className="md:hidden text-gray-400 hover:text-white"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* CVs section */}
      <div className="px-3 py-3 flex-1 overflow-y-auto">
        <div className="flex items-center justify-between mb-2 px-1">
          <span className="text-xs font-medium text-gray-500 uppercase tracking-wider">My CVs</span>
          <button
            onClick={createCV}
            className="text-gray-400 hover:text-white transition-colors"
            title="New CV"
          >
            <Plus className="w-4 h-4" />
          </button>
        </div>

        <div className="space-y-0.5 mb-6">
          {cvs.length === 0 ? (
            <p className="text-xs text-gray-600 px-2 py-2">No CVs yet</p>
          ) : (
            cvs.map(cv => (
              <button
                key={cv.id}
                onClick={() => {
                  setSelectedCvId(cv.id);
                  navigate('/dashboard');
                  setSidebarOpen(false);
                }}
                className={`w-full text-left px-2.5 py-2 rounded-lg text-sm transition-colors flex items-center gap-2 ${
                  selectedCvId === cv.id
                    ? 'bg-gray-800 text-white'
                    : 'text-gray-400 hover:bg-gray-900 hover:text-gray-200'
                }`}
              >
                <FileText className="w-3.5 h-3.5 shrink-0" />
                <span className="truncate">{cv.name}</span>
              </button>
            ))
          )}
          <button
            onClick={createCV}
            className="w-full text-left px-2.5 py-2 rounded-lg text-sm text-gray-500 hover:bg-gray-900 hover:text-gray-300 transition-colors flex items-center gap-2"
          >
            <Plus className="w-3.5 h-3.5" />
            New CV
          </button>
        </div>

        {/* Nav links */}
        <div className="border-t border-gray-800 pt-3 space-y-0.5">
          {[
            { to: '/templates', icon: LayoutTemplate, label: 'Templates' },
            { to: '/profile', icon: User, label: 'Profile' },
            { to: '/chat', icon: MessageSquare, label: 'AI Chat' },
          ].map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              onClick={() => setSidebarOpen(false)}
              className={({ isActive }) =>
                `flex items-center gap-2.5 px-2.5 py-2 rounded-lg text-sm transition-colors ${
                  isActive
                    ? 'bg-gray-800 text-white'
                    : 'text-gray-400 hover:bg-gray-900 hover:text-gray-200'
                }`
              }
            >
              <Icon className="w-4 h-4" />
              {label}
            </NavLink>
          ))}
        </div>
      </div>

      {/* User / Logout */}
      <div className="px-3 py-3 border-t border-gray-800">
        <div className="flex items-center justify-between px-2">
          <span className="text-sm text-gray-400 truncate">{user?.full_name || 'User'}</span>
          <button
            onClick={handleLogout}
            className="text-gray-500 hover:text-red-400 transition-colors"
            title="Logout"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop sidebar */}
      <div className="hidden md:block shrink-0">
        {sidebar}
      </div>

      {/* Mobile drawer */}
      {sidebarOpen && (
        <div className="md:hidden fixed inset-0 z-50 flex">
          <div className="animate-slide-left">
            {sidebar}
          </div>
          <div
            className="flex-1 bg-black/60 animate-fade-in"
            onClick={() => setSidebarOpen(false)}
          />
        </div>
      )}
    </>
  );
}
