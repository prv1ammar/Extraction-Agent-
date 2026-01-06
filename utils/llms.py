import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# ⬅️ حمّل env قبل أي حاجة
load_dotenv()


class LLMModel:
    def get_model(self):
        model = os.getenv("OPENAI_MODEL")
        base_url = os.getenv("OPENAI_BASE_URL")
        api_key = os.getenv("OPENAI_API_KEY")

        # 🔍 Debug (مؤقت)
        if not model:
            raise ValueError("OPENAI_MODEL is missing in .env")
        if not base_url:
            raise ValueError("OPENAI_BASE_URL is missing in .env")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing in .env")

        return ChatOpenAI(
            api_key=api_key,
            base_url=base_url,
            model=model,
            temperature=0
        )
