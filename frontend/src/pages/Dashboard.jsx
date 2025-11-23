import { useEffect, useState } from 'react';
import { dashboardAPI } from '../utils/api';
import { Users, UserCheck, Plane, Heart, AlertCircle } from 'lucide-react';
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import toast from 'react-hot-toast';

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    setLoading(true);
    try {
      const { data } = await dashboardAPI.getStats();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
      toast.error('Fehler beim Laden der Statistiken');
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

  if (!stats) {
    return null;
  }

  // KPI Cards Data
  const kpiCards = [
    {
      title: 'Gesamt',
      value: stats.total_mitarbeiter,
      icon: Users,
      color: 'bg-pav-turquoise',
    },
    {
      title: 'Verfügbar',
      value: stats.verfuegbar,
      icon: UserCheck,
      color: 'bg-pav-dark-green',
    },
    {
      title: 'Im Einsatz',
      value: stats.im_einsatz,
      icon: Users,
      color: 'bg-pav-light-green',
    },
    {
      title: 'Im Urlaub',
      value: stats.im_urlaub,
      icon: Plane,
      color: 'bg-pav-turquoise',
    },
    {
      title: 'Krank',
      value: stats.krank,
      icon: Heart,
      color: 'bg-pav-ink',
    },
    {
      title: 'Ablaufende Zertifikate',
      value: stats.ablaufende_zertifikate,
      icon: AlertCircle,
      color: 'bg-pav-magenta',
    },
  ];

  // Prepare chart data
  const abteilungData = Object.entries(stats.abteilung_distribution || {}).map(([name, value]) => ({
    name,
    value,
  }));

  const qualifikationData = Object.entries(stats.qualifikation_distribution || {})
    .slice(0, 10)
    .map(([name, value]) => ({
      name,
      value,
    }));

  const COLORS = ['#018A9C', '#009657', '#50AF31', '#E62487', '#111111'];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-pav-turquoise mb-2">Dashboard</h1>
        <p className="text-pav-ink/60 uppercase text-sm tracking-pav-nav">
          Übersicht und Kennzahlen
        </p>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-6">
        {kpiCards.map((card, index) => (
          <div key={index} className="card-pav-white">
            <div className="flex items-start justify-between mb-4">
              <div
                className={`${card.color} p-3 rounded-pav-card text-white`}
              >
                <card.icon size={24} strokeWidth={2} />
              </div>
            </div>
            <div>
              <p className="text-3xl font-bold text-pav-ink mb-1">
                {card.value}
              </p>
              <p className="text-sm text-pav-ink/60 uppercase tracking-pav-nav">
                {card.title}
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Department Distribution */}
        <div className="card-pav-white">
          <h3 className="text-xl font-bold text-pav-turquoise mb-6 uppercase tracking-pav-headline">
            Abteilungsverteilung
          </h3>
          {abteilungData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={abteilungData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) =>
                    `${name}: ${(percent * 100).toFixed(0)}%`
                  }
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {abteilungData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-pav-ink/60 text-center py-12">
              Keine Daten verfügbar
            </p>
          )}
        </div>

        {/* Qualification Distribution */}
        <div className="card-pav-white">
          <h3 className="text-xl font-bold text-pav-turquoise mb-6 uppercase tracking-pav-headline">
            Top 10 Qualifikationen
          </h3>
          {qualifikationData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={qualifikationData} layout="vertical">
                <XAxis type="number" />
                <YAxis
                  type="category"
                  dataKey="name"
                  width={150}
                  tick={{ fontSize: 12 }}
                />
                <Tooltip />
                <Bar dataKey="value" fill="#009657" radius={[0, 12, 12, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-pav-ink/60 text-center py-12">
              Keine Daten verfügbar
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
