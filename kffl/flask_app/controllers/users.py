from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.users import User
from flask_app.models.team import Team
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#first page
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    session.clear()
    return render_template("main.html")

#CREATE

@app.route('/first')
def first():
    if 'user_id' in session:
        return redirect('/dashboard')
    session.clear()
    return render_template("login.html")

@app.route('/register', methods=['POST'])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/')
    data ={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']),
        "position": request.form['position'],
        "experience": request.form['experience']
    }
    user_id = User.save(data)

    session['user_id'] = user_id

    return redirect('/dashboard')


#GOOD


#READ

@app.route('/login',methods=['POST'])
def login():
    user = User.login_email(request.form)
    if not user:
        flash("Invalid email!!!!")
        return redirect('/')

    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/events')
def events():
    user = User.get_one({'id':session['user_id']})
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("events.html")
#DELETE
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')