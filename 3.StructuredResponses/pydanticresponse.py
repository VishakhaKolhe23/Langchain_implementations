import truststore
truststore.inject_into_ssl()

import os
import certifi

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class Response(BaseModel):
    answer: str

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite"
)

structured_llm = llm.with_structured_output(Response)

result = structured_llm.invoke("What is Python?")

print(result.answer)