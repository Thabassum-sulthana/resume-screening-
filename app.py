# app_no_images.py
import streamlit as st
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
import fitz  # PyMuPDF
import tempfile

# Watsonx credentials
API_KEY = "your_api_key"
PROJECT_ID = "your_project_id"
WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
MODEL_ID = "ibm/granite-3-3-8b-instruct"

credentials = Credentials(api_key=API_KEY, url=WATSONX_URL)
inference = ModelInference(model_id=MODEL_ID, credentials=credentials, project_id=PROJECT_ID)

# Prompt generator
def generate_prompt(resume_text):
    return f"""You are an intelligent HR assistant.
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

# PDF Text Extractor
def extract_text_from_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    doc = fitz.open(tmp_path)
    return "".join([page.get_text() for page in doc])

# Streamlit UI
st.set_page_config(page_title="Resume Classifier", page_icon="📄")
st.title("📄 Resume Job Role Classifier (PDF/Text Only)")
st.write("Upload a resume (PDF) or paste text to classify the job role.")

option = st.radio("Choose input type:", ["📁 Upload PDF Resume", "⌨️ Paste Resume Text"])
resume_text = ""

if option == "📁 Upload PDF Resume":
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_file:
        resume_text = extract_text_from_pdf(uploaded_file)
        st.text_area("📄 Extracted Resume Text", resume_text, height=200)

elif option == "⌨️ Paste Resume Text":
    resume_text = st.text_area("✍️ Paste resume text:", height=200)

if resume_text.strip():
    if st.button("🔍 Classify Resume"):
        with st.spinner("Classifying..."):
            try:
                prompt = generate_prompt(resume_text)
                response = inference.generate_text(prompt=prompt)
                category = response.strip().split("\n")[0]
                st.success(f"✅ Predicted Category: **{category}**")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

