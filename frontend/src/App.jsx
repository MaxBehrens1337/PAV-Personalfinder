import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { useAuthStore } from './hooks/useStore';

// Pages
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import AIMatching from './pages/AIMatching';
import Mitarbeiter from './pages/Mitarbeiter';
import MitarbeiterDetail from './pages/MitarbeiterDetail';

// Layout
import Layout from './components/Layout';

// Protected Route Component
function ProtectedRoute({ children }) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />

          {/* Protected Routes */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="ai-matching" element={<AIMatching />} />
            <Route path="mitarbeiter" element={<Mitarbeiter />} />
            <Route path="mitarbeiter/:id" element={<MitarbeiterDetail />} />
          </Route>

          {/* Catch all */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>

      {/* Toast Notifications */}
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#111111',
            color: '#FFFFFF',
            borderRadius: '24px',
            padding: '16px',
          },
          success: {
            iconTheme: {
              primary: '#009657',
              secondary: '#FFFFFF',
            },
          },
          error: {
            iconTheme: {
              primary: '#E62487',
              secondary: '#FFFFFF',
            },
          },
        }}
      />
    </>
  );
}

export default App;
