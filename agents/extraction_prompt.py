from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder


def get_extraction_prompt():
    return ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are a document extraction agent.

Your role:
- Read files from a folder
- Use tools to extract structured information
- Output data as structured JSON

Data types to extract:
- text
- tables
- images
- graphs

Always use the provided tools when needed.
"""
        ),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])
