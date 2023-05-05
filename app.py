import streamlit as st
from streamlit_chat import message
import openai

#hide_menu_style = """
#        <style>
#        #MainMenu {visibility: hidden;}
#        </style>
#        """
#st.markdown(hide_menu_style, unsafe_allow_html=True)

openai.api_key = st.secrets["APIKEY"]

def openai_call(prompt):
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=prompt,
    )
    return response


def check_password():
    def password_entered():
        """Check whether correct password entered by user"""
        if st.session_state["password"] == st.secrets["PASSWORD"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        return True
        

if check_password():
    st.title("TCE GPT4 demo app")

    BASE_PROMPT = [{"role": "system", "content": "You are a helpful assistant."}]

    if "messages" not in st.session_state:
        st.session_state["messages"] = BASE_PROMPT

    prompt = st.text_area("Prompt", placeholder="What do you want to know baby?")

    if st.button("Send", key="send"):
        with st.spinner("BEEP BOOOP BEEP BOOP..."):
            st.session_state["messages"] += [{"role": "user", "content": prompt}]
            response = openai_call(st.session_state["messages"])
            message_response = response["choices"][0]["message"]["content"]
            st.session_state["messages"] += [{"role": "assistant", "content": message_response}]
    
    if st.button("Clear", key="clear"):
        st.session_state["messages"] = BASE_PROMPT

    for i in range(len(st.session_state["messages"])-1,-1,-1):
        if st.session_state["messages"][i]['role'] == 'user':
            message(st.session_state["messages"][i]['content'], is_user=True)
        if st.session_state["messages"][i]['role'] == 'assistant':
            message(st.session_state["messages"][i]['content'], avatar_style="bottts-neutral", seed='Aneka')
