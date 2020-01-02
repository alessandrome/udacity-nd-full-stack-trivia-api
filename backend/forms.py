from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class QuestionForm(FlaskForm):
    question = StringField('question', validators=[DataRequired()])
    answer = StringField('answer', validators=[DataRequired()])
    category = IntegerField('category', validators=[DataRequired()])
    difficulty = IntegerField('difficulty', validators=[DataRequired()])
