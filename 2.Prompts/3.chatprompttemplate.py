from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# Create model
model = ChatOllama(model="gpt-oss:120b-cloud")

# Store conversation history
chat_history = []


chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# Console chatbot loop
while True:
    user_input = input("Enter prompt (type 'quit' to exit): ")

    if user_input.lower() == "quit":
        break

    # Add user message to history
    chat_history.append(HumanMessage(content=user_input))

    # Create prompt with history
    prompt = chat_prompt_template.invoke({
        "chat_history": chat_history,
        "input": user_input
    })

    # Get response
    response = model.invoke(prompt)

    # Print response
    print("Bot:", response.content)

    # Addding bot response to history
    chat_history.append(AIMessage(content=response.content))