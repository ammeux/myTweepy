from wtforms import Form, StringField, validators

class InsightForm(Form):
    figure = StringField('Please select a name to analyse', validators=[validators.required()])