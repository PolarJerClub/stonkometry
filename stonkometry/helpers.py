from flask import request, jsonify, render_template
from functools import wraps
import secrets
import decimal
import requests
import json
import time


from stonkometry.models import User

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        """
        This functino takes in any number of args & kwargs and verifies
        that the token passed into the headers is associated with a 
        user in the database
        """
        
        token = None
        
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split()[1]
            print(token)

        if not token:
            return jsonify({'message': 'Token is missing'}), 401 #client error
        
        try:
            our_user = User.query.filter_by(token=token).first()
            print(our_user)
            if not our_user or our_user.token != token:
                return jsonify({'message': 'Token is invalid'}), 401 #client error
            
        except:
            our_user = User.query.filter_by(token=token).first()
            if token != our_user.token and secrets.compare_digest(token, our_user.token):
                return jsonify({'message': 'Token is invalid'}), 401
        
        return our_flask_function(our_user, *args, **kwargs)
    
    return decorated


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return json.JSONEncoder(JSONEncoder, self).default(obj)
    
ticker = "AAPL"
api_key = 'f77c421c58a3448d9762050ae5d60b6c'

def get_stock_price(ticker_symbol, api):
    url = f"https://api.twelvedata.com/price?symbol={ticker_symbol}&apikey={api}"
    response = requests.get(url).json()
    price = response['price'][:-3]
    return price



def get_stock_quote(ticker_symbol):
    url = f"https://api.twelvedata.com/quote?symbol={ticker_symbol}&apikey=f77c421c58a3448d9762050ae5d60b6c"
    response = requests.get(url).json()
    return response

stockdata = get_stock_quote(ticker)
stock_price = get_stock_price(ticker, api_key)

name = stockdata['name']
exchange = stockdata['exchange']
currency = stockdata['currency']
open_price = stockdata['open']
high_price = stockdata['high']
low_price = stockdata['low']
close_price = stockdata['close']
volume = stockdata['volume']




print(name, exchange, currency, open_price, high_price, low_price, close_price, volume, stock_price)


# api_key="3effdf43cdd748afa499f99400d016bf"

# def news():
#     main_url="https://newsapi.org/v2/top-headlines?country=us&apiKey=3effdf43cdd748afa499f99400d016bf"
#     news=requests.get(main_url).json()
#     # print(news)
#     article=news["articles"]
#     # print(article)

#     news_title=[]
#     news_author=[]
#     news_content = []

#     for arti in article:
#         news_title.append(arti['title'])
#         news_author.append(arti['author'])
#         news_content.append(arti['content'])
#         # print(news_article)

#     for i in range(len(article)):
#         print(i+1, news_title[i])
#         print(i+1, news_author[i])
#         print(i+1, news_content[i])

#     mylist = zip(news_title, news_author, news_content)

#     return render_template('news.html', context=mylist)



# news()