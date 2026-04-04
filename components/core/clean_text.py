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


def SelectedPreviousData(prev_info): 
    split_data = prev_info.split('user_query')
    selected_data = ""
    minimun_stack = 5
    current_stack = 0
    for sp_data in reversed(split_data):
        print('-' * 80)
        sp_data = str(sp_data)
        if len(sp_data) > 0:
            sp_data = "user_query: "+ sp_data
            sp_data = clean_previous_text(sp_data)
        if len(selected_data) < 1000:
            selected_data += sp_data
            print(f"if working && current content len: {len(selected_data)}")
            # print(selected_data)
            current_stack += 1
        elif current_stack < minimun_stack:
            selected_data = sp_data + selected_data
            print(f"elif working && current content len: {len(selected_data)}")

            current_stack += 1
        else:
            break
        # print(sp_data)
        # print(len(sp_data))
        print('-' * 80)

    print(selected_data)
    print(current_stack)

    # print(split_data[0])

    return selected_data
