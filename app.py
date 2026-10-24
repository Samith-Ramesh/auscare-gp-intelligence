import streamlit as st
import sqlite3
import pandas as pd
import os
import re
from google import genai

st.set_page_config(page_title="AusCare Intelligence Engine", layout="wide", page_icon="🩺")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ GEMINI_API_KEY environment variable is missing.")
    st.stop()

client = genai.Client(api_key=api_key)
TARGET_MODEL = "models/gemma-4-26b-a4b-it"

st.title("AusCare GP Intelligence Engine 🇦🇺🩺")
st.markdown("##### Real-Time Australian Healthcare Directory & Natural Language Search")

conn = sqlite3.connect("auscare_intelligence.db", check_same_thread=False)

# Metric Summary Cards
col1, col2, col3 = st.columns(3)
total_docs = pd.read_sql_query("SELECT COUNT(*) FROM doctors", conn).iloc[0, 0]
total_clinics = pd.read_sql_query("SELECT COUNT(*) FROM clinics", conn).iloc[0, 0]
bb_clinics = pd.read_sql_query("SELECT COUNT(*) FROM clinics WHERE bulk_billing = 1", conn).iloc[0, 0]

col1.metric("Indexed Doctors", total_docs)
col2.metric("Verified Clinics", total_clinics)
col3.metric("Bulk-Billing Clinics", bb_clinics)

st.divider()

user_query = st.text_input(
    "Search practitioners using natural language:",
    placeholder="e.g. addresses of doctors in lotus medical centre, phone numbers in sydney, bulk billing gps"
)

if st.button("Search Intelligence", type="primary") and user_query:
    schema_prompt = f"""
    You are an expert SQLite translator for an Australian medical directory.
    Convert the user's natural English query into an accurate SQLite SELECT query.

    Database Schema:
    - clinics (clinic_id INTEGER PRIMARY KEY, clinic_name TEXT, street_address TEXT, suburb TEXT, state TEXT, postcode TEXT, phone_number TEXT, bulk_billing BOOLEAN)
    - doctors (doctor_id INTEGER PRIMARY KEY, clinic_id INTEGER, doctor_name TEXT, specialties TEXT)

    CRITICAL RULES:
    1. JOINS: Always join on doctors.clinic_id = clinics.clinic_id unless the question ONLY pertains to clinics without doctor involvement.
    2. COLUMN SELECTION RULE:
       - If the user asks an aggregate/count question (e.g. "how many...", "count of..."), return the aggregate (e.g. SELECT COUNT(*) FROM ...).
       - If the user asks for specific attributes (like "address", "phone", "specialty", "where", "contact", "info", "details", "list", "who is"), ALWAYS SELECT THE RELEVANT INFORMATIVE COLUMNS:
         SELECT d.doctor_name, c.clinic_name, c.street_address, c.suburb, c.state, c.postcode, c.phone_number, CASE WHEN c.bulk_billing = 1 THEN 'Yes' ELSE 'No' END AS bulk_billing, d.specialties FROM doctors d JOIN clinics c ON d.clinic_id = c.clinic_id
         and append the appropriate WHERE clause.
    3. CASE-INSENSITIVE FUZZY MATCHING:
       - Always use LIKE '%term%' for textual filters (e.g. c.clinic_name LIKE '%lotus%', c.suburb LIKE '%melbourne%', d.specialties LIKE '%pediatric%'). Never use exact = matching for text names.
    4. COMMON PHRASINGS:
       - "bulk bill", "bulk billing", "free", "medicare": c.bulk_billing = 1
       - "private billing", "mixed billing", "not bulk billing": c.bulk_billing = 0
    5. OUTPUT:
       - Return ONLY executable raw SQL. No markdown fences, no explanation, no quotes around the output.

    User Question: "{user_query}"
    """
    with st.spinner("Analyzing healthcare query and fetching live records..."):
        try:
            ai_resp = client.models.generate_content(model=TARGET_MODEL, contents=schema_prompt)
            sql = re.sub(r"sql|", "", ai_resp.text).strip()
            st.caption(f"*Executed SQL:* {sql}")
            
            df = pd.read_sql_query(sql, conn)
            
            if not df.empty:
                # Remove internal primary keys if accidentally returned
                for col_to_drop in ["doctor_id", "clinic_id"]:
                    if col_to_drop in df.columns:
                        df = df.drop(columns=[col_to_drop])
                
                # Insert clean 1-indexed sl_no column
                df.insert(0, "sl_no", [str(i) for i in range(1, len(df) + 1)])
                
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "sl_no": st.column_config.TextColumn("sl_no", width="small")
                    }
                )
            else:
                st.warning("No records matched your search criteria. Try a broader search term like 'doctors in South Melbourne' or 'bulk billing'.")
        except Exception as e:
            st.error(f"Execution error: {e}")

st.divider()
st.subheader("Live Extracted Relational Records")
full_df = pd.read_sql_query("""
    SELECT d.doctor_name, c.clinic_name, c.street_address, c.suburb, c.state, c.postcode, c.phone_number, 
           CASE WHEN c.bulk_billing = 1 THEN 'Yes' ELSE 'No' END AS bulk_billing, d.specialties
    FROM doctors d JOIN clinics c ON d.clinic_id = c.clinic_id
""", conn)

full_df.insert(0, "sl_no", [str(i) for i in range(1, len(full_df) + 1)])
st.dataframe(
    full_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "sl_no": st.column_config.TextColumn("sl_no", width="small")
    }
)
