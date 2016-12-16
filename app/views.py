from flask import render_template
from app import app

@app.route('/')
@app.route('/pubs')
def index():
    user = {'nickname': 'Steve'}  # fake user
    return render_template('base.html',
                           title='Publictaions',
                           user=user)