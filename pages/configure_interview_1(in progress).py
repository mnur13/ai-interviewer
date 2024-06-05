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

with st.form("interview_configuration:"):
    # HR interview toggle
    st.session_state["arrange_interview_hr"] = st.checkbox("I want to simulate HR interview")

    # User interview toggle
    st.session_state["arrange_interview_user"] = st.checkbox("I want to simulate user interview")

    # Immediate comment response
    st.session_state["arrange_interview_immediate_comment"] = st.checkbox(
        "I want to be given immediate comment on my interview answer"
    )

    if st.form_submit_button("Continue"):
        if not any((st.session_state["arrange_interview_hr"], st.session_state["arrange_interview_user"])):
            st.error("Please at least choose one interview!")
        else:
            st.switch_page("pages/configure_interview_2.py")
