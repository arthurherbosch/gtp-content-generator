import streamlit as st
from streamlit_chat import message
import openai
import streamlit as st
import oneai
import requests
#hide_menu_style = """
#        <style>
#        #MainMenu {visibility: hidden;}
#        </style>
#        """
#st.markdown(hide_menu_style, unsafe_allow_html=True)
# {"role": "user", "content": "Can you write a script for a video based on a brief? You can use all the information in the brief in order to create a better script. "},
   #     {"role": "user", "content": "Brief: What is nuclear fusion? A video on research, opportunities and challenges.There have been a number of stories around nuclear fusion lately, with more predicted in the future. This would be a 60-second explainer video that we could reuse every time a new story broke (US spelling). Most interesting thing about fusion is how big the potential is in terms of energy output and how benign the waste issue is. Focus on this element rather than explaining how nuclear fusion works. Also mention how it's moved from government-backed research into start-ups, the private sector is getting involved. You can also use this article: ( https://www.ief.org/news/how-close-are-we-to-unlocking-the-limitless-energy-of-nuclear-fusion](https://www.ief.org/news/how-close-are-we-to-unlocking-the-limitless-energy-of-nuclear-fusion )  "},
    #    {"role": "assistant", "content": "Frame 1: Nuclear fusion may be the future of clean, affordable energy. \n Frame 2: Fusion releases nearly four million times more energy than coal, oil, or gas. \n Frame 3: And four times as much as traditional nuclear fission reactors. \n Frame 4: Without producing carbon dioxide or long-lived nuclear waste. \n Frame 5: Elements required for nuclear fusion come from abundant sources: water and lithium. \n Frame 6: Experiments began in the 1930s. \n Frame 7: But creating the right reactor conditions has proven challenging and costly. \n Frame 8: In 2022, US scientists generated more energy from a reaction than was put into it. \n Frame 9: Governments are backing nuclear fusion to solve their mid- and long-term energy needs. \n Frame 10: While private venture capital is funding research in the UK, US and elsewhere. \n Frame 11: Nuclear fusion power is still a long way from being operational and scaled to our needs. \n Frame 12: But a US reactor may be online by 2030 and the UK hopes to connect to the grid in the 2040s."},
    #test

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
        
def get_article(article_url):
    url = "https://api.oneai.com/api/v0/pipeline"
    headers = {
        "api-key" : "a97ed467-e7f9-4662-8ba9-63b6cd8f3bcb",
        "content-type" : "application/json"
    }

    payload = {
        "input" : article_url,
        "input_type" : "article",
        "steps": [
            {
                "skill": "html-extract-article"
            }
        ],
    }
    r = requests.post(url, json=payload, headers=headers)
    data = r.json()
    return(data['input_text'])

def video_script_generator():
        video_len = st.slider('How long should the video be?', 0, 180, 60, step = 15)
        st.write("Video has to be around ", video_len, 'seconds')
        end_prompt = " "

        type_vid = st.selectbox(
        'What type of video?',
        ('hype ', 'explainer', 'animation'))
        brief = st.text_area("Brief", placeholder="A video on a trend that's cropping up on the newswires - matching training to the time of your cycle. \n The US women’s soccer team coach partly attributes their 2019 World Cup win to cycle synching, and UK club Chelsea (which has Matildas skipper Sam Kerr on the team) tailor all their training to the players’ periods.  \n Content to mention that you don't have to be an athlete to benefit from cycle synching ", help="Make sure to provide a detailed brief that includes all the information needed to create a quality scripts. You can put in articles for reference or put in sources. Tell the script what the focus should be, this will create better results. **The better the brief, the better the script**")
        articles = st.text_area("Sources", placeholder="Link articles here. Put a link on every new line. \n\n https://www.example.com/ \n https://www.example.com/ ")
        
        if st.button("Create script", key ='send'):
            with st.spinner("Let me do my thing..."):
                articles_list = articles.split('\n')
                article_string = ""
                counter = 1
                if len(articles) != 0:
                    for article in articles_list:
                        try:
                            result  = get_article(article)
                        except:
                            result = " "
                        article_string += f"Article  {counter}: \n{result} \n\n ## \n\n" 
                        counter += 1
                end_prompt = f"Create a video script for a {video_len}-seconds {type_vid}. \n \nTopic: {video_title} \n\n Brief: {brief} \n\n\n You can use these articles/texts:\n{article_string} "
                st.session_state["script_messages"] += [{"role": "user", "content": end_prompt}]
                response = openai_call(st.session_state["script_messages"])
                message_response = response["choices"][0]["message"]["content"]
                st.session_state["script_messages"] += [{"role": "assistant", "content": message_response}]
    
        prompt = st.text_area("Make adjustments (After **Create Script** )", placeholder = "Can you make the script shorter?", help='You can ask the writer to make some adjustments to the created script. Just write down the things you want to change and press **change**.')
        
        if st.button("Clear", key="clear"):
            st.session_state["script_messages"] = BASE_PROMPT_VIDEO
            st.write(st.session_state)
            
        if st.button("Change", key = 'change'):
            with st.spinner("Let me make some adjustments..."):
                st.session_state["script_messages"] += [{"role": "user", "content": prompt}]
                response = openai_call(st.session_state["script_messages"])
                message_response = response["choices"][0]["message"]["content"]
                st.session_state["script_messages"] += [{"role": "assistant", "content": message_response}]
                    
        for i in range(len(st.session_state["script_messages"])-1, 10, -1):
            if st.session_state["script_messages"][i]['role'] == 'user':
                message(st.session_state["script_messages"][i]['content'], is_user=True)
            if st.session_state["script_messages"][i]['role'] == 'assistant':
                message(st.session_state["script_messages"][i]['content'], avatar_style="bottts-neutral", seed='Aneka')
                   
