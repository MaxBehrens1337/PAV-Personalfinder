import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { mitarbeiterAPI } from '../utils/api';
import { ArrowLeft, Mail, Phone, Calendar, Award } from 'lucide-react';
import toast from 'react-hot-toast';

function MitarbeiterDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [mitarbeiter, setMitarbeiter] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMitarbeiter();
  }, [id]);

  const fetchMitarbeiter = async () => {
    setLoading(true);
    try {
      const { data } = await mitarbeiterAPI.get(id);
      setMitarbeiter(data);
    } catch (error) {
      console.error('Error fetching mitarbeiter:', error);
      toast.error('Fehler beim Laden der Mitarbeiterdaten');
    } finally {
      setLoading(false);
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

  if (!mitarbeiter) {
    return null;
  }

  return (
    <div className="space-y-8">
      {/* Back Button */}
      <button
        onClick={() => navigate('/mitarbeiter')}
        className="btn-pav-outline flex items-center gap-2"
      >
        <ArrowLeft size={20} />
        Zurück
      </button>

      {/* Header */}
      <div className="card-pav-white">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-4xl font-bold text-pav-turquoise mb-2">
              {mitarbeiter.vorname} {mitarbeiter.nachname}
            </h1>
            <p className="text-xl text-pav-ink/70 mb-4">
              {mitarbeiter.position}
            </p>
            <div className="flex gap-3">
              <span className="badge-pav-green">
                {mitarbeiter.status}
              </span>
              <span className="badge-pav-turquoise">
                {mitarbeiter.personal_nummer}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Contact Info */}
      <div className="card-pav-white">
        <h2 className="text-2xl font-bold text-pav-turquoise mb-6 uppercase tracking-pav-headline">
          Kontaktinformationen
        </h2>
        <div className="space-y-4">
          <div className="flex items-center gap-3">
            <Mail size={20} className="text-pav-turquoise" />
            <div>
              <p className="text-sm text-pav-ink/60 uppercase tracking-pav-nav">Email</p>
              <p className="text-pav-ink">{mitarbeiter.email}</p>
            </div>
          </div>
          {mitarbeiter.telefon && (
            <div className="flex items-center gap-3">
              <Phone size={20} className="text-pav-turquoise" />
              <div>
                <p className="text-sm text-pav-ink/60 uppercase tracking-pav-nav">Telefon</p>
                <p className="text-pav-ink">{mitarbeiter.telefon}</p>
              </div>
            </div>
          )}
          <div className="flex items-center gap-3">
            <Calendar size={20} className="text-pav-turquoise" />
            <div>
              <p className="text-sm text-pav-ink/60 uppercase tracking-pav-nav">Eintrittsdatum</p>
              <p className="text-pav-ink">
                {new Date(mitarbeiter.eintritt_datum).toLocaleDateString('de-DE')}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Additional Info */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card-pav-white">
          <h3 className="text-xl font-bold text-pav-turquoise mb-4 uppercase tracking-pav-headline">
            Details
          </h3>
          <div className="space-y-3 text-sm">
            <div>
              <p className="text-pav-ink/60 uppercase tracking-pav-nav">Abteilung</p>
              <p className="text-pav-ink font-medium">{mitarbeiter.abteilung}</p>
            </div>
            <div>
              <p className="text-pav-ink/60 uppercase tracking-pav-nav">Wochenstunden</p>
              <p className="text-pav-ink font-medium">{mitarbeiter.wochenstunden} Stunden</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default MitarbeiterDetail;
