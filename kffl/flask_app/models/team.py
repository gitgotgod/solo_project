from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.users import User

db = "kffl"
class Team:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.wins = data['wins']
        self.losses = data['losses']
        self.ties = data['ties']
        self.user_id = data['user_id']
        self.creator = None

    @classmethod
    def get_all(cls):
        query = """SELECT * FROM teams
        JOIN users on teams.user_id = users.id;
        """
        results = connectToMySQL(db).query_db(query)
        teams = []
        for team in results:
            this_team = cls(team)
            user_data = {
                "id": team['users.id'],
                "first_name": team['first_name'],
                "last_name": team['last_name'],
                "email": team['email'],
                "position": team['position'],
                "experience": team['experience'],
                "password": "",
                "created_at": team['users.created_at'],
                "updated_at": team['users.updated_at']
            }
            this_team.creator = User(user_data)
            teams.append(this_team)
        return teams

    @classmethod
    def save(cls, form_data):
        query = """
                INSERT INTO teams (name,user_id)
                VALUES (%(name)s,%(user_id)s);
                """
        return connectToMySQL(db).query_db(query,form_data)
    
    @classmethod
    def get_one(cls,data):
        query = """
                SELECT * FROM teams
                JOIN users on teams.user_id = users.id
                WHERE teams.id = %(id)s;
                """
        result = connectToMySQL(db).query_db(query,data)
        if not result:
            return False

        result = result[0]
        this_team = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "position": result['position'],
                "experience": result['experience'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_team.creator = User(user_data)
        return this_team
    
    @classmethod
    def created_team(cls,data):
        query = "SELECT * FROM teams WHERE name = %(name)s;"
        result = connectToMySQL(db).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE teams SET name=%(name)s,wins=%(wins)s,losses=%(losses)s,ties=%(ties)s,created_at=NOW(),updated_at=NOW() WHERE user_id = %(user_id)s;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM teams WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)