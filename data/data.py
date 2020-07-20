from pycoingecko import CoinGeckoAPI
import pandas as pd
import numpy as np
import plotly.colors
from plotly.graph_objs import *
import datetime
from datetime import date, timedelta
from datetime import datetime as dt
from sklearn.preprocessing import MinMaxScaler
import talib as ta
from sklearn.preprocessing import MinMaxScaler
import time

#Initialize coingeckpo api
cg = CoinGeckoAPI()

#Get bitcoin prices
def get_btc_price(ids, vs_currencies):
    '''
    This method gets the current price of any crypto currency
    INPUT:
    ids - (str) the id of the cryptocurrency
    vs_currencies - (str) the currency format to return the price

    OUTPUT:
    price - (float) price of coin

    '''
    price = cg.get_price(ids='{}'.format(ids), vs_currencies='{}'.format(vs_currncies))
    return price

#Get Top 20 crypto coins in order of market_cap
def get_top_20_mc(order, vs_currency, per_page, page):
    '''
    This method gets the top 20 cryptocurrency according to market cap
    INPUT:
    order - (str) the order of the list returned
    vs_currencies - (str) the currency format to return the price
    per_page  - (str) the number of results per page
    page - (str) the page number you want to view
    OUTPUT:
    top_20_mc - (dataframe) top_20_mc coins in order of marketcap desc

    '''
    top_20_mc = cg.get_coins_markets(order = '{}'.format(order),
    vs_currency='{}'.format(vs_currency), per_page = '{}'.format(per_page),
    page = '{}'.format(page))
    top_20_mc = pd.DataFrame(top_20_mc)
    return top_20_mc


#Initialize today's date for future use in app
today = datetime.date.today()

#Initialize the date bitcoin prices started  getting logged
origin_btc = pd.to_datetime('03/01/2009').date()

#Get historic daily bitcoin close prices
def get_historic_btc_price(id, vs_currency):
    '''
    This method gets the historic bitcoin price from the date of origin.
    Can be used for other coins
    INPUT:
    id - (str) the id of the cryptocurrency. in this case 'bitcoin'
    vs_currencies - (str) the currency format to return the price
    OUTPUT:
    historic_btc_price - (dataframe) contains historic bitcoin price and tidy data

    '''

    origin_btc = pd.to_datetime('03/01/2009').date()
    n_days = (today -origin_btc).days
    historic_bitcoin_price = cg.get_coin_market_chart_by_id(id = '{}'.format(id),
    vs_currency = '{}'.format(vs_currency), days = '{}'.format(n_days))
    historic_bitcoin_price = pd.DataFrame(historic_bitcoin_price)
    #tidy price column and extract timestamp
    prices = historic_bitcoin_price.prices.astype(str)
    prices = prices.str.split(',', expand=True)
    prices.columns = ['timestamp', 'price']
    prices['timestamp'] = prices.timestamp.str.replace('[', '')
    prices['timestamp'] = prices.timestamp.apply(lambda x: x[:-3])
    prices['price'] = prices.price.str.replace(']', '')
    prices['price'] = prices.price.astype(float)

    #tidy market_caps column and remove timestamp
    market_caps = historic_bitcoin_price.market_caps.astype(str)
    market_caps = market_caps.str.split(',', expand=True)
    market_caps.columns = ['timestamp', 'market_cap']
    market_caps = market_caps.drop('timestamp', axis =1)
    market_caps['market_cap'] = market_caps.market_cap.str.replace(']', '')

    #tidy total_volume column and remove timestamp
    total_volume = historic_bitcoin_price.total_volumes.astype(str)
    total_volume = total_volume.str.split(',', expand=True)
    total_volume.columns = ['timestamp', 'total_volume']
    total_volume = total_volume.drop('timestamp', axis =1)
    total_volume['total_volume'] = total_volume.total_volume.str.replace(']', '')
    total_volume['total_volume'] = total_volume['total_volume'].replace(' None', np.NaN)
    total_volume['total_volume'] = total_volume['total_volume'].fillna('0.0').astype(float)
    total_volume['total_volume'] = total_volume['total_volume'].fillna(method ='bfill')

    #concat price, market_caps and total_volume column and drop doplicates
    historic_btc_price = pd.concat([prices, market_caps, total_volume], axis = 1).drop_duplicates()
    #tidy date column
    historic_btc_price['timestamp'] = historic_btc_price.timestamp.astype(int)
    historic_btc_price['date'] = pd.to_datetime(historic_btc_price.timestamp, unit='s')
    historic_btc_price['day'] = historic_btc_price.date.dt.day
    historic_btc_price['month'] = historic_btc_price.date.dt.month
    historic_btc_price['year'] = historic_btc_price.date.dt.year
    historic_btc_price['date_clean'] = historic_btc_price.date.dt.date
    #prepare data for analysis by setting the date column to datetime index
    historic_btc_price['date_clean'] = pd.to_datetime(historic_btc_price.date_clean)
    historic_btc_price = historic_btc_price.set_index('date_clean')
    historic_btc_price['day_of_week'] = historic_btc_price.date.dt.day_name()

    return historic_btc_price
#Initialize historic_btc_price for future use
historic_btc_price = get_historic_btc_price('bitcoin', 'gbp')

