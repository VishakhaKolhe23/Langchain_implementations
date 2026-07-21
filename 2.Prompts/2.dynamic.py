from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    "Explain {topic}."
)

prompt.invoke({"topic": "LangChain"})