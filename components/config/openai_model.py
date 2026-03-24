from langchain_openai import ChatOpenAI
from components.asset.avaiabality_tools import check_availability

def LoadGPT(model_name='gpt-4.1-2025-04-14'):
    llm = ChatOpenAI(
        model=model_name,
        temperature=0.0
    )

    llm_with_tool = llm.bind_tools([check_availability])
    return llm_with_tool