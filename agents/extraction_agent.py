from langchain.agents import AgentExecutor, create_openai_functions_agent
from utils.llms import LLMModel
from tools.extraction_tool import extract_documents
from agents.extraction_prompt import get_extraction_prompt


def create_extraction_agent():
    llm = LLMModel().get_model()

    tools = [extract_documents]
    prompt = get_extraction_prompt()

    # Use create_openai_functions_agent which is the new API
    agent = create_openai_functions_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    )

    return agent_executor
