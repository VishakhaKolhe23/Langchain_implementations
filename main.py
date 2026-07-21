from langchain_core.output_parsers import PydanticOutputParser,JsonOutputParser
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate
from langchain_ollama import ChatOllama

model = ChatOllama(model = "gpt-oss:120b-cloud")
parser = JsonOutputParser()

template = PromptTemplate.from_template(template = "give me the name and age of the boy along with the city he lives in",
partial_variables = {"format_instructions":parser.get_format_instructions()}) 

chain = template | model | parser

response = chain.invoke({})
print(response)
