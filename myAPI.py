from flask import Flask
from flask_restplus import Api, Resource, fields
from myTweepy import twitterCursor, twitterPoster

app = Flask(__name__)
api = Api(app)

a_message = api.model('NewTweet', {'message' : fields.String('Message:')})
a_figure = api.model('Insight', {'figure': fields.String('Figure:')})

@api.route('/home')
class Home(Resource):
    def get(self):
        cursor = twitterCursor()
        return {status.id: status._json for status in cursor.get_home_timeline()}

@api.route('/newTweet')
class NewTweet(Resource):
    @api.expect(a_message)
    def post(self):
        poster = twitterPoster()
        poster.post_new_tweet(api.payload['message'])
        return {'result': 'Tweet posted'}, 201

@api.route('/insight')
class Insight(Resource):
    @api.expect(a_figure)
    def post(self):
        cursor = twitterCursor()
        return ({str(status.created_at): status._json for status in cursor.get_user_timeline(api.payload['figure'], 200)})


if __name__ == '__main__':
    app.run(debug=True)
    socketio.run(app)