import streamlit as st
import re
from datetime import datetime

st.title("🔐 User Authentication Portal")

# Constants
ADMIN_IDS = ("A001", "B001")   # only these IDs are valid for admin
PASS_ADMIN = "@Dmin"           # admin secret (case sensitive)
PASS_S = "g>nZ"                # password for old SG (S-series)
PASS_T = "Gen*"                # password for new SG (T-series)

# Compile patterns
PATTERN_S = re.compile(r"S\d{7}[A-Z]")
PATTERN_T = re.compile(r"T\d{7}[A-Z]")

# Inputs
user_id = st.text_input("Enter your User ID").strip().upper()
password = st.text_input("Enter your Password", type="password")

# Action
if st.button("Enter"):
    try:
        # Empty input guard
        if not user_id or not password:
            st.warning("Please enter both User ID and Password.")

        # Case 1: Admin
        # P1 bug: `if user_id == "A001" or "B001":` → always true.
        # Fixed by membership test (`in ADMIN_IDS`) + correct password.
        elif user_id in ADMIN_IDS and password == PASS_ADMIN:
            st.write("Welcome administrator")

        # Case 2: S-series NRIC
        # Validates entire string with regex and checks exact password.
        elif PATTERN_S.fullmatch(user_id) and password == PASS_S:
            st.write("Welcome old Singaporean friend")

        # Case 3: T-series NRIC with safe age handling
        elif PATTERN_T.fullmatch(user_id) and password == PASS_T:
            try:
                # Extract YY digits → year of birth = 2000 + YY
                yy = int(user_id[1:3])                 # extract YY after 'T'
                year_born = 2000 + yy
                age = datetime.now().year - year_born

                # Sanity check: avoid negative or out of scope ages
                if age < 0 or age > 125:
                    raise ValueError("Unrealistic age")
                
                # Grammar for singular/plural "year(s)"
                year_word = "year" if age == 1 else "years"
                st.write(f"Welcome back, my Singaporean friend at your {age} {year_word} old")
            except Exception:
                # If parsing/age fails, fall back to safe denial
                # P3 insight: always preserve contract output
                st.error("We couldn’t verify your age from the NRIC. Please re-check your ID.")
                st.write("Sorry, this site is only open to Singaporeans")

        # Case 4: Anything else → generic denial
        else:
            st.write("Sorry, this site is only open to Singaporeans")

    except Exception:
        st.error("Unexpected error occurred. Please try again.")
