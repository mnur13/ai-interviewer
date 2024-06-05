from setuptools import find_packages, setup

install_requires = [
    "streamlit",
    "python-dotenv>=1, <2",
    "pypdf>=4, <5",
    "openai>=1, <2",
    "langchain>=0, <1",
    "langchain-openai>=0, <2",
    "instructor>=1, <2",
]

if __name__ == "__main__":
    setup(
        name="ai-interviewer",
        version="0.1",
        description="modules for ai-interviewer project",
        author="Muhammad Nur Ichsan",
        packages=find_packages(),
        install_requires=install_requires,
    )
