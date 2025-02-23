import streamlit as st
import pandas as pd
import os
from io import BytesIO
from sklearn.impute import SimpleImputer
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

st.set_page_config(page_title="AI Data Sweeper", layout="wide")

st.title("AI-Powered Data Sweeper")
st.write("Transform and clean your data with AI-powered automation, handling missing values and detecting anomalies.")

uploaded_files = st.file_uploader("Upload CSV or Excel files:", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_extension = os.path.splitext(file.name)[-1].lower()
        
        if file_extension == ".csv":
            df = pd.read_csv(file)
        elif file_extension == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_extension}")
            continue
        
        st.write(f"**📄 File Name:** {file.name}")
        st.dataframe(df.head())
        
        st.subheader("📊 Data Profiling Report")
        if st.checkbox(f"Generate AI Analysis for {file.name}"):
            profile = ProfileReport(df, title="Profiling Report")
            st_profile_report(profile)

        st.subheader("🛠️ AI-Based Data Cleaning")
        if st.checkbox(f"Apply AI Cleaning to {file.name}"):
            imputer = SimpleImputer(strategy='mean')
            df[df.select_dtypes(include=['number']).columns] = imputer.fit_transform(df.select_dtypes(include=['number']))
            st.write("✅ Missing values filled using AI-based mean imputation.")
            
        st.subheader("🔄 Convert & Download")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_extension, ".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False, engine='openpyxl')
                file_name = file.name.replace(file_extension, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)
            st.download_button(f"⬇️ Download {file.name} as {conversion_type}", data=buffer, file_name=file_name, mime=mime_type)

st.success("🎉 AI Cleaning & Conversion Completed!")
