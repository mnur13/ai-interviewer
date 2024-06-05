import streamlit as st
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from openai import OpenAI
import instructor


load_dotenv()


def get_score(chat_history: list) -> (float, str):
    """Get the interview score and feedback"""

    class UserScore(BaseModel):
        final_score: float = Field(ge=0, le=10)
        feedback: str = None

    prompt = """rate the above interview based on the quality and seriousness of the response, the personality of the employee, 
                and how capable the employee on their job. Be strict on your rating and dont afraid to give bad rating to unserious employee.
                Give the reason of your rating and give feedback for the employee"""

    # Patch the OpenAI client
    client = instructor.from_openai(OpenAI())

    # Extract structured data from natural language
    score = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=UserScore,
        messages=[{"role": "user", "content": f"{chat_history} \n {prompt} "}],
    )
    return score.final_score, score.feedback


st.set_page_config(page_title="Scoring", page_icon="🫡")

st.title("Interviewer Bot")
st.write("Congratulation, your score is.....")

final_score, feedback = get_score(st.session_state.chat_history)
st.markdown(final_score)
st.markdown(feedback)
