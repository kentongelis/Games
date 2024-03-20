from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SelectField, SelectMultipleField, SubmitField, TextAreaField, FloatField, widgets
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired, Length
from games_app.models import User, Rating

class SelectMultipleFieldWithCheckboxes(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
    
class QuerySelectMultipleFieldWithCheckboxes(QuerySelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
    
class GameForm(FlaskForm):
    title = StringField('Game Title',
        validators=[DataRequired(), Length(min=3, max=80)])
    description = TextAreaField('Game Description', validators=[DataRequired(),
        Length(min=1, message='Description must not be more than 300 characters')])
    price = FloatField('Price', validators=[DataRequired()])
    image = FileField('Image', validators=[
        FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    rating = SelectField('Rating', choices=Rating.choices())
    submit = SubmitField('Submit')
    
class PostForm(FlaskForm):
    data = TextAreaField('Write Something:', validators=[DataRequired(), Length(min=1)])
    submit = SubmitField('Post!')