#plot Top 20 crypto coins in order of market_cap
def plot_top_20_mc():
    '''
    This method plots the top 20 cryptocurrencies in order of market cap
    INPUT:
    None
    OUTPUT:
    Plot of the top 20 cryptocurrencies in order of market cap
    '''

    top_mc = top_20_mc[['id', 'symbol', 'current_price', 'market_cap']].sort_values(by = 'market_cap',
    ascending = False)
    top_mc['market_cap'] = (top_mc.market_cap)/1000000000
    plt.bar(top_mc.id, top_mc.market_cap)
    plt.xticks(rotation=90)
    plt.ylabel('Marketcap (£Bn)')
    plt.xlabel('Date')
    plt.title('Top 20 market cap cryptocurrency by market cap(£Bn)')
    plt.show()

#plot Top 20 crypto coins in order of volume
def plot_top_20_volume():
    '''
    This method plots the top 20 cryptocurrencies in order of volume
    INPUT:
    None
    OUTPUT:
    Plot of the top 20 cryptocurrencies in order of volume
    '''
    top_volume = top_20_mc[['id', 'symbol', 'total_volume']].sort_values(by = 'total_volume',
    ascending = False)
    top_volume['total_volume'] = (top_volume.total_volume)/1000000
    plt.bar(top_volume.id, top_volume.total_volume)
    plt.xticks(rotation=90)
    plt.ylabel('Marketcap (£m)')
    plt.xlabel('Date')
    plt.title('Top 20 market cap cryptocurrency volume(£m)')
    plt.show()

#plot historic bitcoin price
def plot_historic_btc_price():
    '''
    This method plots the historic bitcoin price
    INPUT:
    None
    OUTPUT:
    Plot of the historic bitcoin price
    '''

    plt.plot(historic_btc_price.date_clean, historic_btc_price.price.astype(float))
    plt.xticks(rotation=90)
    plt.ylabel('BTC Price (£m)')
    plt.xlabel('Date')
    plt.title('Historic BTC price(£)')
    plt.show()

#Get 90-Day bitcoin price candlesticks with minutely data
def get_btc_candlesticks(id, vs_currency):
    '''
    This method gets the 90 day OHLC data for bitcoin
    INPUT:
    id - (str) the id of the cryptocurrency. in this case 'bitcoin'
    vs_currencies - (str) the currency format to return the price
    OUTPUT:
    price_ohlc_reindex - (dataframe) contains 90 day OHLC data for bitcoin
    '''

    n = 90
    date_N_days_ago = dt.now() - timedelta(days=n)

    today_timestamp = pd.Timestamp(today).timestamp()
    date_N_days_ago_timestamp = pd.Timestamp(date_N_days_ago).timestamp()

    #Extract btc minutely data and tidy data
    bitcoin_price_date_N_days_ago = cg.get_coin_market_chart_range_by_id(id = '{}'.format(id),
    vs_currency = '{}'.format(vs_currency), from_timestamp = date_N_days_ago_timestamp,
    to_timestamp = today_timestamp)
    bitcoin_price_date_N_days_ago = pd.DataFrame(bitcoin_price_date_N_days_ago)
    prices_ohlc = bitcoin_price_date_N_days_ago.prices.astype(str)
    prices_ohlc = prices_ohlc.str.split(',', expand=True)
    prices_ohlc.columns = ['timestamp', 'price']

    #Tidy timestamp and price data
    prices_ohlc['timestamp'] = prices_ohlc.timestamp.str.replace('[', '')
    prices_ohlc['timestamp'] = prices_ohlc.timestamp.apply(lambda x: x[:-3])
    prices_ohlc['price'] = prices_ohlc.price.str.replace(']', '')
    prices_ohlc['price'] = prices_ohlc.price.astype(float)

    #tidy market_caps and remove timestamp
    market_caps_ohlc = bitcoin_price_date_N_days_ago.market_caps.astype(str)
    market_caps_ohlc = market_caps_ohlc.str.split(',', expand=True)
    market_caps_ohlc.columns = ['timestamp', 'market_cap']
    market_caps_ohlc = market_caps_ohlc.drop('timestamp', axis =1)
    market_caps_ohlc['market_cap'] = market_caps_ohlc.market_cap.str.replace(']', '')
    #tidy total_volume and remove timestamp
    total_volume_ohlc = bitcoin_price_date_N_days_ago.total_volumes.astype(str)
    total_volume_ohlc = total_volume_ohlc.str.split(',', expand=True)
    total_volume_ohlc.columns = ['timestamp', 'total_volume']
    total_volume_ohlc = total_volume_ohlc.drop('timestamp', axis =1)
    total_volume_ohlc['total_volume'] = total_volume_ohlc.total_volume.str.replace(']', '')
    total_volume_ohlc['total_volume'] = total_volume_ohlc['total_volume'].replace(' None', np.NaN)
    total_volume_ohlc['total_volume'] = total_volume_ohlc['total_volume'].fillna('0.0').astype(float)
    total_volume_ohlc['total_volume'] = total_volume_ohlc['total_volume'].fillna(method ='bfill')

    #concat price, market_caps and total_volume
    bitcoin_price_date_N_days_ago = pd.concat([prices_ohlc, market_caps_ohlc, total_volume_ohlc], axis = 1)

    bitcoin_price_date_N_days_ago['timestamp'] = bitcoin_price_date_N_days_ago.timestamp.astype(int)
    bitcoin_price_date_N_days_ago['date'] = pd.to_datetime(bitcoin_price_date_N_days_ago.timestamp, unit='s')
    bitcoin_price_date_N_days_ago['day'] = bitcoin_price_date_N_days_ago.date.dt.day
    bitcoin_price_date_N_days_ago['month'] = bitcoin_price_date_N_days_ago.date.dt.month
    bitcoin_price_date_N_days_ago['year'] = bitcoin_price_date_N_days_ago.date.dt.year
    bitcoin_price_date_N_days_ago['date_clean'] = bitcoin_price_date_N_days_ago.date.dt.date
    bitcoin_price_date_N_days_ago['time'] = bitcoin_price_date_N_days_ago.date.dt.time
    bitcoin_price_date_N_days_ago['day_of_week'] = bitcoin_price_date_N_days_ago.date.dt.day_name()

    #reindex bitcoin price data by date and convert to ohlc data
    price_ohlc_reindex = bitcoin_price_date_N_days_ago.set_index('date')['price'].resample('D').ohlc()
    return price_ohlc_reindex

