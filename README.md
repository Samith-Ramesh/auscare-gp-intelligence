# AusCare GP Intelligence Engine 🇦🇺🩺

An intelligent, natural-language healthcare search engine and directory for Australian General Practitioners (GPs). Powered by SQLite, Streamlit, and Google's Gemini models.

---

## Key Highlights

- *Live & Structured Directory:* Relational SQLite database (clinics and doctors) containing verified Australian practitioners across VIC, NSW, QLD, and WA.
- *Natural Language Text-to-SQL Search:* Convert English queries into case-insensitive SQLite queries using dynamic fuzzy matching and column projections.
- *Full Relational Visibility:* Returns complete practice details including street address, suburb, state, postcode, phone number, specialties, and bulk-billing indicators.
- *Production-Ready Dashboard:* Streamlit web interface featuring real-time metric cards and 1-indexed tables (sl_no).

---

## Project Structure

```text
auscare-gp-intelligence/
├── app.py                     # Streamlit frontend & Text-to-SQL processing engine
├── scraper.py                 # Live web scraping script using BeautifulSoup
├── ingest.py                  # Database initialization and data ingestion pipeline
├── auscare_intelligence.db    # Relational SQLite database
├── auscare_gps_export.csv     # Exported practitioner dataset
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
