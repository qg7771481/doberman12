from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.widgets.core import TextArea


class FeedbackForm(FlaskForm):
    name = StringField("ur name: ", validators=[DataRequired(), Length(10)])
    feedback = TextAreaField("ur feedback: ", validators=[DataRequired(), Length(max=500)])
    submit = SubmitField("send")
