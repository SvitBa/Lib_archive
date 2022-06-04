from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Length, DataRequired


class AddItem (FlaskForm):
    name = StringField(label='Назва книги:', validators=[Length(min=2, max=30), DataRequired()])
    ISBN = StringField(label='ISBN:', validators=[Length(max=12), DataRequired()])
    price = IntegerField(label='Ціна:')
    description = StringField(label='Опис книги:', validators=[Length(max=1024), DataRequired()])
    submit = SubmitField(label='Додати книгу')

