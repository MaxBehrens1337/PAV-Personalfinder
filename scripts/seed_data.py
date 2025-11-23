#!/usr/bin/env python3
"""
Seed Data Script for PAV Personalfinder
Creates demo data for testing and demonstration
"""

import sys
import os
from datetime import date, timedelta
from decimal import Decimal

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.database import SessionLocal, init_db
from app.models.user import User, UserRolle
from app.models.mitarbeiter import Mitarbeiter, MitarbeiterStatus
from app.models.qualifikation import Qualifikation, MitarbeiterQualifikation, QualifikationKategorie, QualifikationLevel
from app.models.verfuegbarkeit import Verfuegbarkeit, VerfuegbarkeitTyp
from app.services.auth import auth_service


def create_users(db):
    """Create demo users"""
    print("Creating users...")

    users_data = [
        {
            "username": "admin",
            "email": "admin@pav.de",
            "password": "admin123",
            "rolle": UserRolle.ADMIN,
        },
        {
            "username": "hr_manager",
            "email": "hr@pav.de",
            "password": "hr123",
            "rolle": UserRolle.USER,
        },
        {
            "username": "viewer",
            "email": "viewer@pav.de",
            "password": "viewer123",
            "rolle": UserRolle.READONLY,
        },
    ]

    for user_data in users_data:
        existing = db.query(User).filter(User.username == user_data["username"]).first()
        if not existing:
            password = user_data.pop("password")
            user = User(
                **user_data,
                password_hash=auth_service.hash_password(password),
                is_active=True
            )
            db.add(user)
            print(f"  ✓ Created user: {user_data['username']}")

    db.commit()


def create_qualifikationen(db):
    """Create demo qualifications"""
    print("Creating qualifications...")

    qualifikationen_data = [
        # Zertifikate
        {"name": "Staplerführerschein", "kategorie": QualifikationKategorie.ZERTIFIKAT, "beschreibung": "Berechtigung zum Führen von Gabelstaplern"},
        {"name": "Kranführerschein", "kategorie": QualifikationKategorie.ZERTIFIKAT, "beschreibung": "Berechtigung zum Führen von Kränen"},
        {"name": "Erste-Hilfe-Schein", "kategorie": QualifikationKategorie.ZERTIFIKAT, "beschreibung": "Erste-Hilfe-Ausbildung"},
        {"name": "Gefahrgut-Schein ADR", "kategorie": QualifikationKategorie.ZERTIFIKAT, "beschreibung": "Gefahrguttransport-Berechtigung"},

        # Skills
        {"name": "SAP", "kategorie": QualifikationKategorie.SKILL, "beschreibung": "SAP ERP Kenntnisse"},
        {"name": "Excel Fortgeschritten", "kategorie": QualifikationKategorie.SKILL, "beschreibung": "Erweiterte Excel-Kenntnisse"},
        {"name": "Projektmanagement", "kategorie": QualifikationKategorie.SKILL, "beschreibung": "Projektmanagement-Kenntnisse"},
        {"name": "Lagerverwaltung", "kategorie": QualifikationKategorie.SKILL, "beschreibung": "Lagerverwaltungssysteme"},
        {"name": "Qualitätsmanagement", "kategorie": QualifikationKategorie.SKILL, "beschreibung": "QM-Systeme und Normen"},
        {"name": "Englisch", "kategorie": QualifikationKategorie.SKILL, "beschreibung": "Englische Sprachkenntnisse"},
        {"name": "Python", "kategorie": QualifikationKategorie.SKILL, "beschreibung": "Python-Programmierung"},
        {"name": "SQL", "kategorie": QualifikationKategorie.SKILL, "beschreibung": "Datenbankabfragen"},

        # Erfahrung
        {"name": "Logistik 5+ Jahre", "kategorie": QualifikationKategorie.ERFAHRUNG, "beschreibung": "Mindestens 5 Jahre Erfahrung in Logistik"},
        {"name": "Führungserfahrung", "kategorie": QualifikationKategorie.ERFAHRUNG, "beschreibung": "Erfahrung in Teamleitung"},
        {"name": "Kundenbetreuung", "kategorie": QualifikationKategorie.ERFAHRUNG, "beschreibung": "Erfahrung im Kundenkontakt"},
    ]

    for qual_data in qualifikationen_data:
        existing = db.query(Qualifikation).filter(Qualifikation.name == qual_data["name"]).first()
        if not existing:
            qual = Qualifikation(**qual_data)
            db.add(qual)
            print(f"  ✓ Created qualification: {qual_data['name']}")

    db.commit()


