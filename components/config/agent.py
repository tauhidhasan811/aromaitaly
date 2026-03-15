from components.config.openai_model import LoadGPT
from langchain.agents import create_agent
from components.asset.beds24 import GetRoomInformation
from components.core.rag_prompt import RAGPrompt

tools = [GetRoomInformation]
llm = LoadGPT()
prompt = RAGPrompt()

def CreateAgent():
    return create_agent(
        model=llm,
        # tools=tools,
        system_prompt=prompt
    )