# app.py
import streamlit as st
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
import fitz  # PyMuPDF
import tempfile
import pytesseract
from PIL import Image
import cv2
import numpy as np

# IBM watsonx credentials
API_KEY = "md9dPIRL3xmevuAk8mc3HS_cTXkc4xrN207ituvdPh_V"
PROJECT_ID = "8efda4cb-b03d-4eab-bb84-f6031372c625"
WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
MODEL_ID = "ibm/granite-3-3-8b-instruct"

# Connect to Watsonx
credentials = Credentials(api_key=API_KEY, url=WATSONX_URL)
inference = ModelInference(model_id=MODEL_ID, credentials=credentials, project_id=PROJECT_ID)

# Generate prompt
def generate_prompt(resume_text):
    return f"""
You are an intelligent HR assistant.

Classify the following resume into one of these job categories:
- Data Science
- Software Development
- Marketing
- Human Resources
- Finance

IMPORTANT: Respond ONLY with the category name. Do NOT include anything else.

Resume:
{resume_text}

Category:
"""

# Extract text from PDF
def extract_text_from_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    doc = fitz.open(tmp_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Extract text from image
def extract_text_from_image(uploaded_file):
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    text = pytesseract.image_to_string(image)
    return text

# Streamlit UI
st.set_page_config(page_title="Resume Classifier", page_icon="📄")
st.title("📄 Resume Job Role Classifier")
st.write("Upload multiple resumes (PDFs/Images) or paste text to classify the job roles.")

# Select input method
option = st.radio("Choose input type:", ["📁 Upload PDFs", "🖼️ Upload Images", "⌨️ Paste Text"])

if option == "📁 Upload PDFs":
    uploaded_files = st.file_uploader("Upload resume PDFs", type=["pdf"], accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.markdown("---")
            st.subheader(f"📄 {uploaded_file.name}")
            resume_text = extract_text_from_pdf(uploaded_file)
            st.text_area("📄 Extracted Text", resume_text, height=150, key=uploaded_file.name)

            with st.spinner("Classifying..."):
                try:
                    prompt = generate_prompt(resume_text)
                    response = inference.generate_text(prompt=prompt)
                    category = response.strip().split("\n")[0]
                    st.success(f"✅ Predicted Category: **{category}**")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

elif option == "🖼️ Upload Images":
    uploaded_images = st.file_uploader("Upload resume screenshots (PNG/JPG)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    if uploaded_images:
        for uploaded_file in uploaded_images:
            st.markdown("---")
            st.subheader(f"🖼️ {uploaded_file.name}")
            resume_text = extract_text_from_image(uploaded_file)
            st.text_area("🖼️ Extracted Text", resume_text, height=150, key=uploaded_file.name)

            with st.spinner("Classifying..."):
                try:
                    prompt = generate_prompt(resume_text)
                    response = inference.generate_text(prompt=prompt)
                    category = response.strip().split("\n")[0]
                    st.success(f"✅ Predicted Category: **{category}**")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

elif option == "⌨️ Paste Text":
    resume_text = st.text_area("✍️ Paste resume text below:", height=200)
    if st.button("🔍 Classify Text"):
        with st.spinner("Classifying..."):
            try:
                prompt = generate_prompt(resume_text)
                response = inference.generate_text(prompt=prompt)
                category = response.strip().split("\n")[0]
                st.success(f"✅ Predicted Category: **{category}**")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
