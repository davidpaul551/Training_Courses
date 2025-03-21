from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from langchain.agents import create_react_agent, AgentExecutor
from langchain_experimental.tools import PythonREPLTool

load_dotenv()

def main():
    print("Start...")

    # Updated prompt with explicit ReAct instructions
    instructions = """
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
    prompt = PromptTemplate(
        template=instructions,
        input_variables=["input", "tool_names", "tools", "agent_scratchpad"]
    )

    # Define tools
    tools = [PythonREPLTool()]

    # Initialize the Ollama LLM
    llm = OllamaLLM(model="llama3.2")

    # Create the ReAct agent
    agent = create_react_agent(
        prompt=prompt,
        llm=llm,
        tools=tools,
    )

    # Create the agent executor with handle_parsing_errors=True
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True  # Handle parsing errors gracefully
    )

    # Invoke the agent with the user input
    result = agent_executor.invoke({
        "input": "Write a python code to print prime numbers and number of prime numbers below n value in two different functions"
    })

    print(result)

if __name__ == "__main__":
    main()