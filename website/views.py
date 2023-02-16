from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import requests

views = Blueprint('views', __name__)
user_id = ''

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form["query"]
        global user_id
        user_id = query
        # Make API request to third-party website
        username = 'DLytvynenko'                    
        password = 'Feeney2022!!'
        response = requests.get(f"https://feeney.coinscloud.com/env/learn/rest/pages/personnel/{query}", auth=(username,password))
        if response.status_code == 200:
            data = response.json()
    
            data_up = {
                "ID": data["hrp_id"],
                "Company": data["ppo_kco"],
                "Full Name": data["ppo_search_name"],
                "Email": data["ppo_email"],
                "Leaver": data["ppo_leaver"],
                "Cloud ID": data["por_cloudID"],
                "Cloud": data["por_cloud"],
                "Internal Reference": data["ppo_seq"]
            }

            return render_template("results.html", data_up=data_up)

    return render_template("search.html"), response.status_code


@views.route("/update", methods=["POST"])
def update():
    if request.method == "POST":
        global user_id
        query = request.form["query"]
        update = {"ppo_email": query}
        username = 'DLytvynenko'                    
        password = 'Feeney2022!!'
        response = requests.patch(f"https://feeney.coinscloud.com/env/learn/rest/pages/personnel/{user_id}", json=update, auth=(username, password))
        if response.status_code == 200:
            updated = response.json()
        
            updated_data = {
                "ID": updated["hrp_id"],
                "Company": updated["ppo_kco"],
                "Full Name": updated["ppo_search_name"],
                "Email": updated["ppo_email"],
                "Leaver": updated["ppo_leaver"],
                "Cloud ID": updated["por_cloudID"],
                "Cloud": updated["por_cloud"],
                "Internal Reference": updated["ppo_seq"]
                }
            # return jsonify(response.json(), updated)
            return render_template("update.html", updated_data=updated_data)
        
    # return render_template("search.html")
    
    return render_template("search.html"), response.status_code
    
