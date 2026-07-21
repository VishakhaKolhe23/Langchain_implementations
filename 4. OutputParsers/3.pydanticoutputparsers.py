from pydantic import BaseModel
from langchain_core.output_parsers import StrOutputParser, ListOutputParser, PydanticOutputParser, JsonOutputParser
from langchain_ollama import ChatOllama
from pydantic import BaseModel , Field
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
 
model = ChatOllama(model="gpt-oss:120b-cloud")
prompt=PromptTemplate(
    input_variable=[],
    template="Write a poen on raining"

)
strParser=StrOutputParser() #used to get data into string format 
sequence= prompt | model | strParser
response=sequence.invoke({})
print(type(response))
print(response)

class CommaSeperatedListParser(ListOutputParser):
    def parse(self , text: str) -> list[str]:
        itemList=[]
        items= text.split(',')
        for item in items:
            itemList.append(item.strip())
        return itemList    
listParser=CommaSeperatedListParser() 
prompt=PromptTemplate(
 
    template="List down only names of top 5 popular countries seperated by commna "
)
strParser=CommaSeperatedListParser() 
sequence= prompt | model | strParser
response=sequence.invoke({})
print(type(response))
print(response)     

class Animal(BaseModel):
    name: str
    color: str
 
parser = PydanticOutputParser(pydantic_object=Animal)
prompt = ChatPromptTemplate.from_messages([
    ('user', "#Format: {format_instructions} \nQuestion: {question}")
]).partial(format_instructions=parser.get_format_instructions())
chain = prompt | model | parser
response = chain.invoke({"question": "Describe any 5 animals in India with details of name and color"})
print(type(response))
print(response)


#json parser 


# ✅ Pydantic Schema (ONLY fields here)
class Person(BaseModel):
    name: str = Field(description="Name of the person")
    age: int = Field(description="Age of the person")
    hobbies: list[str] = Field(description="Hobbies of the person")

# ✅ Parser
parser = PydanticOutputParser(pydantic_object=Person)

# ✅ Prompt
prompt = ChatPromptTemplate.from_messages([
    ("user", 
     "Ivan is 27 years old and he likes swimming, music and cricket.\n"
     "Format: {format_instructions}")
]).partial(format_instructions=parser.get_format_instructions())

# ✅ Chain
chain = prompt | model | parser

# ✅ Invoke
response = chain.invoke({})

# ✅ Output
print(type(response))
print(response)

from pydantic import BaseModel, Field
from typing import List

model = ChatOllama(model="gpt-oss:120b-cloud")

class Employee(BaseModel):
    name: str = Field(description="Name of the employee")
    age: int = Field(description="Age of the employee")
    department: str = Field(description="Department of the employee")

class EmployeeList(BaseModel):
    employees: List[Employee]

parser = PydanticOutputParser(pydantic_object=EmployeeList)

prompt = ChatPromptTemplate.from_messages([
    ("user",
     "Generate details of 5 employees working in a company.\n"
     "Each employee should have name, age, and department.\n"
     "Format: {format_instructions}")
]).partial(format_instructions=parser.get_format_instructions())


chain = prompt | model | parser


response = chain.invoke({})


print(type(response))    
print(response)


for emp in response.employees:
    print(f"{emp.name} | {emp.age} | {emp.department}")







