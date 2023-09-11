import requests
from twilio.rest import Client
import os

TWILIO_ACCOUNT_SID = "Your Twilio SID"
TWILIO_AUTH_TOKEN = "Your Twilio Auth token"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "[Your API key]"

stock_params = {
    "function": "Time_series_daily",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "[Your API key]"

response = requests.get(STOCK_ENDPOINT, stock_params)
response.raise_for_status()

stock_data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in stock_data.items()]

#yesterdays closing stock price
yesterday_data = data_list[0]
yesterday_close_price = yesterday_data["4. close"]


#day before yesterday's closing stock price
day_before_yesterday_close = data_list[1]["4. close"]

#Find the difference
difference = float(yesterday_close_price) - float(day_before_yesterday_close)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

#percentage difference in price between closing price yesterday and closing price the day before yesterday.

percentage_difference = round(difference / float(yesterday_close_price)) * 100

#If percentage is greater than 5 then use the News API to get articles
if abs(percentage_difference) > 5:
    news_params = {
        "apikey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, news_params)
    news_data = news_response.json()["articles"]

#Use Python slice operator to create a list that contains the first 3 articles

    articles = news_data[:3]

#Create a new list of the first 3 article's headline and description using list comprehension.

    news_overview = [(f"{STOCK_NAME}: {up_down} {percentage_difference}% \n Headline: {article['title']}."
                      f" \nBrief: {article['description']}") for article in articles]

#Send each article as a separate message via Twilio.

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    for article in news_overview:
        message = client.messages.create(
            body=article,
            from_='+12568575645',
            to='+353000000000'
        )
        print(message.sid)