from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from tools import search_flights

# Load environment variables từ .env file
load_dotenv()

# Lấy API key
api_key = os.getenv("OPENAI_API_KEY")

    
    # Tạo LLM instance
llm = ChatOpenAI(
    model="gpt-4o-mini"
)
    


