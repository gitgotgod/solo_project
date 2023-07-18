from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.users import User
from flask_app.models.team import Team

db = "kffl"
class Event:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.date = data['date']
        self.team_id = data['team_id']
        self.creator = None

    @classmethod
    def get_all(cls):
        query = """SELECT * FROM events
        JOIN teams on events.team_id = teams.id;
        """
        results = connectToMySQL(db).query_db(query)
        events = []
        for event in results:
            this_event = cls(event)
            team_data = {
                "id": event['teams.id'],
                "bane": event['name'],
                "created_at": event['users.created_at'],
                "updated_at": event['users.updated_at']
            }
            this_event.creator = Team(team_data)
            events.append(this_event)
        return events

    @classmethod
    def save(cls, form_data):
        query = """
                INSERT INTO events (name,team_id)
                VALUES (%(name)s,%(team_id)s);
                """
        return connectToMySQL(db).query_db(query,form_data)
    
    @classmethod
    def get_one(cls,data):
        query = """
                SELECT * FROM events
                JOIN teams on events.team_id = teams.id
                WHERE events.id = %(id)s;
                """
        result = connectToMySQL(db).query_db(query,data)
        if not result:
            return False

        result = result[0]
        this_event = cls(result)
        team_data = {
                "id": result['teams.id'],
                "name": result['name'],
                "created_at": result['teams.created_at'],
                "updated_at": result['teams.updated_at']
        }
        this_event.creator = Team(team_data)
        return this_event
    
    @classmethod
    def created_event(cls,data):
        query = "SELECT * FROM events WHERE name = %(name)s;"
        result = connectToMySQL(db).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE events SET name=%(name)s,created_at=NOW(),updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM events WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)
    
    @staticmethod
    def validate_events(event):
        is_valid = True # we assume this is true
        if len(event['name']) < 3:
            flash("Name of event must be at least 3 characters.")
            is_valid = False
        return is_valid