# 📄 Resume Screening Assistant using IBM watsonx.ai

This project is a smart web application that uses **IBM watsonx.ai's Granite foundation model** to classify resumes into job categories such as **Data Science, Software Development, Marketing, Human Resources**, and **Finance**. It provides a simple interface for users to upload **PDFs**, **images (screenshots of resumes)**, or even **paste plain text**, and receive accurate job role predictions.

---

## 🚀 Project Demo

- 🔗 **GitHub Repository**: [https://github.com/Thabassum-sulthana/resume-screening-](https://github.com/Thabassum-sulthana/resume-screening-)
- 🌐 **Live App (Streamlit)**: [https://3jthkypqqhlwukg36ybjd8.streamlit.app/](https://3jthkypqqhlwukg36ybjd8.streamlit.app/)

---

## 🧠 About the Model

- **Model Used**: `ibm/granite-3-3-8b-instruct`
- **Hosted on**: IBM watsonx.ai
- **Purpose**: Natural language understanding for classification tasks
- **Type**: Instruction-tuned large language foundation model

---

## 🎯 Objective

To build a resume screening assistant that automates job category classification from resume content using **Generative AI**. This project helps HR teams and recruiters quickly identify the right job role for a candidate.

---

## 🛠️ Tools & Technologies Used

| Tool / Library          | Purpose                                      |
|--------------------------|----------------------------------------------|
| Streamlit                | Building the web interface                   |
| IBM watsonx.ai           | Hosting and using the foundation model       |
| ibm-watsonx-ai SDK       | Model inference from IBM foundation models   |
| PyMuPDF (`fitz`)         | Extracting text from PDF files               |
| pytesseract + OpenCV     | Extracting text from image resumes           |
| NumPy, Pillow            | Image processing support                     |
| Google Colab             | Model testing and prototyping                |

---

## 🧾 Features

✅ Upload multiple resume formats: PDF, Image, or plain text  
✅ Automatically extract text using OCR for image-based resumes  
✅ Classify resume content into 5 predefined job roles  
✅ Clean, simple web interface with **Streamlit**  
✅ Runs in browser, no installation needed by end-users

---

## 📂 Project Structure

esume-screening/
├── app.py # Main Streamlit application code
├── README.md # Project documentation
├── requirements.txt # Python dependencies


---

## ⚙️ How to Run This Project

### ✅ Step 1: Clone the Repository

git clone https://github.com/Thabassum-sulthana/resume-screening-
cd resume-screening-
Step 2: Install Dependencies
pip install streamlit ibm-watsonx-ai pytesseract opencv-python-headless Pillow PyMuPDF
✅ Step 3: Run the Streamlit App

streamlit run app.py
Go to http://localhost:8501 in your browser.

💻 Google Colab Testing
Before building the app, model inference was tested using Google Colab with three methods:

📄 PDF Resume Upload + Text Extraction

🖼️ Image Resume Upload + OCR

⌨️ Paste Resume Text Directly

Each method sent text to the IBM watsonx model using the same prompt and displayed the predicted category.

📸 Screenshots
Upload Method	Screenshot
PDF Upload	✅ Text extracted and classified successfully
Image Upload	✅ OCR worked well for scanned resumes
Text Paste	✅ Instant classification based on text input

You can view screenshots of output in the PDF project report or use the Streamlit link to see live results.

📜 Sample Prompt Sent to IBM Model
def generate_prompt(resume_text):
    return f'''
You are an intelligent HR assistant.

Classify the following resume into one of these job categories:
- Data Science
- Software Development
- Marketing
- Human Resources
- Finance

IMPORTANT: Respond ONLY with the category name. Do NOT include anything else.