#Perform SMA analysis to determine buy and sell signals

def SMA(close,sPeriod,lPeriod):
    '''
    This creates the simple moving average data for historic bitcoin data
    INPUT:
    close - (series) the daily close price of bitcoin
    sPeriod - (int)  the short SMA period
    lPeriod - (int)  the long SMA period
    OUTPUT:
    smaSell - categorical series indicating when to sell
    smaBuy - categorical series indicating when to buy
    shortSMA - Series containing the shortSMA calculations
    longSMA - Series containing the longSMA calculations
    '''
    shortSMA = ta.SMA(close,sPeriod)
    longSMA = ta.SMA(close,lPeriod)
    smaSell = ((shortSMA <= longSMA) & (shortSMA.shift(1) >= longSMA.shift(1)))
    smaBuy = ((shortSMA >= longSMA) & (shortSMA.shift(1) <= longSMA.shift(1)))
    return smaSell,smaBuy,shortSMA,longSMA

def SMA_signals(close, sPeriod, lPeriod):
    '''
    This creates the simple moving average signals for historic bitcoin data
    INPUT:
    close - (series) the daily close price of bitcoin
    sPeriod - (int)  the short SMA period
    lPeriod - (int)  the long SMA period
    OUTPUT:
    signals_SMA - (dataframe) merged buy and sell signal from SMA analysis
    '''
    #tidy SMA data to plot
    smaSell,smaBuy,shortSMA,longSMA = SMA(close, sPeriod, lPeriod)
    signals_SMA = pd.concat([smaSell, smaBuy, shortSMA, longSMA, close], axis = 1, keys = ['smaSell', 'smaBuy', 'shortSMA', 'longSMA', 'close'])
    signals_SMA['position'] = 0
    row_indexes=signals_SMA[signals_SMA['smaSell']==True].index
    signals_SMA.loc[row_indexes,'position']= -1
    row_indexes=signals_SMA[signals_SMA['smaBuy']==True].index
    signals_SMA.loc[row_indexes,'position']= 1
    signals_SMA['date'] = signals_SMA.index
    signals_SMA['date'] = pd.to_datetime(signals_SMA.date)
    signals_SMA['year'] = signals_SMA.date.dt.year
    signals_SMA['month'] = signals_SMA.date.dt.month
    signals_SMA['day_of_week'] = signals_SMA.date.dt.day_name()
    signals_SMA.drop('date', axis = 1, inplace = True)
    return signals_SMA

def plot_SMA(close, sPeriod, lPeriod):
    '''
    This creates the simple moving average plot for historic bitcoin data
    INPUT:
    close - (series) the daily close price of bitcoin
    sPeriod - (int)  the short SMA period
    lPeriod - (int)  the long SMA period
    OUTPUT:
    plot showing the simple moving average for historic bitcoin data
    '''
    signals_SMA = SMA_signals(close, sPeriod, lPeriod)
    # Plot the closing price and visualise signals for SMA
    plt.plot(historic_btc_price['price'], lw=2., color = 'purple')
    # Plot the short and long moving averages
    plt.plot(signals_SMA[['shortSMA', 'longSMA']], lw=2.)
    # Plot the buy signals
    plt.plot(signals_SMA.loc[signals_SMA.position == 1.0].index,
             signals_SMA.shortSMA[signals_SMA.position == 1.0],
             '^', markersize=10, color='green')
    # Plot the sell signals
    plt.plot(signals_SMA.loc[signals_SMA.position == -1.0].index,
             signals_SMA.shortSMA[signals_SMA.position == -1.0],
             'v', markersize=10, color='red')
    # Show the plot
    plt.show()

