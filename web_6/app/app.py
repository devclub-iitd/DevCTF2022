import flask
import subprocess
from flask import redirect, flash, request, url_for
import copy
from pdb import set_trace as bp

app = flask.Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'GET':
        print('Inside index function')
        return flask.render_template('index.html')

    # TODO set limit on upload size

    else:
        data = request.form.get('data')
        cmd = 'pandoc --self-contained -f markdown -t html5 --wrap=none'
        p = subprocess.Popen(
            cmd.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        p.stdin.write(data.encode())
        out, err = p.communicate()
        p.stdin.close()
        print(out, err)

        to_display = out.decode()

        # render a string
        return flask.render_template_string(to_display)


if __name__ == '__main__':
    app.run(debug=True)
