WORLDBANK DATA DASHBOARD
-----------------------
Create a dashboard to visualise WorldBank data for easy analysis.
App should run on browser displaying dashboard


Related Blog
----------------------
https://medium.com/@deogakofiofuafor/airbnb-seattle-for-better-understanding-21b1132ee69f

Installation
----------------------

### Clone Repo

* Clone this repo to your computer.
* `myapp.py` is the executable for the app
* `data` folder contains three datasets
    * `data.py`: Extracts data from worldbank API using country codes and indicators. Instructions on how to use the API can be found on https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structures
      * `data.py` contains a `return_figures` method that returns the json figures to plot in graphs
  * `myapp` folder contains
    * `static`: Folder containing all image files
    * `templates`: Folder containing `index.html` homepage which renders when you run the app. It was designed with bootstrap
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

* Include more indicators in the  dataset
* Include more graphs
* Improve HTML layout and introduce filters to graphs using ginger





## Credits

Lead Developer - Deoga Kofi


## License

The MIT License (MIT)

Copyright (c) 2020 Deoga Kofi

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
