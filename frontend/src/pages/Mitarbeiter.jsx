import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { mitarbeiterAPI } from '../utils/api';
import { Users, Search, Mail, Phone } from 'lucide-react';
import toast from 'react-hot-toast';

function Mitarbeiter() {
  const [mitarbeiter, setMitarbeiter] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchMitarbeiter();
  }, [search]);

  const fetchMitarbeiter = async () => {
    setLoading(true);
    try {
      const params = {
        page: 1,
        page_size: 50,
      };
      if (search) {
        params.search = search;
      }

      const { data } = await mitarbeiterAPI.list(params);
      setMitarbeiter(data.items);
    } catch (error) {
      console.error('Error fetching mitarbeiter:', error);
      toast.error('Fehler beim Laden der Mitarbeiter');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'aktiv':
        return 'badge-pav-green';
      case 'urlaub':
        return 'badge-pav-turquoise';
      case 'inaktiv':
        return 'bg-pav-ink/20 text-pav-ink';
      default:
        return 'badge-pav-green';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-pav-turquoise text-lg uppercase tracking-pav-nav">
          Laden...
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-pav-turquoise mb-2">
            Mitarbeiter
          </h1>
          <p className="text-pav-ink/60 uppercase text-sm tracking-pav-nav">
            {mitarbeiter.length} Mitarbeiter
          </p>
        </div>
      </div>

      {/* Search */}
      <div className="card-pav-white">
        <div className="relative">
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input-pav pr-12"
            placeholder="Mitarbeiter suchen (Name, Email, Personalnummer)..."
          />
          <Search
            className="absolute right-4 top-1/2 -translate-y-1/2 text-pav-turquoise"
            size={20}
          />
        </div>
      </div>

      {/* Mitarbeiter Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mitarbeiter.map((m) => (
          <div
            key={m.id}
            className="card-pav-white hover:shadow-lg transition-shadow cursor-pointer"
            onClick={() => navigate(`/mitarbeiter/${m.id}`)}
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <h3 className="text-xl font-bold text-pav-ink mb-1">
                  {m.vorname} {m.nachname}
                </h3>
                <p className="text-sm text-pav-ink/70">
                  {m.position}
                </p>
              </div>
              <span className={`${getStatusColor(m.status)} text-xs`}>
                {m.status}
              </span>
            </div>

            <div className="space-y-2 text-sm text-pav-ink/70">
              <div className="flex items-center gap-2">
                <Users size={16} />
                {m.abteilung}
              </div>
              <div className="flex items-center gap-2">
                <Mail size={16} />
                {m.email}
              </div>
              {m.telefon && (
                <div className="flex items-center gap-2">
                  <Phone size={16} />
                  {m.telefon}
                </div>
              )}
            </div>

            <div className="mt-4 pt-4 border-t border-pav-soft-grey">
              <span className="text-xs text-pav-ink/60 uppercase tracking-pav-nav">
                {m.personal_nummer}
              </span>
            </div>
          </div>
        ))}
      </div>

      {mitarbeiter.length === 0 && (
        <div className="card-pav-white text-center py-12">
          <p className="text-pav-ink/60 text-lg uppercase tracking-pav-nav">
            Keine Mitarbeiter gefunden
          </p>
        </div>
      )}
    </div>
  );
}

export default Mitarbeiter;
