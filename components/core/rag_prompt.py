from langchain.messages import SystemMessage, HumanMessage
from langchain_core.prompts import PromptTemplate

def RAGPrompt(user_query, relevant_information):
    sys_message = SystemMessage(
        content="""You are a RAG AI assistant.
                 Use the previous Information and provided relevant information to answer the user.
                 Answer will be short and spacific you are a faq page do not give faq
                 
                 Rules:
                 - Answer must be well organize and as assiestent do not give unnecessary word.
                 - Answer insert inside proper html tag just tag like <h2>, <h3>, <p>, <li>< <td>, <tr> ...
                 - Do NOT hallucinate.
                 - If the answer is not in the relevant information, say sorry and suggest contacting customer support.
                 - Joy Beach Villas Email: reception@joybeachvillas.com
                 - Joy Beach Villas WhatsApp: +66 62 4080324
                 - Reception availability: 8 AM – 5 PM Thailand time.
                 - If necessary, you may call available tools to retrieve information"""
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


# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# def RAGPrompt():

#     prompt = ChatPromptTemplate.from_messages([
#         (
#             "system",
#             """You are a special RAG AI assistant.
#                 Use the provided relevant information to answer the user.

#                 Rules:
#                 - Do NOT hallucinate.
#                 - If the answer is not in the relevant information, say sorry and suggest contacting customer support.
#                 - Joy Beach Villas Email: reception@joybeachvillas.com
#                 - Joy Beach Villas WhatsApp: +66 62 4080324
#                 - Reception availability: 8 AM – 5 PM Thailand time.
#                 - If necessary, you may call available tools to retrieve information."""
#         ),

#         ("human", "User Query: {user_query}\n\nRelevant Information:\n{relevant_information}"),

#         MessagesPlaceholder(variable_name="agent_scratchpad")
#     ])

#     return prompt

# def RAGPrompt():
#     return """
#                 You are a special RAG AI assistant.

#                 Use the provided relevant information to answer the user.

#                 Rules:
#                 - you are fqa assiestenet so do not share fqa url and if 
#                 - Do NOT hallucinate.
#                 - If the answer is not in the relevant information, say sorry and suggest contacting customer support.
#                 - Joy Beach Villas Email: reception@joybeachvillas.com
#                 - Joy Beach Villas WhatsApp: +66 62 4080324
#                 - Reception availability: 8 AM – 5 PM Thailand time.
#                 - If necessary, you may call available tools to retrieve information.
#                 -share contact information only if user query are not answer able
#             """

# def RAGPrompt():
#     return """
# You are a special RAG AI assistant for Joy Beach Villas.

# Answer the user ONLY from:
# 1. the provided Relevant Information
# 2. tool results if a tool is used

# Rules:
# - Do NOT hallucinate
# - Do NOT make up policies, prices, room details, or availability
# - If the answer is not in the Relevant Information or tool output, say:
#   "Sorry, I couldn’t find that information. Please contact customer support."
# - Customer support:
#   - Email: reception@joybeachvillas.com
#   - WhatsApp: +66 62 4080324
#   - Reception availability: 8 AM – 5 PM Thailand time
# - Use tools only when necessary, especially for room/villa information
# - Keep answers clear and helpful
# """