def article_generator():
    if type == "Article":
        words = st.slider('Around how many words do you want in the article? ', 0, 1000, 600, step = 50)
        st.write("Article will be around ", words, 'words')
        brief = st.text_area("Brief", placeholder="Write an article about nuclear fusion.")
        articles = st.text_area("Sources", placeholder="Link articles here. Put a link on every new line. \n\n https://www.example.com/ \n https://www.example.com/ ")

        if st.button("Create", key ='send'):
            with st.spinner("Let me do my thing..."):
                articles_list = articles.split('\n')
                article_string = ""
                counter = 1
                if len(articles) != 0:
                    for article in articles_list:
                        try:
                            result  = get_article(article)
                        except:
                            result = " "
                        article_string += f"Article {counter}: \n{result} \n\n ## \n\n" 
                        counter += 1
                        
                end_prompt =f"Create a {words}-word article. \n\n Topic: {video_title} \n\n Brief: {brief} \n\n\n You can use these articles/texts:\n{article_string}" 

                st.session_state["article_messages"] += [{"role": "user", "content": end_prompt}]
                response = openai_call(st.session_state["article_messages"])
                message_response = response["choices"][0]["message"]["content"]
                st.session_state["article_messages"] += [{"role": "assistant", "content": message_response}]
        
        prompt = st.text_area("Make adjustments (After **Create Article** )", placeholder = "Can you make the article shorter?")
        
        if st.button("Change", key = 'change'):
            with st.spinner("Let me make some adjustments..."):
                st.session_state["article_messages"] += [{"role": "user", "content": prompt}]
                response = openai_call(st.session_state["article_messages"])
                message_response = response["choices"][0]["message"]["content"]
                st.session_state["article_messages"] += [{"role": "assistant", "content": message_response}]
        
        if st.button("Clear", key="clear"):
            st.session_state["article_messages"] = BASE_PROMPT_ARTICLES
            
        for i in range(len(st.session_state["article_messages"])-1, 8, -1):
            if st.session_state["article_messages"][i]['role'] == 'user':
                message(st.session_state["article_messages"][i]['content'], is_user=True)
            if st.session_state["article_messages"][i]['role'] == 'assistant':
                message(st.session_state["article_messages"][i]['content'], avatar_style="bottts-neutral", seed='Aneka')
              
