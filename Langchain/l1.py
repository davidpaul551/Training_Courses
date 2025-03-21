from langchain_core.prompts import PromptTemplate

from langchain_ollama import OllamaLLM

from third_parties.linkedin import scrape_linkedin_profile
# summary_template = """
#     given te info {information} about a person
#     1. a short summary
#     2. two interesting facts about them
# """

# summary_prompt_template = PromptTemplate(input_variables=["information"],template=summary_template)
# llm = OllamaLLM(model="llama3.2")

# chain = summary_prompt_template | llm
# information = "Hiii"
# res = chain.invoke(input={"information":information})

# print(res)


# summary_template = """
# Given the info {information} about a person:
# 1. A short summary
# 2. Two interesting facts about them
# """

# summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)
# info = "X"

# formatted = summary_prompt_template.format(information = info)
# print(formatted)





summary_template = """
    given te info {information} about a person
    1. a short summary
    2. two interesting facts about them
"""
summary_prompt_template = PromptTemplate(input_variables=["information"],template=summary_template)
llm = OllamaLLM(model="llama3.2")

chain = summary_prompt_template | llm
information = scrape_linkedin_profile("url" , True)
res = chain.invoke(input={"information":information})

print(res)