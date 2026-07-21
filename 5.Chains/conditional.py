from langchain_core.output_parsers import StrOutputParser, ListOutputParser, PydanticOutputParser, JsonOutputParser
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder 
from langchain_core.runnables import RunnableParallel, RunnableSequence, RunnableLambda , RunnableBranch
model = ChatOllama(model="gpt-oss:120b-cloud")
from typing import Literal

#
prompt_1=PromptTemplate(
    template= "Which  is the capital city of {country}",
    input_variables=["country"]
)
prompt_2=PromptTemplate(
    template= "List top 3 tourist places of {country}",
    input_variables=["country"]
)
strParser= StrOutputParser()

parallel_chain=RunnableParallel(
    {"response_1": prompt_1  | model| strParser,
    "response_2": prompt_2  | model| strParser}

)
response=parallel_chain.invoke({"country": "India"})
print(response)

class FeedbackSentiment(BaseModel):
    sentiment: Literal["positive", "negative"]

parser = PydanticOutputParser(pydantic_object=FeedbackSentiment)

sentiment_prompt = PromptTemplate(
    input_variables=["feedback"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
    template=""" Decide the sentiment (positive or negative) of the feedback.
Feedback: {feedback}
Return ONLY JSON:
{format_instructions}
"""
)

sentiment_chain = sentiment_prompt | model | parser

positive_prompt = PromptTemplate(
    input_variables=["feedback"],
    template="Write a short thankyou email for this feedback: {feedback}"
)

negative_prompt = PromptTemplate(
    input_variables=["feedback"],
    template="Write a short apology email for this feedback: {feedback}"
)


strParser = StrOutputParser()

positive_chain = positive_prompt | model | strParser
negative_chain = negative_prompt | model | strParser

feedback = "Room was clean."

result = sentiment_chain.invoke({"feedback": feedback})

if result.sentiment == "positive":
    reply = positive_chain.invoke({"feedback": feedback})
else:
    reply = negative_chain.invoke({"feedback": feedback})


print("Sentiment:", result.sentiment)
print("Reply:", reply)
#Negative/positive chains code
 
prompt2 = PromptTemplate(
    template='Write appropriate response to the positive feedback of customer\n\n{customer_feedback}',
    input_variables=['customer_feedback']
)
 
parser2 = StrOutputParser()
positive_chain = prompt2 | model | parser2
 
prompt3 = PromptTemplate(
    template='Write appropriate response to the negative feedback of customer\n\n{customer_feedback}',
    input_variables=['customer_feedback']
)
 
negative_chain = prompt3 | model | parser2
 
prompt4 = PromptTemplate(
    template='Write appropriate response to the neutral feedback of customer\n\n{customer_feedback}',
    input_variables=['customer_feedback']
)
 
neutral_chain = prompt4 | model | parser2


#  Positive / Negative / Neutral chains

prompt2 = PromptTemplate(
    template='Write appropriate response to the positive feedback of customer\n\n{customer_feedback}',
    input_variables=['customer_feedback']
)

parser2 = StrOutputParser()
positive_chain = prompt2 | model | parser2

prompt3 = PromptTemplate(
    template='Write appropriate response to the negative feedback of customer\n\n{customer_feedback}',
    input_variables=['customer_feedback']
)

negative_chain = prompt3 | model | parser2

prompt4 = PromptTemplate(
    template='Write appropriate response to the neutral feedback of customer\n\n{customer_feedback}',
    input_variables=['customer_feedback']
)

neutral_chain = prompt4 | model | parser2  


conditional_chain = RunnableBranch(
    (lambda x: x["sentiment"].sentiment == "positive", positive_chain),
    (lambda x: x["sentiment"].sentiment == "negative", negative_chain),
    neutral_chain
)


customer_feedback = "Room was good "

sentiment_result = sentiment_chain.invoke({
    "feedback": customer_feedback  
})

response = conditional_chain.invoke({
    "customer_feedback": customer_feedback,   
    "sentiment": sentiment_result             
})

print("Sentiment:", sentiment_result.sentiment)
print("Reply:", response)