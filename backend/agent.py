import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents import create_pandas_dataframe_agent

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=os.getenv("GEMINI_API_KEY")
)


def ask_dataframe(df, question):
    agent = create_pandas_dataframe_agent(
        llm,
        df,
        allow_dangerous_code=True,
        verbose=True
    )

    response = agent.invoke(question)

    return response["output"]