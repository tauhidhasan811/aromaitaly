from langchain.messages import SystemMessage, HumanMessage
from langchain_core.prompts import PromptTemplate

def RAGPrompt(user_query, relevant_information):
    sys_message = SystemMessage(
        content="""You are a special RAG AI assistant. Your task is to assist the user based on their request and the relevant information provided.
                    Do not hallucinate. If you do not find information, say sorry and suggest contacting customer support.
                    Joy Beach Villas’ Email: reception@joybeachvillas.com
                    Joy Beach Villas’ WhatsApp: +66 62 4080324 (Reception is available from 8 AM to 5 PM Thailand time.)"""
    )

    hum_message = HumanMessage(
        content=f"User Query: {user_query}\n\nRelevant Information: {relevant_information}"
    )

    temp = PromptTemplate(
        template="System Message: {sys_message}\n\nHuman Message: {hum_message}",
        input_variables=["sys_message", "hum_message"]
    )

    prompt = temp.format(
        sys_message=sys_message.content,
        hum_message=hum_message.content
    )

    return prompt