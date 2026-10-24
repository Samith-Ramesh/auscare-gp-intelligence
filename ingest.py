import os
import sqlite3
import pandas as pd

DB_PATH = "auscare_intelligence.db"

practitioners = [
    {
        "doctor_name": "Dr. Masood Noroozian Avval",
        "clinic_name": "Lotus Medical Centre",
        "street_address": "285 Moray Street",
        "suburb": "South Melbourne",
        "state": "VIC",
        "postcode": "3205",
        "phone_number": "(03) 9699 9122",
        "bulk_billing": False,
        "specialties": "Chronic Disease Management, Diabetes Care, Skin Checks"
    },
    {
        "doctor_name": "Dr. Maryam Assadollahianbonab",
        "clinic_name": "Lotus Medical Centre",
        "street_address": "285 Moray Street",
        "suburb": "South Melbourne",
        "state": "VIC",
        "postcode": "3205",
        "phone_number": "(03) 9699 9122",
        "bulk_billing": False,
        "specialties": "Women's Health, Antenatal Care, Family Medicine"
    },
    {
        "doctor_name": "Dr. Magdy Ramzy",
        "clinic_name": "Lotus Medical Centre",
        "street_address": "285 Moray Street",
        "suburb": "South Melbourne",
        "state": "VIC",
        "postcode": "3205",
        "phone_number": "(03) 9699 9122",
        "bulk_billing": True,
        "specialties": "Pediatric Care, Immunisations, Minor Surgeries"
    },
    {
        "doctor_name": "Dr. Siew Li Tan",
        "clinic_name": "Lotus Medical Centre",
        "street_address": "285 Moray Street",
        "suburb": "South Melbourne",
        "state": "VIC",
        "postcode": "3205",
        "phone_number": "(03) 9699 9122",
        "bulk_billing": False,
        "specialties": "Preventive Health, Geriatric Medicine, Mental Health Plans"
    },
    {
        "doctor_name": "Dr. Mohsen Sadrneshin",
        "clinic_name": "Lotus Medical Centre",
        "street_address": "285 Moray Street",
        "suburb": "South Melbourne",
        "state": "VIC",
        "postcode": "3205",
        "phone_number": "(03) 9699 9122",
        "bulk_billing": False,
        "specialties": "Men's Health, Travel Medicine, Cardiology Screening"
    },
    {
        "doctor_name": "Dr. Lachlan Murphy",
        "clinic_name": "Sydney CBD Medical & Wellness Centre",
        "street_address": "Suite 401, Level 4, 321 George St",
        "suburb": "Sydney",
        "state": "NSW",
        "postcode": "2000",
        "phone_number": "(02) 9231 4455",
        "bulk_billing": False,
        "specialties": "Preventative Health, Travel Medicine, Men's Health"
    },
    {
        "doctor_name": "Dr. Priya Sen",
        "clinic_name": "St Kilda Bayside Family Clinic",
        "street_address": "Shop 2, 78 Acland Street",
        "suburb": "St Kilda",
        "state": "VIC",
        "postcode": "3182",
        "phone_number": "(03) 9534 8920",
        "bulk_billing": True,
        "specialties": "Pediatric Care, Women's Health, Dermatology"
    },
    {
        "doctor_name": "Dr. Darcy Wilson",
        "clinic_name": "Fortitude Valley Community Doctors",
        "street_address": "1040 Ann St",
        "suburb": "Fortitude Valley",
        "state": "QLD",
        "postcode": "4006",
        "phone_number": "(07) 3852 1100",
        "bulk_billing": False,
        "specialties": "Mental Health Treatment Plans, ADHD Management, Youth Health"
    },
    {
        "doctor_name": "Dr. Amina El-Masri",
        "clinic_name": "Fremantle Portside Practice",
        "street_address": "12 Henderson Street",
        "suburb": "Fremantle",
        "state": "WA",
        "postcode": "6160",
        "phone_number": "(08) 9430 7711",
        "bulk_billing": True,
        "specialties": "Geriatric Medicine, Diabetes Management, Chronic Illness Care"
    },
    {
        "doctor_name": "Dr. Jason Chen",
        "clinic_name": "Parramatta Riverside Medical Group",
        "street_address": "150 Church Street",
        "suburb": "Parramatta",
        "state": "NSW",
        "postcode": "2150",
        "phone_number": "(02) 9687 3344",
        "bulk_billing": True,
        "specialties": "Occupational Health, Workers Compensation, Skin Cancer Checks"
    }
]

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE clinics (
        clinic_id INTEGER PRIMARY KEY AUTOINCREMENT,
        clinic_name TEXT,
        street_address TEXT,
        suburb TEXT,
        state TEXT,
        postcode TEXT,
        phone_number TEXT,
        bulk_billing BOOLEAN
    );
    CREATE TABLE doctors (
        doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        clinic_id INTEGER,
        doctor_name TEXT,
        specialties TEXT,
        FOREIGN KEY (clinic_id) REFERENCES clinics(clinic_id)
    );
    """)
    for p in practitioners:
        cur.execute("""
            INSERT INTO clinics (clinic_name, street_address, suburb, state, postcode, phone_number, bulk_billing)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (p["clinic_name"], p["street_address"], p["suburb"], p["state"], p["postcode"], p["phone_number"], p["bulk_billing"]))
        cid = cur.lastrowid
        cur.execute("INSERT INTO doctors (clinic_id, doctor_name, specialties) VALUES (?, ?, ?)",
                    (cid, p["doctor_name"], p["specialties"]))
    conn.commit()
    conn.close()
    print("[✓] Database initialized cleanly.")

if _name_ == "_main_":
    init_db()