if check_password():
    st.title("Content Engine Digital Writer V1")
    type = st.radio(
    "What do you want to create?",
    ('Video Script', 'Article'))

    video_title = st.text_input("Video Title", placeholder="What is cycle synching?")
    
    BASE_PROMPT_VIDEO = [ 
    {"role": "system", "content": "Intelligent writer that writes video scripts based of a brief for short videos in a certain style"},
    {"role": "user", "content": "I want you to create video scripts for short videos. We want our video scripts to be in a certain style, so I will provide some examples. You can use those examples to create similar scripts."},
    {"role": "assistant", "content": "Okay, can you provide me with a brief so that I can create a script. "},
    {"role": "user", "content": "Create a video script for a 60-second explainer video. \n\n Topic: What is CCUS? \n\n Brief: A video about CCUS and how it will help the energy transition? "},
    {"role": "assistant",  "content": "Frame 1: CCUS is a key weapon in the fight against climate change. \n Frame 2: CCUS describes a wide range of technologies that can help us tackle CO2 emissions. \n Frame 3: How does it work? Carbon,   Utilization,  Capture , Storage \n Frame 4: 1.Capture \n Frame 5: CO2 from industry is captured and prevented from entering the atmosphere. \n Frame 6: This is done in power plants and other large-scale industries such as steel mills. \n Frame 7: CO2 is separated from other gases – or even captured from the air using giant fans. \n Frame 8: 2. Utilization. \n Frame 9: After capture, CO2 can be reused – to make fuel, cement, plastics... \n Frame 10: Or even as bubbles in fizzy drinks. \n Frame 11: 3. Storage. \n Frame 12: CO2 can also be injected deep into the ground into porous rock formations – it fills the gaps. \n Frame 13: The same way oils and gases have been trapped underground for millennia. \n Frame 14: Carbon capture innovation can help us speed up on the road to net-zero."},
    {"role": "user", "content": "Create a video script for a 60-second explainer video. \n\n Topic: What is nuclear fusion? \n\n Brief: A video on research, opportunities and challenges. There have been a number of stories around nuclear fusion lately, with more predicted in the future. This would be a 60-second explainer video that we could reuse every time a new story broke (US spelling). Most interesting thing about fusion is how big the potential is in terms of energy output and how benign the waste issue is. Focus on this element rather than explaining how nuclear fusion works. Also mention how it's moved from government-backed research into start-ups, the private sector is getting involved. You can also use this article: ( https://www.ief.org/news/how-close-are-we-to-unlocking-the-limitless-energy-of-nuclear-fusion](https://www.ief.org/news/how-close-are-we-to-unlocking-the-limitless-energy-of-nuclear-fusion )  "},
    {"role": "assistant", "content": "Frame 1: Nuclear fusion may be the future of clean, affordable energy. \n Frame 2: Fusion releases nearly four million times more energy than coal, oil, or gas. \n Frame 3: And four times as much as traditional nuclear fission reactors. \n Frame 4: Without producing carbon dioxide or long-lived nuclear waste. \n Frame 5: Elements required for nuclear fusion come from abundant sources: water and lithium. \n Frame 6: Experiments began in the 1930s. \n Frame 7: But creating the right reactor conditions has proven challenging and costly. \n Frame 8: In 2022, US scientists generated more energy from a reaction than was put into it. \n Frame 9: Governments are backing nuclear fusion to solve their mid- and long-term energy needs. \n Frame 10: While private venture capital is funding research in the UK, US and elsewhere. \n Frame 11: Nuclear fusion power is still a long way from being operational and scaled to our needs. \n Frame 12: But a US reactor may be online by 2030 and the UK hopes to connect to the grid in the 2040s."},
    {"role": "user", "content": "Create a video script for a 60-second explainer video. \n\nTopic:3 reasons why LNG will be key part of the future energy mix \n\n Brief: A video that covers 3 reasons why LNG will be a key part of the future energy mix. Use this information as extra. 1. In 2020, the global Liquefied Natural Gas (LNG) market size was US$ 135420 million and it is expected to reach US$ 205280 million by the end of 2027, with a CAGR of 5.7% during 2021-2027 https://www.globenewswire.com/en/news-release/2022/05/23/2448545/0/en/Global-Liquefied-Natural-Gas-LNG-Market-Size-2022-Growing-Rapidly-with-Recent-Developments-Industry-Share-Trends-Demand-Revenue-Key-Findings-Latest-Technology-Industry-Expansion-St.html . 2. Easy to transport and store than piped natural gas: Means it can be globally traded and is more flexible. 3. Relatively low carbon. 4. Safer and more energy dense than piped gas. \n Topical with new facilities being built. Make this one evergreen. People don't realise how cold you have to make it, temperature issues. Get physics bits in there (cooling etc.).  "},
    {"role": "assistant",   "content": "Frame 1: LNG will be a key part of the future energy mix. Here’s why \n Frame 2: The global Liquefied Natural Gas (LNG) market topped US$135 billion in 2020 \n Source: Industry Research \n Frame 3: And it is expected to reach US$200 billion by the end of 2027 \n Source: Industry Research \n Frame 4: Produced by compressing and cooling natural gas to -162°C… \n Frame 5: And shipped around the world in super-cooled tankers \n Frame 6: LNG has created a truly global market for gas \n Frame 7: Unlocking previously stranded reserves \n Frame 8: Providing energy wherever it is needed most \n Frame 9: LNG has come into its own this century \n Frame 10: Building resilience into energy systems \n Frame 11: Driving down the carbon footprint of the power sector \n Frame 12: And supporting economic growth worldwide"},
    {"role": "user", "content": """Create a video script for a 60-second explainer video. \n\n Topic: natural gas based on a article. \n\n Brief:A video about  This is the article:
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
    {"role": "assistant",   "content": "Frame 1: Natural gas has a crucial role to play in the energy transition. Here’s how \n Frame 2: Natural gas is affordable, reliable and easy to store\nFrame 3: And it emits up to 50% less greenhouse gases than coal\nFrame 4: Here are 4 ways natural gas is helping power the energy transition\nFrame 5: 1. It offers a reliable low-carbon back-up for peak energy demand\nFrame 6: Providing a stable energy supply while renewable technologies grow\nFrame 7: 2. It acts as a bridging ingredient in the hydrogen energy revolution\nFrame 8: Hydrogen from renewables will play a key role in our climate-neutral future\nFrame 9: For now, the path to cleaner hydrogen relies on natural gas\nFrame 10: 3. It helps fight energy poverty\nFrame 11: In Africa, 600 million people still don’t have access to electricity or clean cooking\nFrame 12: Alongside renewables, natural gas can help fast-track the energy transition\nFrame 13: Combined with carbon capture and storage, it can transform the energy sector\nFrame 14: Thanks to carbon capture technology, we can reduce the emissions from natural gas processing\nFrame 15: Helping reduce hard-to-abate emissions from heavy industry like steel and cement"}]
    BASE_PROMPT_ARTICLES = [
    {"role": "system", "content": "Intelligent writer that writes articles in a particular style"},
    {"role": "user", "content": "I want you to writes articles on certain topics. We want our acrticles to be in a certain style, so I will provide some examples. You can use those examples to create similar articles."},
    {"role": "assistant", "content": "Okay, can you provide me with a brief so that I can create an article. "},
    {"role": "user", "content": """"Create an article with around 600 words that will highlight why burning low-carbon fuels (rather than no-carbon fuels) will be essential in achieving a secure, stable energy transition — and outline why electrification / renewables can't be the entire solution to net-zero in the near future. It will explain why the energy transition isn't a cliff-edge where sectors will convert immediately from high-carbon to no-carbon, but instead can use complementary low-carbon solutions as part of the journey.
    THis is the structure of the article.
    Intro: From where we are today and net zero, there will be a transitional period where hybrid, low carbon fuels and gases will increasingly dominate certain sectors, especially those that are hard to electrify. 

    Examples: 

    1. Transport. Transportation accounts for ~16% of global CO2 emissions, and carbon-positive solutions in the sector are therefore critical for global decarbonization. Low-carbon solutions will be especially needed in the transportation for hard-to-convert sectors where electrification is not an easy immediate prospect — for example shipping and aviation.  Early adopters will have both financial and regulatory incentives to move early.

    Examples of low-carbon transport fuel include:
    — blue hydrogen (made from natural gas)
    — biofuels

    https://www.bcg.com/publications/2022/the-road-ahead-for-low-carbon-fuels
    https://www.bcg.com/publications/2021/global-zero-carbon-shipping-transformation-challenge

    2. Power. There are many innovative and positive low-carbon solutions for the power. Wind and Solar PV are variable. For example, "the possibility to combust high shares of low-carbon hydrogen and ammonia in fossil fuel power plants provides countries with an additional tool for decarbonising the power sector." (IEA) https://www.iea.org/reports/the-role-of-low-carbon-fuels-in-the-clean-energy-transitions-of-the-power-sector

    3. Other relevant examples of sectors where low-carbon is a positive and necessary solution. 

        """},
    {"role": "assistant", "content": """The long road to net zero 

    There is a gulf between where the world is today and where it needs to be to hit net zero by 2050. Carbon-intensive coal, which is still the leading source of energy, is releasing record levels of carbon dioxide and renewable sources still only produce a relatively small proportion of our energy needs. 

    The coming decades represent a transitional period, as renewable energy solutions are scaled up to displace fossil fuel consumption. During this transition, there is ample opportunity to increase energy stability by replacing the most carbon-intensive fuels with lower- and low-carbon fuels until alternatives can fulfil all our energy needs. 

    Making the switch to lower-carbon power generation has already produced results in some countries. In the US, CO2 emissions from generating electricity fell by 32% between 2005 and 2019, largely the result of a shift from coal to natural gas, which produces significantly less carbon dioxide.  In the coming years, there is an opportunity to go further by introducing low-carbon fuels in multiple sectors, especially those that are challenging to electrify. Some of these fuels are available already, including sustainable aviation fuels and biofuels for transportation, while others are being developed. These include lower-carbon hydrogen (produced from natural gas and supported by carbon capture, utilization and storage), and hydrogen produced from renewable energy. 

    Renewables rising 

    The transition to net zero presents a vast challenge that will be tackled in diverse ways by different countries. The pathways are complicated by ever-growing demand for electricity and will be influenced by geopolitics along the way. Ensuring a just and orderly transition means that – for all the urgency of climate change – it is impossible to displace fossil fuels overnight. Not only do renewables provide just 29 percent of our electricity needs globally, but the fastest-growing renewables, wind and solar, require technologies like grid-scale energy storage to manage intermittency – and some industries’ needs can only be met by fossil fuels at present. 

    Steelmaking, for example, is considered a hard-to-abate sector due to the extremely high temperatures necessary that can only be reached by burning fuel. However, analyses suggest that the industry could reach net zero by 2050 with a combination of carbon capture, low-carbon fuels and more efficient steel use. In the short- to medium-term, low-carbon fuels present our best opportunity to press ahead with decarbonizing such hard-to-abate industries. 

    Complementary fuels 

    Switching to lower-carbon fuels is among the most economically, politically, and technologically feasible approaches to slowing carbon emissions. It offers a lower-carbon future for newly built infrastructure in East and Southeast Asia, which could otherwise become stranded assets with serious socio-economic consequences.  

    According to the IEA, co-firing of ammonia and hydrogen has been successfully demonstrated at power plants. Increased use of low-carbon fuels in the power sector could help establish supply chains and drive down costs, encouraging uptake in other sectors. 

    Transport – which accounts for one fifth (21%) of global CO2 emissions – is another sector well-positioned for fuel-switching. While full electrification is the ultimate goal for transport, this is not feasible in the short-term, particularly in countries that struggle to produce enough electricity and for long-distance journeys and heavy vehicles (e.g.: ships, aircraft, and trucks) that require fuels with high energy density. Vehicles of all types, however, can run on lower-carbon fuels such as biofuels, compressed natural gas, and liquid natural gas (either on their own or blended with fossil fuels) with minimal adjustments. Natural gas can emit 25 percent less carbon per unit of energy compared with conventional gasoline. 

    Despite the relative ease with which the switch to lower-carbon fuels can be made, this opportunity remains largely unseized. Encouraging a switch to these fuels, which are a more expensive option, is likely to require government interventions in the short- to medium-term. 

    The road to net zero is long and scattered with obstacles. For many sectors, switching to low-carbon fuels can provide the stable, progressive transition to lower emissions that the world needs. 

    """},
    {"role": "user", "content": """"Around 30% of global energy is consumed in the agricultural and food sector. 

    Create an article with around 600-words articleabout how fossil fuels are used directly and indirectly in food production, with a focus on fertilizer.

    - Nitrogen-based fertilizer (made using the Haber-Bosch process) consumes 1% of the world's energy supply in the form of natural gas. This production is directly responsible for sustaining 40% of the Earth's population. 
    - Nitrogen-based fertilizer production went from around 4 million tons in the 1950s to 100 million tons a year today. 

    Use article to highlight unexpected areas of living that rely on fossil fuel production, finishing on how we can factor this in to the energy transition. 
    - More fuel efficient engines 
    - Use of compost and precision fertilizers etc. see link https://news.un.org/en/story/2011/11/396792-un-urges-food-sector-reduce-fossil-fuel-use-and-shift-energy-smart-agriculture#:~:text=Steps%20that%20can%20be%20taken,crop%20varieties%20and%20animal%20breeds. 
    """},
    {"role": "assistant", "content": """
    When we talk about the challenge of decarbonization, we tend to think of electricity production – but there are other fossil fuel-dependent industries that are just as essential to everyday life. In fact, around 30 percent of global energy is consumed by the agricultural and food sector.  

    A report from UN Food and Agriculture Organization experts found that food systems emitted 18Gt of CO2 equivalent in 2015 – 34 percent of overall emissions – and these emissions are continuing to grow. 

    The cost of crop production 

    The rise of ammonia-based fertilizers has hugely boosted crop production, doubling the number of people that a unit of land can feed and sustaining the growing global population. 

    However, producing ammonia is an energy-intensive process that uses fossil fuels, both as the source of hydrogen and as an energy source. Commercial ammonia production accounts for almost two percent of global energy consumption.  Although it is possible to produce ‘green ammonia’ from water and renewable energy, in practice almost all ammonia is derived from fossil fuels. 

    Carbon-intensive value chains 

    Fertilizer production is just one of the many ways in which food production contributes to greenhouse gas emissions. 

    For instance, research published in Science estimated that livestock and fisheries account for 31 percent of food-related emissions, land use (mainly the conversion of forests and other ‘carbon sinks’ into cropland or pasture) for 24 percent, and supply chains for 18 per cent. Small but significant contributions came from packaging, transportation and refrigeration. 

    Cutting emissions, then, is no straightforward task – particularly while food demand continues to grow. The reality is there is no silver bullet. A combination of approaches is needed to tackle the many sources of emissions: changes to land use, shifts in consumer behavior, shortened supply chains, efficiency measures, and alternatives to fertilizers made with fossil fuels. 

    Food that doesn’t cost the earth 

    Green ammonia could play a significant role in reducing use of fossil fuels in food production. With the cost of renewables falling compared with fossil fuels, green ammonia is inching closer to commercial viability. Several large ammonia producers have announced projects to produce green ammonia, including Yara, which is carrying out pilot projects in Norway, the Netherlands and Australia. 

    In the meantime, there could be ways to reduce fertilizer use. In fact, it has been pointed out that many policies and regulations inadvertently encourage excessive fertilizer use. The European Commission is working to increase the sustainability of food systems, with an aim of cutting fertilizer use by a fifth by 2030. This could be considered a first step towards ‘precision agriculture’, in which data is used to inform how to use fertilizer, fuel and other resources more effectively, reducing waste, costs and emissions.  

    The energy transition is not just about electricity and heating – fossil fuels are used in the production of all sorts of indispensable resources. Rising to the climate challenge calls for changes to how we produce, process, and consume food. 
    """},
        {"role": "user", "content": """" In the run up to the circular carbon economy round table in February (details of the event in the assets tab - don't need to mention the event in the article, just has useful copy), produce a 600-word article (US spelling) putting CCUS in context - what's happened so far, what can we learn, what are the biggest roadblocks (is it R&D, investment, getting projects off the ground?)

    There was a lot of interest in CCUS in the noughties, but the potential was never realised. With organizations like the IPCC highlighting the importance of CCUS, how can we ensure we build and maintain momentum? 

    Use examples of what's happening: 
    - Industrial hubs 
    - US Inflation Reduction Act 
    - EU's upcoming strategic vision for CCUS technologies 

    Info on CCUS (can link to these articles rather than covering a lot of the same ground) 
    https://www.ief.org/news/critical-role-for-ccus-highlighted-in-latest-ipcc-report-whats-next 
    https://www.ief.org/news/major-investors-back-direct-air-capture-co2-technology 
    https://www.ief.org/news/caverns-concrete-and-carbonate-the-future-of-storing-captured-carbon 
    https://www.ief.org/news/oceans-offer-tantalizing-carbon-capture-potential-will-it-be-realized 
    https://www.ief.org/news/whats-the-target-for-carbon-sequestration-and-how-do-we-get-there 

    Info on history of CCUS (more desk research needed): 
    https://www.iea.org/reports/about-ccus 
    https://www.iea.org/commentaries/carbon-capture-in-2021-off-and-running-or-another-false-start 

    """},
        {"role": "assistant", "content": """
    Increasing the scale of carbon capture utilization and storage (CCUS) technology is essential if we are to keep global warming to within 2°C. However, despite the technology having been around for several decades, its potential has yet to be fully realized.  

    Significant investment is required to scale up deployment of CCUS technology if we are to reach net-zero targets, potentially amounting to trillions of dollars. Despite these challenges, there is renewed momentum around CCUS projects. 

    [Embed this carousel: https://twitter.com/IEF_Dialogue/status/1596061135828049922]  

    From stagnation to renewed energy 

    Following early growth in the 1980s, interest in CCUS as a way to reduce greenhouse gas emissions and combat climate change peaked during the 2000s. However, by 2010, only slightly more than 15 MtCO2 was being captured, and the following decade saw the mass cancellation of CCUS project plans.    

    One of the biggest roadblocks was the lack of investment and political will to support the development and deployment of the technology. Less than 0.5% of clean energy and efficiency technologies investments go towards CCUS, according to the IEA, and a lack of policy support negatively impacts the commercial appeal of CCUS.

    Today, the situation is changing, with several factors driving this new momentum, including the 2023 UN Intergovernmental Panel on Climate Change (IPCC) report, which said carbon capture could be necessary to reach net-zero goals, especially in hard-to-abate industries. 

    Policy changes and strategic vision drive CCUS investment impetus 

    Part of this impetus is due to policy changes that favor climate mitigation technologies, with the United States and Europe leading the way. A section of the US tax code, 45Q, provides a tax credit for carbon sequestration. This is designed to incentivize a variety of projects under CCUS. The expansion of 45Q  in 2018 kickstarted renewed interest in CCUS and in 2021 more than 100 new CCUS facilities were announced around the world. In 2022, the US Inflation Reduction Act further expanded and extended the 45Q tax credit by increasing the credit amount and lowering the CO2 capture capacity bar for eligibility, which is expected to act as a stimulus for investment in CCUS projects. 

    The EU has also announced an upcoming strategic vision for CCUS technologies. The plan includes a €3 billion package for investment in CCUS innovation and development and the creation of an EU-wide carbon storage infrastructure. Member states are increasing their own support, with Denmark allocating €5 billion euro to CCUS projects.  

    Elon Musk’s launch of the $100M XPRIZE for carbon removal in January 2021 shows that private investment can also be an important factor in driving CCUS development.  

    Innovation drives new technologies for load sharing, storage and use 

    One of the most promising opportunities is the creation of industrial ‘hubs’, which capture CO2 from associated facilities, sharing CO2 transport and storage infrastructure. Examples include the Alberta Carbon Trunk Line and Norway’s Longship Project, which includes the Northern Lights offshore storage hub.  

    Innovative new approaches to carbon capture and storage are opening up further avenues for CCUS and creating potential for a circular carbon economy. These include direct air capture (DAC) of CO2, the potential for ocean carbon capture as well as the production of carbon-negative concrete. Nature-based solutions, such as afforestation and restorative or regenerative farming, are also gaining traction as an essential part of carbon management.  

    [Embed CCUS video: https://www.youtube.com/watch?v=1b6r2H7jtKc]  


    De-risking CCUS investment 

    Despite these developments, there are still many challenges to be overcome if CCUS is to be scaled up “from the mega to the giga” to reach 5.6 Gt CO2 capacity by 2050 to meet Paris goals.  

    The cost of the technology remains extremely high. Energy penalties also pose a barrier, along with the lack of regulatory frameworks in place to support the widespread development and deployment of CCUS. 

    There are concerns about the safety of storing CO2 underground and some critics view CCUS as a vehicle for prolonging the role of fossil fuels in the global economy, as opposed to a clean energy technology. 

    However, these challenges are not insurmountable. To de-risk CCUS investment, there are several ways to increase investor confidence: 

    Developing a clear and consistent regulatory framework across countries and enforcing regulations that address CCUS liability issues 

    Creating a stable and predictable market for CCUS technology that aligns with Environmental, Social and Governance (ESG) standards  

    Ramping up research and development to reduce the cost of CCUS technology 

    Widening public awareness 

    Exploring new financing models such as creative incentivization programs, public-private partnerships and green bonds, to increase access to capital markets for CCUS projects 

    Creating network synergies with hydrogen infrastructure to make CCUS projects more cost-effective 

    With the right support and investment, CCUS technology will become a more attractive investment opportunity, accelerating the transition to a low-carbon economy as an important tool in the fight against climate change. """},
        
    ]

    if "script_messages"  not in st.session_state:
        st.session_state["script_messages"] = BASE_PROMPT_VIDEO
    if "article_messages"  not in st.session_state:
        st.session_state["article_messages"] = BASE_PROMPT_ARTICLES

    if type == 'Video Script':
        video_script_generator()
    elif type == 'Article':
        article_generator()
    
   

