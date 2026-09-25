from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

load_dotenv()

llm = ChatOpenAI(
    model="openrouter/free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def web_agent(goal):

    print("\n[GOAL]")
    print(goal)

    print("\n[WEB AGENT]")
    print("Thinking about what action to take...")

    response = llm.invoke(goal)

    answer = response.content

    print("\n[WEB AGENT RESULT]")
    print(answer)

    return answer


if __name__ == "__main__":

    goal = input("What do you want me to research? ")

    result = web_agent(goal)

    print("\n[FINAL ANSWER]")
    print(result)