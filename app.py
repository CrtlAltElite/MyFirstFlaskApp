from flask import Flask, render_template, request
import requests

app = Flask(__name__)

registered_users = {
    'kevinb@codingtemple.com':{"name":"Kevin","password":"abc123"},
    'johnl@codingtemple.com':{"name":"John", "password":"Colt45"},
    'joelc@codingtemple.com':{"name":"Joel","password":"MorphinTime"}
}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')

@app.route('/students', methods=['GET'])
def students():
    my_students=["Thu", "Leo", "Sydney", "Josh", "Chris", "Fernado", "Benny", "Vicky", "Bradley"]
    return render_template("students.html.j2",students=my_students)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # Do login Stuff
        email = request.form.get('email').lower()
        password = request.form.get('password')
        if email in registered_users.keys() and password == registered_users.get(email).get('password'):
            #Login success!!!!!!!!
            return f"Login Success Welcome {registered_users.get(email).get('name')}" 
        error_string = "Incorrect Email/Password Combo"
        return render_template("login.html.j2", error=error_string)
    return render_template("login.html.j2")

@app.route('/ergast', methods=['GET','POST'])
def ergast():
    if request.method == 'POST':
        year = request.form.get('year')
        round = request.form.get('round')
        url = f'http://ergast.com/api/f1/{year}/{round}/driverStandings.json'
        response = requests.get(url)
        if response.ok:
            #do stuff with the data
            ## This part I changed from class.. 
            # instead of the try else I check to make sure the Driver standing list
            #  is not empty before we grab the data
            data = response.json()["MRData"]["StandingsTable"]["StandingsLists"]
            if not data:
                error_string=f'There is no info for {year} round {round}'
                return render_template("ergast.html.j2",error=error_string)

            data = data[0].get("DriverStandings")
            all_racers = []
            for racer in data:
                racer_dict={
                    'first_name':racer['Driver']['givenName'],
                    'last_name':racer['Driver']['familyName'],
                    'position':racer['position'],
                    'wins':racer['wins'],
                    'DOB':racer['Driver']['dateOfBirth'],
                    'nationality':racer['Driver']['nationality'],
                    'constructor':racer['Constructors'][0]['name']
                }
                all_racers.append(racer_dict)
            return render_template("ergast.html.j2",racers=all_racers)
        else:
            error_string="Houston We Have a Problem"
            render_template("ergast.html.j2",error=error_string)
    return render_template("ergast.html.j2")

#export/set FLASK_APP=app.py
#export/set FLASK_ENV=development