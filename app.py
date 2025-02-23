import streamlit as st
import pandas as pd
import os
from io import BytesIO
from sklearn.impute import SimpleImputer

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
        
        # Display basic statistics
        st.subheader("📊 Data Overview")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Sample Data:")
            st.dataframe(df.head())
            
        with col2:
            st.write("Basic Statistics:")
            st.write(f"- Total Rows: {len(df)}")
            st.write(f"- Total Columns: {len(df.columns)}")
            st.write("- Missing Values:")
            missing_stats = df.isnull().sum()
            for col, missing in missing_stats[missing_stats > 0].items():
                st.write(f"  • {col}: {missing} missing values")

        st.subheader("🛠️ AI-Based Data Cleaning")
        if st.checkbox(f"Apply AI Cleaning to {file.name}"):
            # Handle numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                imputer = SimpleImputer(strategy='mean')
                df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
                st.write("✅ Missing numeric values filled using AI-based mean imputation.")
            
            # Handle categorical columns
            categorical_cols = df.select_dtypes(exclude=['number']).columns
            if len(categorical_cols) > 0:
                cat_imputer = SimpleImputer(strategy='most_frequent')
                df[categorical_cols] = cat_imputer.fit_transform(df[categorical_cols])
                st.write("✅ Missing categorical values filled using most frequent value.")
            
            st.write("Cleaned Data Preview:")
            st.dataframe(df.head())
            
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
            st.download_button(f"⬇️ Download {file.name} as {conversion_type}", 
                             data=buffer, 
                             file_name=file_name, 
                             mime=mime_type)

st.success("🎉 AI Cleaning & Conversion Completed!")
