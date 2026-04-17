import streamlit as st
import PyPDF2
import pandas as pd
import os


st.title("📄 Resume Analyzer")

# Upload file
uploaded_file = st.file_uploader("Upload your resume", type=["pdf"])

if uploaded_file is not None:
    st.success("Resume uploaded successfully")

    # Read PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text()

    text = text.lower()

    

    # Extract clean entities
    entities = []

    

    # Remove duplicates
    entities = list(set(entities))

    # Load skills.csv
    skills_df = pd.read_csv("skills.csv")

    # Convert skills column to list
    skills_list = skills_df["skills"].tolist()

    found_skills = []

    # Match skills
    for skill in skills_list:
        if skill.lower() in text:
            found_skills.append(skill)

    # Show results
    st.subheader(" Skills Found:")
    st.write(found_skills)

    st.subheader(" Skills Missing:")
    missing_skills = list(set(skills_list) - set(found_skills))
    st.write(missing_skills)

    # Score
    score = (len(found_skills) / len(skills_list)) * 100
    st.subheader(" Resume Score:")
    st.write(str(round(score, 2)) + "%")

    job_role = st.selectbox("Select Job Role",
                            ["Data Scientist", "Web Developer"])

    if job_role == "Data Scientist":
        required_skills = ["python", "machine learning", "sql", "pandas", "numpy"]
    else:
        required_skills = ["html", "css", "javascript", "java", "python", "C"]

    found_skills = []

    for skill in required_skills:
        if skill.lower() in text:
            found_skills.append(skill)

    missing_skills = list(set(required_skills) - set(found_skills))

    score = (len(found_skills) / len(required_skills)) * 100
    st.progress(int(score))
    st.write(f"Score: {round(score, 2)}%")

    if os.path.exists("skills.csv") and os.stat("skills.csv").st_size > 0:
        skills_df = pd.read_csv("skills.csv")
    else:
        print("skills.csv is empty or missing")

