from flask_app.config.mysqlconnection import connectToMySQL, DB
from flask_bcrypt import Bcrypt
from flask_app import app
from flask import flash

import re

bcrypt = Bcrypt(app)

class User:

    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

    def __init__(self , data):
        self.id = data['id']
        self.email = data['email']
        self.fullname = data['fullname']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def register(cls , data):
        encrypted_password = bcrypt.generate_password_hash(data['password'])
        data = dict(data)
        data['password'] = encrypted_password
        query = "INSERT INTO users (fullname , email , password) VALUES(%(fullname)s , %(email)s , %(password)s);"
        return connectToMySQL(DB).query_db(query , data)
    
    @classmethod
    def get_by_id(cls , data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query , data)
        user = None
        if result:
            user = cls(result[0])
        return user
    
    @classmethod
    def get_by_email(cls , data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DB).query_db(query , data)
        user = None
        if result:
            user = cls(result[0])
        return user

    @staticmethod
    def validate_register(data):
        is_valid = True
        user_in_db = User.get_by_email(data)
        if len(data['fullname']) < 6:
            flash("Register: Full name needs to be longer then 5 characters")
            is_valid = False
        if not User.EMAIL_REGEX.match(data['email']):
            flash("Register: Invalid email format.")
            is_valid = False
        if user_in_db:
            flash("Register: User email already exists.")
            is_valid = False
        if len(data['password']) < 8:
            flash("Register: Password needs to be 8 characters or more.")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Register: Passwords don't match.")
            is_valid = False

        return is_valid
    
    @staticmethod
    def validate_login(data):
        is_valid = True
        user_in_db = User.get_by_email(data)
        if not User.EMAIL_REGEX.match(data['email']):
            flash("Login: Invalid email format.")
            is_valid = False
        if not user_in_db:
            flash("Login: User with this email doesn't exist.")
            is_valid = False
        elif not bcrypt.check_password_hash(user_in_db.password , data['password']):
            flash("Login: Incorrect Password.")
            is_valid = False
        if len(data['password']) < 8:
            flash("Login: Password needs to be 8 characters or more.")
            is_valid = False
        
        
        return is_valid
    


