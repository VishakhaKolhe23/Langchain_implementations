from langchain_core.output_parsers import StrOutputParser, ListOutputParser, PydanticOutputParser, JsonOutputParser
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder 
from langchain_core.runnables import RunnableSequence
model = ChatOllama(model="gpt-oss:120b-cloud")


# ex 1 
prompt_1=PromptTemplate(
    template= "Which  is the capital city of {country}",
    input_variables=["country"]
)
prompt_2=PromptTemplate(
    template= "List top 3 tourist places of {city}",
    input_variables=["city"]
)
strParser= StrOutputParser()
sequential_chain= prompt_1 | model | strParser | prompt_2 | model | strParser
response=sequential_chain.invoke({"country": "India"})
print(response)
#ex 2 - using classes
prompt_1=PromptTemplate(
    template= "Which  is the capital city of {country}",
    input_variables=["country"]
)
prompt_2=PromptTemplate(
    template= "List top 3 tourist places of {city}",
    input_variables=["city"]
)
strParser= StrOutputParser()
chain_1= prompt_1 | model | strParser 
chain_2= prompt_2 | model | strParser 
sequential_chain= RunnableSequence(chain_1 , chain_2)
response=sequential_chain.invoke({"country": "India"})
print(response)
