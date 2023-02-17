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
        note = request.form.get('note') #Gets the note from the HTML 

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
        username = 'DLytvynenko'                    
        password = 'Feeney2022!!'
        # Send API request to the server with Basic Auth
        response = requests.get(f"https://feeney.coinscloud.com/env/learn/rest/pages/personnel1/{query}", auth=(username,password))
        if response.status_code == 200:
            data = response.json()
            # Changed data from JSON format to Text
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


@views.route("/update", methods=["POST", "PUT"])
def update():
    if request.method == "POST":
        global user_id
        email_unput = request.form["email_unput"]
        cloud_id_input = request.form["cloud_id_input"]
        full_name_input = request.form["full_name_input"]
        company_id_input = request.form["company_id_input"]
        status_input = request.form["status_input"]
        cloud_status_input = request.form["cloud_status_input"]
        url = (f"https://feeney.coinscloud.com/env/learn/rest/pages/personnel1/{user_id}")
        payload = json.dumps({
            "ppo_kco": company_id_input,
            "ppo_search_name": full_name_input,
            "por_cloud": cloud_status_input,
            "por_cloudID": cloud_id_input,
            "ppo_email": email_unput,
            "ppo_leaver": status_input
            })
        headers = {
            'Authorization': 'Basic REx5dHZ5bmVua286RmVlbmV5MjAyMiEh',
            'Content-Type': 'application/json'
            }

        response = requests.request("PUT", url, headers=headers, data=payload)

        if response.status_code == 200:
            updated = response.json()
            # Changed data from JSON format to Text
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





    #     update = {
    #         "ppo_email": query
    #         # "ppo_kco": query,
    #         # "ppo_leaver": query,
    #         # "por_cloudID": query
    #         # "por_cloud": query
            
    #     }
    #     username = 'DLytvynenko'                    
    #     password = 'Feeney2022!!'
    #     # Send API request to the server with Basic Auth
    #     response = requests.patch(f"https://feeney.coinscloud.com/env/learn/rest/pages/personnel1/{user_id}", json=update, auth=(username, password))
    #     if response.status_code == 200:
    #         updated = response.json()
    #         # Changed data from JSON format to Text
    #         updated_data = {
    #             "ID": updated["hrp_id"],
    #             "Company": updated["ppo_kco"],
    #             "Full Name": updated["ppo_search_name"],
    #             "Email": updated["ppo_email"],
    #             "Leaver": updated["ppo_leaver"],
    #             "Cloud ID": updated["por_cloudID"],
    #             "Cloud": updated["por_cloud"],
    #             "Internal Reference": updated["ppo_seq"]
    #             }
    #         # return jsonify(response.json(), updated)
    #         return render_template("update.html", updated_data=updated_data)
        
    # # return render_template("search.html")
    
    # return render_template("search.html"), response.status_code
    
        