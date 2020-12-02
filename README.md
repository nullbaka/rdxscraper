# Project RDX

A take home task for interview at RD&X



## Enviroment

This project is written in Python@3.8.6

* Make python virtual environment: `python3 -m venv venv`
* Activate venv: `source venv/bin/activate`
* Install the requirements: `pip install -r requirements.txt`
* Install [mongodb](https://docs.mongodb.com/manual/administration/install-community/) `version 4.4`

I used [Robo 3T](https://robomongo.org/download), a GUI for mongodb to visualize my collections.



## Usage

* There are four spiders: **timesofindia**, **firstpost**, **indianexpress**, **moneycontrol**.
* To run them in default mode, simply command: `scrapy crawl <name_of_spider>`.
* To run on news category use `-a category=<category>`: `scrapy crawl indianexpress -a category=sports`
* **moneycontrol** and **timesofindia** support `pages` as an option. **firstpost** and **indianexpress** do not support this option
* To stop crawling during the process, press `Ctrl`+`C`

### Options
* **timesofindia**: `business` (default)
* **firstpost**: `all` (default), `news`, `sports`, `business`
* **indiaexpress**: `all` (default), `news`, `sports`, `business`
* **moneycontrol**: `all` (default), `markets`, `mutual-funds`
