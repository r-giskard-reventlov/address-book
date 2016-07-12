from flask import render_template, request,flash, redirect, url_for
from seldon_address_book import app, db
from seldon_address_book.models import Organisation 

@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        org=Organisation(request.form['name'], request.form['address'], request.form['phone'])
        db.session.add(org)
        db.session.commit()
        flash('New entry was successfully posted')
    return render_template('add_organisation.html')
