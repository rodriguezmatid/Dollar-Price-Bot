import tweepy
import telebot
import requests
from bs4 import BeautifulSoup
import dotenv as _dotenv
import os as _os

_dotenv.load_dotenv()

#############################################################################################################################################################
########################################################################## SCRAPPER #########################################################################
#############################################################################################################################################################

URL = "https://dolarhoy.com/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="main_body ")
job_elements = results.find_all("div", class_="val")

quotes = []

for job_element in job_elements:
    quotes.extend(job_element)

scrapeo_for_tw = ("------------------ Dólar ------------------\n"
                     f"Blue.        C: {quotes[2]} //  V: {quotes[3]}\n"
                     f"Oficial.    C: {quotes[4]} //    V: {quotes[5]}\n"
                     f"Bolsa.      C: {quotes[6]} //   V: {quotes[7]}\n"
                     f"CCL.         C: {quotes[8]} //   V: {quotes[9]}\n"
                     f"Crypto.    C: {quotes[10]} //   V: {quotes[11]}\n"
                     f"Solidario. V: {quotes[12]}")

scrapeo_for_tg = ("-------------- Dólar --------------\n"
                     f"Blue.        C: {quotes[2]} //  V: {quotes[3]}\n"
                     f"Oficial.    C: {quotes[4]} //    V: {quotes[5]}\n"
                     f"Bolsa.      C: {quotes[6]} //   V: {quotes[7]}\n"
                     f"CCL.         C: {quotes[8]} //   V: {quotes[9]}\n"
                     f"Crypto.    C: {quotes[10]} //   V: {quotes[11]}\n"
                     f"Solidario. V: {quotes[12]}")

#############################################################################################################################################################
########################################################################## TWITTER ##########################################################################
#############################################################################################################################################################

# Authenticate to Twitter
TW_API_KEY = _os.environ["TWITTER_API_KEY"]
TW_API_SECRET = _os.environ["TWITTER_SECRET_KEY"]
TW_ACCESS_TOKEN = _os.environ["TWITTER_ACCESS_TOKEN"]
TW_ACCESS_SECRET = _os.environ["TWITTER_ACCESS_SECRET"]

auth = tweepy.OAuthHandler(TW_API_KEY, TW_API_SECRET)
auth.set_access_token(TW_ACCESS_TOKEN, TW_ACCESS_SECRET)

api_twitter = tweepy.API(auth)

try:
    api_twitter.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

########## Read the last tweet ##########

id = 1548411397456814080
last_tweet = api_twitter.user_timeline(user_id = id, count = 1, tweet_mode = 'extended')
for tweet in last_tweet:
    last_tweet = tweet.full_text

########## Twittea ##########

if scrapeo_for_tw != last_tweet:
    api_twitter.update_status(scrapeo_for_tw)
else:
    print("The price didn't change")

#############################################################################################################################################################
########################################################################## TELEGRAM #########################################################################
#############################################################################################################################################################

T_TOKEN = _os.environ["TELEGRAM_TOKEN"]
T_CHANNEL_1 = _os.environ["TELEGRAM_CID_CHANNEL_1"]

bot_telegram = telebot.TeleBot(T_TOKEN)
bot_telegram.send_message(T_CHANNEL_1, scrapeo_for_tg)