def create_SMA_portfolio(close, sPeriod, lPeriod):
    '''
    This creates the simple moving average portfolio to calculate returns
    INPUT:
    close - (series) the daily close price of bitcoin
    sPeriod - (int)  the short SMA period
    lPeriod - (int)  the long SMA period
    OUTPUT:
    portfolio - (dataframe) simulation of a portfolio that buys and sells according
    to SMA signals
    '''
    signals_SMA = SMA_signals(close, sPeriod, lPeriod)
    # Create portfolio and Set the initial capital SMA
    initial_capital= float(150000.0)
    # Create a DataFrame `positions`
    positions = pd.DataFrame(index=signals_SMA.index).fillna(0.0)
    # Buy a 20 bitcoin
    positions['btc'] = 20*signals_SMA['position']
    # Initialize the portfolio with value owned
    portfolio = positions.multiply(historic_btc_price['price'], axis=0)
    # Store the difference in shares owned
    pos_diff = positions.diff()
    # Add `holdings` to portfolio
    portfolio['holdings'] = (positions.multiply(historic_btc_price['price'], axis=0)).sum(axis=1)
    # Add `cash` to portfolio
    portfolio['cash'] = initial_capital - (pos_diff.multiply(historic_btc_price['price'], axis=0)).sum(axis=1).cumsum()
    # Add `total` to portfolio
    portfolio['total'] = portfolio['cash'] + portfolio['holdings']
    # Add `returns` to portfolio
    portfolio['returns'] = portfolio['total'].pct_change()
    portfolio['date'] = portfolio.index
    portfolio['date'] = pd.to_datetime(portfolio.date)
    portfolio['year'] = portfolio.date.dt.year
    portfolio['month'] = portfolio.date.dt.month
    portfolio['day_of_week'] = portfolio.date.dt.day_name()
    # Print the first lines of `portfolio`
    return portfolio


origin = pd.to_datetime('2013-04-28')
def calculate_SMA_pct_change(close, sPeriod, lPeriod):
    '''
    This calculates the returns from investing in the SMA buy and sell signals
    INPUT:
    close - (series) the daily close price of bitcoin
    sPeriod - (int)  the short SMA period
    lPeriod - (int)  the long SMA period
    OUTPUT:
    avg_pct_change - (int) the avg yearly percentage returns according
    to SMA signals
    total_pct_change - (int) the total percentage returns according
    to SMA signals
    '''
    portfolio = create_SMA_portfolio(close, sPeriod, lPeriod)
    avg_pct_change = ((((portfolio.loc[today]['total']).drop_duplicates() - (portfolio.loc[origin]['total']))/portfolio.loc[origin]['total'])/(portfolio.year.max() - portfolio.year.min()))*100
    total_pct_change = ((((portfolio.loc[today]['total']).drop_duplicates() - (portfolio.loc[origin]['total']))/portfolio.loc[origin]['total']))*100
    avg_pct_change  = avg_pct_change.values[0]
    total_pct_change = total_pct_change.values[0]

    return avg_pct_change, total_pct_change

def plot_SMA_returns(close, sPeriod, lPeriod):
    '''
    This calculates the returns from investing in the SMA buy and sell signals
    INPUT:
    close - (series) the daily close price of bitcoin
    sPeriod - (int)  the short SMA period
    lPeriod - (int)  the long SMA period
    OUTPUT:
    Scaled plot showing the SMA portfolio returns compared with the price of bitcoin
    '''
    portfolio = create_SMA_portfolio(close, sPeriod, lPeriod)
    scaler = MinMaxScaler()
    plt.plot(scaler.fit_transform(historic_btc_price['price'].values.reshape(-1, 1)), lw=2., color = 'purple')
    plt.plot(scaler.fit_transform(portfolio.total.values.reshape(-1, 1)))
    plt.show()


#perform RSI analysis
def RSI(close,timePeriod):
    '''
    This creates the relative strength index data for historic bitcoin data
    INPUT:
    close - (series) the daily close price of bitcoin
    timePeriod - (int)  timePeriod to base RSI calculations on
    OUTPUT:
    rsiSell - categorical series indicating when to sell
    rsiBuy - categorical series indicating when to buy
    rsi - Series containing the rsi calculations
    '''
    rsi = ta.RSI(close,timePeriod)
    rsiSell = (rsi>80) & (rsi.shift(1)<=80)
    rsiBuy = (rsi<20) & (rsi.shift(1)>=20)
    return rsiSell,rsiBuy, rsi


def RSI_signals(close, timePeriod):
    '''
    This creates the RSI signals for historic bitcoin data
    INPUT:
    close - (series) the daily close price of bitcoin
    timePeriod - (int)  timePeriod to base RSI calculations on
    OUTPUT:
    signals_RSI - (dataframe) merged buy and sell signal from RSI analysis
    '''
    rsiSell,rsiBuy, rsi = RSI(close, timePeriod)
    #tidy RSI data to plot
    signals_RSI = pd.concat([rsiSell,rsiBuy, rsi, close], axis = 1, keys = ['rsiSell','rsiBuy', 'rsi', 'close'])
    signals_RSI['position'] = 0
    row_indexes=signals_RSI[signals_RSI['rsiSell']==True].index
    signals_RSI.loc[row_indexes,'position']= 1
    row_indexes=signals_RSI[signals_RSI['rsiBuy']==True].index
    signals_RSI.loc[row_indexes,'position']= -1
    return signals_RSI


