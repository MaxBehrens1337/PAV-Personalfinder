import { useState } from 'react';
import { aiMatchingAPI } from '../utils/api';
import { Search, Sparkles, Mail, Phone, Award, TrendingUp, AlertTriangle } from 'lucide-react';
import toast from 'react-hot-toast';

function AIMatching() {
  const [query, setQuery] = useState('');
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [aiEnabled, setAiEnabled] = useState(false);
  const [executionTime, setExecutionTime] = useState(0);
  const [useAI, setUseAI] = useState(true);

  const exampleQueries = [
    'Finde jemanden für ein Logistik-Projekt mit SAP-Kenntnissen',
    'Wer ist verfügbar nächste Woche mit Staplerführerschein?',
    'Zeige Logistik-Experten mit Zertifikat',
    'Ich brauche einen IT-Spezialisten mit Python-Kenntnissen',
  ];

  const handleSearch = async (e) => {
    e.preventDefault();

    if (!query.trim()) {
      toast.error('Bitte geben Sie eine Suchanfrage ein');
      return;
    }

    setLoading(true);
    try {
      const { data } = await aiMatchingAPI.search({
        query: query.trim(),
        max_results: 10,
        use_ai: useAI,
      });

      setMatches(data.matches);
      setAiEnabled(data.ai_enabled);
      setExecutionTime(data.execution_time_seconds);
      toast.success(`${data.total_matches} Treffer gefunden`);
    } catch (error) {
      console.error('Search error:', error);
      toast.error('Fehler bei der Suche');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'bg-pav-dark-green';
    if (score >= 60) return 'bg-pav-light-green';
    if (score >= 40) return 'bg-pav-turquoise';
    return 'bg-pav-ink/50';
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-pav-turquoise mb-2">KI-Suche</h1>
        <p className="text-pav-ink/60 uppercase text-sm tracking-pav-nav">
          Intelligentes Mitarbeiter-Matching
        </p>
      </div>

      {/* Search Form */}
      <div className="card-pav-white">
        <form onSubmit={handleSearch} className="space-y-4">
          {/* Search Input */}
          <div>
            <label className="block text-sm font-medium text-pav-ink mb-2 uppercase tracking-pav-nav">
              Beschreiben Sie Ihre Anforderungen
            </label>
            <div className="relative">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="input-pav pr-12"
                placeholder="z.B. Ich suche jemanden für ein Logistik-Projekt mit SAP-Kenntnissen..."
                disabled={loading}
              />
              <Search
                className="absolute right-4 top-1/2 -translate-y-1/2 text-pav-turquoise"
                size={20}
              />
            </div>
          </div>

          {/* AI Toggle */}
          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              id="use-ai"
              checked={useAI}
              onChange={(e) => setUseAI(e.target.checked)}
              className="w-5 h-5 text-pav-dark-green focus:ring-pav-turquoise rounded"
            />
            <label
              htmlFor="use-ai"
              className="text-sm text-pav-ink uppercase tracking-pav-nav flex items-center gap-2"
            >
              <Sparkles size={16} className="text-pav-magenta" />
              KI-Matching verwenden
            </label>
          </div>

          {/* Search Button */}
          <button
            type="submit"
            disabled={loading}
            className="btn-pav-primary w-full md:w-auto"
          >
            {loading ? 'Suche läuft...' : 'Mitarbeiter suchen'}
          </button>
        </form>

        {/* Example Queries */}
        <div className="mt-6 pt-6 border-t border-pav-soft-grey">
          <p className="text-sm text-pav-ink/60 mb-3 uppercase tracking-pav-nav">
            Beispiel-Anfragen:
          </p>
          <div className="flex flex-wrap gap-2">
            {exampleQueries.map((example, index) => (
              <button
                key={index}
                onClick={() => setQuery(example)}
                className="text-sm bg-pav-soft-grey hover:bg-pav-turquoise hover:text-white px-3 py-2 rounded-pav-pill transition-colors"
              >
                {example}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Results */}
      {matches.length > 0 && (
        <div className="space-y-6">
          {/* Results Header */}
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-pav-turquoise uppercase tracking-pav-headline">
              Suchergebnisse
            </h2>
            <div className="flex items-center gap-4 text-sm">
              {aiEnabled && (
                <span className="badge-pav-magenta flex items-center gap-2">
                  <Sparkles size={14} />
                  KI-Powered
                </span>
              )}
              <span className="text-pav-ink/60">
                {matches.length} Treffer in {executionTime}s
              </span>
            </div>
          </div>

          {/* Match Cards */}
          <div className="space-y-4">
            {matches.map((match, index) => (
              <div key={index} className="card-pav-white hover:shadow-lg transition-shadow">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-xl font-bold text-pav-ink">
                        {match.full_name}
                      </h3>
                      <span className="badge-pav-turquoise">
                        {match.personal_nummer}
                      </span>
                      <span className="badge-pav-green">
                        {match.status}
                      </span>
                    </div>
                    <p className="text-pav-ink/70">
                      {match.position} • {match.abteilung}
                    </p>
                  </div>

                  {/* Match Score */}
                  <div className="text-right">
                    <div className="text-3xl font-bold text-pav-dark-green mb-1">
                      {match.match_score.toFixed(0)}%
                    </div>
                    <div className="w-24 h-2 bg-pav-soft-grey rounded-pav-pill overflow-hidden">
                      <div
                        className={`h-full ${getScoreColor(match.match_score)}`}
                        style={{ width: `${match.match_score}%` }}
                      />
                    </div>
                  </div>
                </div>

                {/* Contact Info */}
                <div className="flex gap-4 mb-4 text-sm text-pav-ink/70">
                  <div className="flex items-center gap-2">
                    <Mail size={16} />
                    {match.email}
                  </div>
                </div>

                {/* AI Reasoning */}
                {match.reasoning && (
                  <div className="bg-pav-soft-grey p-4 rounded-pav-card mb-4">
                    <div className="flex items-start gap-2">
                      <Sparkles size={16} className="text-pav-magenta mt-1 flex-shrink-0" />
                      <div className="flex-1">
                        <p className="text-sm text-pav-ink font-medium mb-2 uppercase tracking-pav-nav">
                          KI-Begründung:
                        </p>
                        <p className="text-sm text-pav-ink/80">{match.reasoning}</p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Strengths */}
                {match.strengths && match.strengths.length > 0 && (
                  <div className="mb-4">
                    <div className="flex items-center gap-2 mb-2">
                      <TrendingUp size={16} className="text-pav-dark-green" />
                      <p className="text-sm text-pav-ink font-medium uppercase tracking-pav-nav">
                        Stärken:
                      </p>
                    </div>
                    <ul className="space-y-1 ml-6">
                      {match.strengths.map((strength, idx) => (
                        <li key={idx} className="text-sm text-pav-ink/80 list-disc">
                          {strength}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Gaps */}
                {match.gaps && match.gaps.length > 0 && (
                  <div className="mb-4">
                    <div className="flex items-center gap-2 mb-2">
                      <AlertTriangle size={16} className="text-pav-magenta" />
                      <p className="text-sm text-pav-ink font-medium uppercase tracking-pav-nav">
                        Mögliche Lücken:
                      </p>
                    </div>
                    <ul className="space-y-1 ml-6">
                      {match.gaps.map((gap, idx) => (
                        <li key={idx} className="text-sm text-pav-ink/80 list-disc">
                          {gap}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Qualifications */}
                {match.qualifikationen && match.qualifikationen.length > 0 && (
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <Award size={16} className="text-pav-turquoise" />
                      <p className="text-sm text-pav-ink font-medium uppercase tracking-pav-nav">
                        Qualifikationen:
                      </p>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {match.qualifikationen.map((qual, idx) => (
                        <span
                          key={idx}
                          className="badge-pav-green text-xs"
                        >
                          {qual}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* No Results */}
      {!loading && matches.length === 0 && query && (
        <div className="card-pav-white text-center py-12">
          <p className="text-pav-ink/60 text-lg uppercase tracking-pav-nav">
            Keine Ergebnisse gefunden
          </p>
          <p className="text-pav-ink/40 mt-2">
            Versuchen Sie eine andere Suchanfrage
          </p>
        </div>
      )}
    </div>
  );
}

export default AIMatching;
