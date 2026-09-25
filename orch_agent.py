
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Import the specialist agents
from web_agent import web_agent
from gmail_agent import gmail_agent
from calender_agent import calendar_agent


# ============================================
# SETUP
# ============================================

load_dotenv()

llm = ChatOpenAI(
    model="openrouter/free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


# ============================================
# SUPERVISOR AGENT
# ============================================

def supervisor(goal):

    print("\n========================================")
    print("          SUPERVISOR AGENT")
    print("========================================")

    print("\n[USER GOAL]")
    print(goal)


    # ========================================
    # STEP 1: SUPERVISOR DECIDES
    # ========================================

    print("\n[SUPERVISOR]")
    print("Choosing the right specialist...")


    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are a Supervisor Agent.

You manage three specialist agents.

WEB:
Use for internet research, current information,
news, facts and general web searches.

GMAIL:
Use for emails, inbox, messages and email searches.

CALENDAR:
Use for meetings, events, appointments and schedules.

Choose the correct specialist for the user's request.

Return ONLY one of:

WEB
GMAIL
CALENDAR

Do not explain.
"""
        ),
        (
            "user",
            "{goal}"
        )
    ])


    # ========================================
    # CREATE LANGCHAIN CHAIN
    # ========================================

    chain = prompt | llm


    # ========================================
    # GET SUPERVISOR DECISION
    # ========================================

    response = chain.invoke({
        "goal": goal
    })


    raw_decision = response.content


    if raw_decision:
        decision = raw_decision.strip().upper()
    else:
        decision = ""


    # Handle unexpected LLM output

    if "GMAIL" in decision:
        decision = "GMAIL"

    elif "CALENDAR" in decision:
        decision = "CALENDAR"

    elif "WEB" in decision:
        decision = "WEB"

    else:
        decision = "UNKNOWN"


    print("\n[SUPERVISOR DECISION]")
    print("Delegate to:", decision)


    # ========================================
    # STEP 2: DELEGATE
    # ========================================

    if decision == "WEB":

        result = web_agent(goal)

    elif decision == "GMAIL":

        result = gmail_agent(goal)

    elif decision == "CALENDAR":

        result = calendar_agent(goal)

    else:

        result = (
            "I could not identify the correct "
            "specialist agent."
        )


    # ========================================
    # STEP 3: OBSERVE RESULT
    # ========================================

    print("\n[SUPERVISOR OBSERVATION]")
    print(result)


    # ========================================
    # STEP 4: FINAL ANSWER
    # ========================================

    final_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are the Supervisor Agent.

Give the user a short final answer based only
on the specialist agent's result.

Do not invent information.
"""
        ),
        (
            "user",
            """
User request:

{goal}

Specialist agent result:

{result}
"""
        )
    ])


    final_chain = final_prompt | llm


    final_response = final_chain.invoke({
        "goal": goal,
        "result": result
    })


    answer = final_response.content


    # ========================================
    # FINAL ANSWER
    # ========================================

    print("\n[FINAL ANSWER]")

    if answer:
        print(answer)
    else:
        print("No final answer generated.")


# ============================================
# RUN
# ============================================

if __name__ == "__main__":

    goal = input(
        "\nWhat do you want me to do? "
    )

    supervisor(goal)
