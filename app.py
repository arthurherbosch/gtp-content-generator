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
    model="gpt-4",
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
    type = st.radio(
    "What do you want to create?",
    ('Video Script', 'Article'))

    BASE_PROMPT_VIDEO = [ 
        {"role": "system", "content": "Intelligent writer that writes video scripts based of a brief for short videos in a certain style"},
        {"role": "user", "content": "I want you to create video scripts for short videos. We want our video scripts to be in a certain style, so I will provide some examples. You can use those examples to create similar scripts."},
        {"role": "assistant", "content": "Okay, can you provide me with a brief so that I can create a script. "},
        {"role": "user", "content": "Can you write a video script for a 60-second video about CCUS and how it will help the energy transition? "},
        {"role": "assistant",  "content": "Frame 1: CCUS is a key weapon in the fight against climate change. \n Frame 2: CCUS describes a wide range of technologies that can help us tackle CO2 emissions. \n Frame 3: How does it work? Carbon,   Utilization,  Capture , Storage \n Frame 4: 1.Capture \n Frame 5: CO2 from industry is captured and prevented from entering the atmosphere. \n Frame 6: This is done in power plants and other large-scale industries such as steel mills. \n Frame 7: CO2 is separated from other gases – or even captured from the air using giant fans. \n Frame 8: 2. Utilization. \n Frame 9: After capture, CO2 can be reused – to make fuel, cement, plastics... \n Frame 10: Or even as bubbles in fizzy drinks. \n Frame 11: 3. Storage. \n Frame 12: CO2 can also be injected deep into the ground into porous rock formations – it fills the gaps. \n Frame 13: The same way oils and gases have been trapped underground for millennia. \n Frame 14: Carbon capture innovation can help us speed up on the road to net-zero."},
        {"role": "user", "content": "Can you write a video script about what nuclear fusion is? A video on research, opportunities and challenges. There have been a number of stories around nuclear fusion lately, with more predicted in the future. This would be a 60-second explainer video that we could reuse every time a new story broke (US spelling). Most interesting thing about fusion is how big the potential is in terms of energy output and how benign the waste issue is. Focus on this element rather than explaining how nuclear fusion works. Also mention how it's moved from government-backed research into start-ups, the private sector is getting involved. You can also use this article: ( https://www.ief.org/news/how-close-are-we-to-unlocking-the-limitless-energy-of-nuclear-fusion](https://www.ief.org/news/how-close-are-we-to-unlocking-the-limitless-energy-of-nuclear-fusion )  "},
        {"role": "assistant", "content": "Frame 1: Nuclear fusion may be the future of clean, affordable energy. \n Frame 2: Fusion releases nearly four million times more energy than coal, oil, or gas. \n Frame 3: And four times as much as traditional nuclear fission reactors. \n Frame 4: Without producing carbon dioxide or long-lived nuclear waste. \n Frame 5: Elements required for nuclear fusion come from abundant sources: water and lithium. \n Frame 6: Experiments began in the 1930s. \n Frame 7: But creating the right reactor conditions has proven challenging and costly. \n Frame 8: In 2022, US scientists generated more energy from a reaction than was put into it. \n Frame 9: Governments are backing nuclear fusion to solve their mid- and long-term energy needs. \n Frame 10: While private venture capital is funding research in the UK, US and elsewhere. \n Frame 11: Nuclear fusion power is still a long way from being operational and scaled to our needs. \n Frame 12: But a US reactor may be online by 2030 and the UK hopes to connect to the grid in the 2040s."},
        {"role": "user", "content": "Can you write a video script that covers 3 reasons why LNG will be a key part of the future energy mix. Use this information as extra. 1. In 2020, the global Liquefied Natural Gas (LNG) market size was US$ 135420 million and it is expected to reach US$ 205280 million by the end of 2027, with a CAGR of 5.7% during 2021-2027 https://www.globenewswire.com/en/news-release/2022/05/23/2448545/0/en/Global-Liquefied-Natural-Gas-LNG-Market-Size-2022-Growing-Rapidly-with-Recent-Developments-Industry-Share-Trends-Demand-Revenue-Key-Findings-Latest-Technology-Industry-Expansion-St.html . 2. Easy to transport and store than piped natural gas: Means it can be globally traded and is more flexible. 3. Relatively low carbon. 4. Safer and more energy dense than piped gas. \n Topical with new facilities being built. Make this one evergreen. People don't realise how cold you have to make it, temperature issues. Get physics bits in there (cooling etc.).  "},
        {"role": "assistant",   "content": "Frame 1: LNG will be a key part of the future energy mix. Here’s why \n Frame 2: The global Liquefied Natural Gas (LNG) market topped US$135 billion in 2020 \n Source: Industry Research \n Frame 3: And it is expected to reach US$200 billion by the end of 2027 \n Source: Industry Research \n Frame 4: Produced by compressing and cooling natural gas to -162°C… \n Frame 5: And shipped around the world in super-cooled tankers \n Frame 6: LNG has created a truly global market for gas \n Frame 7: Unlocking previously stranded reserves \n Frame 8: Providing energy wherever it is needed most \n Frame 9: LNG has come into its own this century \n Frame 10: Building resilience into energy systems \n Frame 11: Driving down the carbon footprint of the power sector \n Frame 12: And supporting economic growth worldwide"},
        {"role": "user", "content": """Can you write a video script based on a article. This is the article:
         The versatility of natural gas is one key to its expected prominent role in the energy transition, serving as an energy source for all sectors including heating, cooking and industrial applications. When it comes to greenhouse gas emissions, natural gas has a significant advantage over coal, emitting about half the CO2.  This makes it an attractive option for stabilizing the path to renewables while reducing carbon emissions in the short term.  1. Natural gas is a reliable, affordable energy source which enables innovation   The impact of the COVID pandemic as well as of recent extreme weather events has drawn attention to the systemic risks that impact energy security.    In many countries, nuclear power is being phased out or shelved, creating additional need for other technologies to provide a reliable baseload. Natural gas, as an easy to store, lower-carbon option, stands out as a good candidate to provide an uninterrupted, flexible energy supply in tandem with intermittent output from wind and solar while storage technologies are scaled up and innovative new energy pathways are explored.  In a 2019 report, the United Nations Economic Commission for Europe (UNECE) said that the ability of natural gas to provide a relatively low carbon backup at peak energy usage times, rather than play a traditional role of round-the-clock baseload, may prove to be its greatest contribution to the energy transition.   

        2. It acts as a bridging ingredient in the hydrogen revolution  

        Natural gas is also frequently cited as a driver of the energy transition because of its central role in the scaling up (production and transport) of hydrogen – which the European Union, among others, has predicted will play a key role in a future climate-neutral economy.   


        The EU’s hydrogen policy notes that although the cost of producing ‘clean hydrogen’ (made entirely using renewable electricity) is falling, it remains comparatively high. The EU strategy envisions the development of ‘clean hydrogen’ as a gradual trajectory, initially including ‘hydrogen’ from natural gas.  

        3. It is a key tool in the fight against energy poverty  

        Although great progress has been made in ensuring access to electricity globally, in the Global South, over 700 million people remain cut off from electric power and clean cooking technologies. Almost 600 million of them live in Africa – and the continent accounts for less than 4 percent of annual global carbon emissions. Although renewable energy capacity is expanding rapidly, the technology faces challenges. For example, Kenya, which is home to the continent’s largest wind farm, is achieving only around 15 percent of installed capacity from wind and solar.    

        Natural gas is a plentiful and valuable resource for countries from Algeria and Egypt to Ghana, Senegal and Mozambique. According to a report by the United Nations Economic Commission for Africa, the continent’s traditional reliance on biomass, coal and oil means that a combination of renewables and other cleaner fuels such as natural gas is important in fast-tracking the energy transition.  

        4. Along with Carbon Capture and Storage, it can transform the energy sector    

        In the short to medium term, and in conjunction with renewables and carbon capture, utilization, and storage (CCUS), new natural gas developments can complement the decarbonization of the energy sector.  

        According to the UNECE report, carbon capture, use and storage offers a real prospect for natural gas to work with renewable energy sources on decarbonization. In particular, it helps to address the problem of how to cope with hard-to-abate emissions from heavy industry, notably steel, cement and petrochemicals.  

        Scaling up of CCUS will be critical, given the scale and urgency of the decarbonization challenge – not only with respect to electricity generation, but also heating. An IHS Markit study illustrates how far the world is from electrification of heating – for instance, New York City’s power system has 31GW total capacity, but would require 150GW capacity to electrify heating (133GW, with full deployment of heat pumps). Natural gas is unlikely, then, to be phased out in the near term, but will continue to play a role in the hydrogen production, in combination with accelerated deployment of CCUS until hydrogen produced from renewables or nuclear is economically viable as a fuel for heating.   


        Natural gas can contribute to climate targets, and serves as a bridge to overcome technology gaps.  

        In a report published earlier this year, the G20 observed that natural gas meets a considerable share of seasonal energy demand in many countries, offering resilience and security of supply in the face of adverse weather and volatile markets. In addition to this short-term role, the group suggested that an extensive roll-out of CCUS technology and hydrogen production in the longer term would enable natural gas to align with a net-zero pathway.
        """},
        {"role": "assistant",   "content": "Frame 1: Natural gas has a crucial role to play in the energy transition. Here’s how \n Frame 2: Natural gas is affordable, reliable and easy to store\nFrame 3: And it emits up to 50% less greenhouse gases than coal\nFrame 4: Here are 4 ways natural gas is helping power the energy transition\nFrame 5: 1. It offers a reliable low-carbon back-up for peak energy demand\nFrame 6: Providing a stable energy supply while renewable technologies grow\nFrame 7: 2. It acts as a bridging ingredient in the hydrogen energy revolution\nFrame 8: Hydrogen from renewables will play a key role in our climate-neutral future\nFrame 9: For now, the path to cleaner hydrogen relies on natural gas\nFrame 10: 3. It helps fight energy poverty\nFrame 11: In Africa, 600 million people still don’t have access to electricity or clean cooking\nFrame 12: Alongside renewables, natural gas can help fast-track the energy transition\nFrame 13: Combined with carbon capture and storage, it can transform the energy sector\nFrame 14: Thanks to carbon capture technology, we can reduce the emissions from natural gas processing\nFrame 15: Helping reduce hard-to-abate emissions from heavy industry like steel and cement"},

        ]
    
    BASE_PROMPT_ARTICLES = [
          {"role": "system", "content": "Intelligent writer that writes articles in a particular style"},
        {"role": "user", "content": "I want you to writes articles on certain topics. We want our acrticles to be in a certain style, so I will provide some examples. You can use those examples to create similar articles."},
    ]

    if "messages" not in st.session_state:
        if type == 'Video Script':
            st.session_state["script_messages"] = BASE_PROMPT_VIDEO
        elif  type == 'Article':
            st.session_state["article_messages"] = BASE_PROMPT_ARTICLES
        else:
            st.write('Make a choice between article or video script')

    prompt = st.text_area("Prompt", placeholder="Give me the brief baby")

    if st.button("Send", key="send"):
        with st.spinner("Let me do my thing"):
            if type == 'Video Script':
                st.session_state["script_messages"] += [{"role": "user", "content": prompt}]
                response = openai_call(st.session_state["script_messages"])
                message_response = response["choices"][0]["script_messages"]["content"]
                st.session_state["script_messages"] += [{"role": "assistant", "content": message_response}]
            elif type == 'Article':
                st.session_state["article_messages"] += [{"role": "user", "content": prompt}]
                response = openai_call(st.session_state["article_messages"])
                message_response = response["choices"][0]["article_messages"]["content"]
                st.session_state["article_messages"] += [{"role": "assistant", "content": message_response}]
    
    if type == 'Video Script':
        for i in range(len(st.session_state["script_messages"])-1,-1,-1):
            if st.session_state["script_messages"][i]['role'] == 'user':
                message(st.session_state["script_messages"][i]['content'], is_user=True)
            if st.session_state["script_messages"][i]['role'] == 'assistant':
                message(st.session_state["script_messages"][i]['content'], avatar_style="bottts-neutral", seed='Aneka')
    elif type == 'Article':
        for i in range(len(st.session_state["article_messages"])-1,-1,-1):
            if st.session_state["article_messages"][i]['role'] == 'user':
                message(st.session_state["article_messages"][i]['content'], is_user=True)
            if st.session_state["article_messages"][i]['role'] == 'assistant':
                message(st.session_state["article_messages"][i]['content'], avatar_style="bottts-neutral", seed='Aneka')
