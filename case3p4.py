import streamlit as st
import os
import csv
from datetime import datetime

# --- Title ---
st.title("📁 Sales CSV Uploader")
st.markdown("Upload your monthly sales file and save it with a standardized name format.")

# --- Inputs ---
now = datetime.now()
year = st.number_input("Enter Year (YYYY)", min_value=2000, max_value=2100, step=1, value=now.year)
month = st.number_input("Enter Month (MM)", min_value=1, max_value=12, step=1, value=now.month)
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

sales_folder = "sales"
os.makedirs(sales_folder, exist_ok=True)   

# Helpers
def _norm_agent_key(name: str) -> str:
    """Use stable uppercase key for summing"""
    return name.strip().upper()

def _label(name: str) -> str:
    """Human-friendly label → keep user spelling, trimmed."""
    return name.strip()

def _is_number(token: str) -> bool:
    """
    Light guard for headers/garbage.
    Accept integers or decimals with optional commas and spaces (e.g., '1,200' or '200.50').
    """
    
    if not token:
        return False
    s = token.replace(",", "").strip()
    if s.startswith("-"):
        s = s[1:]
    if s.isdigit():
        return True
    parts = s.split(".")
    return len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit()

def _to_float(token: str) -> float:
    """Convert cleaned numeric text to float."""
    return float(token.replace(",", "").strip())

def _month_file_path(folder: str, yy: int, mm: int) -> str:
    return os.path.join(folder, f"Sales{yy}{mm:02d}.csv")

# --- Save Logic ---
if uploaded_file and year and month:
    filename = f"Sales{year}{int(month):02d}.csv"   
    save_path = os.path.join(sales_folder, filename)
    try:  # P4 ADD: basic error handling on save
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"✅ File saved as `{filename}` in `{sales_folder}/`.")
        st.info("Existing file for the same month (if any) was overwritten.")
    except Exception as e:
        st.error(f"Could not save the file: {e}")

# --- Sales Summary ---
st.header("📊 Agent Sales Summary for the Year")

# --- Display Table ---
st.subheader(f"🧮 Sales Totals for {year}")
st.write("Each row shows total sales per agent per month.")

# CHANGE: use normalized keys for summing, keep original label for display
summary = {}       
agent_labels = {}  

bad_files = 0      
bad_rows = 0
files_processed = 0
grand_total = 0.0

# Scan months 01..12 for existing files
for m in range(1, 13):
    path = _month_file_path(sales_folder, int(year), m)
    if not os.path.exists(path):
        continue

    try:  
        with open(path, newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row or len(row) < 3:
                    continue

                agent_raw = row[1]
                amt_raw = row[2]

                # Skip non-numeric amounts
                if not _is_number(amt_raw):
                    bad_rows += 1
                    continue

                amount = _to_float(amt_raw)    # floats from the start
                key = _norm_agent_key(agent_raw)

                # Record display label on first sighting
                if key not in agent_labels:     # first-seen display label
                    agent_labels[key] = _label(agent_raw)
                 # Initialize agent months on first sighting
                if key not in summary:
                    summary[key] = {f"{x:02d}": 0.0 for x in range(1, 13)}  # float zeros
                summary[key][f"{m:02d}"] += amount
                grand_total += amount
        files_processed += 1
    except Exception:
        bad_files += 1
        # continue to next month file

# --- Display table ---
if summary:
    # Build list-of-dicts for st.table 
    rows = []
    for key in sorted(summary.keys()):
        row = {"Agent": agent_labels.get(key, key)}
        agent_total = 0.0
        for mm in [f"{x:02d}" for x in range(1, 13)]:
            val = summary[key][mm]
            agent_total += val
            row[mm] = f"{val:.2f}"
        row["TOTAL"] = f"{agent_total:.2f}"  # per-agent total (helps checking)
        rows.append(row)

    st.table(rows)
    st.success(f"Grand Total (all agents, all months): {grand_total:.2f}")
    st.caption(f"Files processed: {files_processed} | Skipped files: {bad_files} | Skipped rows: {bad_rows}")
else:
    st.write("No sales files found for this year yet.")