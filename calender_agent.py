
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


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
# CALENDAR TOOL
# ============================================

def search_calendar(query):
    """
    Demo calendar search tool.

    Later, replace this function with
    the real Google Calendar API.
    """

    events = [
        {
            "date": "2026-09-16",
            "time": "10:00 AM",
            "title": "AI Workshop",
            "description": "Agentic AI workshop with students."
        },
        {
            "date": "2026-09-16",
            "time": "02:00 PM",
            "title": "Project Review",
            "description": "Review student Agentic AI projects."
        },
        {
            "date": "2026-09-17",
            "time": "11:00 AM",
            "title": "Team Meeting",
            "description": "Weekly company team meeting."
        }
    ]

    results = []

    for event in events:

        text = (
            event["date"]
            + " "
            + event["time"]
            + " "
            + event["title"]
            + " "
            + event["description"]
        ).lower()

        if query.lower() in text:
            results.append(event)

    return results


# ============================================
# CALENDAR AGENT
# ============================================

def calendar_agent(goal):

    print("\n[GOAL]")
    print(goal)


    # ========================================
    # STEP 1: LLM DECISION
    # ========================================

    print("\n[CALENDAR AGENT]")
    print("I need to find the relevant calendar information.")


    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are a calendar assistant.

Understand the user's request and decide
what keyword should be searched in the calendar.

Return ONLY the search keyword.

Examples:

User: What meetings do I have?
Answer: meeting

User: Show me my AI events
Answer: AI

User: What project reviews do I have?
Answer: project
"""
        ),
        (
            "user",
            "{goal}"
        )
    ])


    chain = prompt | llm


    response = chain.invoke({
        "goal": goal
    })


    search_query = response.content.strip()


    print("\n[CALENDAR AGENT DECISION]")
    print("Search Calendar for:", search_query)


    # ========================================
    # STEP 2: CALL CALENDAR TOOL
    # ========================================

    print("\n[TOOL]")
    print("Calling Calendar search tool...")


    events = search_calendar(search_query)


    print("\n[CALENDAR OBSERVATION]")
    print("Found", len(events), "event(s).")


    # ========================================
    # STEP 3: PREPARE RESULTS
    # ========================================

    event_text = ""


    for event in events:

        event_text += f"""
Date: {event['date']}
Time: {event['time']}
Event: {event['title']}
Description: {event['description']}

"""


    # ========================================
    # STEP 4: FINAL LLM RESPONSE
    # ========================================

    final_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are a helpful calendar assistant.

Answer the user's request using the
calendar events provided.

Keep the answer short and clear.

If no events were found, clearly say so.
"""
        ),
        (
            "user",
            """
User request:

{goal}

Calendar results:

{event_text}
"""
        )
    ])


    final_chain = final_prompt | llm


    final_response = final_chain.invoke({
        "goal": goal,
        "event_text": event_text
    })


    answer = final_response.content


    # ========================================
    # RETURN RESULT TO SUPERVISOR
    # ========================================

    print("\n[CALENDAR AGENT RESULT]")
    print(answer)


    return answer


# ============================================
# RUN AGENT DIRECTLY
# ============================================

if __name__ == "__main__":

    goal = input(
        "\nWhat do you want me to check in your calendar? "
    )

    result = calendar_agent(goal)

    print("\n[FINAL ANSWER]")
    print(result)
