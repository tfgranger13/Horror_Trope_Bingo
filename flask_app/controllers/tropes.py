from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.trope import Trope

#CREATE
#route to add a new trope
@app.route('/new_trope', methods = ['POST'])
def create_trope():
    data = {
        'content': request.form['new_trope_content'],
        'is_flagged': 0,
        'user_id': session['user_id']
    }
    trope_id = Trope.add_to_db(data)
    flash('Trope successfully added!', 'trope')
    return redirect('/tropes')



#READ
#route to show tropes page
@app.route('/tropes')
def tropes():
    if 'user_id' not in session:
        flash("I'm sorry, you must be logged in to view that page.", "logging")
        return redirect('/')
    all_tropes = Trope.get_all_tropes()
    return render_template('tropes.html', all_tropes = all_tropes)

#route for search query
@app.route('/search_tropes', methods = ['POST'])
def searchQuery():
    if 'user_id' not in session:
        flash("I'm sorry, you must be logged in to view that page.", "logging")
        return redirect('/')
    data = {
        'search': request.form['search_query'] + "*"
    }
    searched_tropes = Trope.searchTropes(data)
    if isinstance(searched_tropes, bool) or len(searched_tropes) < 1:
        flash("I'm sorry, no results were found with that search. Please try again.", "tropes")
        return redirect('/tropes')
    return render_template('search.html', searched_tropes = searched_tropes)

#TODO: route for search results?

#route to board page
@app.route('/game')
def game():
    # if 'user_id' not in session:
    #     flash("I'm sorry, you must be logged in to view that page.", "logging")
    #     return redirect('/')
    random_tropes = Trope.get_random_tropes()
    if len(random_tropes) < 24:
        flash("I'm sorry, you must add more tropes to play a game.", "tropes")
        return redirect('/tropes')
    return render_template('game.html', random_tropes = random_tropes)



#UPDATE
#route to edit trope
@app.route('/edit_tropes/<int:trope_id>')
def render_edit_trope(trope_id):
    data = {
        'id': trope_id
    }
    trope_info = Trope.get_single_trope(data)
    return render_template("update.html", trope_info = trope_info)

#route to submit edit
@app.route('/update_trope/<int:trope_id>', methods = ['POST'])
def submit_edit_trope(trope_id):
    if 'user_id' not in session:
        flash("I'm sorry, you must be logged in to view that page.", "logging")
        return redirect('/')
    data = {
        'id': trope_id,
        'content': request.form['edit_trope_content']
    }
    Trope.update_trope(data)
    flash("Trope successfully updated!", 'trope')
    return redirect('/tropes')




#DELETE
#route to delete trope
@app.route('/tropes/delete/<int:trope_id>')
def delete_trope_from_db(trope_id):
    data = {
        'id': trope_id
    }
    Trope.delete_from_db(data)
    flash("Trope has been removed.", "trope")
    return redirect('/tropes')