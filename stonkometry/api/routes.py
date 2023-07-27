from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
# import config
# import alpaca_trade_api as tradeapi
from stonkometry.helpers import token_required
from stonkometry.models import db, Stocks, stock_schema, stocks_schema


api = Blueprint('api', __name__, url_prefix='/api')



@api.route('/stonks')
def getdata():
    return {'some': 'value'}



 