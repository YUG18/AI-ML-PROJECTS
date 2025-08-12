import streamlit as st
from newspaper import Article
from newspaper import build
from transformers import pipeline
from transformers import  AutoTokenizer, AutoModelForSeq2SeqLM
from googletrans import Translator
import pyttsx3

st.title("News summary app with translation and speech")
category = st.selectbox("Select news category",['Technology','Business'])

#Speech conversion options
speech_convert = st.checkbox("Want an audio about summary?")
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# Choose a voice: 0 for male, 1 for female
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 135)  # Speed of speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

#Translation options
language_map = {'Hindi':'hi','Gujarati':'gu'}
translate_option=st.checkbox("Translate news into other language?")
selected_language_name=st.selectbox("Choose language",list(language_map.keys()))
selected_language=language_map[selected_language_name]
def translate_text(text,target_language='hi'):
    try:
        translator = Translator()
        translated = translator.translate(text,dest=target_language)
        return translated.text
    except Exception as e:
        st.warning("Translation failed.")
        return text

#function for text summarization
@st.cache_resource
def load_summarizer():
    model_name = "t5-small"
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return pipeline("summarization", model=model, tokenizer=tokenizer)

summarizer = load_summarizer()

def text_summarizer(text):
    summary = summarizer(text,max_length=150,min_length=100,do_sample=False)[0]['summary_text']
    return summary
@st.cache_data(ttl=3600)  #Remembers or stores data for duration of 1 hour
def tech_news():
    tech = build('https://techcrunch.com/',memoize_articles=False) #scans webpages and gets links point to articles
    articles = tech.articles[:5] # top five articles
    tech_data = []
    for article in articles:
        article.download()   #downloads raw html content
        article.parse()    #extracts information
        tech_text = article.text
        summary = text_summarizer(tech_text)
        if translate_option:
            translated_summary = translate_text(summary,target_language=selected_language)
            summary = translated_summary
        tech_data.append({'title': article.title , 'summary':summary , 'url':article.url})
    return tech_data

@st.cache_data(ttl=3600)
def business_news():
    business = build('https://www.moneycontrol.com/news/business/',memoize_articles=False)
    articles = business.articles[:5]
    business_data = []
    for article in articles:
        article.download()
        article.parse()
        business_text=article.text
        summary=text_summarizer(business_text)
        if translate_option:
            translated_summary = translate_text(summary,target_language=selected_language)
            summary = translated_summary
        business_data.append({'title':article.title,'summary':summary,'url':article.url})
    return business_data

news_data = []
if "news_data" not in  st.session_state:
    st.session_state.news_data = []
if st.button("Fetch News"):
    with st.spinner("Fetching and summarizing news..."):
        if category == 'Technology':
            st.session_state.news_data = tech_news()
        else:
            st.session_state.news_data = business_news()

#display the result
for items in st.session_state.news_data:
    st.subheader(items['title'])
    st.markdown(items['summary'])
    st.write(f"[Read More]({items['url']})",unsafe_allow_html=True)
    st.markdown("-----------")

if speech_convert and st.session_state.news_data:
    titles = [item['title'] for item in st.session_state.news_data]
    selected_title = st.selectbox("Choose a news summary to hear",titles)
    summary_to_speak=next((item['summary'] for item in st.session_state.news_data if item['title']==selected_title),None)
    if st.button("Speak selected summary"):
        speak(summary_to_speak)
if st.button("Refresh News"):
    st.cache_data.clear()
    st.session_state.news_data = []
