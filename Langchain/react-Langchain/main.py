from ast import List, mod
from ctypes import Union
from dotenv import load_dotenv
from typing import List 
from langchain.tools import Tool 
from langchain.agents import tool
from langchain.prompts import PromptTemplate
from langchain.tools.render import render_text_description
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from ollama import Tool
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

print("react langchain")


# decorator of tool , which means the func in converted as a tool with name , desc , result and etc attributes , which the agent can use for validation
@tool
def get_text_length(text:str) ->int:
    """ Return the length of a text by characters"""
    print(f"get_text_length enter with {text}")
    text = text.strip("'\n".strip("'"))
    return len(text)

def find_tool_by_name(tools: List[Tool] , tool_name:str)->Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool with name {tool_name} not found")

# print(get_text_length("David"))
# invoking in below style due to it is a tool , and input should be of dictionary with keyword arguments

tools = [get_text_length]

template = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Instructions:
- If an observation provides the answer to the question, immediately follow with "Thought: I now know the final answer" and "Final Answer: [answer]" without taking further actions.
- Use the scratchpad to review previous steps and avoid repeating unnecessary actions.

Your previous steps (scratchpad):
{agent_scratchpad}

Begin!

Question: {input}
Thought: {thought}
"""

prompt = PromptTemplate.from_template(template=template).partial(tools = render_text_description(tools) , tool_names = ", ".join([t.name for t in tools]))

#render_text_description for converting the output of  tools to string for the input to llm

llm = OllamaLLM(model="llama3.2" , stop=["\nObservation"])# to stop the llm op generation when the observation token is matched


# Using LCEL(Lanchain Expression Language)
# The pipe operator (|) is a shorthand in LCEL to connect components.
# It essentially tells Langchain to send the output of the prompt directly to the llm as input.

#{"input":lambda x:x["input"]}
#The lambda extracts just the "input" value, discarding "extra".

agent = (
    {
        "input": lambda x: x["input"],
        "thought": lambda x: x.get("thought", "I need to calculate the length of the text provided in the question."),
        "agent_scratchpad": lambda x: x.get("agent_scratchpad", "")
    }
    | prompt
    | llm
    | StrOutputParser()
)



def parse_agent_output(output: str):
    lines = output.strip().split("\n")
    action = None
    action_input = None
    for line in lines:
        if line.startswith("Action:"):
            action = line.split(":", 1)[1].strip()
        elif line.startswith("Action Input:"):
            action_input = line.split(":", 1)[1].strip()
    return {"tool": action, "tool_input": action_input}


def run_agent_with_scratchpad(input_question: str, max_iterations: int = 5):
    agent_scratchpad = ""
    thought = "I need to calculate the length of the text provided in the question."
    iteration = 0

    while iteration < max_iterations:
        # Invoke the agent with current input and scratchpad
        agent_output = agent.invoke({
            "input": input_question,
            "thought": thought,
            "agent_scratchpad": agent_scratchpad
        })
        print(f"\nIteration {iteration + 1} Output:")
        print(agent_output)

        # Parse the output
        parsed_output = parse_agent_output(agent_output)

        final_answer = parsed_output.get("final_answer")
        if final_answer:
            print(f"Final Answer Found: {final_answer}")
            return agent_output

        if parsed_output["tool"]:
            tool_name = parsed_output["tool"]
            tool_input = parsed_output["tool_input"]
            tool_to_use = find_tool_by_name(tools, tool_name)
            observation = tool_to_use.func(tool_input)
            print(f"Observation: {observation}")

            # Update scratchpad with the current step
            agent_scratchpad += f"{agent_output}\nObservation: {observation}\n"
            thought = "I should check if this observation answers the question or requires further action."
        else:
            print("No valid action or final answer found. Stopping.")
            break

        iteration += 1

    print("Max iterations reached without a final answer.")
    return agent_scratchpad

input_question = "What is the length of DOG in characters"
result = run_agent_with_scratchpad(input_question)
print("\nFull Agent Execution Result:")
print(result)

