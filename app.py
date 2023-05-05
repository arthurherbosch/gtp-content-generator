import streamlit as st
from streamlit_chat import message
import openai

#hide_menu_style = """
#        <style>
#        #MainMenu {visibility: hidden;}
#        </style>
#        """
#st.markdown(hide_menu_style, unsafe_allow_html=True)
# {"role": "user", "content": "Can you write a script for a video based on a brief? You can use all the information in the brief in order to create a better script. "},
   #     {"role": "user", "content": "Brief: What is nuclear fusion? A video on research, opportunities and challenges.There have been a number of stories around nuclear fusion lately, with more predicted in the future. This would be a 60-second explainer video that we could reuse every time a new story broke (US spelling). Most interesting thing about fusion is how big the potential is in terms of energy output and how benign the waste issue is. Focus on this element rather than explaining how nuclear fusion works. Also mention how it's moved from government-backed research into start-ups, the private sector is getting involved. You can also use this article: ( https://www.ief.org/news/how-close-are-we-to-unlocking-the-limitless-energy-of-nuclear-fusion](https://www.ief.org/news/how-close-are-we-to-unlocking-the-limitless-energy-of-nuclear-fusion )  "},
    #    {"role": "assistant", "content": "Frame 1: Nuclear fusion may be the future of clean, affordable energy. \n Frame 2: Fusion releases nearly four million times more energy than coal, oil, or gas. \n Frame 3: And four times as much as traditional nuclear fission reactors. \n Frame 4: Without producing carbon dioxide or long-lived nuclear waste. \n Frame 5: Elements required for nuclear fusion come from abundant sources: water and lithium. \n Frame 6: Experiments began in the 1930s. \n Frame 7: But creating the right reactor conditions has proven challenging and costly. \n Frame 8: In 2022, US scientists generated more energy from a reaction than was put into it. \n Frame 9: Governments are backing nuclear fusion to solve their mid- and long-term energy needs. \n Frame 10: While private venture capital is funding research in the UK, US and elsewhere. \n Frame 11: Nuclear fusion power is still a long way from being operational and scaled to our needs. \n Frame 12: But a US reactor may be online by 2030 and the UK hopes to connect to the grid in the 2040s."},
       

openai.api_key = st.secrets["APIKEY"]
openai.organization = st.secrets["ORGID"]

