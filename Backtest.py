# Dans la console il faut faire
# sudo pip3 install bta-lib
# sudo pip3 install backtrader
# sudo pip3 install matplotlib==3.2.2

import btalib
import backtrader as bt
import datetime

class RSIStrategy(bt.Strategy):

    def __init__(self):
        self.rsi = bt.talib.RSI(self.data, period=5)
    
    def next(self):
        if self.rsi < 40 and not self.position:
            self.buy(size=0.01)

        if self.rsi > 60 and self.position:
            self.close()


cerebro = bt.Cerebro() # create a "Cerebro" engine instance

cerebro.broker.setcash(200000000.0)

data = bt.feeds.GenericCSVData(dataname='Final/candles_custom.csv', dtformat=2, compression=15, timeframe=bt.TimeFrame.Minutes) # Create a data feed
# compression 15 signifit que le timeframe utilise est de 15 unite de timeframe
# pour 15minutes on va utiliser setup le timeframe a minute

# si l'on veut garder le meme fichier de dataset mais que l'on veut limiter l'analys
# a un range de date bien definie
# fromdate = datetime.datetime.strptime('2021-03-10', '%Y-%m-%d') 
# todate = datetime.datetime.strptime('2021-03-18', '%Y-%m-%d') 
# data = bt.feeds.GenericCSVData(dataname='15minute.csv', dtformat=2, compression=15, timeframe=bt.TimeFrame.Minutes, fromdate=fromdate, todate=todate) 


cerebro.adddata(data) # Add the data feed
cerebro.addstrategy(RSIStrategy) # Add the trading strategy
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue()) # Cash at start
cerebro.run() # run it all
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue()) # Cash at end
cerebro.plot()  # and plot it with a single command
