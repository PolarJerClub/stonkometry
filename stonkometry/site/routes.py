from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from stonkometry.forms import StockForm
from stonkometry.models import Stocks, db
from stonkometry.helpers import get_stock_quote, get_stock_price
# from profile import myWidget
import requests


site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # stonkform = StockForm()
    # try:
    #     if request.method == 'POST' and stonkform.validate_on_submit():
    #         name = stonkform.name.data
    #         user_token = current_user.token
    #         data = get_stock_quote(name)

    #         stonk = Stocks(name, user_token)

    #         db.session.add(stonk)
    #         db.session.commit()

    # except:
    #     raise Exception('Stock not created, please check your form and try again.')

    # user_token = current_user.token
    # stonks = Stocks.query.filter_by(user_token=user_token)

    return render_template('profile.html')

@site.route('/news')
def news():
    main_url="https://newsapi.org/v2/top-headlines?country=us&apiKey=3effdf43cdd748afa499f99400d016bf"
    news=requests.get(main_url).json()
    article=news["articles"]

    news_img=[]
    news_title=[]
    news_author=[]
    news_description = []
    news_url=[]

    for arti in article:
        news_title.append(arti['title'])
        news_author.append(arti['author'])
        news_description.append(arti['description'])
        news_img.append(arti['urlToImage'])
        news_url.append(arti['url'])

    mylist = zip(news_img, news_title, news_author, news_description, news_url)

    return render_template('news.html', context=mylist)

@site.route('/playground')
def playground():
    return render_template('playground.html')
