import streamlit as st
import PyPDF2
import pandas as pd
import os
from transformers import pipeline

st.title("📄 Resume Analyzer")

uploaded_file = st.file_uploader("Upload your resume", type=["pdf"])

if uploaded_file is not None:
    st.success("Resume uploaded successfully")

    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""

    for page in pdf_reader.pages:
        extracted_text = page.extract_text()
        if extracted_text:
            text += extracted_text

    text_lower = text.lower()

    ner = pipeline("ner", model="dslim/bert-base-NER")

    ner_results = ner(text)

    entities = []

    current_word = ""
    current_label = ""

    for item in ner_results:
        word = item["word"].replace("##", "")
        label = item["entity"]

        if label.startswith("B-"):
            if current_word:
                entities.append((current_label, current_word))

            current_word = word
            current_label = label.replace("B-", "")

        elif label.startswith("I-"):
            current_word += " " + word

    if current_word:
        entities.append((current_label, current_word))

    entities = list(set(entities))

    st.subheader("🧠 Named Entities Found")

    person_entities = [entity[1] for entity in entities if entity[0] == "PER"]
    org_entities = [entity[1] for entity in entities if entity[0] == "ORG"]
    loc_entities = [entity[1] for entity in entities if entity[0] == "LOC"]

    st.write("Persons:", person_entities)
    st.write("Organizations:", org_entities)
    st.write("Locations:", loc_entities)

    if os.path.exists("skills.csv") and os.stat("skills.csv").st_size > 0:
        skills_df = pd.read_csv("skills.csv")
    else:
        st.error("skills.csv is empty or missing")
        st.stop()

    skills_list = skills_df["skills"].dropna().tolist()

    found_skills = []

    for skill in skills_list:
        if skill.lower().strip() in text_lower:
            found_skills.append(skill)

    missing_skills = list(set(skills_list) - set(found_skills))

    st.subheader("✅ Skills Found")
    st.write(found_skills)

    st.subheader("❌ Skills Missing")
    st.write(missing_skills)

    score = (len(found_skills) / len(skills_list)) * 100

    st.subheader("📊 Resume Score")
    st.write(f"{round(score, 2)}%")

    job_role = st.selectbox(
        "Select Job Role",
        ["Data Scientist", "Web Developer"]
    )

    if job_role == "Data Scientist":
        required_skills = [
            "python",
            "machine learning",
            "sql",
            "pandas",
            "numpy",
            "deep learning",
            "tensorflow"
        ]
    else:
        required_skills = [
            "html",
            "css",
            "javascript",
            "react",
            "bootstrap",
            "node.js"
        ]

    role_found_skills = []

    for skill in required_skills:
        if skill.lower().strip() in text_lower:
            role_found_skills.append(skill)

    role_missing_skills = [skill for skill in required_skills if skill not in role_found_skills]

    role_score = (len(role_found_skills) / len(required_skills)) * 100

    st.subheader(f"🎯 {job_role} Skill Match")

    st.write("Matched Skills:")
    st.write(role_found_skills)

    st.write("Missing Skills:")
    st.write(role_missing_skills)

    st.progress(int(role_score))
    st.write(f"Match Score: {round(role_score, 2)}%")
