from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from househunt.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
 
class HouseHunt(FlaskForm):
    choices = [('rent', 'rent'),
               ('buy', 'buy')]
    select = SelectField('Search for your dream house:', choices=choices)
    search_place = StringField('search_place')
    search_description = StringField('search_description')
    
# from facebook_business.api import FacebookAdsApi
# from facebook_business.adobjects.ad import Ad
# from facebook_business.adobjects.adset import AdSet
# from facebook_business.adobjects.ad import Ad as AdObject
# from facebook_business.adobjects.user import User
# from facebook_business.adobjects.targeting import Targeting
# from facebook_business.adobjects.customaudience import CustomAudience
# from facebook_business.adobjects.adaccount import AdAccount
# from datetime import datetime
# from time import sleep

# import requests
# import util
# import json
# import facebook_business    


# #Import Storage Configuration File
# credentials = json.loads(open('config/credentials.json').read())

# #Connect to Facebook API
# def connection():
#     my_app_id = credentials["facebook"]["my_app_id"]
#     my_app_secret = credentials["facebook"]["my_app_secret"]
#     my_access_token = credentials["facebook"]["my_access_token"]
#     FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)