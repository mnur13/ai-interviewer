# AI Interviewer Bot

The AI Interviewer Bot is a powerful tool designed to streamline the employee interview process. This bot can conduct interviews with candidates based on their CVs, or interact with them even if they do not have a CV. By leveraging advanced natural language processing (NLP) techniques, the bot can ask relevant questions, evaluate responses, and provide an initial assessment of the candidate's fit for the role.

## Features

- **Interview with CV**: Candidates can upload their CVs, and the bot will tailor its questions based on the information provided.
- **Interview without CV**: Candidates can also participate in interviews without providing a CV. The bot will ask general questions to gather information about their background and skills.
- **Dynamic Questioning**: The bot adjusts its questions based on candidate responses to provide a more personalized interview experience.
- **Feedback and Scoring**: The bot can provide feedback and an initial score based on the interview responses.

## Installation

To run the AI-Interviewer Bot, follow these steps:

1. **Clone the repository**:
```bash
git clone https://github.com/mnur13/ai-interviewer.git
cd ai-interviewer
```

2. **Set up your virtual environment**:
```console
py -m venv venv
```

2. **Install the required dependencies**:
```console
pip install .
```

3. **Create a .env file in the root directory and add the necessary environment variables**:

```
OPENAI_API_KEY="your_openai_api_key"
```

4. **Run the application**:
```console
streamlit run main.py
```
