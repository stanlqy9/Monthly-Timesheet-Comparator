import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader

# Page configuration
st.set_page_config(
    page_title="Timesheet Comparator",
    page_icon="⏱️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Page title and introduction
st.title("⏱️ Timesheet Comparator")
st.markdown("---")

# File upload section
st.header("📂 Upload Files")
st.write("Drag and drop your files below to begin the comparison:")

csudh_time_sheet_pdf = st.file_uploader(
    "📄 Upload Actual Attendance (CSUDH Timesheet)", type="pdf"
)
ghl_time_sheet_csv = st.file_uploader(
    "📋 Upload Actual Attendance (GHL Form CSV File)", type="csv"
)

if st.button("Submit"):
    if csudh_time_sheet_pdf and ghl_time_sheet_csv:
        # Extract data from CSUDH Timesheet PDF
        pdf_reader = PdfReader(csudh_time_sheet_pdf)
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
        
        # Parse times from CSUDH PDF (example format: "10-21-24 Monday 06:00 09:00")
        csudh_data = []
        for line in pdf_text.split("\n"):
            if "Monday" in line or "Tuesday" in line or "Wednesday" in line or "Thursday" in line or "Friday" in line:
                parts = line.split()
                date = parts[0]
                in_time = parts[2]
                out_time = parts[3]
                csudh_data.append({"Date": date, "In": in_time, "Out": out_time})

        csudh_df = pd.DataFrame(csudh_data)

        # Load GHL Form CSV
        ghl_df = pd.read_csv(ghl_time_sheet_csv)

        # Standardize GHL data
        ghl_df = ghl_df.rename(columns={"Date": "Date", "Time In": "In", "Time Out": "Out"})
        ghl_df = ghl_df[["Date", "In", "Out"]]

        # Compare data
        comparison = pd.merge(csudh_df, ghl_df, on="Date", suffixes=("_CSUDH", "_GHL"))
        comparison["Match"] = (
            (comparison["In_CSUDH"] == comparison["In_GHL"])
            & (comparison["Out_CSUDH"] == comparison["Out_GHL"])
        )

        # Display results
        st.header("📊 Comparison Results")
        st.dataframe(comparison)
    else:
        st.error("Please upload both the CSUDH Timesheet and GHL Form files.")

