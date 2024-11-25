import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Timesheet Comparator",
    page_icon="⏱️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Page title and introduction
st.title("⏱️ Timesheet Comparator")
st.markdown(
    """ 
    ---
    """
)

#**Welcome to the Timesheet Comparator Tool!** 
#Easily compare time records across multiple formats. Just drag and drop your files below, and we'll handle the rest.  

# File upload section with styled headers
st.header("📂 Upload Files")
st.write("Drag and drop your files below to begin the comparison:")

csudh_time_sheet_pdf = st.file_uploader(
    "📄 Upload Actual Attendance (CSUDH Timesheet)", type="pdf"
)
ghl_time_sheet_csv = st.file_uploader(
    "📋 Upload Actual Attendance (GHL Form CSV File)", type="csv"
)
actual_work_schedule_csv = st.file_uploader(
    "📅 Upload Expected Attendance (Work Schedule CSV File)", type="csv"
)

st.button("Submit")

# Divider for sections
st.markdown("---")

# Display mock accuracy table
st.header("📊 Accuracy Table")
st.write("Below is the accuracy table based on your uploaded files:")

# Create mock data
mock_data = {
    "Date": ["2024-11-01", "2024-11-02", "2024-11-03", "2024-11-04", "2024-11-05"],
    "CSUDH Timesheet (Hours)": [
        "In: 6:00 Out: 9:00",
        "In: 6:00 Out: 9:00",
        "In: 6:00 Out: 9:00",
        "In: 6:00 Out: 9:00",
        "In: 6:00 Out: 9:00",
    ],
    "GHL Form (Hours)": [
        "In: 6:00 Out: 9:00",
        "In: 6:00 Out: 9:00",
        "In: 6:00 Out: 9:00",
        "In: 6:00 Out: 9:00",
        "In: 6:00 Out: 9:00",
    ],
    "Work Schedule (Hours)": [
        "In: 6:00 Out: 9:00",
        "In: 6:00 Out: 9:00",
        "In: 6:00 Out: 9:00",
        "In: 6:00 Out: 9:00",
        "In: 6:00 Out: 9:00",
    ],
    "Accuracy (%)": ["100%", "100%", "100%", "100%", "100%"],
}

# Create a DataFrame
mock_df = pd.DataFrame(mock_data)

# Display the table with an improved layout
# Display the mock accuracy table
st.dataframe(mock_df)


# Add a final note or footer
st.markdown(
    """
    ---
    ✅ **Pro Tip**: Ensure all files are for the same time period to get accurate results.  
    📩 Need help? Contact [Stanley](mailto:snavarrete10@csudh.edu).
    """
)
