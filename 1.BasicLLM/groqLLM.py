from dotenv import load_dotenv
from langchain_groq import ChatGroq
import ssl_fix
load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

response = llm.invoke("What is LangChain?")

print(response.content)

