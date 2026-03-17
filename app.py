import streamlit as st
import pandas as pd
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.title("🛡️ AI Anomaly Detection Platform")

# 1. Upload Data
uploaded_file = st.file_uploader("Upload your Dataset (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Data Preview", df.head())

    if st.button("Detect Anomalies"):
        with st.spinner("Analyzing patterns..."):
            # Convert a small sample of data to string for the AI to read
            data_sample = df.to_string(index=False)
            
            # The AI Prompt
            prompt = f"""
            Act as a data forensic expert. Analyze the following dataset and identify:
            1. Any data points that look like anomalies (outliers).
            2. Explain WHY they are suspicious.
            3. Suggest a possible cause (Fraud, Sensor Error, etc.).
            
            Dataset:
            {data_sample}
            """
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            st.write("### 🚨 Anomaly Report", response.text)