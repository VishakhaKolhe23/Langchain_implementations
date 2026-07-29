from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

chat_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

print("Blog post generator")
print("Provide ideas or topics for the blog post. Type exit to finish")

topic=input("Enter blog post topic: ")
chat_prompt_template=ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("You are a professional blog writer . Help generate informative, engaging and well structured blog post about a {topic}."),
    HumanMessagePromptTemplate.from_template("Write a detialed blog post about {topic}.")

])

#initialize a chat history using list
chat_history=[]
while True:
    user_input=input("Ideas or intruction or type exit ")
    if user_input.lower()=="exit":
        print("Existing blog post geenrator") 
        break 
     










