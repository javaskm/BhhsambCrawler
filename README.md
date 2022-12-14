# BHHSAMB Crawler

## Installation

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/javaskm/BhhsambCrawler.git
$ cd BhhsambCrawler
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ Python3 -m venv venv
$ source venv/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv`.

Once `pip` has finished downloading the dependencies

## Extract data

```sh
(env)$ scrapy crawl agent -O output.json
```