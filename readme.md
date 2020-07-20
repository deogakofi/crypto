CRYPTO DASHBOARD
-----------------------
Motivation
------------
Having previously dabbled in the trading of cryptocurrency in 2016 before the huge boom and bust, I have always wondered if there was a less risky way to reap the benefits of trading and if there was a way to know when to buy or sell.

If there was a system to do this then everyone would be doing it and be rich by now but the reality is, it is possible to build a system to buy and sell crypto but the performance will depend on the quality of data and methodology chosen.

Approach
-----------
There are a few approaches that can be taken to build the system.
* Sentiment analysis - Scraping for sentiments on the coin and analysing to make trading decisions
* Technical analysis - Using the historical price of the coin to make trading decisions
* A combination of both

I decided to go for the latter for proof of concept as there is more readily available data for free to explore this method.

Techniques
-------------
During technical analysis the following systems were used to make trading decisions:
* SMA - Using simple moving averages to determine when to buy or sell based on the intercept of the short and long moving averages.

* RSI - Performing relative strength analysis on a 14 day cycle and using a threshold of 80%

Traditional machine learning was not used for this project because it doesn't add any real life value to trading as it simply applies a smoothing curve with no logic.

Performance of Models
-------------------------
* SMA - Average year gains = 0.6966840372094414%
        Total gains = 4.87678826046609%
* RSI - Average year gains = 3.1764317126603365%
        Total gains = 22.235021988622357%


Related Blog
----------------------
https://medium.com/@deogakofiofuafor/airbnb-seattle-for-better-understanding-21b1132ee69f

Installation
----------------------

### Clone Repo

* Clone this repo to your computer.
* `myapp.py` is the executable for the app

* `data` folder contains three datasets
    * `data.py`: Extracts data from coingecko API.
    Instructions on how to use the API can be found on https://www.coingecko.com/en/api
      * `data.py` contains
      * `get_btc_price`: This method returns the current price of any crypto currency
      * `get_top_20_mc`: This method returns the top 20 cryptocurrency according to market cap in a dataframe
      * `get_historic_btc_price`: This method returns the historic bitcoin price from the date of origin. Can be used for other coins
      * `plot_top_20_mc`: This method plots the top 20 cryptocurrencies in order of market cap
      * `plot_top_20_volume`: This method plots the top 20 cryptocurrencies in order of volume
      * `plot_historic_btc_price`: This method plots the historic bitcoin price
      * `get_btc_candlesticks`: This method gets the 90 day OHLC data for bitcoin
      * `SMA`: This creates the simple moving average data for historic bitcoin data
      * `SMA_signals`: This creates the simple moving average signals for historic bitcoin data
      * `plot_SMA`: This creates the simple moving average plot for historic bitcoin data
      * `create_SMA_portfolio`: This creates the simple moving average portfolio to calculate returns
      * `calculate_SMA_pct_change`: This calculates the returns from investing in the SMA buy and sell signals
      * `plot_SMA_returns`: This calculates the returns from investing in the SMA buy and sell signals
      * `RSI`: This creates the relative strength index data for historic bitcoin data
      * `RSI_signals`: This creates the relative strength index signals for historic bitcoin data
      * `plot_RSI`: This creates the relative strength index plot for historic bitcoin data
      * `create_RSI_portfolio`: This creates the relative strength index portfolio to calculate returns
      * `calculate_RSI_pct_change`: This calculates the returns from investing in the RSI buy and sell signals
      * `plot_RSI_returns`: This calculates the returns from investing in the RSI buy and sell signals
      * `return_figures`: method that returns the json figures to plot in graphs

  * `myapp` folder contains
    * `static`: Folder containing all image files
    * `templates`: Folder containing
      * `index.html` homepage which renders when you run the app. It was designed with bootstrap
      * `trade_view.html` tradeview for bitcoin which renders when you run the app
    * `__init__.py`: Initiate flask app
    * `routes.py`: Defines the app routes
* It is recommended you run the solution in a virtual environment. Please see https://docs.python.org/3/library/venv.html


### Install the requirements
* For mac please ensure you have xcode or download it from the app store (probably not needed)
* From your CLI install homebrew using `/usr/bin/ruby -e "$(curl -fsSL https:/raw.githubusercontent.com/Homebrew/install/master/install)"`
* After installing homebrew successfully, install python3 using `brew install python3`
* Check python3 installed correctly using `python3 --version` and this should return python3 version
* Install the requirements using `pip3 install -r requirements.txt`.
    * Make sure you use Python 3
* `cd` to the location of myapp.py (should be located in parent folder)
* Execute `python3 myapp.py`
* Follow the information printed in your environment to the site. Usually 0.0.0.0:3001 or localhost:3001


Extending this
-------------------------

If you want to extend this work, here are a few places to start:

* Get access to API with more detailed data preferably shorter ticks
* Include more graphs
* Improve buy and sell signals and explore more methods





## Credits

Lead Developer - Deoga Kofi


## License

The MIT License (MIT)

Copyright (c) 2020 Deoga Kofi

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
