import os
import sys
import ssl
from dotenv import load_dotenv

from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import( create_react_agent , AgentExecutor)
from langchain import hub
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.tool import get_profile_url_tavily

# Configure requests to use the custom certificate

def lookup(name:str) ->str:


    llm = OllamaLLM(model="llama3.2")
    template = """given the full name {name_of_person} I want you t get me a username to their Twitter profile page.You should only give me only a username"""
    prompt_template = PromptTemplate(template=template , input_variables=["name_of_person"])
    tools_for_agent = [
        Tool(
            name = "Crawl Google 4 Twitter profile pages",
            func=get_profile_url_tavily,
            description="Useful for when you need to get the twitter page url"
        )
    ]


    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm , tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent,tools=tools_for_agent,verbose=True)

    result = agent_executor.invoke(
        input={"input":prompt_template.format(name_of_person=name)}
    )

    linkedin_profile_url = result["output"]


    return linkedin_profile_url

print(lookup("David"))