
import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Audit Fraud Quiz", layout="wide")

# Load data
@st.cache_data
def load_questions():
    return pd.read_csv("questions_combined.csv")

df = load_questions()

st.title("🔍 Audit Fraud MCQ Game")
st.markdown("Test your fraud knowledge by choosing a real Indian fraud case and answering 20 randomized MCQs!")

# Mandatory name input
name = st.text_input("Enter your full name (required to start):")
if not name:
    st.warning("Please enter your name to begin.")
    st.stop()

# Case selection
case_options = sorted(df['case'].unique())
selected_case = st.selectbox("Choose a fraud case:", case_options)

# Filter and randomize
case_df = df[df['case'] == selected_case].sample(n=20, random_state=42).reset_index(drop=True)

user_answers = {}
score = 0

st.markdown(f"### 📚 Case: {selected_case}")

# Display all questions
for i, row in case_df.iterrows():
    st.markdown(f"**Q{i+1}. {row['question']}**")
    options = {
        'a': row['option_a'],
        'b': row['option_b'],
        'c': row['option_c'],
        'd': row['option_d']
    }
    choice = st.radio(
        label="",
        options=list(options.keys()),
        format_func=lambda x: f"{x}) {options[x]}",
        key=f"q{i}"
    )
    user_answers[i] = choice

# Submit button
if st.button("✅ Submit Answers"):
    for i, row in case_df.iterrows():
        if user_answers.get(i) == row['answer']:
            score += 1

    st.success(f"🎉 {name}, you scored {score} out of {len(case_df)}!")

    if score == len(case_df):
        st.balloons()

    st.markdown("### ✅ Correct Answers:")
    for i, row in case_df.iterrows():
        ans_letter = row["answer"]
        ans_text = row[f"option_{ans_letter}"]
        st.markdown(f"**Q{i+1}. {row['question']}**")
        st.markdown(f"✔️ Correct: {ans_letter}) {ans_text}")

    st.markdown("---")
    st.markdown("### ✉️ Submit your score to Madhu")
    st.markdown("Click below to submit your result.")
    st.link_button("📨 Submit via Google Form", "https://forms.gle/HDQMTwk6x8CrhiUA9")
