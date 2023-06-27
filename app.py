import streamlit as st
from streamlit_chat import message
import openai
import streamlit as st
from _config import BASE_PROMPT_ARTICLES, BASE_PROMPT_VIDEO, HOLCIM_VIDEO, ADECCO_ARTICLE, LLH_ARTICLES,LLH_SCRIPT
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

if check_password():
    st.title("Content Engine Digital Writer V1")
    type = st.radio(
    "What do you want to create?",
    ('Video Script', 'Article'))
    
    video_title = st.text_input("Video Title", placeholder="What is cycle synching?")
    
    if "script_messages"  not in st.session_state:
        st.session_state["script_messages"] = BASE_PROMPT_VIDEO
    if "article_messages"  not in st.session_state:
        st.session_state["article_messages"] = BASE_PROMPT_ARTICLES
    end_prompt = " "

    st.write(st.session_state)
   
    if type == 'Video Script':
        
        video_len = st.slider('How long should the video be?', 0, 180, 60, step = 15)
        st.write("Video has to be around ", video_len, 'seconds')
    
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
        
        if st.button("Change", key = 'change'):
            with st.spinner("Let me make some adjustments..."):
                st.session_state["script_messages"] += [{"role": "user", "content": prompt}]
                response = openai_call(st.session_state["script_messages"])
                message_response = response["choices"][0]["message"]["content"]
                st.session_state["script_messages"] += [{"role": "assistant", "content": message_response}]
        
    

        if st.button("Clear", key="clear"):
            st.session_state["script_messages"] = BASE_PROMPT_VIDEO
            
        for i in range(len(st.session_state["script_messages"])-1, 10, -1):
            if st.session_state["script_messages"][i]['role'] == 'user':
                message(st.session_state["script_messages"][i]['content'], is_user=True)
            if st.session_state["script_messages"][i]['role'] == 'assistant':
                message(st.session_state["script_messages"][i]['content'], avatar_style="bottts-neutral", seed='Aneka')
                
        

    
    
          

            
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
        
