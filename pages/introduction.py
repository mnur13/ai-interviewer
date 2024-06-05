import streamlit as st
import pypdf
import instructor
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI
from typing import Literal

# load openai_api_key from .env
load_dotenv()


def read_pdf(file) -> str:
    """Reads pdf file and output as text string."""
    # Create a PDF object
    pdf = pypdf.PdfReader(file)

    # Get the number of pages in the PDF document
    num_pages = len(pdf.pages)
    text = ""

    for page in range(num_pages):
        # Extract the text from the page
        page_text = pdf.pages[page].extract_text()
        text += page_text

    return text


def cv_guardrail(emp_cv_text: str):
    """Check if PDF contain legit cv"""

    # Specify OpenAi output
    class GuardRail(BaseModel):
        permission: Literal["allowed", "not_allowed"]

    prompt = """Check whether the above text is a cv or not. Only CV texts are allowed.
                If it is other type of text or nothing exist above this text, then dont allow it"""

    # Patch the OpenAI client
    client = instructor.from_openai(OpenAI())

    # Extract structured data from natural language
    guardrail = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=GuardRail,
        messages=[
            {
                "role": "user",
                "content": f"{emp_cv_text} \n {prompt}",
            }
        ],
    )
    return guardrail.permission


def get_name_and_salutation(emp_cv_text: str):
    """Let OpenAi analyze CV text to get name and salutation"""

    # Specify OpenAi output
    class UserInfo(BaseModel):
        short_name: str
        salutation: Literal["Mr.", "Ms.", "Mrs."]

    # Patch the OpenAI client
    client = instructor.from_openai(OpenAI())

    # Extract structured data from natural language
    user_info = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=UserInfo,
        messages=[{"role": "user", "content": f"{emp_cv_text} \n get the person short name/call name and salutation"}],
    )
    st.session_state["emp_name"] = user_info.short_name.title()
    st.session_state["emp_salutation"] = user_info.salutation


st.set_page_config(page_title="Interviewer Bot", page_icon="🫡")

st.header("Introduction")

st.header("Hi! My name is Edgar!")
st.write("Please introduce yourself!")

with st.form("emp_information_cv"):

    # Upload CV
    st.write("Please submit your latest/preferred CV")
    emp_cv = st.file_uploader("Upload CV", type=["pdf", "docx"])

    # Get emp_cv, emp_name, and emp_salutation
    if emp_cv:  # Triggered by form submit button
        st.markdown("file uploaded")
        st.session_state["emp_cv"] = read_pdf(emp_cv)
        if cv_guardrail(st.session_state["emp_cv"]) == "allowed":
            get_name_and_salutation(st.session_state["emp_cv"])
        else:
            st.error("Please upload only appropriate CV!")

    # Get Job title
    st.write("What job are you applying to?")
    st.session_state["emp_job_title"] = st.text_input("Job title")

    # Continue without CV
    alternative_form = st.toggle("Continue without uploading CV")

    if st.form_submit_button("Submit"):
        if not any((emp_cv, alternative_form)):
            st.error("Please upload your cv or agree to continue without cv!")

        elif alternative_form:
            st.session_state["emp_cv"] = False
            st.switch_page("pages/introduction_without_cv.py")

        elif st.session_state["emp_job_title"] == "":
            st.error("Please tell me what job you're applying to!")

        else:
            st.switch_page("pages/configure_interview_2.py")
