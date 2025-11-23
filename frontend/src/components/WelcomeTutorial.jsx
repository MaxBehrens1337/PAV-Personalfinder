import { useState, useEffect } from 'react';
import { X, Sparkles, LayoutDashboard, Search, Users, ArrowRight } from 'lucide-react';

function WelcomeTutorial({ onClose }) {
  const [step, setStep] = useState(0);

  const steps = [
    {
      title: 'Willkommen beim PAV Personalfinder!',
      description: 'Ihre intelligente Lösung für Mitarbeiter-Matching mit KI-Unterstützung.',
      icon: Sparkles,
      color: 'text-pav-magenta',
      bgColor: 'bg-pav-magenta',
      content: (
        <div className="space-y-4">
          <p className="text-pav-ink/80">
            Dieses System nutzt modernste KI-Technologie, um den perfekten Mitarbeiter für Ihre Anforderungen zu finden.
          </p>
          <div className="bg-pav-soft-grey p-4 rounded-pav-card">
            <p className="text-sm text-pav-ink/70 mb-2 font-bold uppercase tracking-pav-nav">
              Was können Sie tun?
            </p>
            <ul className="space-y-2 text-sm text-pav-ink/80">
              <li className="flex items-start gap-2">
                <span className="text-pav-dark-green mt-1">✓</span>
                <span>Natürlichsprachliche Suche nach Mitarbeitern</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-pav-dark-green mt-1">✓</span>
                <span>KI-generierte Match-Scores und Begründungen</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-pav-dark-green mt-1">✓</span>
                <span>Übersichtliches Dashboard mit Analytics</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-pav-dark-green mt-1">✓</span>
                <span>Vollständige Mitarbeiterverwaltung</span>
              </li>
            </ul>
          </div>
        </div>
      ),
    },
    {
      title: 'Dashboard - Ihr Überblick',
      description: 'Sehen Sie alle wichtigen Kennzahlen auf einen Blick.',
      icon: LayoutDashboard,
      color: 'text-pav-turquoise',
      bgColor: 'bg-pav-turquoise',
      content: (
        <div className="space-y-4">
          <p className="text-pav-ink/80">
            Das Dashboard zeigt Ihnen:
          </p>
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-pav-soft-grey p-3 rounded-pav-card">
              <p className="text-xs uppercase tracking-pav-nav text-pav-ink/60 mb-1">Verfügbar</p>
              <p className="text-2xl font-bold text-pav-dark-green">24</p>
            </div>
            <div className="bg-pav-soft-grey p-3 rounded-pav-card">
              <p className="text-xs uppercase tracking-pav-nav text-pav-ink/60 mb-1">Im Einsatz</p>
              <p className="text-2xl font-bold text-pav-turquoise">8</p>
            </div>
            <div className="bg-pav-soft-grey p-3 rounded-pav-card">
              <p className="text-xs uppercase tracking-pav-nav text-pav-ink/60 mb-1">Im Urlaub</p>
              <p className="text-2xl font-bold text-pav-light-green">3</p>
            </div>
            <div className="bg-pav-soft-grey p-3 rounded-pav-card">
              <p className="text-xs uppercase tracking-pav-nav text-pav-ink/60 mb-1">Ablaufende Zertifikate</p>
              <p className="text-2xl font-bold text-pav-magenta">2</p>
            </div>
          </div>
          <p className="text-sm text-pav-ink/70">
            Zusätzlich sehen Sie Charts zur Abteilungs- und Qualifikations-Verteilung.
          </p>
        </div>
      ),
    },
    {
      title: 'KI-Suche - Das Highlight!',
      description: 'Finden Sie Mitarbeiter mit natürlicher Sprache.',
      icon: Search,
      color: 'text-pav-dark-green',
      bgColor: 'bg-pav-dark-green',
      content: (
        <div className="space-y-4">
          <p className="text-pav-ink/80">
            Beschreiben Sie einfach in normaler Sprache, wen Sie suchen:
          </p>
          <div className="bg-pav-soft-grey p-4 rounded-pav-card border-2 border-pav-turquoise">
            <p className="text-sm text-pav-ink/60 mb-2 uppercase tracking-pav-nav">Beispiel-Anfrage:</p>
            <p className="text-pav-ink italic">
              "Finde SAP-Experten für ein Logistik-Projekt"
            </p>
          </div>
          <div className="bg-pav-dark-green/10 p-4 rounded-pav-card">
            <p className="text-sm font-bold text-pav-dark-green mb-2 uppercase tracking-pav-nav flex items-center gap-2">
              <Sparkles size={16} />
              Die KI antwortet mit:
            </p>
            <ul className="space-y-2 text-sm text-pav-ink/80">
              <li className="flex items-start gap-2">
                <span className="text-pav-dark-green mt-1">→</span>
                <span><strong>Match-Score:</strong> Wie gut passt der Kandidat? (0-100%)</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-pav-dark-green mt-1">→</span>
                <span><strong>Begründung:</strong> Warum passt dieser Mitarbeiter?</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-pav-dark-green mt-1">→</span>
                <span><strong>Stärken:</strong> Was spricht dafür?</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-pav-dark-green mt-1">→</span>
                <span><strong>Mögliche Lücken:</strong> Was fehlt eventuell?</span>
              </li>
            </ul>
          </div>
          <p className="text-sm text-pav-ink/70">
            <strong>Tipp:</strong> Klicken Sie auf die Beispiel-Anfragen unter dem Suchfeld!
          </p>
        </div>
      ),
    },
    {
      title: 'Mitarbeiterverwaltung',
      description: 'Verwalten Sie alle Mitarbeiterdaten zentral.',
      icon: Users,
      color: 'text-pav-light-green',
      bgColor: 'bg-pav-light-green',
      content: (
        <div className="space-y-4">
          <p className="text-pav-ink/80">
            Unter "Mitarbeiter" finden Sie:
          </p>
          <ul className="space-y-3 text-sm text-pav-ink/80">
            <li className="flex items-start gap-3">
              <span className="bg-pav-light-green text-white rounded-full w-6 h-6 flex items-center justify-center flex-shrink-0 mt-0.5">1</span>
              <div>
                <strong>Übersichtsliste:</strong> Alle Mitarbeiter mit Suche und Filter
              </div>
            </li>
            <li className="flex items-start gap-3">
              <span className="bg-pav-light-green text-white rounded-full w-6 h-6 flex items-center justify-center flex-shrink-0 mt-0.5">2</span>
              <div>
                <strong>Detailansichten:</strong> Kontaktdaten, Qualifikationen, Verfügbarkeit
              </div>
            </li>
            <li className="flex items-start gap-3">
              <span className="bg-pav-light-green text-white rounded-full w-6 h-6 flex items-center justify-center flex-shrink-0 mt-0.5">3</span>
              <div>
                <strong>Schnellsuche:</strong> Nach Name, Email oder Personalnummer
              </div>
            </li>
          </ul>
          <div className="bg-pav-soft-grey p-3 rounded-pav-card">
            <p className="text-xs text-pav-ink/60 uppercase tracking-pav-nav">
              💡 Hinweis: Ihre Rolle bestimmt, was Sie bearbeiten dürfen.
            </p>
          </div>
        </div>
      ),
    },
    {
      title: 'Bereit loszulegen!',
      description: 'Viel Erfolg mit dem PAV Personalfinder!',
      icon: Sparkles,
      color: 'text-pav-magenta',
      bgColor: 'bg-gradient-to-br from-pav-turquoise via-pav-dark-green to-pav-light-green',
      content: (
        <div className="space-y-4">
          <p className="text-pav-ink/80">
            Sie sind jetzt bereit, den PAV Personalfinder zu nutzen!
          </p>
          <div className="bg-pav-soft-grey p-4 rounded-pav-card">
            <p className="font-bold text-pav-ink mb-3 uppercase tracking-pav-nav">Quick-Tipps:</p>
            <ul className="space-y-2 text-sm text-pav-ink/80">
              <li className="flex items-start gap-2">
                <span className="text-pav-dark-green">✓</span>
                <span>Probieren Sie verschiedene Suchanfragen aus</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-pav-dark-green">✓</span>
                <span>Nutzen Sie die Beispiel-Anfragen als Vorlage</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-pav-dark-green">✓</span>
                <span>Schauen Sie sich die Match-Begründungen genau an</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-pav-dark-green">✓</span>
                <span>Bei Fragen: Siehe USER_MANUAL.md</span>
              </li>
            </ul>
          </div>
          <div className="bg-gradient-to-r from-pav-turquoise/10 to-pav-dark-green/10 p-4 rounded-pav-card border-2 border-pav-turquoise">
            <p className="text-sm text-pav-ink/80">
              <strong>🎯 Empfohlener Start:</strong><br />
              Gehen Sie zu "KI-Suche" und probieren Sie: <em>"Finde SAP-Experten für Logistik"</em>
            </p>
          </div>
        </div>
      ),
    },
  ];

  const currentStep = steps[step];
  const Icon = currentStep.icon;

  const handleNext = () => {
    if (step < steps.length - 1) {
      setStep(step + 1);
    } else {
      localStorage.setItem('pav_tutorial_completed', 'true');
      onClose();
    }
  };

  const handleSkip = () => {
    localStorage.setItem('pav_tutorial_completed', 'true');
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-pav-ink/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-pav-white rounded-pav-card max-w-2xl w-full shadow-2xl">
        {/* Header */}
        <div className={`${currentStep.bgColor} p-6 rounded-t-pav-card text-white relative overflow-hidden`}>
          <button
            onClick={handleSkip}
            className="absolute top-4 right-4 hover:bg-white/20 p-2 rounded-pav-pill transition-colors"
          >
            <X size={24} />
          </button>

          <div className="flex items-start gap-4">
            <div className="bg-white/20 p-4 rounded-pav-card">
              <Icon size={32} strokeWidth={2} />
            </div>
            <div className="flex-1">
              <h2 className="text-2xl font-bold mb-2 uppercase tracking-pav-headline">
                {currentStep.title}
              </h2>
              <p className="text-white/90">
                {currentStep.description}
              </p>
            </div>
          </div>

          {/* Progress indicators */}
          <div className="flex gap-2 mt-4">
            {steps.map((_, index) => (
              <div
                key={index}
                className={`h-1 flex-1 rounded-pav-pill transition-all ${
                  index === step
                    ? 'bg-white'
                    : index < step
                    ? 'bg-white/60'
                    : 'bg-white/20'
                }`}
              />
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="p-6">
          {currentStep.content}
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-pav-soft-grey flex items-center justify-between">
          <button
            onClick={handleSkip}
            className="text-pav-ink/60 hover:text-pav-ink uppercase text-sm tracking-pav-nav font-medium"
          >
            Überspringen
          </button>

          <div className="flex items-center gap-3">
            <span className="text-sm text-pav-ink/60">
              {step + 1} von {steps.length}
            </span>
            <button
              onClick={handleNext}
              className="btn-pav-primary flex items-center gap-2"
            >
              {step === steps.length - 1 ? (
                <>
                  <span>Los geht's!</span>
                  <Sparkles size={20} />
                </>
              ) : (
                <>
                  <span>Weiter</span>
                  <ArrowRight size={20} />
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default WelcomeTutorial;
