import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():
    '''scrape random fact from unkno.com'''
    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()


def get_route(fact):
    '''
    return the location (url) from a POST request made to piglantinize
    where 'fact' is the Form Data
    '''
    response = requests.post(
        "https://hidden-journey-62459.herokuapp.com/piglatinize/", data={'input_text': fact}, allow_redirects=False)
    return response.headers['Location']


@app.route('/')
def home():
    '''format the Location url as a link'''
    url_str = get_route(get_fact())
    return f'<a href="{url_str}">{url_str}</a>'


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
