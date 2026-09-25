
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

llm = ChatOpenAI(
    model="openrouter/free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)



def search_gmail(query):
    """
    Demo Gmail search tool.

    Later, replace this function with
    the real Gmail API.
    """

    emails = [
        {
            "from": "nanig0385@gmail.com",
            "subject": "Tomorrow's meeting",
            "body": "Please attend the meeting tomorrow at 10 AM."
        },
        {
            "from": "hr@company.com",
            "subject": "Workshop Schedule",
            "body": "The AI workshop is scheduled for Friday."
        },
        {
            "from": "student@example.com",
            "subject": "Agentic AI Course",
            "body": "Can you share the Agentic AI course material?"
        }
    ]

    results = []

    for email in emails:

        text = (
            email["from"]
            + " "
            + email["subject"]
            + " "
            + email["body"]
        ).lower()

        if query.lower() in text:
            results.append(email)

    return results




def gmail_agent(goal):

    print("\n[GOAL]")
    print(goal)



    print("\n[GMAIL AGENT]")
    print("I need to decide what information is required.")


    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are a Gmail assistant.

Understand the user's request and decide
what keyword should be searched in Gmail.

Return ONLY the search keyword.
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


    print("\n[GMAIL AGENT DECISION]")
    print("Search Gmail for:", search_query)


    # ========================================
    # STEP 2: CALL GMAIL TOOL
    # ========================================

    print("\n[TOOL]")
    print("Calling Gmail search tool...")


    emails = search_gmail(search_query)


    print("\n[GMAIL OBSERVATION]")
    print("Found", len(emails), "email(s).")


    # ========================================
    # STEP 3: PREPARE RESULTS
    # ========================================

    email_text = ""


    for email in emails:

        email_text += f"""
From: {email['from']}
Subject: {email['subject']}
Message: {email['body']}

"""


    # ========================================
    # STEP 4: FINAL LLM ANSWER
    # ========================================

    final_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are a helpful Gmail assistant.

Answer the user's request using the
emails provided to you.

If no emails were found, clearly say so.

Keep the answer short and clear.
"""
        ),
        (
            "user",
            """
User request:

{goal}

Gmail results:

{email_text}
"""
        )
    ])


    final_chain = final_prompt | llm


    final_response = final_chain.invoke({
        "goal": goal,
        "email_text": email_text
    })


    answer = final_response.content


    # ========================================
    # RETURN RESULT TO SUPERVISOR
    # ========================================

    print("\n[GMAIL AGENT RESULT]")
    print(answer)


    return answer


# ============================================
# RUN AGENT DIRECTLY
# ============================================

if __name__ == "__main__":

    goal = input(
        "\nWhat do you want me to find in Gmail? "
    )

    result = gmail_agent(goal)

    print("\n[FINAL ANSWER]")
    print(result)

