import json
import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def get_config():
    with open('config.json', 'r') as f:
        config = json.load(f)

    return render_template('home.html', post = config)

@app.route("/", methods=['POST'])
def set_config():
    course = request.form['course']
    date = request.form['date']
    position = request.form['position']
    today = str(datetime.datetime.now())

    with open('config.json', 'r') as f:
        config = json.load(f)

    config['course'] = course
    config['date'] = date
    config['position'] = position
    config['last_update'] = today

    with open('config.json', 'w') as f:
        json.dump(config, f)

    return render_template('home.html', post = config)

def main():
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()