import pandas as pd 
import snscrape.modules.twitter as sntwitter
import streamlit as st
import pymongo



client =pymongo.MongoClient("mongodb://localhost:27017")
db = client["twitter"]

keyword="python"
start_date="2023-01-01"
end_date="2023-03-15"
limit=1000

def twitter_data(keyword,start_date,end_date,limit):
  tweets=[]
  for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{keyword} since:(start_date)until:(end_date)').get_items()):
    if i >= limit:
      break
  tweet_dict={
      "date":tweet.date,
      "id":tweet.id,
      "user":tweet.user.username,
      "content":tweet.content,
      "url":tweet.url,
      "reply_count":tweet.reply_count,
      "retweet_count":tweet.retweetcount,
      "language":tweet.lang,
      "source":tweet.sourcelabel,
      "like_count":tweet.likecount,
  }

  tweets.append(tweet_dict)

  db[keyword].insert_many(tweets)
  return pd.Dataframe(tweets)

st.sidebar.title("twitter_scraper")
keyword = st.sidebar.text_input("enter your keyword or hastag to search for :")
start_date = st.sidebar.date_input("start_date:")
end_date = st.sidebar.date_input("end_date :")
limit = st.sidebar.slider('limit:',1,1000,100)

st.title("Twitter Scraper")
if keyword:
  st.write(f'scraping tweets containing "{keyword}"...')
  data=twitter_data(keyword,start_date,end_date,limit)
  st.write(data)

  if st.button("upload to mongoDB"):
    db[keyword].insert_many(data.to_dict("records"))
    st.success(f'successfully uploaded{len(data)} tweets to mongoDB')

  file_format = st.selectbox('choose a file format to download :',('csv','json'))
  if st.button('download'):
    if file_format == 'csv':
      data.to_csv(f'{keyword}.csv',index=False)
      st.success(f'successfully dowloaded{len(data)} tweets as csv!')
    else:
      data.to_json(f'{keyword}.json',orient = 'records')
      st.success(f'successfully uploaded{len(data)} tweets as json!')


if __name__ == '__main__':
  st.set_page_config(page_title='Twitter scraper')
  st.cache(persist=True)
 
