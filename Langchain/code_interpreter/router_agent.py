from typing import Any

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_ollama import OllamaLLM
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain_experimental.tools import PythonREPLTool
from langchain_experimental.agents.agent_toolkits import create_csv_agent

load_dotenv()

def main():
    print("Start...")

    # Python Agent Instructions
    python_instructions = """
        You are an agent designed to write and execute Python code to answer questions using the ReAct framework.
        You have access to the following tools: {tool_names}.
        Tool descriptions: {tools}

        To solve the user's request, follow these steps:
        1. **Thought**: Explain your reasoning step-by-step about how to approach the problem.
        2. **Action**: Use the `PythonREPLTool` by specifying `Action: PythonREPLTool` followed by the Python code in triple backticks (```python ... ```).
        3. **Observation**: The tool will execute the code and return the output (handled automatically).
        4. Provide your final answer based on the code output in the format: ```FINAL ANSWER: <your_answer>```

        Important:
        - Always include 'Thought:', 'Action:', and the final answer in the specified format.
        - Use the `PythonREPLTool` to execute code.
        - Wrap the final answer exactly as: ```FINAL ANSWER: <your_answer>```

        User Input: {input}
        Agent Scratchpad: {agent_scratchpad}
        """

    python_prompt = PromptTemplate(
        template=python_instructions,
        input_variables=["input", "tool_names", "tools", "agent_scratchpad"]
    )

    ollama_llm = OllamaLLM(model="llama3.2")

    # Define tools for Python Agent
    python_tools = [PythonREPLTool()]
    python_agent = create_react_agent(
        prompt=python_prompt,
        llm=ollama_llm,
        tools=python_tools,
    )
    python_agent_executor = AgentExecutor(agent=python_agent, tools=python_tools, verbose=True)

    # CSV Agent
    csv_agent = create_csv_agent(
        llm=ollama_llm,
        path="C:/Users/david.doggala/OneDrive - ascendion/Desktop/Langchain/code_interpreter/episode_info.csv",
        verbose=True,
        allow_dangerous_code=True,
    )

    ################################ Router Grand Agent ########################################################

    def python_agent_executor_wrapper(original_prompt: str) -> dict[str, Any]:
        return python_agent_executor.invoke({"input": original_prompt})

    # Tools for Grand Agent
    grand_tools = [
        Tool(
            name="Python Agent",
            func=python_agent_executor_wrapper,
            description="""useful when you need to transform natural language to python and execute the python code,
                          returning the results of the code execution
                          DOES NOT ACCEPT CODE AS INPUT""",
        ),
        Tool(
            name="CSV Agent",
            func=csv_agent.invoke,
            description="""useful when you need to answer questions over episode_info.csv file,
                         takes an input the entire question as a string and returns the answer after running pandas calculations""",
        ),
    ]

    # Refined Grand Agent Instructions
    grand_instructions = """
        You are a grand agent designed to route user requests to the appropriate tool and provide answers.
        You have access to the following tools: {tool_names}.
        Tool descriptions: {tools}

        To solve the user's request, follow these steps:
        1. **Thought**: Explain your reasoning step-by-step about which tool to use and why.
        2. **Action**: Write `Action: <tool_name>` (e.g., `Action: CSV Agent`), followed by the exact input string 
           for the tool in triple backticks (```<input string>```). The input string must be plain text matching 
           the user's request, NOT Python code, dictionaries, or executable commands. The tool will handle execution.
        3. **Observation**: The tool will process the input and return the output (handled automatically).
        4. Provide your final answer based on the tool's output in the format: ```FINAL ANSWER: <your_answer>```

        Examples:
        User Input: "which season has the most episodes?"
        Thought: This is a question about episode data, so I will use the CSV Agent.
        Action: CSV Agent
        ```which season has the most episodes?```
        Observation: [tool output]
        ```FINAL ANSWER: Season 3```

        User Input: "Generate 15 QR codes"
        Thought: This requires generating Python code, so I will use the Python Agent.
        Action: Python Agent
        ```Generate 15 QR codes```
        Observation: [tool output]
        ```FINAL ANSWER: 15 QR codes generated```

        Important:
        - Do NOT include Python code, dictionaries, or extra parameters in the triple backticks after `Action:`.
        - The input in triple backticks must be a plain text string that the tool can process directly.

        User Input: {input}
        Agent Scratchpad: {agent_scratchpad}
        """

    grand_prompt = PromptTemplate(
        template=grand_instructions,
        input_variables=["input", "tool_names", "tools", "agent_scratchpad"]
    )

    grand_agent = create_react_agent(
        prompt=grand_prompt,
        llm=ollama_llm,
        tools=grand_tools,
    )
    grand_agent_executor = AgentExecutor(
        agent=grand_agent,
        tools=grand_tools,
        verbose=True,
        handle_parsing_errors=True  # Allow the agent to retry on parsing errors
    )

    # Test the Grand Agent
    print(
        grand_agent_executor.invoke(
            {
                "input": "which season has the most episodes?",
            }
        )
    )

    print(
        grand_agent_executor.invoke(
            {
                "input": "Write a python code to print the natural numbers till n",
            }
        )
    )

if __name__ == "__main__":
    main()