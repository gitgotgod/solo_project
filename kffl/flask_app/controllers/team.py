from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.team import Team
from flask_app.models.users import User


# Dashboard
# Show dashboard of all teams and associated users
@app.route('/dashboard')
def main():
    return render_template("dashboard.html", user = User.get_one({'id':session['user_id']}), teams = Team.get_all())

# clicking on my teams leads to session user/account page

#CREATE

@app.route('/new/team')
def teams():
    user = User.get_one({'id':session['user_id']})
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("new_teams.html", user = user, teams = Team.get_all())

@app.route('/create_team', methods=['POST'])
def create_team():
    user = User.get_one({'id':session['user_id']})
    if not user:
        return redirect('/logout')
    data = {
        'user_id': session['user_id'],
        'name': request.form['name']
    }

    Team.save(data)
    return redirect('/dashboard')



#READ

@app.route('/standings')
def standings():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("standings.html", user = User.get_one({'id':session['user_id']}), teams = Team.get_all())

#update and edit

@app.route('/adjust')
def adjust():
    return render_template("adjustment.html")
#delete

@app.route('/make_changes', methods=['POST'])
def update_team():
    data = {
        'user_id': session['user_id'],
        'name': request.form['name'],
        'wins': request.form['wins'],
        'losses': request.form['losses'],
        'ties': request.form['ties'],
    }

    Team.update(data)
    return redirect('/adjust')

@app.route('/destroy/<int:id>')
def destroy_teams(id):
    if 'user_id' not in session:
        return redirect('/logout')
    Team.destroy({'id':id})
    return redirect('/dashboard')