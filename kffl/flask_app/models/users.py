from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

db = "kffl"
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.password = data['password']
        self.email = data['email']
        self.position = data['position']
        self.experience = data['experience']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.teams = []

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        users_in_db = connectToMySQL(db).query_db(query)
        users_list = []
        for user in users_in_db:
            users_list.append(cls(user))
        return users_list
            
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, password, email, position, experience, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(password)s, %(email)s, %(position)s, %(experience)s, NOW(), NOW());"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def login_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s,password=%(password)s,email=%(email)s,position=%(position)s,experience=%(experience)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)
    
    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 2:
            flash("first name must be at least 2 characters.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("last name must be at least 2 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False
        if user['password'] != user['confirm_pw']:
            flash("Passwords don't match, please double check!")
            is_valid = False
        return is_valid
