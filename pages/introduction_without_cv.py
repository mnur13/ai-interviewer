import streamlit as st

st.set_page_config(page_title="Interviewer Bot", page_icon="🫡")

st.header("Introduction")

st.header("Hi! My name is Edgar!")
st.write("Please introduce yourself!")

with st.form("emp_information_form"):
    # Get initial name
    st.write("What would you like to be called?")
    st.session_state["emp_name"] = st.text_input("Initial name")

    # Get salutation
    st.write("What's your salutation?")
    st.session_state["emp_salutation"] = st.radio("Title", ["Mr.", "Ms.", "Mrs."])

    # Get job title
    st.write("What's the job you're applying to?")
    st.session_state["emp_job_title"] = st.text_input("Job title")

    # Submit form
    if st.form_submit_button("Submit"):
        if not all(
            (
                st.session_state["emp_name"],
                st.session_state["emp_salutation"],
                st.session_state["emp_job_title"],
            )
        ):
            st.error("Please fill out all fields!")

        else:
            st.write("Nice to meet you, ", st.session_state["emp_salutation"], " ", st.session_state["emp_name"], "!")
            st.write("Click continue to configure our interview!")

if st.button("Continue"):
    st.switch_page("pages/configure_interview_2.py")
