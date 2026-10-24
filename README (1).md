# AusCare GP Intelligence Engine 🇦🇺🩺

A natural-language search engine for Australian general practitioner (GP) directories. Powered by SQLite, Streamlit, and Google's Gemini models.

## Architecture

- *Ingestion & Scraping:* scraper.py parses doctor and clinic directories from live Australian healthcare web endpoints.
- *Relational Storage:* Normalized SQLite database (clinics and doctors) with complete multi-field records.
- *Text-to-SQL Engine:* Gemini translates free-form natural language queries into case-insensitive SQLite queries using fuzzy matching.
- *Interactive UI:* Streamlit interface featuring live metrics, 1-indexed tables (sl_no), and relational filtering.

## Quickstart (Local Execution)

1. *Clone Repository & Install Dependencies:*
   ```bash
   git clone [https://github.com/Samith-Ramesh/auscare-gp-intelligence.git](https://github.com/Samith-Ramesh/auscare-gp-intelligence.git)
   cd auscare-gp-intelligence
   pip install -r requirements.txt
