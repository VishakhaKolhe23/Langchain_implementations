# database by using streamlit interface                                                                                       import streamlit as st
import sqlite3
import uuid
from  typing import List
from dotenv import load_dotenv
import uuid
 
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_groq import ChatGroq
from langchain_core.messages import(
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
 
# here we are importing loaded the credentials by using load_dotenv
load_dotenv
 
# Database
# for the database part, we have tried to connect this particular chat memory
# if that database is not present it will be created
# here database is chat_memory1.db
conn = sqlite3.connect("chat_memory1.db", check_same_thread=False)
cursor=conn.cursor()
 
# after that here if table is not present we are creating the table
cursor.execute(# here particular chat_history table will created
    """
    CREATE TABLE IF NOT EXISTS chat_history(
    session_id TEXT,
    role TEXT,
    content TEXT
    )
    """
)
conn.commit()
 
"""
for saving message here we defined a helper function here,
to save the session_d, role and content
 
"""
def save_message(session_id:str, role:str, content:str):
    cursor.execute(
        "INSERT INTO chat_history VALUES (?,?,?)",
        (session_id,role, content)
    )
"""
To load the chat history, again created a helper function,
which will return back the chat hsitroy that has been saved into a databse for a particular session_id
 
"""
 
def load_chat_history(session_id:str)-> List[BaseMessage]:
    cursor.execute(
        "Select role, content from chat_history where session_id=?", (session_id,)
    )
    rows = cursor.fetchall()
    history: List[BaseMessage]= []
 
    for role, content in rows:
        if role=="human":
            history.append(HumanMessage(content=content))
        elif role=="ai":
            history.append(AIMessage(content=content))
    return history
 
# again i created another function to get all sessions
# and the databse part is done upto this  point
def get_all_sessions():
    cursor.execute(
        "SELECT DISTINCT session_id from chat_history order by rowid desc"
    )
    return [row[0] for row in cursor.fetchall()]
 
 
# streamlit configurations
"""
Then for the stream configuration, and here i set page config and then
page title is conversational drag
"""
st.set_page_config(page_title = "Conversational RAG", layout= "wide")
st.title("Conversational RAG with memory")
 
# sidebar : with a title chats
"""
Now for an individual session or then new session, here i have created empty chat_ history
as well as unique session_id
 
And then also tried to load the previous converstions using this get_all functions here
 
"""
 
st.sidebar.title("Chats")
 
if "session_id" not in st.session_state:
    st.session_state.session_id=str(uuid.uuid4())
    st.session_state.chat_history=[]
 
if st.sidebar.button("New Chat"):
    st.session_state.session_id=str(uuid.uuid4())
    st.session_state.chat_history=[]
 
st.sidebar.markdown("Previous conversations")
 
 
 
for sid in get_all_sessions():# get function
    if st.sidebar.button(sid[:8]):
        st.session_state.session_id=sid
        st.session_state.chat_history=load_chat_history(sid)# and here chat histoy is loading
        # by using chat history function by passing the session ID inside it
 
session_id = st.session_state.session_id
 
#now no matter where the session Id comes from a vaild ID is maintained
# now langchain part
 
# load and index pdf
 
@st.cache_resource
def load_vectorstore():
    loader = PyMuPDFLoader("PYTHON PROGRAMMING NOTES.pdf")
    document =loader.load()
 
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap =150
    )
 
    chunks = splitter.split_documents(document)
 
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )
 
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding= embeddings
    )
    return vectorstore
 
"""
So, the vector store is created and then the vectorstore is used as retriever
 
 
 
"""
 
vectorstore= load_vectorstore()
retriever = vectorstore.as_retriever(searc_kwargs={"k":4})
 
 
llm= ChatGroq(model="llama-3.3-70b-versatile")
 
prompt = ChatPromptTemplate.from_messages(
    [
 
        SystemMessage(
            content=(
                """
                You are a helpful AI assistant. Answer strictly from the provide context.
                If the answer is not present, just say you don't know
 
 
            """
 
            )
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        (
            "human",
            "Context: {context}, question: {input}"
            # here we add a new context and new user input in this particular place
        )
    ]
 
)
# so now for the conversation rag model
def conversation_rag(user_input:str, chat_history: List[BaseMessage]):
    docs=retriever.invoke(user_input)
 
 
    context= "\n\n".join(
        f"[page {d.metadata.get('page', 'N/A')}]\n{d.page_content}"for d in docs
    )
    # and the appended them all into one single string
    # now the prompt is in this particular from -> dwon messages is prompt
    messages= prompt.invoke(
        {
            "input":user_input,
            "context":context,
             "chat_history": chat_history              
        }
    )
 
    response=llm.invoke(messages) # then invoking that particular prompt
    return response,docs # here returning the response as well as document
 
 
# load chat history
 
if not st.session_state.chat_history:
    st.session_state.chat_history= load_chat_history(session_id)
 
# chat window
 
for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    elif isinstance(msg,AIMessage):
        st.chat_message("AI").wrote(msg.content)
 
user_input=st.chat_input("Ask a question from a PDF")
if user_input:
    st.chat_meassage("user").write(user_input)
    save_message(session_id, "human", user_input)
    st.session_state.chat_history.append(HumanMessage(content=user_input))
 
    response, sources = conversation_rag(
        user_input, st.session_state.chat_history
    )
 
    st.chat_message("AI").write(response.content)
    save_message(session_id, "ai",response.content)
    st.session_state.chat_history.append(AIMessage(content=response.content))