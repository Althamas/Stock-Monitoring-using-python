import requests
import datetime
from twilio.rest import Client

STOCK_NAME = "IBM"
COMPANY_NAME = "IBM"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_KEY = "YOUR KEY"

# STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases between yesterday and the day before yesterday.
today = datetime.datetime.today().date()
yesterday = str(today - datetime.timedelta(days=1))
day_before_yesterday = str(today - datetime.timedelta(days=2))

stock_price = \
    requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo").json()[
        "Time Series (Daily)"]

two_yesterday_close = [float(value["4. close"]) for (key, value) in stock_price.items() if
                       key == yesterday or key == day_before_yesterday]
print(two_yesterday_close)
# Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20

dif = abs(two_yesterday_close[0] - two_yesterday_close[1])
print(dif)

# Work out the percentage difference in price between closing price yesterday and closing price the day
# before yesterday.

percentage = ((two_yesterday_close[1] / two_yesterday_close[0]) - 1)
print(percentage)

if percentage < 0.006:
    print("Get news")

# STEP 2: https://newsapi.org/

news_params = {
    "apiKey": "YOUR KEY",
    "qInTitle": COMPANY_NAME,
}
news = requests.get(NEWS_ENDPOINT, params=news_params).json()["articles"]


three_news = news[:3]
print(three_news)

# STEP 3: Use twilio.com/docs/sms/quickstart/python


# Create a new list of the first 3 articles headline and description using list comprehension.
news_content = {i["title"]: i["content"] for i in three_news}
print(news_content)
for i in news_content:
    print(f"{STOCK_NAME} 📈 {'{:.3f}'.format(percentage)}\n{i}\n{news_content.get(i)}")

# Send each article as a separate message via Twilio.

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure


account_sid = "YOUR SID"
auth_token = "YOUR TOKEN"
client = Client(account_sid, auth_token)

for i in news_content:
    message = client.messages \
        .create(
         body=f"{STOCK_NAME} 📈 {'{:.2f}'.format(percentage)}\n{i}\n{news_content.get(i)}",
         from_='NUMBER FROM TWILIO',
         to='YOUR NUMBER'
        )

    print(message.sid)
