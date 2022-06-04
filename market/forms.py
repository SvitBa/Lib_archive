from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from Lib_archive.market.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Користувач з таким логіном вже існує!')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Користувач з таким Email вже існує! Спробуйте інший')

    username = StringField(label="Ім'я", validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Пароль:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Підтвердіть пароль:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Зареєструватися')

class LoginForm(FlaskForm):
    username = StringField(label="Ім'я", validators=[DataRequired()])
    password = PasswordField(label='Пароль:', validators=[DataRequired()])
    submit = SubmitField(label='Увійти')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Отримати')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Повернути')