def create_mitarbeiter(db):
    """Create demo employees"""
    print("Creating employees...")

    mitarbeiter_data = [
        {
            "personal_nummer": "MA-001",
            "vorname": "Max",
            "nachname": "Mustermann",
            "email": "max.mustermann@pav.de",
            "abteilung": "Logistik",
            "position": "Lagerleiter",
            "telefon": "+49 431 1234-101",
            "eintritt_datum": date(2018, 3, 1),
            "status": MitarbeiterStatus.AKTIV,
            "wochenstunden": Decimal("40.00"),
            "qualifikationen": ["SAP", "Staplerführerschein", "Logistik 5+ Jahre", "Führungserfahrung"],
        },
        {
            "personal_nummer": "MA-002",
            "vorname": "Anna",
            "nachname": "Schmidt",
            "email": "anna.schmidt@pav.de",
            "abteilung": "IT",
            "position": "IT-Administratorin",
            "telefon": "+49 431 1234-102",
            "eintritt_datum": date(2019, 7, 15),
            "status": MitarbeiterStatus.AKTIV,
            "wochenstunden": Decimal("40.00"),
            "qualifikationen": ["Python", "SQL", "Projektmanagement", "Englisch"],
        },
        {
            "personal_nummer": "MA-003",
            "vorname": "Thomas",
            "nachname": "Weber",
            "email": "thomas.weber@pav.de",
            "abteilung": "Logistik",
            "position": "Lagerist",
            "telefon": "+49 431 1234-103",
            "eintritt_datum": date(2020, 1, 10),
            "status": MitarbeiterStatus.AKTIV,
            "wochenstunden": Decimal("40.00"),
            "qualifikationen": ["Staplerführerschein", "Lagerverwaltung"],
        },
        {
            "personal_nummer": "MA-004",
            "vorname": "Julia",
            "nachname": "Becker",
            "email": "julia.becker@pav.de",
            "abteilung": "HR",
            "position": "Personalreferentin",
            "telefon": "+49 431 1234-104",
            "eintritt_datum": date(2017, 9, 1),
            "status": MitarbeiterStatus.AKTIV,
            "wochenstunden": Decimal("30.00"),
            "qualifikationen": ["SAP", "Excel Fortgeschritten", "Kundenbetreuung"],
        },
        {
            "personal_nummer": "MA-005",
            "vorname": "Michael",
            "nachname": "Fischer",
            "email": "michael.fischer@pav.de",
            "abteilung": "Logistik",
            "position": "Staplerfahrer",
            "telefon": "+49 431 1234-105",
            "eintritt_datum": date(2021, 2, 1),
            "status": MitarbeiterStatus.AKTIV,
            "wochenstunden": Decimal("40.00"),
            "qualifikationen": ["Staplerführerschein", "Erste-Hilfe-Schein"],
        },
        {
            "personal_nummer": "MA-006",
            "vorname": "Sarah",
            "nachname": "Meyer",
            "email": "sarah.meyer@pav.de",
            "abteilung": "Qualität",
            "position": "QM-Beauftragte",
            "telefon": "+49 431 1234-106",
            "eintritt_datum": date(2019, 5, 1),
            "status": MitarbeiterStatus.AKTIV,
            "wochenstunden": Decimal("40.00"),
            "qualifikationen": ["Qualitätsmanagement", "Excel Fortgeschritten", "Projektmanagement"],
        },
        {
            "personal_nummer": "MA-007",
            "vorname": "Lars",
            "nachname": "Wagner",
            "email": "lars.wagner@pav.de",
            "abteilung": "Logistik",
            "position": "Lagerist",
            "telefon": "+49 431 1234-107",
            "eintritt_datum": date(2022, 1, 1),
            "status": MitarbeiterStatus.URLAUB,
            "wochenstunden": Decimal("40.00"),
            "qualifikationen": ["Staplerführerschein", "Gefahrgut-Schein ADR"],
        },
        {
            "personal_nummer": "MA-008",
            "vorname": "Petra",
            "nachname": "Hoffmann",
            "email": "petra.hoffmann@pav.de",
            "abteilung": "Verwaltung",
            "position": "Buchhalterin",
            "telefon": "+49 431 1234-108",
            "eintritt_datum": date(2016, 4, 1),
            "status": MitarbeiterStatus.AKTIV,
            "wochenstunden": Decimal("35.00"),
            "qualifikationen": ["SAP", "Excel Fortgeschritten"],
        },
        {
            "personal_nummer": "MA-009",
            "vorname": "Jan",
            "nachname": "Schulz",
            "email": "jan.schulz@pav.de",
            "abteilung": "Logistik",
            "position": "Kranführer",
            "telefon": "+49 431 1234-109",
            "eintritt_datum": date(2020, 8, 1),
            "status": MitarbeiterStatus.AKTIV,
            "wochenstunden": Decimal("40.00"),
            "qualifikationen": ["Kranführerschein", "Staplerführerschein", "Erste-Hilfe-Schein"],
        },
        {
            "personal_nummer": "MA-010",
            "vorname": "Claudia",
            "nachname": "Richter",
            "email": "claudia.richter@pav.de",
            "abteilung": "IT",
            "position": "IT-Support",
            "telefon": "+49 431 1234-110",
            "eintritt_datum": date(2021, 6, 1),
            "status": MitarbeiterStatus.AKTIV,
            "wochenstunden": Decimal("40.00"),
            "qualifikationen": ["Python", "SQL", "Kundenbetreuung", "Englisch"],
        },
        {
            "personal_nummer": "MA-011",
            "vorname": "Stefan",
            "nachname": "Klein",
            "email": "stefan.klein@pav.de",
            "abteilung": "Logistik",
            "position": "Logistikkoordinator",
            "telefon": "+49 431 1234-111",
            "eintritt_datum": date(2018, 11, 1),
            "status": MitarbeiterStatus.AKTIV,
            "wochenstunden": Decimal("40.00"),
            "qualifikationen": ["SAP", "Logistik 5+ Jahre", "Projektmanagement", "Englisch"],
        },
        {
            "personal_nummer": "MA-012",
            "vorname": "Nicole",
            "nachname": "Wolf",
            "email": "nicole.wolf@pav.de",
            "abteilung": "HR",
            "position": "HR-Assistentin",
            "telefon": "+49 431 1234-112",
            "eintritt_datum": date(2022, 3, 1),
            "status": MitarbeiterStatus.AKTIV,
            "wochenstunden": Decimal("20.00"),
            "qualifikationen": ["Excel Fortgeschritten", "Kundenbetreuung"],
        },
        {
            "personal_nummer": "MA-013",
            "vorname": "Robert",
            "nachname": "Zimmermann",
            "email": "robert.zimmermann@pav.de",
            "abteilung": "Logistik",
            "position": "Lagerist",
            "telefon": "+49 431 1234-113",
            "eintritt_datum": date(2019, 10, 1),
            "status": MitarbeiterStatus.AKTIV,
            "wochenstunden": Decimal("40.00"),
            "qualifikationen": ["Staplerführerschein", "Lagerverwaltung", "Gefahrgut-Schein ADR"],
        },
        {
            "personal_nummer": "MA-014",
            "vorname": "Martina",
            "nachname": "Krüger",
            "email": "martina.krueger@pav.de",
            "abteilung": "Qualität",
            "position": "Qualitätsprüferin",
            "telefon": "+49 431 1234-114",
            "eintritt_datum": date(2020, 4, 1),
            "status": MitarbeiterStatus.AKTIV,
            "wochenstunden": Decimal("40.00"),
            "qualifikationen": ["Qualitätsmanagement", "Excel Fortgeschritten"],
        },
        {
            "personal_nummer": "MA-015",
            "vorname": "Andreas",
            "nachname": "Schmitt",
            "email": "andreas.schmitt@pav.de",
            "abteilung": "Verwaltung",
            "position": "Controller",
            "telefon": "+49 431 1234-115",
            "eintritt_datum": date(2017, 2, 1),
            "status": MitarbeiterStatus.AKTIV,
            "wochenstunden": Decimal("40.00"),
            "qualifikationen": ["SAP", "Excel Fortgeschritten", "Englisch"],
        },
    ]

    for ma_data in mitarbeiter_data:
        existing = db.query(Mitarbeiter).filter(Mitarbeiter.personal_nummer == ma_data["personal_nummer"]).first()
        if not existing:
            qualifikationen_names = ma_data.pop("qualifikationen")

            mitarbeiter = Mitarbeiter(**ma_data)
            db.add(mitarbeiter)
            db.flush()

            # Add qualifications
            for qual_name in qualifikationen_names:
                qual = db.query(Qualifikation).filter(Qualifikation.name == qual_name).first()
                if qual:
                    level = QualifikationLevel.EXPERTE if "5+ Jahre" in qual_name or "Führung" in qual_name else QualifikationLevel.FORTGESCHRITTEN

                    # Set validity dates for certifications
                    gueltig_von = None
                    gueltig_bis = None
                    if qual.kategorie == QualifikationKategorie.ZERTIFIKAT:
                        gueltig_von = date.today() - timedelta(days=365)
                        gueltig_bis = date.today() + timedelta(days=365)

                    mq = MitarbeiterQualifikation(
                        mitarbeiter_id=mitarbeiter.id,
                        qualifikation_id=qual.id,
                        level=level,
                        gueltig_von=gueltig_von,
                        gueltig_bis=gueltig_bis
                    )
                    db.add(mq)

            print(f"  ✓ Created employee: {ma_data['personal_nummer']} - {ma_data['vorname']} {ma_data['nachname']}")

    db.commit()


