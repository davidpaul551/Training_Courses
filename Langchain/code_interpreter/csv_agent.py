from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_experimental.agents.agent_toolkits import create_csv_agent

load_dotenv()

def main():
    print("Start...")

    ollama_llm = Ollama(model="llama3.2")

    csv_agent = create_csv_agent(
        llm=ollama_llm,
        path="C:/Users/david.doggala/OneDrive - ascendion/Desktop/Langchain/code_interpreter/episode_info.csv",
        verbose=True,
        allow_dangerous_code=True
    )

    csv_agent.invoke({
        "input": "how many columns are there in file episode_info.csv"
    })

    csv_agent.invoke({
        "input": "print the seasons by ascending order of the number of episodes they have"
    })

if __name__ == "__main__":
    main()
