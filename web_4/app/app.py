import flask
from flask import redirect, flash, url_for
import copy
from pdb import set_trace as bp

app = flask.Flask(__name__)

flashed_msgs = []
PRODUCTS = {
    'Smartphone': {
        'name': 'Smartphone',
        'price': 'OUT OF STOCK',
        'image': 'smartphone2.jpg'
    },
    'CTF Flag': {
        'name': 'CTF Flag',
        'price': '₹40,000',
        'image': 'flag2.jpg'
    },
    'Car': {
        'name': 'Car',
        'price': 'OUT OF STOCK',
        'image': 'car.jpg'
    },
}


def get_flashed_messages():
    global flashed_msgs
    to_ret = copy.deepcopy(flashed_msgs)
    flashed_msgs = []
    return to_ret


@app.route('/')
def index():
    print('Inside index function')
    # msgs = request.args['messages']
    return flask.render_template('index.html', products=list(PRODUCTS.values()), get_flashed_messages=get_flashed_messages)


@app.route('/buy/<path:product_name>')
def buy(product_name):
    global flashed_msgs
    try:
        product = PRODUCTS[product_name]
        if product['price'] == 'OUT OF STOCK':
            flashed_msgs = ["Product is Out of Stock"]
        elif product['name'] == 'CTF Flag':
            flashed_msgs = [
                "You cannot bribe and get the flag. This action will be reported"]
    except:
        flashed_msgs = ["Product not found"]
    return flask.render_template_string(f'Trying to Buy <b>{product_name}</b>  Please Wait'), {"Refresh": f"2; url=../"}


@app.route('/echo/<path:shrine>')
def echo(shrine):
    def safe_jinja(s):
        # bp()
        # s = s.replace('(', '').replace(')', '')
        blacklist = ['config', 'self']
        return ''.join(['{{% set {}=None%}}'.format(c) for c in blacklist])+s
    return flask.render_template_string(safe_jinja(shrine))


if __name__ == '__main__':
    app.run(debug=True)
