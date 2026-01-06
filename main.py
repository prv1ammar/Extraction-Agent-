from agents.extraction_agent import create_extraction_agent

if __name__ == "__main__":
    agent = create_extraction_agent()

    result = agent.invoke({
        "input": "Go to the documents folder and extract all PDF, DOCX and TXT files"
    })

    print(result)
