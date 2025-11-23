# 🚀 Quick Start - In 5 Minuten loslegen!

Willkommen beim PAV Personalfinder! Diese Anleitung bringt Sie in **5 Minuten** zum laufenden System.

---

## ⚡ Super-Schnellstart (1 Befehl!)

```bash
bash setup.sh
```

**Das war's!** 🎉 Das Setup-Script erledigt alles automatisch:
- ✅ Prüft Voraussetzungen
- ✅ Erstellt Konfiguration
- ✅ Startet alle Services
- ✅ Lädt Demo-Daten
- ✅ Öffnet Browser

**Danach:**
1. Browser öffnet automatisch → http://localhost:3000
2. Login mit: `admin` / `admin123`
3. Fertig! Probieren Sie die KI-Suche aus!

---

## 📋 Manuelle Installation (3 Schritte)

Falls Sie es Schritt für Schritt machen möchten:

### Schritt 1: Voraussetzungen prüfen

```bash
# Docker installiert?
docker --version

# Docker Compose installiert?
docker-compose --version
```

**Nicht installiert?**
- Docker: https://docs.docker.com/get-docker/
- Docker Compose: https://docs.docker.com/compose/install/

### Schritt 2: Projekt vorbereiten

```bash
# .env-Datei erstellen
cp .env.example .env

# Optional: Secret Key ändern (für Produktion empfohlen)
# Öffnen Sie .env und ändern Sie SECRET_KEY
```

### Schritt 3: Starten

```bash
# Alle Services starten
make start

# Oder mit Docker Compose direkt:
docker-compose up -d
```

**Warten Sie 2-3 Minuten** - die Services starten gerade!

### Schritt 4: Demo-Daten laden

```bash
# Demo-Daten laden (3 User, 15 Mitarbeiter)
make seed

# Oder direkt:
docker-compose exec backend python ../scripts/seed_data.py
```

---

## 🎯 Erste Schritte nach dem Start

### 1. Anmelden

Öffnen Sie: **http://localhost:3000**

**Demo-Accounts:**
| Rolle | Benutzername | Passwort |
|-------|--------------|----------|
| Admin | `admin` | `admin123` |
| User | `hr_manager` | `hr123` |
| Viewer | `viewer` | `viewer123` |

### 2. Dashboard erkunden

Nach dem Login sehen Sie:
- **KPI-Cards** mit Mitarbeiter-Statistiken
- **Charts** mit Abteilungs- und Qualifikations-Verteilung

### 3. KI-Suche ausprobieren (DAS HIGHLIGHT!)

1. Klicken Sie auf **"KI-Suche"** in der Navigation
2. Geben Sie ein: *"Finde SAP-Experten für Logistik-Projekt"*
3. Klicken Sie auf **"MITARBEITER SUCHEN"**
4. **Staunen Sie!** 🤖

Die KI zeigt Ihnen:
- ✨ **Match-Score** (wie gut passt der Kandidat?)
- ✨ **KI-Begründung** (warum passt er?)
- ✨ **Stärken** (was spricht dafür?)
- ✨ **Mögliche Lücken** (was fehlt eventuell?)

**Weitere Beispiel-Anfragen:**
- *"Wer ist verfügbar nächste Woche mit Staplerführerschein?"*
- *"Zeige IT-Spezialisten mit Python-Erfahrung"*
- *"Finde einen Lagerleiter mit Führungserfahrung"*

### 4. Mitarbeiter anschauen

1. Klicken Sie auf **"Mitarbeiter"**
2. Sehen Sie alle 15 Demo-Mitarbeiter
3. Klicken Sie auf einen für Details

---

## 🛠️ Nützliche Befehle

Mit dem **Makefile** haben Sie einfache Shortcuts:

```bash
# Hilfe anzeigen
make help

# Services verwalten
make start          # Starten
make stop           # Stoppen
make restart        # Neustarten
make status         # Status anzeigen

# Logs & Monitoring
make logs           # Alle Logs
make backend-logs   # Nur Backend
make frontend-logs  # Nur Frontend
make health         # Gesundheits-Check

# Daten
make seed           # Demo-Daten laden
make db-backup      # Backup erstellen

# Probleme beheben
make restart        # Neustart
make clean          # Aufräumen
make reset          # Komplett zurücksetzen (ACHTUNG: Löscht Daten!)
```

---

## 🔍 Ist alles OK?

### Quick-Check

```bash
# Gesundheits-Check ausführen
make health
```

Dieser Befehl prüft:
- ✅ Alle Container laufen
- ✅ Frontend erreichbar
- ✅ Backend erreichbar
- ✅ Datenbank verbunden
- ✅ Ollama/KI läuft

