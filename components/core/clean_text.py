import re
from html import unescape

def clean_previous_text(text):
    # Decode HTML entities (like &amp;, &nbsp;)
    text = unescape(text)
    
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


# def SelectedPreviousData(prev_info): 
#     split_data = prev_info.split('user_query')
#     selected_data = ""
#     minimun_stack = 20
#     current_stack = 0
#     for sp_data in reversed(split_data):
#         print('-' * 80)
#         sp_data = str(sp_data)
#         if len(sp_data) > 0:
#             sp_data = "user_query: "+ sp_data
#             sp_data = clean_previous_text(sp_data)
#         if len(selected_data) < 2000:
#             selected_data += sp_data
#             print(f"if working && current content len: {len(selected_data)}")
#             # print(selected_data)
#             current_stack += 1
#         elif current_stack < minimun_stack:
#             selected_data = sp_data + selected_data
#             print(f"elif working && current content len: {len(selected_data)}")

#             current_stack += 1
#         else:
#             break
#         # print(sp_data)
#         # print(len(sp_data))
#         print('-' * 80)

#     print(selected_data)
#     print(current_stack)

#     # print(split_data[0])

#     return selected_data

def SelectedPreviousData(prev_info: str) -> str:
    """
    Returns the most recent conversation turns, newest-first,
    trimmed to stay under 2000 characters but always keeping
    at least the last 20 turns.
    """
    split_data = prev_info.split('user_query')
    
    # Build turns cleanly, most recent first
    turns = []
    for sp_data in reversed(split_data):
        sp_data = sp_data.strip()
        if sp_data:
            turns.append("user_query: " + clean_previous_text(sp_data))

    selected_parts = []
    total_len = 0
    MIN_TURNS = 20

    for i, turn in enumerate(turns):
        # Always include minimum turns; after that, stop if over budget
        if i >= MIN_TURNS and total_len + len(turn) > 2000:
            break
        selected_parts.append(turn)
        total_len += len(turn)

    # Reverse back so oldest→newest order for the LLM
    selected_parts.reverse()
    
    result = "\n".join(selected_parts)
    print(f"Selected {len(selected_parts)} turns, {total_len} chars")
    return result