def plot_RSI(close, timePeriod):
    '''
    This creates the RSI plot for historic bitcoin data
    INPUT:
    close - (series) the daily close price of bitcoin
    timePeriod - (int)  timePeriod to base RSI calculations on
    OUTPUT:
    plot showing the RSI for historic bitcoin data
    '''
    signals_RSI = RSI_signals(close, timePeriod)
    # Plot the closing price and visualise signals for RSI
    plt.plot(historic_btc_price['price'], lw=2., color = 'purple')
    # Plot the short and long moving averages
    plt.plot(signals_RSI['rsi'], lw=2.)
    # Plot the buy signals
    plt.plot(signals_RSI.loc[signals_RSI.position == -1.0].index,
             signals_RSI.rsi[signals_RSI.position == -1.0],
             '^', markersize=10, color='red')
    # Plot the sell signals
    plt.plot(signals_RSI.loc[signals_RSI.position == 1.0].index,
             signals_RSI.rsi[signals_RSI.position == 1.0],
             'v', markersize=10, color='green')
    # Show the plot
    plt.show()


def create_RSI_portfolio(close, timePeriod):
    '''
    This creates the relative strength index portfolio to calculate returns
    INPUT:
    close - (series) the daily close price of bitcoin
    timePeriod - (int)  timePeriod to base RSI calculations on
    OUTPUT:
    portfolio - (dataframe) simulation of a portfolio that buys and sells according
    to RSI signals
    '''
    signals_RSI = RSI_signals(close, timePeriod)
    # Create portfolio and Set the initial capital RSI
    initial_capital= float(150000.0)
    # Create a DataFrame `positions`
    positions = pd.DataFrame(index=signals_RSI.index).fillna(0.0)
    # Buy a 20 bitcoin
    positions['btc'] = 20*signals_RSI['position']
    # Initialize the portfolio with value owned
    portfolio = positions.multiply(historic_btc_price['price'], axis=0)
    # Store the difference in shares owned
    pos_diff = positions.diff()
    # Add `holdings` to portfolio
    portfolio['holdings'] = (positions.multiply(historic_btc_price['price'], axis=0)).sum(axis=1)
    # Add `cash` to portfolio
    portfolio['cash'] = initial_capital - (pos_diff.multiply(historic_btc_price['price'], axis=0)).sum(axis=1).cumsum()
    # Add `total` to portfolio
    portfolio['total'] = portfolio['cash'] + portfolio['holdings']
    # Add `returns` to portfolio
    portfolio['returns'] = portfolio['total'].pct_change()
    portfolio['date'] = portfolio.index
    portfolio['date'] = pd.to_datetime(portfolio.date)
    portfolio['year'] = portfolio.date.dt.year
    portfolio['month'] = portfolio.date.dt.month
    portfolio['day_of_week'] = portfolio.date.dt.day_name()
    # Print the first lines of `portfolio`
    return portfolio

def calculate_RSI_pct_change(close, timePeriod):
    '''
    This calculates the returns from investing in the SMA buy and sell signals
    INPUT:
    close - (series) the daily close price of bitcoin
    timePeriod - (int)  timePeriod to base RSI calculations on
    OUTPUT:
    avg_pct_change - (int) the avg yearly percentage returns according
    to RSI signals
    total_pct_change - (int) the total percentage returns according
    to RSI signals
    '''
    portfolio = create_RSI_portfolio(close, timePeriod)
    avg_pct_change = ((((portfolio.loc[today]['total']).drop_duplicates() - (portfolio.loc[origin]['total']))/portfolio.loc[origin]['total'])/(portfolio.year.max() - portfolio.year.min()))*100
    total_pct_change = ((((portfolio.loc[today]['total']).drop_duplicates() - (portfolio.loc[origin]['total']))/portfolio.loc[origin]['total']))*100
    avg_pct_change  = avg_pct_change.values[0]
    total_pct_change = total_pct_change.values[0]

    return avg_pct_change, total_pct_change


def plot_RSI_returns(close, timePeriod):
    '''
    This calculates the returns from investing in the SMA buy and sell signals
    INPUT:
    close - (series) the daily close price of bitcoin
    timePeriod - (int)  timePeriod to base RSI calculations on
    OUTPUT:
    Scaled plot showing the RSI portfolio returns compared with the price of bitcoin
    '''
    portfolio = create_RSI_portfolio(close, timePeriod)
    scaler = MinMaxScaler()
    plt.plot(scaler.fit_transform(historic_btc_price['price'].values.reshape(-1, 1)), lw=2., color = 'purple')
    plt.plot(scaler.fit_transform(portfolio.total.values.reshape(-1, 1)))
    plt.show()




