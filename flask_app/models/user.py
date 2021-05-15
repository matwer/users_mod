# user.py
from flask_app.config.mysqlconnection import connectToMySQL


class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    # gets all the users and returns them in a list of user objects 
    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"

        users_from_db = connectToMySQL("users").query_db(query)
        
        users = []

        for user in users_from_db:
            # cls refers to the class - standard naming convention for a class method
            users.append(cls(user))
            
        return users


    # gets one user and returns the user with a matching user id
    @classmethod
    def get_one_user(cls,user):
        query = "SELECT * FROM users WHERE id = %(id)s;"

        user_from_db = connectToMySQL("users").query_db(query,user)

        user_obj = cls(user_from_db[0])

        return user_obj


    # creates a new user and inserts the user into the daatabase
    @classmethod
    def add_user(cls,new_user):
        query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) " \
            "VALUES (%(first_name)s, %(last_name)s, %(email)s, NOW(), NOW());"
        
        user_from_db = connectToMySQL("users").query_db(query,new_user)

        return user_from_db
    
    
    # updates and existing user in the database
    @classmethod
    def update_user(cls,user):

        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW() WHERE id = %(id)s;"

        return connectToMySQL("users").query_db(query,user)


    # deletes a user based on the suer id
    @classmethod
    def delete_user(cls,user):
        query = "DELETE FROM users WHERE id = %(id)s;"
        
        connectToMySQL("users").query_db(query,user)