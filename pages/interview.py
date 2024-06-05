import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from openai import OpenAI
from typing import Literal
import instructor

# Load OpenAI_API_KEY
load_dotenv()


def query_guardrail(query: str):
    """Filter gibberish answer"""

    # Specify OpenAi output
    class GuardRail(BaseModel):
        permission: Literal["allowed", "not_allowed"]

    prompt = """Check whether this query is allowed or not. Only answer to an interview question is allowed.
                If it's some gibberish or not an appropriate answer, then don't allow it"""
    # Patch the OpenAI client
    client = instructor.from_openai(OpenAI())

    # Extract structured data from natural language
    guardrail = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=GuardRail,
        messages=[
            {
                "role": "user",
                "content": f"{query} \n {prompt}",
            }
        ],
    )
    return guardrail.permission


def get_response(query: str, chat_history: list) -> str:
    """Get bot response"""
    if len(st.session_state.chat_history) >= int(st.session_state["interview_hr_question_num"]) * 2 + 3:
        st.switch_page("pages/score.py")

    if st.session_state["arrange_interview_immediate_feedback"]:
        arrange_interview_immediate_feedback = "Give the employee immediate feedback and advice on their response"
    else:
        arrange_interview_immediate_feedback = ""

    template = f"""
    You are an AI HR Assistant and this is an HR interview.
    You are interviewing {st.session_state["emp_salutation"]} {st.session_state["emp_name"]}.
    He's applying to be a {st.session_state["emp_job_title"]}.
    Either generate question based on their cv or response to the employee response.
    Question must be given one by one.
    And don't stay too long on the same topic, give it max 3 questions/responses per topic
    {arrange_interview_immediate_feedback}

    Chat history: {chat_history}

    employee response: {query}
    """
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI()
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"chat_history": chat_history, "emp_response": query})


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Interviewer Bot", page_icon="🫡")

st.title("Interviewer Bot")

# Welcome Conversation
if not st.session_state.chat_history:
    if not st.session_state["emp_cv"]:
        emp_cv = "employee didnt give their cv"
    else:
        emp_cv = st.session_state["emp_cv"]

    job_title = st.session_state["emp_job_title"]
    st.session_state.chat_history.append(HumanMessage(f"employee cv: {emp_cv}, desirable job: {job_title}"))
    with st.chat_message("AI"):
        ai_response = "Welcome to the interview! Are you ready?"
        st.markdown(ai_response)
    st.session_state.chat_history.append(AIMessage(ai_response))

# Conversation
for message in st.session_state.chat_history[2:]:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)

# User input
user_query = st.chat_input("your message")

# Chat markdown
if user_query is not None and user_query != "":
    if query_guardrail(user_query) == "allowed":
        st.session_state.chat_history.append(HumanMessage(user_query))

        with st.chat_message("Human"):
            st.markdown(user_query)

        with st.chat_message("AI"):
            ai_response = get_response(user_query, st.session_state.chat_history)
            st.markdown(ai_response)

        st.session_state.chat_history.append(AIMessage(ai_response))
    else:
        st.error("Please answer the question appropriately")
