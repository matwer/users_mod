from flask_app import app

from flask import render_template,redirect,request,session,flash

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

@app.route("/")
def home():
    return redirect("/users")


# CRUD

# Read All
@app.route("/users")
def index():
    return render_template("index.html", all_users = User.get_all_users())


# Read One
@app.route("/users/<int:user_id>")
def show_user(user_id):
    this_user = User.get_one_user( {"id": user_id } )

    return render_template("user.html", user = this_user)


# Create
@app.route("/users/new")
def add_user_form():
    return render_template("create.html")


@app.route("/users/create", methods = ["POST"])
def add_user():

    new_user = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email']
    }

    User.add_user(new_user)

    return redirect("/users")


# Update - needs to be updated
@app.route("/users/<int:user_id>/edit")
def edit_user_form(user_id):
    query = "SELECT * FROM users WHERE id = %(id)s;"
    
    mySQL = connectToMySQL("users")
    
    this_user = {
        "id": user_id
    }
    
    user_list = mySQL.query_db(query, this_user)

    return render_template("edit_user.html", user = user_list[0])


@app.route('/users/<int:user_id>/update', methods = ['POST'])
def update(user_id):
    user = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "id": user_id
   }

    User.update_user(user)

    return redirect(f"/users/{user_id}")


# Delete
@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    User.delete_user( {"id": user_id} )   

    return redirect("/users")
