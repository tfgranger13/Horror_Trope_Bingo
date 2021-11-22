from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.trope import Trope

#route to show tropes page
@app.route('/tropes')
def tropes():
    all_tropes = Trope.get_all_tropes()
    return render_template('tropes.html', all_tropes = all_tropes)

#route to add a new trope
@app.route('/new_trope', methods = ['POST'])
def create_trope():
    data = {
        'content': request.form['new_trope_content'],
        'is_flagged': 0,
        'user_id': session['user_id']
    }
    trope_id = Trope.add_to_db(data)
    flash('Trope added successfully!', 'trope')
    return redirect('/tropes')

#route to board page
@app.route('/game')
def game():
    random_tropes = Trope.get_random_tropes()
    return render_template('game.html', random_tropes = random_tropes)