def return_figures():
    '''
    This returns all the figures for the flask app
    INPUT:
    None
    OUTPUT:
    Plots for flask app
    '''
    #Create Graph one
    graph_one = []
    df_one = get_top_20_mc('market_cap_desc',
    'gbp', 20, 1).sort_values(by = 'market_cap', ascending = False)
    print(df_one.columns)
    coin_list = df_one.id.tolist()
    print(coin_list)

    for coin in coin_list:
        x_val = df_one[df_one['id'] == coin]['id'].tolist()
        y_val = df_one[df_one['id'] == coin]['market_cap'].tolist()
        print(x_val)
        graph_one.append(
            Bar(
            x = x_val,
            y = y_val,
            name = coin
            )
        )

        layout_one = dict(title = "Top 20 cryptocurrencies in order of Marketcap",
                    xaxis = dict(title = 'cyptocurrency',
                      autotick=False),
                    yaxis = dict(title = 'Marketcap (£Bn)'),
                    )
    #Create Graph two
    graph_two = []
    df_two = df_one.sort_values(by = 'total_volume', ascending = False)
    coin_list = df_two.id.tolist()
    for coin in coin_list:
        x_val = df_two[df_two['id'] == coin].id.tolist()
        y_val = df_two[df_two['id'] == coin].total_volume.tolist()

        graph_two.append(
            Bar(
            x = x_val,
            y = y_val,
            name = coin
          )
        )

        layout_two = dict(title = 'Top 20 cryptocurrencies in order of current 24hr Volume',
                  xaxis = dict(title = 'cryptocurrency',
                    autotick=False),
                  yaxis = dict(title = 'Volume (£Bn)'),
                  )

    #Create Graph three
    graph_three = []
    df_three = historic_btc_price.groupby('year').mean()['price'].sort_values()
    year_list = df_three.index.tolist()
    for year in year_list:
        x_val = df_three[df_three.index == year].index.tolist()
        y_val = df_three[df_three.index == year].values.tolist()


        graph_three.append(
          Bar(
            x = x_val,
            y = y_val,
            name = year
          )
        )

        layout_three = dict(title = 'Average Yearly bitcoin price',
              xaxis = dict(title = 'Year',
                autotick=False),
              yaxis = dict(title = 'Average yearly bitcoin price (£)'),
              )

    #Create Graph four
    graph_four = []
    df_four = historic_btc_price.groupby('month').mean()['price'].sort_index()
    df_four.index = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
    'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    print(df_four)
    month_list = df_four.index.tolist()
    for month in month_list:
        x_val = df_four[df_four.index == month].index.tolist()
        y_val = df_four[df_four.index == month].values.tolist()


        graph_four.append(
          Bar(
            x = x_val,
            y = y_val,
            name = month
          )
        )

        layout_four = dict(title = 'Average monthly bitcoin price',
              xaxis = dict(title = 'Month',
                autotick=False),
              yaxis = dict(title = 'Average monthly bitcoin price (£)'),
              )



    #Create Graph five
    graph_five = []
    df_five = historic_btc_price.groupby('day_of_week').mean()['price'].sort_values()
    day_of_week = df_five.index.tolist()
    for day in day_of_week:
        x_val = df_five[df_five.index == day].index.tolist()
        y_val = df_five[df_five.index == day].values.tolist()


        graph_five.append(
          Bar(
            x = x_val,
            y = y_val,
            name = day
          )
        )

        layout_five = dict(title = 'Average bitcoin price for each day of the week (ASC)',
              xaxis = dict(title = 'Day_of_week',
                autotick=False),
              yaxis = dict(title = 'Average price (£)'),
              )

    #Create Graph five
    sma_range = 50
    log_yaxis = False
    df_six = get_btc_candlesticks('bitcoin', 'gbp')
    graph_six = []
    graph_six.append(Candlestick(x=df_six.index,
        open=df_six.open,
        high=df_six.high,
        low=df_six.low,
        close=df_six.close,
        name = '',
        )
    )



    for i in range(5, (sma_range + 1), 5):

        sma = Scatter(
            x = df_six.index,
            y = df_six.close.rolling(i).mean(), # Pandas SMA
            name = "SMA" + str(i),
            mode = "lines",
            line = dict(color = "green"),
            opacity = 0.7,
            visible = False,
        )
        graph_six.append(sma)


    #set up sliders
    sliders = dict(

        # GENERAL
        steps = [],
        currentvalue = dict(
            font = dict(size = 16),
            prefix = "SMA: ",
            xanchor = "left",
        ),

        # PLACEMENT
        x = 0.15,
        y = 0,
        len = 0.85,
        pad = dict(t = 0, b = 0),
        yanchor = "bottom",
        xanchor = "left",
    )

    for i in range((sma_range // 5) + 1):

        step = dict(
            method = "restyle",
            label = str(i * 5),
            value = str(i * 5),
            args = ["visible", [False] * ((sma_range // 5) + 1)], # Sets all to false
        )

        step['args'][1][0] = True # Main trace
        step['args'][1][i] = True # Selected trace through slider
        sliders["steps"].append(step)



    updatemenus = dict(

        # GENERAL
        type = "buttons",
        showactive = False,
        x = 0,
        y = 0,
        pad = dict(t = 0, b = 0),
        yanchor = "bottom",
        xanchor = "left",

        # BUTTONS
        buttons=[
            dict(
                method = "restyle",
                label = "Golden Cross",
                args = ["visible", [False] * ((sma_range // 5) + 1)],
            ),
            dict(
                method = "restyle",
                label = "Common SMAs",
                args = ["visible", [False] * ((sma_range // 5) + 1)],
            )
        ],

    )

    # Set all traces to invisible, then toggle these ones selectively

    # Golden cross refers to the 50SMA and 200SMA cross
    # and is an indicator of long term market support
    updatemenus["buttons"][0]["args"][1][0] = True # Main plot
    updatemenus["buttons"][0]["args"][1][1] = True # SMA 5
    updatemenus["buttons"][0]["args"][1][8] = True # SMA 40

    # Create layout
    layout_six = dict(

        title = 'Bitcoin 90 day data candlesticks',

        # GENERAL LAYOUT
        width = 1080,
        height = 720,
        autosize = True,
        font = dict(
            family = "Overpass",
            size = 12,
        ),
        margin = dict(
            t = 80,
            l = 50,
            b = 50,
            r = 50,
            pad = 5,
        ),
        showlegend = False,

        # ANIMATIONS
        sliders = [sliders],
        updatemenus = [updatemenus],

        # COLOR THEME
        plot_bgcolor = "#FFFFFF",
        paper_bgcolor = "#FAFAFA",

        # LINEAR PLOTS
        xaxis = dict(

            # RANGE
            range = [df_six.index.values[0], df_six.index.values[(len(df_six.index)-1)]],

            # RANGE SLIDER AND SELECTOR
            rangeslider = dict(
                bordercolor = "#FFFFFF",
                bgcolor = "#FFFFFF",
                thickness = 0.1,
            ),

            # Buttons for date range (1D, 5D, 1M, 3M, 6M, 1Y, 2Y, 5Y, Max, YTD)
            rangeselector = dict(
                activecolor = "#888888",
                bgcolor = "#DDDDDD",
                buttons = [
                    dict(count = 1, step = "day", stepmode = "backward", label = "1D"),
                    dict(count = 5, step = "day", stepmode = "backward", label = "5D"),
                    dict(count = 1, step = "month", stepmode = "backward", label = "1M"),
                    dict(count = 3, step = "month", stepmode = "backward", label = "3M"),
                    dict(count = 6, step = "month", stepmode = "backward", label = "6M"),
                    dict(count = 1, step = "year", stepmode = "backward", label = "1Y"),
                    dict(count = 2, step = "year", stepmode = "backward", label = "2Y"),
                    dict(count = 5, step = "year", stepmode = "backward", label = "5Y"),
                    dict(count = 1, step = "all", stepmode = "backward", label = "MAX"),
                    dict(count = 1, step = "year", stepmode = "todate", label = "YTD"),
                ]
            ),

        ),
        yaxis = dict(
            title = 'Bitcoin Price (£)',
            tickprefix = "£",
            type = "linear",
            domain = [0.25, 1],
        ),

    )

    if log_yaxis: layout["yaxis"]["type"] = "log"

    #Create Graph seven
    graph_seven = []
    df_seven = historic_btc_price
    df_seven_signals = SMA_signals(df_seven.price, 21, 49)
    print(df_seven.head())
    sma_range = 200
    log_yaxis = False
    trace_one = Scatter(x = df_seven.index.to_list(),
        y=df_seven.price.to_list(),
        visible=True,
        line={'color': 'blue'},
        name='btc',
        mode='lines',
        opacity = 0.7)
    trace_two = Scatter(x = df_seven.index.to_list(),
        y=df_seven_signals.shortSMA.to_list(),
        visible=True,
        line={'color': 'green'},
        name='smaShort(21)',
        opacity = 0.7,
        mode='lines')
    trace_three = Scatter(x = df_seven.index.to_list(),
        y=df_seven_signals.longSMA.to_list(),
        visible=True,
        line={'color': 'red'},
        name='smaLong(49)',
        opacity = 0.7,
        mode='lines')
    trace_four = Scatter(
        name = 'buy',
        mode = 'markers',
        x = df_seven_signals[df_seven_signals.smaBuy == True].index,
        y = df_seven_signals[df_seven_signals.smaBuy == True].close,
        marker = dict(
        color = 'green',
        size = 5,
        )
    )
    trace_five = Scatter(
        name = 'sell',
        mode = 'markers',
        x = df_seven_signals[df_seven_signals.smaSell == True].index,
        y = df_seven_signals[df_seven_signals.smaSell == True].close,
        marker = dict(
        color = 'red',
        size = 5
        ),
    )
    graph_seven = [trace_one, trace_two, trace_three, trace_four, trace_five]

    # Create layout
    layout_seven = dict(

        title = 'Bitcoin historic price with SMA(14) and SMA(49) signals',

        # GENERAL LAYOUT
        width = 1080,
        height = 720,
        autosize = True,
        font = dict(
            family = "Overpass",
            size = 12,
        ),
        margin = dict(
            t = 80,
            l = 50,
            b = 50,
            r = 50,
            pad = 5,
        ),
        showlegend = True,


        # COLOR THEME
        plot_bgcolor = "#FFFFFF",
        paper_bgcolor = "#FAFAFA",

        # LINEAR PLOTS
        xaxis = dict(

            # RANGE
            range = [df_seven.index.values[0], df_seven.index.values[(len(df_seven.index)-1)]],

            # RANGE SLIDER AND SELECTOR
            rangeslider = dict(
                bordercolor = "#FFFFFF",
                bgcolor = "#FFFFFF",
                thickness = 0.1,
            ),

            # Buttons for date range (1D, 5D, 1M, 3M, 6M, 1Y, 2Y, 5Y, Max, YTD)
            rangeselector = dict(
                activecolor = "#888888",
                bgcolor = "#DDDDDD",
                buttons = [
                    dict(count = 1, step = "day", stepmode = "backward", label = "1D"),
                    dict(count = 5, step = "day", stepmode = "backward", label = "5D"),
                    dict(count = 1, step = "month", stepmode = "backward", label = "1M"),
                    dict(count = 3, step = "month", stepmode = "backward", label = "3M"),
                    dict(count = 6, step = "month", stepmode = "backward", label = "6M"),
                    dict(count = 1, step = "year", stepmode = "backward", label = "1Y"),
                    dict(count = 2, step = "year", stepmode = "backward", label = "2Y"),
                    dict(count = 5, step = "year", stepmode = "backward", label = "5Y"),
                    dict(count = 1, step = "all", stepmode = "backward", label = "MAX"),
                    dict(count = 1, step = "year", stepmode = "todate", label = "YTD"),
                ]
            ),

        ),
        yaxis = dict(
            title = 'Bitcoin Price (£)',
            tickprefix = "£",
            type = "linear",
            domain = [0.25, 1],
        ),

    )

    if log_yaxis: layout["yaxis"]["type"] = "log"

    #Create Graph eight
    graph_eight = []
    df_eight = historic_btc_price
    df_eight_signals = RSI_signals(df_eight.price, 14)
    print(df_eight.head())
    log_yaxis = False
    trace_one = Scatter(x = df_eight.index.to_list(),
        y=df_eight.price.to_list(),
        visible=True,
        line={'color': 'blue'},
        name='btc',
        mode='lines',
        opacity = 0.7)
    trace_two = Scatter(
        name = 'buy',
        mode = 'markers',
        x = df_eight_signals[df_eight_signals.rsiBuy == True].index,
        y = df_eight_signals[df_eight_signals.rsiBuy == True].close,
        marker = dict(
        color = 'green',
        size = 5,
        )
    )
    trace_three = Scatter(
        name = 'sell',
        mode = 'markers',
        x = df_eight_signals[df_eight_signals.rsiSell == True].index,
        y = df_eight_signals[df_eight_signals.rsiSell == True].close,
        marker = dict(
        color = 'red',
        size = 5
        ),
    )
    graph_eight = [trace_one, trace_two, trace_three]


    # Create layout
    layout_eight = dict(

        title = 'Bitcoin historic price RSI buy sell signals',

        # GENERAL LAYOUT
        width = 1080,
        height = 720,
        autosize = True,
        font = dict(
            family = "Overpass",
            size = 12,
        ),
        margin = dict(
            t = 80,
            l = 50,
            b = 50,
            r = 50,
            pad = 5,
        ),
        showlegend = True,


        # COLOR THEME
        plot_bgcolor = "#FFFFFF",
        paper_bgcolor = "#FAFAFA",

        # LINEAR PLOTS
        xaxis = dict(

            # RANGE
            range = [df_eight.index.values[0], df_eight.index.values[(len(df_eight.index)-1)]],

            # RANGE SLIDER AND SELECTOR
            rangeslider = dict(
                bordercolor = "#FFFFFF",
                bgcolor = "#FFFFFF",
                thickness = 0.1,
            ),

            # Buttons for date range (1D, 5D, 1M, 3M, 6M, 1Y, 2Y, 5Y, Max, YTD)
            rangeselector = dict(
                activecolor = "#888888",
                bgcolor = "#DDDDDD",
                buttons = [
                    dict(count = 1, step = "day", stepmode = "backward", label = "1D"),
                    dict(count = 5, step = "day", stepmode = "backward", label = "5D"),
                    dict(count = 1, step = "month", stepmode = "backward", label = "1M"),
                    dict(count = 3, step = "month", stepmode = "backward", label = "3M"),
                    dict(count = 6, step = "month", stepmode = "backward", label = "6M"),
                    dict(count = 1, step = "year", stepmode = "backward", label = "1Y"),
                    dict(count = 2, step = "year", stepmode = "backward", label = "2Y"),
                    dict(count = 5, step = "year", stepmode = "backward", label = "5Y"),
                    dict(count = 1, step = "all", stepmode = "backward", label = "MAX"),
                    dict(count = 1, step = "year", stepmode = "todate", label = "YTD"),
                ]
            ),

        ),
        yaxis = dict(
            title = 'Bitcoin Price (£)',
            tickprefix = "£",
            type = "linear",
            domain = [0.25, 1],
        ),

    )

    if log_yaxis: layout["yaxis"]["type"] = "log"

    #Create Graph Nine
    avg_yearly_gains_SMA, total_gains_SMA = calculate_SMA_pct_change(historic_btc_price.price, 21,49)
    avg_yearly_gains_RSI, total_gains_RSI = calculate_RSI_pct_change(historic_btc_price.price, 14)
    graph_nine = Figure(data=[Table(header=dict(values=['Model', 'avg_yearly_gains_pct', 'total_gains_pct']),
                 cells=dict(values=[['SMA', 'RSI'], [avg_yearly_gains_SMA, avg_yearly_gains_RSI],
                 [total_gains_SMA, total_gains_RSI]]))
                     ],
                     layout = dict(
                     title = 'Performance for SMA and RSI'
                     ))

    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))
    figures.append(dict(data=graph_five, layout=layout_five))
    figures.append(dict(data=graph_six, layout=layout_six))
    figures.append(dict(data=graph_seven, layout=layout_seven))
    figures.append(dict(data=graph_eight, layout=layout_eight))
    figures.append(dict(data=graph_nine))
    return figures