def openai_call(prompt):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages= prompt
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

    BASE_PROMPT = [ 
        {"role": "system", "content": "Intelligent write that writes video scripts based of a brief for short videos in a certain style"},
        {"role": "user", "content": "I want you to create video scripts for short videos. We want our video scripts to be in a certain style, so I will provide some examples. You can use those examples to create similar scripts."},
        {"role": "assistant", "content": "Okay, can you provide me with a brief so that I can create a script. "},
        {"role": "user", "content": "Brief: 60-second video about CCUS and how it will help the energy transition? "},
        {"role": "assistant",  "content": "Frame 1: CCUS is a key weapon in the fight against climate change. \n Frame 2: CCUS describes a wide range of technologies that can help us tackle CO2 emissions. \n Frame 3: How does it work? Carbon,   Utilization,  Capture , Storage \n Frame 4: 1.Capture \n Frame 5: CO2 from industry is captured and prevented from entering the atmosphere. \n Frame 6: This is done in power plants and other large-scale industries such as steel mills. \n Frame 7: CO2 is separated from other gases – or even captured from the air using giant fans. \n Frame 8: 2. Utilization. \n Frame 9: After capture, CO2 can be reused – to make fuel, cement, plastics... \n Frame 10: Or even as bubbles in fizzy drinks. \n Frame 11: 3. Storage. \n Frame 12: CO2 can also be injected deep into the ground into porous rock formations – it fills the gaps. \n Frame 13: The same way oils and gases have been trapped underground for millennia. \n Frame 14: Carbon capture innovation can help us speed up on the road to net-zero."},
        {"role": "user", "content": "Brief: What is nuclear fusion? A video on research, opportunities and challenges.There have been a number of stories around nuclear fusion lately, with more predicted in the future. This would be a 60-second explainer video that we could reuse every time a new story broke (US spelling). Most interesting thing about fusion is how big the potential is in terms of energy output and how benign the waste issue is. Focus on this element rather than explaining how nuclear fusion works. Also mention how it's moved from government-backed research into start-ups, the private sector is getting involved. You can also use this article: ( https://www.ief.org/news/how-close-are-we-to-unlocking-the-limitless-energy-of-nuclear-fusion](https://www.ief.org/news/how-close-are-we-to-unlocking-the-limitless-energy-of-nuclear-fusion )  "},
        {"role": "assistant", "content": "Frame 1: Nuclear fusion may be the future of clean, affordable energy. \n Frame 2: Fusion releases nearly four million times more energy than coal, oil, or gas. \n Frame 3: And four times as much as traditional nuclear fission reactors. \n Frame 4: Without producing carbon dioxide or long-lived nuclear waste. \n Frame 5: Elements required for nuclear fusion come from abundant sources: water and lithium. \n Frame 6: Experiments began in the 1930s. \n Frame 7: But creating the right reactor conditions has proven challenging and costly. \n Frame 8: In 2022, US scientists generated more energy from a reaction than was put into it. \n Frame 9: Governments are backing nuclear fusion to solve their mid- and long-term energy needs. \n Frame 10: While private venture capital is funding research in the UK, US and elsewhere. \n Frame 11: Nuclear fusion power is still a long way from being operational and scaled to our needs. \n Frame 12: But a US reactor may be online by 2030 and the UK hopes to connect to the grid in the 2040s."},
        {"role": "user", "content": "A video that explains 3 reasons LNG will be a key part of the future energy mix. Use this information as extra. 1. In 2020, the global Liquefied Natural Gas (LNG) market size was US$ 135420 million and it is expected to reach US$ 205280 million by the end of 2027, with a CAGR of 5.7% during 2021-2027 https://www.globenewswire.com/en/news-release/2022/05/23/2448545/0/en/Global-Liquefied-Natural-Gas-LNG-Market-Size-2022-Growing-Rapidly-with-Recent-Developments-Industry-Share-Trends-Demand-Revenue-Key-Findings-Latest-Technology-Industry-Expansion-St.html . 2. Easy to transport and store than piped natural gas: Means it can be globally traded and is more flexible. 3. Relatively low carbon. 4. Safer and more energy dense than piped gas. \n Topical with new facilities being built. Make this one evergreen. People don't realise how cold you have to make it, temperature issues. Get physics bits in there (cooling etc.).  "},
        {"role": "assistant",   "content": "Frame 1: LNG will be a key part of the future energy mix. Here’s why \n Frame 2: The global Liquefied Natural Gas (LNG) market topped US$135 billion in 2020 \n Source: Industry Research \n Frame 3: And it is expected to reach US$200 billion by the end of 2027 \n Source: Industry Research \n Frame 4: Produced by compressing and cooling natural gas to -162°C… \n Frame 5: And shipped around the world in super-cooled tankers \n Frame 6: LNG has created a truly global market for gas \n Frame 7: Unlocking previously stranded reserves \n Frame 8: Providing energy wherever it is needed most \n Frame 9: LNG has come into its own this century \n Frame 10: Building resilience into energy systems \n Frame 11: Driving down the carbon footprint of the power sector \n Frame 12: And supporting economic growth worldwide"},
       
        ]

    if "messages" not in st.session_state:
        st.session_state["messages"] = BASE_PROMPT

    prompt = st.text_area("Prompt", placeholder="Give me the brief baby")

    if st.button("Send", key="send"):
        with st.spinner("Let me do my thing"):
            st.session_state["messages"] += [{"role": "user", "content": prompt}]
            response = openai_call(st.session_state["messages"])
            message_response = response["choices"][0]["message"]["content"]
            st.session_state["messages"] += [{"role": "assistant", "content": message_response}]
 

    for i in range(len(st.session_state["messages"])-1,-1,-1):
        if st.session_state["messages"][i]['role'] == 'user':
            message(st.session_state["messages"][i]['content'], is_user=True)
        if st.session_state["messages"][i]['role'] == 'assistant':
            message(st.session_state["messages"][i]['content'], avatar_style="bottts-neutral", seed='Aneka')
