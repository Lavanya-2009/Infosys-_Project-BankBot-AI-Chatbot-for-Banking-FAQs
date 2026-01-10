from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print("API KEY:", api_key)  # should NOT be None

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    api_key=api_key
)

response = llm.invoke([
    HumanMessage(content="What is data scientist? Explain step by step.")
])

print(response.content)
