import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { LayoutDashboard, Search, Users, LogOut, Menu, X, HelpCircle } from 'lucide-react';
import { useState, useEffect } from 'react';
import { useAuthStore } from '../hooks/useStore';
import { authAPI } from '../utils/api';
import toast from 'react-hot-toast';
import WelcomeTutorial from './WelcomeTutorial';

function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [showTutorial, setShowTutorial] = useState(false);
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  // Check if user has seen the tutorial
  useEffect(() => {
    const tutorialCompleted = localStorage.getItem('pav_tutorial_completed');
    if (!tutorialCompleted) {
      // Show tutorial after a short delay
      setTimeout(() => setShowTutorial(true), 500);
    }
  }, []);

  const handleLogout = async () => {
    try {
      await authAPI.logout();
      logout();
      navigate('/login');
      toast.success('Erfolgreich abgemeldet');
    } catch (error) {
      console.error('Logout error:', error);
      logout();
      navigate('/login');
    }
  };

  const navItems = [
    { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    { to: '/ai-matching', icon: Search, label: 'KI-Suche' },
    { to: '/mitarbeiter', icon: Users, label: 'Mitarbeiter' },
  ];

  return (
    <div className="flex h-screen bg-pav-soft-grey">
      {/* Sidebar */}
      <aside
        className={`${
          sidebarOpen ? 'w-64' : 'w-20'
        } nav-pav transition-all duration-300 flex flex-col shadow-lg`}
      >
        {/* Header */}
        <div className="p-6 flex items-center justify-between">
          {sidebarOpen && (
            <h1 className="text-xl font-bold uppercase tracking-pav-headline">
              PAV Personalfinder
            </h1>
          )}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 hover:bg-white/10 rounded-lg transition-colors"
          >
            {sidebarOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-4 space-y-2">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-pav-card transition-colors ${
                  isActive
                    ? 'bg-pav-dark-green'
                    : 'hover:bg-white/10'
                }`
              }
            >
              <item.icon size={24} strokeWidth={2} />
              {sidebarOpen && (
                <span className="nav-pav-item font-medium">{item.label}</span>
              )}
            </NavLink>
          ))}
        </nav>

        {/* User Info & Logout */}
        <div className="p-4 border-t border-white/20 space-y-2">
          {sidebarOpen && user && (
            <div className="mb-3 px-2">
              <p className="text-sm text-white/80">Angemeldet als</p>
              <p className="text-white font-bold uppercase text-sm tracking-pav-nav">
                {user.username}
              </p>
              <p className="text-xs text-white/60 uppercase">{user.rolle}</p>
            </div>
          )}
          <button
            onClick={() => setShowTutorial(true)}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-pav-card hover:bg-white/10 transition-colors"
            title="Tutorial anzeigen"
          >
            <HelpCircle size={20} strokeWidth={2} />
            {sidebarOpen && (
              <span className="nav-pav-item font-medium">Tutorial</span>
            )}
          </button>
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-pav-card hover:bg-pav-magenta transition-colors"
          >
            <LogOut size={20} strokeWidth={2} />
            {sidebarOpen && (
              <span className="nav-pav-item font-medium">Abmelden</span>
            )}
          </button>
        </div>

        {/* PAV Logo (Bottom-Right Position in Sidebar) */}
        {sidebarOpen && (
          <div className="p-4 flex justify-end">
            <div className="text-white text-xs uppercase tracking-wider">
              PAV
            </div>
          </div>
        )}
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto scrollbar-pav">
        <div className="container mx-auto p-8">
          <Outlet />
        </div>
      </main>

      {/* Welcome Tutorial Modal */}
      {showTutorial && (
        <WelcomeTutorial onClose={() => setShowTutorial(false)} />
      )}
    </div>
  );
}

export default Layout;
