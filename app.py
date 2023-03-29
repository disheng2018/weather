from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    url = 'https://tianqi.moji.com/weather/china'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return render_template('index.html', url=url, content=soup.prettify())

@app.route('/crawl', methods=['POST'])
def crawl():
    url = request.form['url']
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.prettify()
    return render_template('index.html', url=url, content=content)

if __name__ == '__main__':
    app.run(debug=True)
