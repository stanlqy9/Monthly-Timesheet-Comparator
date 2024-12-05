import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
from io import BytesIO

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
        # Read PDF using BytesIO for compatibility
        pdf_bytes = csudh_time_sheet_pdf.read()
        pdf_reader = PdfReader(BytesIO(pdf_bytes))
        
        pdf_text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                pdf_text += page_text + "\n"
        
        # Parse times from CSUDH PDF 
        # Expected format line example (subject to adjustment based on actual PDF):
        # "10-21-24 Monday 06:00 09:00"
        # We'll look for weekday keywords and ensure we have enough parts.
        
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        csudh_data = []
        for line in pdf_text.split("\n"):
            if any(day in line for day in weekdays):
                parts = line.split()
                # Ensure we have enough parts. Adjust indexing if needed based on PDF format.
                if len(parts) >= 4:
                    date = parts[0]
                    # parts[1] might be the weekday, so check carefully:
                    # Assuming format: DATE DAY IN_TIME OUT_TIME
                    # Index:          0    1   2       3
                    in_time = parts[2]
                    out_time = parts[3]
                    csudh_data.append({"Date": date, "In": in_time, "Out": out_time})
        
        if not csudh_data:
            st.error("No attendance data found in the CSUDH PDF. Please check the PDF format.")
            st.stop()

        csudh_df = pd.DataFrame(csudh_data)

        # Load GHL Form CSV
        try:
            ghl_df = pd.read_csv(ghl_time_sheet_csv)
        except Exception as e:
            st.error(f"Could not read the CSV file: {e}")
            st.stop()

        # Ensure the expected columns exist in GHL CSV
        required_cols = ["Date", "Time In", "Time Out"]
        if not all(col in ghl_df.columns for col in required_cols):
            st.error("The GHL CSV file must contain 'Date', 'Time In', and 'Time Out' columns.")
            st.stop()

        # Standardize GHL data
        ghl_df = ghl_df.rename(columns={"Time In": "In", "Time Out": "Out"})
        ghl_df = ghl_df[["Date", "In", "Out"]]

        # Compare data
        comparison = pd.merge(csudh_df, ghl_df, on="Date", suffixes=("_CSUDH", "_GHL"), how="outer")
        comparison["Match"] = (
            (comparison["In_CSUDH"] == comparison["In_GHL"])
            & (comparison["Out_CSUDH"] == comparison["Out_GHL"])
        )

        # Display results
        st.header("📊 Comparison Results")
        st.dataframe(comparison)
    else:
        st.error("Please upload both the CSUDH Timesheet and GHL Form files.")


