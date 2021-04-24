from flask import Flask, render_template, request, flash, redirect, jsonify, session
import config_final, csv 
from binance.client import Client
from binance.enums import *

    # to start flask we need to type in the consol
    # sudo -H pip3 install flask
    # export FLASK_APP=Final/Cryptobot.py
    # echo $FLASK_APP
    # export FLASK_ENV=development
    # flask run

app = Flask(__name__, template_folder='../Final/Templates')  # type pwd to know current path
app.secret_key = b'qasdoaf51wonewfoinADFasoid2452'

    # We need to connect to Binance using the API keys
client = Client(config_final.API_KEY, config_final.API_SECRET)

print("Python Starting now")

    #How to get the candlesticks data from Binance API and write in a csv
csvfile = open('Final/candles_custom.csv','w', newline='')
candlestick_writer = csv.writer(csvfile, delimiter=',')
candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_5MINUTE, "15 Jan, 2020 10:00 PM GMT", "17 Jan, 2020 10:00 PM GMT")
for candlestick in candlesticks:
        candlestick[0] = candlestick[0] / 1000
        # print(candlestick)
        candlestick_writer.writerow(candlestick)
csvfile.close()



@app.route('/')
def index():
    
    # We need to pull our account information, such as how many of each crypto we have
    account = client.get_account() 
    balances = account['balances']

    # We need to pull the list of all the available cryptocurrency pairs.
    exchange_info = client.get_exchange_info() #could we also use client.get_all_tickers() ?
    symbols = exchange_info['symbols']
    # We need to sort it in alphabetical order

    # We need to pull all the possible KLINE/Candlestick interval possible
        # THE BELOW IS STATIC BUT WE DON'T WANT THAT, 
        # WE NEED IT TO BE TAKEN FROM Binance API same as we did for the symbols
    frequencies = [{'frequency': '1m'}, {'frequency': '3m'}, {'frequency': '5m'}, {'frequency': '15m'}, {'frequency': '30m'}, {'frequency': '1h'}, {'frequency': '2h'}, {'frequency': '4h'}, {'frequency': '6h'}, {'frequency': '8h'}, {'frequency': '12h'}, {'frequency': '1d'}, {'frequency': '1w'}, {'frequency': '1M'}, ]

    # Here we will offer an easy way to load the chart for the past XX period
    # "for the past 30minutes", "for the last 1 hour", " for the last 3 hours", ...
    periode = [{'period': '30m'}, {'period': '1h'}, {'period': '3h'}, {'period': '6h'}, {'period': '12h'}]
    
    return render_template('index.html', my_balances=balances, symbols=symbols, frequencies=frequencies, periods=periode)





    # Here we are trying to get the parameters the user entered in the dashboard
    # There must be a smarter way to do that...
@app.route('/testcustom', methods=['POST', 'GET'])
def testcustom():
    session['symbol_toppage'] = request.values.get('symbol_toppage') #get the cryptocurrency pair selected by the user
    frequency = request.values.get('frequency')  #get the kline interval selected by the user
    start_date = request.values.get('start_date')  #get the start date
    end_date = request.values.get('end_date')   #get the end date, end date is optional
    hour_start = request.values.get('hour_start')  #get the starting time, starting time is optional
    hour_end = request.values.get('hour_end')   #get the ending time, end time is optional

    return redirect('/')






    # Here we are going to pull the historical trade data using the parameters the user entered in the dashboard
    # NOT COMPLETE... and i believe we do not need to use session.get or /testcustom
@app.route('/history')
def history():

    var1 = session.get('symbol_toppage', None) # definitely not the smartest way to get the data from the user...
    var2 = "18 Mar, 2021 05:00 PM GMT" #careful of the date and time format
    var3 = "18 Apr, 2021 05:00 AM GMT" # more info on format https://dateparser.readthedocs.io/en/latest/

    candlesticks = client.get_historical_klines(var1, Client.KLINE_INTERVAL_15MINUTE, var2, var3)
    # Still need to include the correct KLINE interval, and make sure the date/time is formatted the right way
    # We are trying to achieve something like :
    # candlesticks = client.get_historical_klines(symbol_toppage, "Client.KLINE_INTERVAL_" + frequency, start_date + hour_start + "GMT", end_date + hour_end + "GMT")
    # more info on https://python-binance.readthedocs.io/en/latest/market_data.html#id7
    # and https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data

    processed_candlesticks = []

    for data in candlesticks:
        candlestick = { 
            "time": data[0]/1000, #we need to divide the timestamp by 1000 so the chart from TradingView can read it
            "open": data[1], 
            "high": data[2], 
            "low": data[3], 
            "close": data[4] 
        }
        processed_candlesticks.append(candlestick)
    # We also would like to add the 'volumes' to our processed_candlesticks and to the graph

    return jsonify(processed_candlesticks)





    #Here we are going to make the buy order
    #We use the parameters entered by the user on the dashboard : Quantity and Symbol

@app.route('/buy', methods=['POST'])
def buy():
    print(request.form)
    try:
        order = client.create_order(
            symbol=request.form['symbol'],
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET, #here it is a market order, but we would like to also include limit orders
            # timeInForce=TIME_IN_FORCE_GTC,
            quantity=request.form['quantity'])
    except Exception as e:
        flash(e.message, "error")

    # using the below
    # https://python-binance.readthedocs.io/en/latest/account.html#id2

    return redirect('/')



