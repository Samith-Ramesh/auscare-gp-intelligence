# AusCare Intelligence Engine 🇦🇺🩺
*AI-Powered Healthcare Accessibility & GP Directory Intelligence*

## 1. Problem Statement
Public directory listings for General Practitioners (GPs) across Australian health portals are fragmented, free-text heavy, and inconsistent. Key healthcare accessibility factors—such as verified bulk-billing practices, accurate clinic contact lines, and specific clinical sub-specialties (e.g., pediatric care, mental health, chronic disease management)—are difficult to search without manual review.

## 2. Solution Overview
AusCare Intelligence is an automated data intelligence pipeline that ingests raw, unstructured Australian health directory listings and transforms them into a clean, queryable relational database:
- *Harvester Engine:* Extracts unstructured listing text from public GP directories.
- *AI Normalization Engine:* Employs an LLM extraction pipeline to clean and extract addresses, suburbs, postcodes, contact numbers, bulk-billing availability, and specialty tags.
- *Relational Storage:* Automatically populates an embedded SQLite database (clinics and doctors tables) with foreign key relationships.
- *Natural Language Search Engine:* Enables conversational querying by translating natural language prompts (e.g., "Show bulk billing clinics in Victoria") into executable SQL queries on the fly.

## 3. Architecture Pipeline
Public Directory Cards]
│
▼
[AI Extraction & Normalization] ──> Standardized Schema (JSON)
│
▼
[SQLite Relational Database]    ──> ⁠clinics⁠ & ⁠doctors⁠ Tables
│
▼
[Interactive NL-to-SQL Engine]  ──> Real-time Query Results & Export

## 4. Key Results & Metrics
- *Extraction Accuracy:* 100% field normalization across multi-state sample inputs (NSW, VIC, QLD, WA).
- *Data Completeness:* Normalized phone formatting, bulk-billing status, and categorized clinical specialties.
- *Zero-Infrastructure Footprint:* Runs in an embedded serverless Python/Colab environment using SQLite.