def create_verfuegbarkeit(db):
    """Create demo availability entries"""
    print("Creating availability entries...")

    # Get some employees
    mitarbeiter_list = db.query(Mitarbeiter).limit(10).all()

    if not mitarbeiter_list:
        print("  ⚠️  No employees found, skipping availability")
        return

    today = date.today()

    # MA-007 is on vacation (status URLAUB)
    ma_007 = db.query(Mitarbeiter).filter(Mitarbeiter.personal_nummer == "MA-007").first()
    if ma_007:
        verf = Verfuegbarkeit(
            mitarbeiter_id=ma_007.id,
            typ=VerfuegbarkeitTyp.URLAUB,
            von_datum=today - timedelta(days=3),
            bis_datum=today + timedelta(days=7),
            notizen="Jahresurlaub"
        )
        db.add(verf)
        print(f"  ✓ Added vacation for MA-007")

    # MA-001 on assignment
    ma_001 = db.query(Mitarbeiter).filter(Mitarbeiter.personal_nummer == "MA-001").first()
    if ma_001:
        verf = Verfuegbarkeit(
            mitarbeiter_id=ma_001.id,
            typ=VerfuegbarkeitTyp.EINSATZ,
            von_datum=today - timedelta(days=10),
            bis_datum=today + timedelta(days=20),
            notizen="Projekt Lageroptimierung"
        )
        db.add(verf)
        print(f"  ✓ Added assignment for MA-001")

    # MA-005 future vacation
    ma_005 = db.query(Mitarbeiter).filter(Mitarbeiter.personal_nummer == "MA-005").first()
    if ma_005:
        verf = Verfuegbarkeit(
            mitarbeiter_id=ma_005.id,
            typ=VerfuegbarkeitTyp.URLAUB,
            von_datum=today + timedelta(days=30),
            bis_datum=today + timedelta(days=44),
            notizen="Sommerurlaub geplant"
        )
        db.add(verf)
        print(f"  ✓ Added future vacation for MA-005")

    db.commit()


def main():
    """Main seeding function"""
    print("\n" + "="*60)
    print("PAV Personalfinder - Database Seeding")
    print("="*60 + "\n")

    # Initialize database
    print("Initializing database...")
    init_db()
    print("✓ Database initialized\n")

    # Create session
    db = SessionLocal()

    try:
        # Seed data
        create_users(db)
        print()
        create_qualifikationen(db)
        print()
        create_mitarbeiter(db)
        print()
        create_verfuegbarkeit(db)
        print()

        print("="*60)
        print("✅ Seeding completed successfully!")
        print("="*60)
        print("\nDemo Users:")
        print("  - admin / admin123 (Admin)")
        print("  - hr_manager / hr123 (User)")
        print("  - viewer / viewer123 (Read-Only)")
        print()

    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
