from flask import Flask, render_template, request, flash, redirect, url_for
import requests
import json
from models.newTweetForm import PostTweetForm
from models.insightForm import InsightForm
from myTweepy import newStream
from flask_socketio import SocketIO
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading")
streamer = newStream(socketio)
myStream = streamer.get_stream()

@app.route('/')
def home():
    r = requests.get('http://127.0.0.1:5000/home')
    return render_template('home.html', tweets = json.loads(r.text))

@app.route('/newTweet', methods=['GET', 'POST'])
def newTweet():
    form = PostTweetForm(request.form)
    if request.method == 'POST' and form.validate():
        message = request.form['message']
        r = requests.post('http://127.0.0.1:5000/newTweet', json = {"message" : message})
        return redirect(url_for('newTweet'))
    return render_template('newTweet.html', form=form)

@app.route('/streamer', methods=['GET', 'POST'])
def sessions():
    return render_template('streamer.html')

@socketio.on('launchStream')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    myStream.filter(track = [json['targetname']], async=True)

@socketio.on('stopStream')
def handle_my_stop_event(methods=['GET', 'POST']):
    myStream.disconnect()

@app.route('/insight', methods=['GET', 'POST'])
def insight():
    form = InsightForm(request.form)
    if request.method == 'POST' and form.validate():
        figure = request.form['figure']
        print(figure)
        r = requests.post('http://127.0.0.1:5000/insight', json = {"figure" : figure})
        print (r)
        data = []
        for key, value in json.loads(r.text).items():
            print(key)
            utc_time = datetime.strptime(key, "%Y-%m-%d %H:%M:%S")
            epoch_time = (utc_time - datetime(1970, 1, 1)).total_seconds() * 1000
            data.append([epoch_time, value['favorite_count']])
        return render_template('insight.html', form=form, rawdata = data)
    return render_template('insight.html', form=form)

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0',port='4000', debug=True)
    socketio.run(app, debug=True)