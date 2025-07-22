# 📄 Resume Analyzer & Job Matcher

This is my AI-based project that analyzes resumes (PDF) or manually entered skills and matches them with real IT job roles based on required skills.

Built using **Python + Streamlit**, it gives match scores, shows matched and missing skills, and helps users know where they stand.

---

## 🔧 Features

- 📄 Extracts skills from uploaded PDF resumes
- ⌨️ Accepts manual skill input
- 🧠 Compares with real job data (`IT_Job_Roles_Skills.csv`)
- 📊 Shows top job matches with score
- 🧾 Clean Streamlit UI

---

## 💻 Tech Stack

- Python, Streamlit, pandas, PyMuPDF (fitz)

---

## 🚀 Run it

```bash
pip install pandas streamlit PyMuPDF
streamlit run ResumeAnalyzerAndJobMatcher.py

