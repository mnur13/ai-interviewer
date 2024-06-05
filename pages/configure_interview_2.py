import streamlit as st

st.set_page_config(page_title="Interviewer Bot", page_icon="🫡")

st.title("Interview Configuration")

st.header("Configure your interview")
st.write(
    "Choose how would you like your interview to be",
    st.session_state["emp_salutation"],
    " ",
    st.session_state["emp_name"],
)
continue_button = False
with st.form("interview_configuration:"):
    # Limit number of questions
    st.session_state["interview_hr_question_num"] = st.slider(
        "How many qustion would you like before the final scoring?", 1, 20, 10
    )

    # Immediate comment toggle
    st.session_state["arrange_interview_immediate_feedback"] = st.checkbox(
        "I want to be given immediate comment on my interview answer"
    )

    if st.form_submit_button("Submit"):
        st.switch_page("pages/interview.py")
