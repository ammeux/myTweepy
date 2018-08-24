from wtforms import Form, StringField, validators

class PostTweetForm(Form):
    message = StringField('Please send 140 characters max:', validators=[validators.required()])