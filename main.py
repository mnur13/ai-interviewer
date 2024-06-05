import streamlit as st

st.set_page_config(page_title="Interviewer Bot", page_icon="🫡")

st.title("AI-Powered HR Interviewer")

st.header("Welcome to the AI-Powered HR Assistant")

if st.button("Continue"):
    st.switch_page("pages/introduction.py")
