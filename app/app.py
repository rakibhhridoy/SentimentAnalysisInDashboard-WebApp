import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


st.title("Sentiment Analysis Tweets About US Airlines")
st.sidebar.title("Sentiment Analysis Tweets About US Airlines")
st.markdown(" This Application is a streamlit Dashboard to analyze Sentiment of Airlines Tweets in US 🐦")
st.sidebar.markdown(" This Application is a streamlit Dashboard to analyze Sentiment of Airlines Tweets in US 🐦")

DATA_URL = ("./data/Tweets.csv")

@st.cache(persist = True)   # so it will cached the data for no reloding data again and again

def load_data():
    data_matrix = pd.read_csv(DATA_URL)
    data_matrix['tweet_created'] = pd.to_datetime(data_matrix['tweet_created'])

    return data_matrix

df = load_data()

st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio("Sentiment", ("positive", 'neutral', 'negative'))
st.sidebar.markdown(df.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0, 0])


st.sidebar.markdown("### Number of Tweet By Sentiment")
select = st.sidebar.selectbox('Visualization Type', ["Histogram", 'Pie Chart'], key = '1')
sentiment_count = df['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index, "Tweets": sentiment_count.values})

if not st.sidebar.checkbox("Hide", True):
    st.markdown('### Number of tweets by sentiment')
    if select =='Histogram':
        fig = px.bar(sentiment_count, x = 'Sentiment', y = 'Tweets',color = 'Tweets', height= 500)
        st.plotly_chart(fig)

    else:
        fig = px.pie(sentiment_count, values= 'Tweets', names= 'Sentiment')
        st.plotly_chart(fig)


st.sidebar.subheader("When and Where are users tweeting from")
hour = st.sidebar.slider("Hour of day",0, 23)
modified_data = df[df['tweet_created'].dt.hour == hour]

if not st.sidebar.checkbox("Close", True, key ='1'):
    st.markdown('### Tweets loactions based on the time')
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)


st.sidebar.subheader('Breakdown airline tweets by sentimnet')
choice = st.sidebar.multiselect('Pick airlines', ('US Airways', 'Unitedd', 'American', 'Southwest', 'Delta', 'Virgin America'), key= '0')


if len(choice) >0:
    choice_data  = df[df.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x = 'airline', y = 'airline_sentiment', histfunc = 'count', color = 'airline_sentiment', facet_col = 'airline_sentiment', labels = {'airline_sentiment': 'tweets'}, height = 600, width= 800)
    st.plotly_chart(fig_choice)



st.sidebar.header("World Cloud")
word_sentiment = st.sidebar.radio('Display word cloud for what sentiment?', ('positive', 'neutral', 'negative'))

if not st.sidebar.checkbox("CLose", True, key = '3'):
    st.header("Word Cloud for %s sentiment" % (word_sentiment))
    df = df[df['airline_sentiment']== word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords = STOPWORDS, background_color = 'white',height = 640, width = 800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()
