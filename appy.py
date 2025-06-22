import streamlit as st
import random
import re
import pandas as pd
from datetime import datetime
import os

LOG_FILE = "submissions_log.csv"
ADMIN_PASSWORD = st.secrets["general"]["admin_password"]

def generate_random_cpn():
    while True:
        cpn = ''.join([str(random.randint(0, 9)) for _ in range(9)])
        if not re.match(r"^(000|666|9)", cpn):
            return cpn  # FIXED: typo was `return can`

def is_valid_ssn(ssn):
    return bool(re.fullmatch(r"\d{3}-\d{2}-\d{4}", ssn))

def log_submission(data):
    df = pd.DataFrame([data])
    file_exists = os.path.isfile(LOG_FILE)
    df.to_csv(LOG_FILE, mode='a', header=not file_exists, index=False)

st.set_page_config(page_title="Secure Identifier Generator", layout="centered")

st.sidebar.title("🔒 Admin Access")
admin_mode = st.sidebar.checkbox("Login as Admin")

if admin_mode:
    password = st.sidebar.text_input("Enter admin password", type="password")

    if password == ADMIN_PASSWORD:
        st.title("📋 Admin Dashboard – Submissions Log")

        if os.path.exists(LOG_FILE):
            df = pd.read_csv(LOG_FILE)
            st.success("Log loaded successfully.")

            name_filter = st.text_input("Filter by Name")
            cpn_filter = st.text_input("Filter by Generated Number")
            date_filter = st.date_input("Filter by Date (DOB)", value=None)

            filtered_df = df.copy()

            if name_filter:
                filtered_df = filtered_df[filtered_df["Name"].str.contains(name_filter, case=False)]

            if cpn_filter:
                filtered_df = filtered_df[filtered_df["GeneratedNumber"].astype(str).str.contains(cpn_filter)]

            if date_filter:
                filtered_df = filtered_df[filtered_df["DOB"] == date_filter.strftime("%Y-%m-%d")]

            st.dataframe(filtered_df)

            csv_data = filtered_df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Filtered Logs as CSV", data=csv_data, file_name="filtered_logs.csv", mime="text/csv")
        else:
            st.warning("No log file found yet.")
    else:
        st.error("Incorrect password.")

else:
    st.title("🔐 CPN Generator")
    st.markdown("""
    Generate a **CPN** for personal use.  
    ⚠️ **Download CPN basics if you do not know how to use a CPN.**
    """)

    with st.form("cpn_form"):
        nam
