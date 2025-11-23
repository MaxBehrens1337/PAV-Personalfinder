# PAV Personalfinder

🤖 **KI-gestützter Personalfinder mit lokalem LLM**

Ein intelligentes Mitarbeiter-Matching-System für PAV, das lokales Llama 3.1 8B, semantische Suche mit Qdrant und ein modernes React-Frontend mit PAV Corporate Design kombiniert.

![PAV Logo](https://via.placeholder.com/150x50/018A9C/FFFFFF?text=PAV)

---

## 🎯 Überblick

Der PAV Personalfinder ist eine vollständig **offline-fähige** Anwendung, die KI-Technologie nutzt, um die besten Mitarbeiter für spezifische Anforderungen zu finden. Das System versteht natürlichsprachliche Anfragen und rankt Kandidaten intelligent basierend auf ihren Qualifikationen, Erfahrungen und Verfügbarkeit.

### Hauptfunktionen

✨ **KI-Matching** - Semantische Suche mit Llama 3.1 8B + Qdrant
📊 **Dashboard** - Echtzeit-KPIs und Analytics
👥 **Mitarbeiterverwaltung** - CRUD-Operationen für alle Mitarbeiterdaten
🎨 **PAV Corporate Design** - Perfekt umgesetztes PAV-Branding
🔒 **Sicherheit** - DSGVO-konform mit Audit-Log und Rollen-Management
🐳 **Docker-Ready** - Komplettes System mit einem Befehl starten

---

## 🏗️ Architektur

```
┌─────────────────┐
│   Frontend      │  React + Vite + Tailwind (PAV CI)
│   (Port 3000)   │
└────────┬────────┘
         │
┌────────▼────────┐
│   Backend API   │  FastAPI (Python)
│   (Port 8000)   │
└────┬───────┬────┘
     │       │
     ▼       ▼
┌─────────┐ ┌──────────┐
│PostgreSQL│ │  Qdrant  │  Vector Database
│ (Port   │ │ (Port    │  (Semantic Search)
│  5432)  │ │  6333)   │
└──────────┘ └────┬─────┘
                  │
            ┌─────▼─────┐
            │  Ollama   │  Llama 3.1 8B
            │ (Port     │  (LLM Evaluation)
            │ 11434)    │
            └───────────┘
```

### Tech-Stack

**Backend:**
- FastAPI (Python 3.11)
- SQLAlchemy + PostgreSQL
- Ollama (Llama 3.1 8B)
- Qdrant (Vector Database)
- Sentence-Transformers (Embeddings)
- JWT Authentication

**Frontend:**
- React 18
- Vite
- Tailwind CSS (PAV Custom Config)
- Zustand (State Management)
- React Router
- Recharts (Analytics)
- Lucide Icons

**Deployment:**
- Docker + Docker Compose
- 5 Container (Frontend, Backend, DB, Qdrant, Ollama)

---

## 🚀 Installation & Start

### Voraussetzungen

- Docker & Docker Compose installiert
- Mindestens 16 GB RAM (empfohlen: 32 GB)
- ~50 GB freier Festplattenspeicher
- Optional: NVIDIA GPU für schnellere KI-Inferenz

### Schnellstart (3 Schritte)

```bash
# 1. Repository klonen
git clone <repo-url>
cd PAV-Personalfinder

# 2. Environment-Datei erstellen
cp .env.example .env
# Optional: Passen Sie die Werte in .env an

# 3. Starten
docker-compose up -d
```

### Erste Schritte nach dem Start

1. **Warten Sie ~2-3 Minuten**, bis alle Services gestartet sind
2. **Llama-Modell wird beim ersten Start automatisch geladen** (~4.7 GB Download)
3. **Öffnen Sie die Anwendung**: [http://localhost:3000](http://localhost:3000)

### Demo-Accounts

| Rolle | Username | Passwort | Berechtigungen |
|-------|----------|----------|----------------|
| Admin | `admin` | `admin123` | Voller Zugriff |
| User | `hr_manager` | `hr123` | Lesen + Schreiben |
| Read-Only | `viewer` | `viewer123` | Nur Lesen |

### Seed-Daten einfügen

```bash
# Backend-Container betreten
docker-compose exec backend bash

# Seed-Script ausführen
python ../scripts/seed_data.py

# Verlassen
exit
```

Dies erstellt:
- 3 Demo-User
- 15 Beispiel-Mitarbeiter
- ~15 Qualifikationen
- Verfügbarkeits-Einträge

---

## 📖 Bedienungsanleitung

### 1. Login

Öffnen Sie [http://localhost:3000](http://localhost:3000) und melden Sie sich mit einem der Demo-Accounts an.

### 2. Dashboard

Nach dem Login sehen Sie das Dashboard mit:
- **KPI-Cards**: Verfügbare Mitarbeiter, Im Einsatz, Im Urlaub, etc.
- **Abteilungsverteilung**: Pie Chart
- **Top Qualifikationen**: Bar Chart

### 3. KI-Suche (Hauptfeature!)

Navigieren Sie zu **KI-Suche** und geben Sie eine natürlichsprachliche Anfrage ein:

**Beispiele:**
- *"Ich suche jemanden für ein Logistik-Projekt mit SAP-Kenntnissen"*
- *"Wer ist verfügbar nächste Woche mit Staplerführerschein?"*
- *"Zeige mir IT-Spezialisten mit Python-Erfahrung"*

Die KI wird:
1. Ihre Anfrage verstehen
2. Semantisch ähnliche Profile finden (Qdrant)
3. Jeden Kandidaten mit Llama 3.1 evaluieren
4. Ranked Results mit **Match-Score**, **Begründung**, **Stärken** und **möglichen Lücken** liefern

### 4. Mitarbeiterverwaltung

- **Liste anzeigen**: Alle Mitarbeiter mit Filter/Suche
- **Details ansehen**: Klicken Sie auf einen Mitarbeiter
- **Bearbeiten/Löschen**: Admin/User-Rechte erforderlich

---

## 🎨 PAV Corporate Design

Das Frontend implementiert **100% PAV Corporate Identity**:

### Farben

```css
--pav-turquoise: #018A9C;    /* Primary: Navigation, Key-UI */
--pav-dark-green: #009657;   /* Buttons (CTA), Akzente */
--pav-light-green: #50AF31;  /* Sekundäre UI-Akzente */
--pav-magenta: #E62487;      /* Nur Badges/Highlights (sparsam!) */
--pav-white: #FFFFFF;        /* Haupt-Hintergrund */
--pav-ink: #111111;          /* Standard-Fließtext */
--pav-soft-grey: #F4F6F7;    /* Panels, Sektionen */
```

### Typografie

- **Font**: Inter (Bold, Medium, Regular)
- **Headlines**: UPPERCASE, Bold, +80 Letter-Spacing
- **Navigation**: UPPERCASE, Medium/Bold, +60 Letter-Spacing
- **Body**: Regular, +20 Letter-Spacing

### Komponenten

- **Buttons**: Pill-Form (999px Radius), Dunkelgrün
- **Cards**: 24px Radius, Soft-Grey Hintergrund
- **Icons**: 2px Stroke, Outline-Stil, Rounded Caps
- **Logo**: Bottom-Right Position

---

## 🔒 Sicherheit & DSGVO

### Sicherheits-Features

✅ **Passwörter mit bcrypt gehasht**
✅ **JWT-basierte Authentifizierung**
✅ **Rollen-basierte Zugriffskontrolle (RBAC)**
✅ **SQL-Injection-Schutz (ORM)**
✅ **Input-Validation (Backend + Frontend)**
✅ **Session-Timeout (30 Min)**
✅ **Audit-Log für alle kritischen Aktionen**
✅ **CORS konfiguriert**

### DSGVO-Compliance

- **Datenminimierung**: Nur notwendige Felder
- **Audit-Trail**: Wer hat was wann geändert?
- **Datenexport**: Möglich über API
- **Lösch-Funktion**: DSGVO Artikel 17 konform
- **Zugriffskontrolle**: Rollen-basiert

### User-Rollen

| Rolle | Berechtigung |
|-------|--------------|
| **Admin** | Voller Zugriff, User-Verwaltung, System-Settings |
| **User** | CRUD auf Mitarbeiter, Suchen, Reports |
| **Read-Only** | Nur Ansicht, keine Änderungen |

---

## 🤖 KI-Matching Details

### Wie funktioniert das KI-Matching?

1. **User-Anfrage**: "Finde SAP-Experten für Logistik"

2. **Embedding-Generierung**:
   - Query wird mit Sentence-Transformer in 384-dim Vektor umgewandelt

3. **Semantische Suche (Qdrant)**:
   - Vector Similarity Search findet Top-20 ähnlichste Profile
   - Threshold: 0.3 (nur relevante Ergebnisse)

4. **LLM-Evaluation (Llama 3.1 8B)**:
   - Jeder Kandidat wird einzeln bewertet
   - Prompt enthält: User-Anfrage + Mitarbeiter-Profil
   - LLM generiert:
     - **Match-Score** (0-100%)
     - **Begründung** (1-2 Sätze)
     - **Stärken** (2-3 Punkte)
     - **Lücken** (optional)

5. **Ranked Results**:
   - Sortiert nach Match-Score
   - Mit KI-generierten Insights

### Fallback-Modus

Wenn Ollama nicht verfügbar ist:
- Klassische SQL-basierte Textsuche
- Funktioniert weiterhin, nur ohne KI-Insights

---

## 📊 API-Dokumentation

Nach dem Start verfügbar unter:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Wichtige Endpoints

```
POST   /api/auth/login           # Login
GET    /api/dashboard/stats      # Dashboard KPIs
POST   /api/ai-match/search      # KI-Matching
GET    /api/mitarbeiter/          # Mitarbeiter-Liste
POST   /api/mitarbeiter/          # Mitarbeiter erstellen
```

---

## 🛠️ Entwicklung

### Backend entwickeln

```bash
# Backend-Container Shell
docker-compose exec backend bash

# Tests ausführen (optional)
pytest

# Linting
black .
flake8 .
```

### Frontend entwickeln

```bash
# Frontend-Container Shell
docker-compose exec frontend sh

# Dependencies installieren
npm install

# Linting
npm run lint
```

### Logs anzeigen

```bash
# Alle Services
docker-compose logs -f

# Nur Backend
docker-compose logs -f backend

# Nur Ollama
docker-compose logs -f ollama
```

---

## 🔧 Konfiguration

### Environment Variables (.env)

Wichtige Einstellungen:

```env
# Datenbank
DATABASE_URL=postgresql://pav_user:pav_password@db:5432/pav_personalfinder

# Security (WICHTIG: In Produktion ändern!)
SECRET_KEY=your-super-secret-key-change-this-in-production

# KI-Features
ENABLE_AI_MATCHING=true
OLLAMA_MODEL=llama3.1:8b
QDRANT_COLLECTION_NAME=employee_profiles

# Performance
MAX_SEARCH_RESULTS=50
AI_MATCHING_TIMEOUT=10
```

### Anpassungen

**Andere LLM-Modelle verwenden:**
```env
OLLAMA_MODEL=llama3.1:70b  # Für bessere Ergebnisse (benötigt mehr RAM)
OLLAMA_MODEL=mistral:7b    # Alternative
```

**Embedding-Modell ändern:**
```env
EMBEDDING_MODEL=all-MiniLM-L6-v2     # Standard (klein, schnell)
EMBEDDING_MODEL=all-mpnet-base-v2   # Besser, aber langsamer
```

---

## 📦 Backup & Restore

### Datenbank-Backup

```bash
# Backup erstellen
docker-compose exec db pg_dump -U pav_user pav_personalfinder > backup.sql

# Restore
docker-compose exec -T db psql -U pav_user pav_personalfinder < backup.sql
```

### Qdrant-Daten sichern

```bash
# Volumes sichern
docker cp pav-personalfinder_qdrant_data:/qdrant/storage ./qdrant_backup
```

---

## ⚠️ Troubleshooting

### Problem: Ollama startet nicht

**Lösung:**
```bash
# Ollama-Logs prüfen
docker-compose logs ollama

# Container neu starten
docker-compose restart ollama

# Modell manuell laden
docker-compose exec ollama ollama pull llama3.1:8b
```

### Problem: KI-Matching funktioniert nicht

**Lösung:**
1. Prüfen ob Ollama läuft: [http://localhost:11434](http://localhost:11434)
2. Prüfen ob Qdrant läuft: [http://localhost:6333](http://localhost:6333)
3. Re-index ausführen:
   ```bash
   curl -X POST http://localhost:8000/api/ai-match/reindex \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

### Problem: Frontend lädt nicht

**Lösung:**
```bash
# Frontend-Logs prüfen
docker-compose logs frontend

# Container neu starten
docker-compose restart frontend

# Node-Modules neu installieren
docker-compose exec frontend npm install
```

### Problem: Login schlägt fehl

**Lösung:**
1. Seed-Daten eingefügt? Siehe "Seed-Daten einfügen"
2. Backend-Logs prüfen: `docker-compose logs backend`
3. Datenbank-Verbindung testen:
   ```bash
   docker-compose exec db psql -U pav_user -d pav_personalfinder -c "SELECT * FROM users;"
   ```

---

## 🚢 Deployment (Produktion)

### Wichtige Änderungen für Produktion

1. **Secrets ändern**:
   ```env
   SECRET_KEY=$(openssl rand -hex 32)
   POSTGRES_PASSWORD=<sicheres-passwort>
   ```

2. **Debug ausschalten**:
   ```env
   DEBUG=False
   LOG_LEVEL=WARNING
   ```

3. **HTTPS aktivieren**:
   - Nginx Reverse Proxy vor Frontend/Backend
   - SSL-Zertifikate (Let's Encrypt)

4. **Backups automatisieren**:
   - Cronjob für tägliche DB-Backups
   - Qdrant-Volume-Backups

5. **Resource Limits setzen**:
   ```yaml
   # docker-compose.yml
   services:
     backend:
       deploy:
         resources:
           limits:
             cpus: '2'
             memory: 4G
   ```

---

## 📄 Lizenz & Credits

**Entwickelt für PAV**
© 2025 PAV Personalfinder

**Open Source Libraries:**
- FastAPI (MIT)
- React (MIT)
- Ollama (MIT)
- Qdrant (Apache 2.0)
- Tailwind CSS (MIT)

---

## 🆘 Support

Bei Problemen oder Fragen:

1. **Issue erstellen**: GitHub Issues
2. **Logs prüfen**: `docker-compose logs`
3. **Dokumentation**: Diese README + USER_MANUAL.md

---

## 🎯 Roadmap

Mögliche zukünftige Features:

- [ ] Email-Benachrichtigungen bei ablaufenden Zertifikaten
- [ ] Excel/CSV-Import für Bulk-Mitarbeiter
- [ ] PDF-Export von Reports
- [ ] PWA-Support (Offline-Nutzung)
- [ ] Multi-Language (DE/EN)
- [ ] Advanced Analytics (Trends, Predictions)
- [ ] Slack/Teams-Integration

---

**Made with ❤️ for PAV**
