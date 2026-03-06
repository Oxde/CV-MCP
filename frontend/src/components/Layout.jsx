import { Outlet } from 'react-router-dom';
import { Menu, Briefcase } from 'lucide-react';
import { useApp } from '../lib/store';
import Sidebar from './Sidebar';
import JobsPanel from './JobsPanel';

export default function Layout() {
  const { setSidebarOpen, setJobsPanelOpen } = useApp();

  return (
    <div className="h-screen flex bg-gray-900 overflow-hidden">
      {/* Sidebar */}
      <Sidebar />

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Mobile top bar */}
        <div className="md:hidden flex items-center justify-between bg-gray-950 border-b border-gray-800 px-4 py-3">
          <button
            onClick={() => setSidebarOpen(true)}
            className="text-gray-400 hover:text-white"
          >
            <Menu className="w-5 h-5" />
          </button>
          <span className="font-bold text-white text-sm">CV Craft</span>
          <button
            onClick={() => setJobsPanelOpen(true)}
            className="text-gray-400 hover:text-white"
          >
            <Briefcase className="w-5 h-5" />
          </button>
        </div>

        <main className="flex-1 overflow-y-auto">
          <Outlet />
        </main>
      </div>

      {/* Jobs panel */}
      <JobsPanel />
    </div>
  );
}
