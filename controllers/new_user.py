from app import app
from flask import render_template, request, session

@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    html = render_template(
        'new_user.html',
    )
    return html