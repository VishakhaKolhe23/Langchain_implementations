from langchain_core.prompts import PromptTemplate

dynamic_prompt = PromptTemplate(
    template="Write a short paragraph about {topic} in a {style} style.",
    input_variables=["topic", "style"]
)

prompt_text = dynamic_prompt.format(topic="AI", style="humorous")
prompt_text1 = dynamic_prompt.format(topic="blockchain", style="formal")

print(prompt_text)
print(prompt_text1)


