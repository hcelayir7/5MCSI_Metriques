from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') # Commentaire

@app.route("/contact/")
def formulairedecontact():
    return render_template("contact.html")

@app.route('/paris/')
def meteo():
    response = urlopen('https://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&cnt=16&appid=bd5e378503939ddaee76f12ad7a97608')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('temp', {}).get('day') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route('/commits/')
def commits_graph():
    # Appel à l'API GitHub pour récupérer les données sur les commits
    response = urlopen('https://api.github.com/repos/hcelayir7/5MCSI_Metriques/commits')
    data = response.json()

    # Initialisation du dictionnaire pour stocker le nombre de commits par minute
    commits_per_minute = {}

    # Parcourir les données des commits
    for commit in data:
        # Extraire la date du commit
        commit_date = commit['commit']['author']['date']
        # Convertir la date en objet datetime
        date_object = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
        # Extraire la minute de la date du commit
        minute = date_object.minute
        # Ajouter 1 au compteur de commits pour cette minute
        commits_per_minute[minute] = commits_per_minute.get(minute, 0) + 1

    # Retourner les données sous forme JSON
    return jsonify(minute)
  
if __name__ == "__main__":
  app.run(debug=True)
