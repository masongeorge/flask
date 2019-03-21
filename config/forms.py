from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from config.models import User

class RegistrationForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired(), Length(min=4, max=20)])
    last_name = StringField('last_name', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=20)])
    passwordc = PasswordField('passwordc', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Create account')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken')

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])

    submit = SubmitField('Sign in')
	
class SearchForm(FlaskForm):
    search_pattern = StringField('search_pattern')
    submit = SubmitField('Search')
	
class CheckOut(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired(), Length(min=2, max=16)])
    last_name = StringField('last_name', validators=[DataRequired(), Length(min=2, max=14)])
    email = StringField('email', validators=[DataRequired(), Email()])
    address = StringField('address', validators=[DataRequired()])
	#country
    postal = StringField('postal_code', validators=[DataRequired()])
    card_name = StringField('card_name', validators=[DataRequired(), Length(min=2, max=16)])
    card_number = StringField('card_num', validators=[DataRequired()])
    expr_date = StringField('expr_date', validators=[DataRequired()])
    cvv = StringField('cvv', validators=[DataRequired()])
	