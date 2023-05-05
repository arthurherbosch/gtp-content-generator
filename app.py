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
openai.organization = st.secrets["ORGID"]

def openai_call():
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are an intelligent writer that writes video scripts for short videos."},
        {"role": "user", "content": "Brief: A 60-second video about CCUS and how it will help the energy transition? "},
        {"role": "assistant",   "content": "Frame 1: CCUS is a key weapon in the fight against climate change. \n Frame 2: CCUS describes a wide range of technologies that can help us tackle CO2 emissions. \n Frame 3: How does it work? Carbon,   Utilization,  Capture , Storage \n Frame 4: 1.Capture \n Frame 5: CO2 from industry is captured and prevented from entering the atmosphere. \n Frame 6: This is done in power plants and other large-scale industries such as steel mills. \n Frame 7: CO2 is separated from other gases – or even captured from the air using giant fans. \n Frame 8: 2. Utilization. \n Frame 9: After capture, CO2 can be reused – to make fuel, cement, plastics... \n Frame 10: Or even as bubbles in fizzy drinks. \n Frame 11: 3. Storage. \n Frame 12: CO2 can also be injected deep into the ground into porous rock formations – it fills the gaps. \n Frame 13: The same way oils and gases have been trapped underground for millennia. \n Frame 14: Carbon capture innovation can help us speed up on the road to net-zero."},
        {"role": "user", "content": "Can you write a script for a video based on a brief? You can use all the information in the brief in order to create a better script. "},
        {"role": "user", "content": "Brief: What is nuclear fusion? A video on research, opportunities and challenges.There have been a number of stories around nuclear fusion lately, with more predicted in the future. This would be a 60-second explainer video that we could reuse every time a new story broke (US spelling). Most interesting thing about fusion is how big the potential is in terms of energy output and how benign the waste issue is. Focus on this element rather than explaining how nuclear fusion works. Also mention how it's moved from government-backed research into start-ups, the private sector is getting involved. You can also use this article: ( https://www.ief.org/news/how-close-are-we-to-unlocking-the-limitless-energy-of-nuclear-fusion](https://www.ief.org/news/how-close-are-we-to-unlocking-the-limitless-energy-of-nuclear-fusion )  "},
        {"role": "assistant", "content": "Frame 1: Nuclear fusion may be the future of clean, affordable energy. \n Frame 2: Fusion releases nearly four million times more energy than coal, oil, or gas. \n Frame 3: And four times as much as traditional nuclear fission reactors. \n Frame 4: Without producing carbon dioxide or long-lived nuclear waste. \n Frame 5: Elements required for nuclear fusion come from abundant sources: water and lithium. \n Frame 6: Experiments began in the 1930s. \n Frame 7: But creating the right reactor conditions has proven challenging and costly. \n Frame 8: In 2022, US scientists generated more energy from a reaction than was put into it. \n Frame 9: Governments are backing nuclear fusion to solve their mid- and long-term energy needs. \n Frame 10: While private venture capital is funding research in the UK, US and elsewhere. \n Frame 11: Nuclear fusion power is still a long way from being operational and scaled to our needs. \n Frame 12: But a US reactor may be online by 2030 and the UK hopes to connect to the grid in the 2040s."},
       

        ],
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
    st.title("Intelligent writer for scripts and articles ")

    BASE_PROMPT = [ {"role": "assistant", "content": "Can I help you to create another script? "}]

    if "messages" not in st.session_state:
        st.session_state["messages"] = BASE_PROMPT

    prompt = st.text_area("Prompt", placeholder="Give me the brief baby")

    if st.button("Send", key="send"):
        with st.spinner("Let me do my thing"):
            st.session_state["messages"] += [{"role": "user", "content": prompt}]
            response = openai_call()
            print(response)
            message_response = response["choices"][0]["message"]["content"]
            st.session_state["messages"] += [{"role": "assistant", "content": message_response}]
 

    for i in range(len(st.session_state["messages"])-1,-1,-1):
        if st.session_state["messages"][i]['role'] == 'user':
            message(st.session_state["messages"][i]['content'], is_user=True)
        if st.session_state["messages"][i]['role'] == 'assistant':
            message(st.session_state["messages"][i]['content'], avatar_style="bottts-neutral", seed='Aneka')
