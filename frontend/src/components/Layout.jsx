import { NavLink, Outlet } from 'react-router-dom';
import { FileText, Briefcase, MessageSquare, User, LayoutTemplate } from 'lucide-react';
import { useApp } from '../lib/store';

const navItems = [
  { to: '/dashboard', icon: FileText, label: 'CVs' },
  { to: '/vacancies', icon: Briefcase, label: 'Jobs' },
  { to: '/chat', icon: MessageSquare, label: 'Chat' },
  { to: '/templates', icon: LayoutTemplate, label: 'Templates' },
  { to: '/profile', icon: User, label: 'Profile' },
];

export default function Layout() {
  const { user } = useApp();

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Top bar - desktop */}
      <header className="hidden md:flex items-center justify-between bg-white border-b border-gray-200 px-6 py-3">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <FileText className="w-5 h-5 text-white" />
          </div>
          <span className="font-bold text-lg text-gray-900">CV Craft</span>
        </div>
        <nav className="flex gap-1">
          {navItems.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-100'
                }`
              }
            >
              <Icon className="w-4 h-4" />
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="text-sm text-gray-500">
          {user?.full_name || 'User'}
        </div>
      </header>

      {/* Main content */}
      <main className="flex-1 pb-20 md:pb-0">
        <Outlet />
      </main>

      {/* Bottom nav - mobile */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 flex justify-around py-2 z-50">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex flex-col items-center gap-0.5 px-2 py-1 text-xs ${
                isActive ? 'text-blue-600' : 'text-gray-400'
              }`
            }
          >
            <Icon className="w-5 h-5" />
            {label}
          </NavLink>
        ))}
      </nav>
    </div>
  );
}
