# PAV Personalfinder - Benutzerhandbuch

## Für HR-Personal & Anwender

---

## 📋 Inhaltsverzeichnis

1. [Anmeldung](#1-anmeldung)
2. [Dashboard](#2-dashboard)
3. [KI-Suche - Mitarbeiter finden](#3-ki-suche---mitarbeiter-finden)
4. [Mitarbeiterverwaltung](#4-mitarbeiterverwaltung)
5. [Häufig gestellte Fragen (FAQ)](#5-häufig-gestellte-fragen)

---

## 1. Anmeldung

### So melden Sie sich an:

1. Öffnen Sie die Anwendung in Ihrem Browser: **http://localhost:3000**

2. Geben Sie Ihre Zugangsdaten ein:
   - **Benutzername**
   - **Passwort**

3. Klicken Sie auf **"ANMELDEN"**

### Benutzer-Rollen

Es gibt drei verschiedene Benutzer-Typen:

| Rolle | Was können Sie tun? |
|-------|---------------------|
| **Admin** | Alles - Mitarbeiter verwalten, Benutzer anlegen, System konfigurieren |
| **User** | Mitarbeiter anlegen, bearbeiten, löschen, suchen |
| **Viewer** | Nur anschauen - keine Änderungen möglich |

---

## 2. Dashboard

Nach der Anmeldung sehen Sie das **Dashboard** - Ihre Übersicht.

### Was sehen Sie hier?

#### KPI-Karten (oben)

- **Gesamt**: Wie viele Mitarbeiter gibt es insgesamt?
- **Verfügbar**: Wie viele sind aktuell einsatzbereit?
- **Im Einsatz**: Wie viele sind gerade in Projekten?
- **Im Urlaub**: Wie viele sind im Urlaub?
- **Krank**: Wie viele sind krankgemeldet?
- **⚠️ Ablaufende Zertifikate**: Wie viele Zertifikate laufen in den nächsten 30 Tagen ab?

#### Diagramme (unten)

- **Abteilungsverteilung**: Kreisdiagramm zeigt, wie viele Mitarbeiter in welcher Abteilung sind
- **Top 10 Qualifikationen**: Balkendiagramm zeigt die häufigsten Skills/Zertifikate

---

## 3. KI-Suche - Mitarbeiter finden

**Das Hauptfeature!** Hier finden Sie den perfekten Mitarbeiter für Ihre Anforderungen.

### So funktioniert's:

1. **Klicken Sie in der Navigation auf "KI-SUCHE"**

2. **Beschreiben Sie, wen Sie suchen** - in normaler Sprache!

   **Beispiele:**
   - *"Ich suche jemanden für ein Logistik-Projekt mit SAP-Kenntnissen"*
   - *"Wer ist verfügbar nächste Woche mit Staplerführerschein?"*
   - *"Zeige mir IT-Spezialisten mit Python-Erfahrung"*
   - *"Finde einen Lagerleiter mit Führungserfahrung"*

3. **Klicken Sie auf "MITARBEITER SUCHEN"**

4. **Warten Sie 3-10 Sekunden** - Die KI analysiert gerade alle Profile!

### Ergebnisse verstehen

Für jeden gefundenen Mitarbeiter sehen Sie:

#### Match-Score (0-100%)
- **80-100%**: Perfekte Übereinstimmung ⭐⭐⭐
- **60-79%**: Gute Übereinstimmung ⭐⭐
- **40-59%**: Teilweise passend ⭐
- **0-39%**: Wenig passend

#### KI-Begründung
Die KI erklärt Ihnen in 1-2 Sätzen, **warum** dieser Mitarbeiter passt.

**Beispiel:**
> *"Hervorragende Übereinstimmung: Max verfügt über 5 Jahre SAP-Erfahrung im Logistik-Bereich und hat bereits ähnliche Projekte geleitet."*

#### Stärken
Liste der **passenden Qualifikationen** und Erfahrungen:
- ✅ 5 Jahre SAP-Erfahrung
- ✅ Logistik-Background
- ✅ Verfügbar ab nächster Woche
- ✅ Staplerführerschein vorhanden

#### Mögliche Lücken (falls vorhanden)
Was könnte fehlen oder wo gibt es Einschränkungen:
- ⚠️ Kein Kranführerschein
- ⚠️ Englischkenntnisse nur Grundlagen

#### Qualifikationen
Alle Zertifikate, Skills und Erfahrungen des Mitarbeiters als grüne Badges.

### Tipps für bessere Suchergebnisse

✅ **Gut:**
- "Finde SAP-Experten für Logistik-Projekt"
- "Wer hat Staplerführerschein und ist verfügbar?"
- "Zeige Python-Entwickler mit IT-Erfahrung"

❌ **Weniger gut:**
- "MA-001" (nutzen Sie dafür die normale Mitarbeiter-Suche)
- "Alle" (zu unspezifisch)
- Einzelne Buchstaben

### KI-Matching ein/ausschalten

Sie können die KI-Suche deaktivieren:
- Checkbox **"KI-Matching verwenden"** ausschalten
- Dann wird eine klassische Textsuche durchgeführt (schneller, aber weniger intelligent)

---

## 4. Mitarbeiterverwaltung

Hier verwalten Sie alle Mitarbeiter-Daten.

### Mitarbeiter-Liste anzeigen

1. **Klicken Sie auf "MITARBEITER"** in der Navigation

2. Sie sehen alle Mitarbeiter als Karten mit:
   - Name
   - Position & Abteilung
   - Status (verfügbar, im Urlaub, etc.)
   - Email
   - Personalnummer

### Mitarbeiter suchen

Nutzen Sie das Suchfeld oben:
- Suche nach **Name** (z.B. "Max Mustermann")
- Suche nach **Email** (z.B. "max@pav.de")
- Suche nach **Personalnummer** (z.B. "MA-001")

### Mitarbeiter-Details ansehen

**Klicken Sie auf eine Mitarbeiter-Karte**, um Details zu sehen:
- Vollständige Kontaktinformationen
- Abteilung & Position
- Eintrittsdatum
- Wochenstunden
- Status

### Mitarbeiter bearbeiten (nur User/Admin)

*(Feature wird in der nächsten Version verfügbar sein)*

### Mitarbeiter löschen (nur User/Admin)

*(Feature wird in der nächsten Version verfügbar sein)*

---

## 5. Häufig gestellte Fragen (FAQ)

### Allgemeine Fragen

**F: Wie finde ich den besten Mitarbeiter für mein Projekt?**
A: Nutzen Sie die **KI-Suche**! Beschreiben Sie einfach in normaler Sprache, was Sie brauchen. Die KI findet und rankt automatisch die besten Kandidaten.

**F: Was bedeutet der Match-Score?**
A: Der Score zeigt, wie gut ein Mitarbeiter zu Ihren Anforderungen passt:
- 80%+ = Sehr gut passend
- 60-79% = Gut passend
- 40-59% = Teilweise passend
- unter 40% = Weniger passend

**F: Wie lange dauert die KI-Suche?**
A: In der Regel **3-10 Sekunden**. Je mehr Mitarbeiter Sie haben, desto länger kann es dauern.

**F: Funktioniert die Suche auch ohne Internet?**
A: **Ja!** Die gesamte Anwendung läuft lokal auf Ihrem Server. Kein Internet nötig.

### Technische Fragen

**F: Ich kann mich nicht anmelden - was tun?**
A:
1. Prüfen Sie Benutzername und Passwort (Groß-/Kleinschreibung beachten!)
2. Kontaktieren Sie Ihren Admin
3. Prüfen Sie, ob Ihr Account noch aktiv ist

**F: Die KI-Suche liefert keine Ergebnisse - warum?**
A:
1. Versuchen Sie eine **andere Formulierung**
2. Versuchen Sie **weniger spezifische Anforderungen**
3. Deaktivieren Sie "KI-Matching" und nutzen Sie die klassische Suche

**F: Ich sehe nur "Laden..." - was tun?**
A:
1. Warten Sie noch 10 Sekunden
2. Laden Sie die Seite neu (F5)
3. Kontaktieren Sie Ihren IT-Support

**F: Kann ich Mitarbeiter-Daten exportieren?**
A: Diese Funktion wird in einer zukünftigen Version verfügbar sein.

### Datenschutz-Fragen

**F: Wer kann meine Suchanfragen sehen?**
A: Nur **Admins** können im Audit-Log sehen, wer wann gesucht hat. Normale User und Viewer sehen nur ihre eigenen Daten.

**F: Werden meine Daten in die Cloud gesendet?**
A: **Nein!** Alle Daten bleiben auf Ihrem lokalen Server. Nichts wird ins Internet gesendet.

**F: Wer darf Mitarbeiter-Daten ändern?**
A: Nur **User** und **Admins**. Viewer können nur lesen.

---

## 🆘 Hilfe & Support

### Ich habe ein Problem!

1. **Seite neu laden**: Drücken Sie F5
2. **Aus- und wieder einloggen**: Manchmal hilft das
3. **Kontaktieren Sie Ihren Admin**
4. **IT-Support kontaktieren**

### Feedback & Verbesserungsvorschläge

Wir freuen uns über Ihr Feedback!
- Was gefällt Ihnen?
- Was könnte besser sein?
- Welche Funktionen wünschen Sie sich?

→ Sprechen Sie mit Ihrem Admin oder IT-Team

---

## 🎓 Tipps für Fortgeschrittene

### Workflow-Empfehlung

So finden Sie schnell den richtigen Mitarbeiter:

1. **Dashboard checken**: Wie viele sind überhaupt verfügbar?
2. **KI-Suche nutzen**: "Finde [Qualifikation] für [Projekt/Aufgabe]"
3. **Top-3-Matches ansehen**: Detailinfos prüfen
4. **Mitarbeiter kontaktieren**: Email/Telefon aus Detailansicht

### Power-User-Tricks

🔥 **Tipp 1: Gespeicherte Suchen**
*(Feature kommt bald)*
Speichern Sie häufige Suchanfragen wie "Logistik-Mitarbeiter mit Stapler" zur späteren Wiederverwendung.

🔥 **Tipp 2: Beispiel-Anfragen nutzen**
Unter dem Suchfeld finden Sie Beispiel-Anfragen. Klicken Sie darauf, um sie als Vorlage zu nutzen und anzupassen.

🔥 **Tipp 3: Dashboard-Widgets**
Nutzen Sie die Diagramme, um zu sehen, welche Qualifikationen häufig vorkommen. Das hilft bei der Projekt-Planung!

---

**Viel Erfolg mit dem PAV Personalfinder! 🚀**

Bei Fragen wenden Sie sich an Ihren Administrator oder IT-Support.

---

© 2025 PAV Personalfinder - Benutzerhandbuch v1.0
