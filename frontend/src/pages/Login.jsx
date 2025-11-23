import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../hooks/useStore';
import { authAPI } from '../utils/api';
import toast from 'react-hot-toast';
import { LogIn } from 'lucide-react';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const { data } = await authAPI.login(username, password);
      const token = data.access_token;

      // Get user info
      const { data: userData } = await authAPI.getCurrentUser();

      login(token, userData);
      toast.success(`Willkommen, ${userData.username}!`);
      navigate('/dashboard');
    } catch (error) {
      console.error('Login error:', error);
      toast.error(
        error.response?.data?.detail || 'Anmeldung fehlgeschlagen'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pav-turquoise via-pav-dark-green to-pav-light-green flex items-center justify-center p-4">
      <div className="card-pav-white max-w-md w-full">
        {/* Logo / Brand */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-pav-turquoise mb-2">
            PAV Personalfinder
          </h1>
          <p className="text-pav-ink/60 uppercase text-sm tracking-pav-nav">
            KI-gestütztes Mitarbeiter-Matching
          </p>
        </div>

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-pav-ink mb-2 uppercase tracking-pav-nav">
              Benutzername
            </label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="input-pav"
              placeholder="Benutzername eingeben"
              required
              autoFocus
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-pav-ink mb-2 uppercase tracking-pav-nav">
              Passwort
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="input-pav"
              placeholder="Passwort eingeben"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-pav-primary w-full flex items-center justify-center gap-2"
          >
            {loading ? (
              <span>Anmelden...</span>
            ) : (
              <>
                <LogIn size={20} />
                <span>Anmelden</span>
              </>
            )}
          </button>
        </form>

        {/* Demo Credentials */}
        <div className="mt-8 pt-8 border-t border-pav-soft-grey">
          <p className="text-sm text-pav-ink/60 mb-3 uppercase tracking-pav-nav">
            Demo-Zugänge:
          </p>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="font-medium">Admin:</span>
              <span className="text-pav-ink/70">admin / admin123</span>
            </div>
            <div className="flex justify-between">
              <span className="font-medium">HR Manager:</span>
              <span className="text-pav-ink/70">hr_manager / hr123</span>
            </div>
            <div className="flex justify-between">
              <span className="font-medium">Viewer:</span>
              <span className="text-pav-ink/70">viewer / viewer123</span>
            </div>
          </div>
        </div>
      </div>

      {/* Footer with PAV Logo */}
      <div className="fixed bottom-4 right-4">
        <div className="text-white text-lg font-bold uppercase tracking-wider bg-pav-turquoise px-4 py-2 rounded-pav-pill shadow-lg">
          PAV
        </div>
      </div>
    </div>
  );
}

export default Login;
