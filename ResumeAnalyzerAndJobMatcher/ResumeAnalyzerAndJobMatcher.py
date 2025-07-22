import pandas as pd
import streamlit as st
import fitz
st.set_page_config(page_title="Resume matcher",layout="centered")
#we use a decorator cache data stores memory in RAM so the work of loading data again and again does not happen
@st.cache_data
def load_data():
    jobs_df = pd.read_csv("IT_Job_Roles_Skills.csv",encoding="cp1252")
    #why we use encoding ? It is used to read special characters otherwise throws unicodedecode error
    jobs_df = jobs_df.rename(columns={"Job Title":"Job_Title","Skills":"required_skills"})
    jobs_df['required_skills'] = jobs_df['required_skills'].str.lower()
    return jobs_df
jobs_df = load_data()
#All skills required for a particular job are here in all_skills
all_skills = set()
for skills in jobs_df['required_skills']:
    all_skills.update([s.strip() for s in skills.split(',')])
st.title("Resume Analyzer and Job matcher")
st.markdown("Input your skills to see the matched jobs")
#upload resume in pdf format
uploaded_resume = st.file_uploader("Upload your resume here(PDF ONLY)",type=["pdf"])
#function to extract text from pdf file
def extract_text_from_file(uploaded_file):
    text = ""
    pdf = fitz.open(stream=uploaded_file.read(),filetype = "pdf")
    for page in pdf:
        text+=page.get_text()
    return text.lower()
#extract skills from the given text
def extract_skills_from_text(text,known_skills):
    return [skill for skill in known_skills if skill in text]
user_skill = []
if uploaded_resume:
    resume_text = extract_text_from_file(uploaded_resume)
    st.subheader("Preview of the text in resume.")
    st.text_area("",resume_text[:1000],height=300)
    user_skill = extract_skills_from_text(resume_text,all_skills)
    st.success(f"Skills found in resume : {','.join(user_skill) if user_skill else "No known skills found"}")
#If resume not uploaded then use form
with st.form("resume_form"):
    name = st.text_input("Full Name")
    Email = st.text_input("Email Address")
    manual_skills = st.text_area("Technical skills")
    submitted = st.form_submit_button("Tap to see the job roles")
#logic for appending user skills into a list of user_skills
if submitted:
    if manual_skills:
        typed_skills = [s.strip().lower() for s in skills.split(',') if s.strip()!='']
        user_skill = list(set(user_skill) | set(typed_skills)) #combine both skills set
    if not user_skill:
        st.error("Upload resume properly")
    else:
        #logic for matching the skills with the dataset
        job_matches = []
        for _,row in jobs_df.iterrows():
            required = [s.strip() for s in row['required_skills'].split(',')]
            matched = set(user_skill) & set(required)
            missing = set(user_skill) - set(required)
            score = len(matched)
            job_matches.append((row['Job_Title'],score,matched,missing))
            #we use lambda func and x[1] to sort on the basis of score in descending order
        sorted_jobs = sorted(job_matches,key=lambda x : x[1] , reverse = True)
        st.subheader("Top Job Matches")
        #output logic
        for title,score,matched,missing in sorted_jobs[:5]:
            with st.expander(f"{title} (Match score:{score})"):
                st.markdown(f"Matches skills : {','.join(matched) if matched else None}")
                st.markdown(f"Missing skills : {','.join(missing) if missing else None}")
    st.success(f"Done, Keep improving your skills")