### URLs zum Testen

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/health
- **API Dokumentation:** http://localhost:8000/docs
- **Qdrant:** http://localhost:6333/dashboard
- **Ollama:** http://localhost:11434

Alle sollten erreichbar sein!

---

## ⚠️ Probleme?

### Problem: Services starten nicht

**Lösung:**
```bash
# Logs prüfen
make logs

# Neustart
make restart

# Falls das nicht hilft - Clean Start
make clean
make start
make seed
```

### Problem: "Port already in use"

Ein anderer Service nutzt bereits Port 3000, 8000, 5432, 6333 oder 11434.

**Lösung:**
```bash
# Welcher Prozess nutzt Port 3000?
lsof -i :3000

# Oder alle Ports prüfen
lsof -i :3000 -i :8000 -i :5432 -i :6333 -i :11434

# Prozess stoppen oder Port in .env ändern
```

### Problem: KI-Suche funktioniert nicht

Die KI-Suche braucht Ollama mit dem Llama-Modell.

**Lösung:**
```bash
# Ollama-Status prüfen
make ollama-status

# Ollama-Logs ansehen
docker-compose logs ollama

# Modell wird beim ersten Start geladen (~4.7 GB, 10-15 Min)
# Warten Sie, bis Download abgeschlossen ist
```

**Fallback:** Deaktivieren Sie die Checkbox "KI-Matching verwenden" für klassische Suche.

### Problem: Keine Demo-Daten

**Lösung:**
```bash
# Einfach nochmal ausführen
make seed

# Oder manuell
docker-compose exec backend python ../scripts/seed_data.py
```

### Weitere Probleme?

Schauen Sie in **README.md** → Abschnitt "Troubleshooting"

---

## 💡 Tipps & Tricks

### Tipp 1: Makefile nutzen

Statt `docker-compose logs -f backend` → einfach `make backend-logs`

Alle Befehle: `make help`

### Tipp 2: Ollama-Download beschleunigen

Beim ersten Start lädt Ollama Llama 3.1 8B (~4.7 GB). Bei langsamer Verbindung:

```bash
# Download-Fortschritt beobachten
make ollama-status

# Logs live verfolgen
docker-compose logs -f ollama
```

### Tipp 3: Eigene Mitarbeiter anlegen

*(Feature kommt in nächster Version)*

Aktuell: Passen Sie `scripts/seed_data.py` an und führen Sie aus:
```bash
make seed
```

### Tipp 4: Backup erstellen

Bevor Sie Änderungen machen:
```bash
make db-backup
```

Backups finden Sie in `backups/`

### Tipp 5: Production-Deployment

Für echten Einsatz:
1. Ändern Sie `SECRET_KEY` in `.env` (wichtig!)
2. Ändern Sie alle Passwörter in `.env`
3. Aktivieren Sie HTTPS (Nginx Reverse Proxy)
4. Setup automatische Backups (Cronjob)

Details in **README.md** → "Deployment (Produktion)"

---

## 🎓 Wie geht's weiter?

### Sie sind jetzt startklar! 🎉

**Nächste Schritte:**
1. ✅ System läuft
2. ✅ Sie kennen die Grundlagen
3. 📖 Lesen Sie **USER_MANUAL.md** für Details
4. 🤖 Experimentieren Sie mit der KI-Suche
5. 👥 Schauen Sie sich Mitarbeiter-Details an

### Weiterführende Dokumentation

- **README.md** - Vollständige technische Dokumentation
- **USER_MANUAL.md** - Benutzerhandbuch für HR-Personal
- **API Docs** - http://localhost:8000/docs (Swagger UI)

---

## 📞 Hilfe & Support

**Bei Problemen:**
1. Prüfen Sie diese Datei (GETTING_STARTED.md)
2. Schauen Sie in README.md → Troubleshooting
3. Führen Sie `make health` aus
4. Prüfen Sie Logs mit `make logs`

**Feedback & Fragen:**
- GitHub Issues
- Ihr IT-Team
- Admin kontaktieren

---

## ✅ Checkliste für erfolgreichen Start

Haken Sie ab:

- [ ] Docker & Docker Compose installiert
- [ ] Repository geklont
- [ ] `bash setup.sh` ausgeführt ODER
  - [ ] `.env` erstellt
  - [ ] `make start` ausgeführt
  - [ ] `make seed` ausgeführt
- [ ] http://localhost:3000 öffnet sich
- [ ] Login mit `admin / admin123` funktioniert
- [ ] Dashboard zeigt Daten
- [ ] KI-Suche getestet
- [ ] Mitarbeiter-Liste angeschaut

**Alles ✓?** → **Glückwunsch, Sie sind startklar! 🚀**

---

**Made with ❤️ for PAV**

Viel Erfolg mit dem PAV Personalfinder!
