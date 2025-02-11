import hashlib
import string

from datetime import datetime
from flask import Flask, render_template, request, redirect


app = Flask(__name__)


urlMap = {}


def shortUrl(url: string) -> string:
    # add uniq
    time_now = datetime.now()
    time_now_ts = str(time_now.timestamp())
    url_with_ts = "{}/{}".format(url, time_now_ts)
    shorten_url = hashlib.md5(url_with_ts.encode()).hexdigest()[:8]

    urlMap[shorten_url] = {
        "url": url,
        "visited": 0,
        "created_at": time_now.timestamp(),
        "updated_at": time_now.timestamp(),
    }

    return shorten_url


@app.route('/')
def hello_world():  # put application's code here
    # return 'Hello World!'
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit_url():
    url = request.form.get('url')
    print('URL retrieved: {}'.format(url))

    short_url = shortUrl(url)

    return render_template('index.html', short_url=short_url)


@app.route('/<shorten_url>')
def redirect_url(shorten_url):
    print('shorten_url: {}'.format(shorten_url))

    urlData = urlMap[shorten_url]

    print('urlData: {}'.format(urlData))

    urlData['updated_at'] = datetime.now().timestamp()
    urlData['visited'] += 1
    original_url = urlData["url"]

    return redirect(original_url)


@app.route('/detail')
def detail():
    return render_template('detail.html')

@app.route('/detail', methods=['POST'])
def detail_url():
    short_url = request.form.get('short_url')
    urlData = urlMap[short_url]
    return render_template('detail.html', detail_url=urlData, short_url=short_url)


if __name__ == '__main__':
    app.run()
