import os
import requests
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from functools import wraps

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db.init_app(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

def login_required(f):
    """
    Requires login for a given route

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return render_template("error.html", message="Vul een gebruikersnaam in.")

        if not password:
            return render_template("error.html", message="Vul een wachtwoord in.")

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.hash, password):
            return render_template("error.html", message="Onjuiste gebruikersnaam of wachtwoord, probeer het opnieuw.")

        session["user_id"] = user.id

        return redirect("/")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    if request.method == "POST":
        
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        if not username:
            return render_template("error.html", message="Vul een gebruikersnaam in.")
        if not password or not confirmation:
            return render_template("error.html", message="Vul een wachtwoord in.")
        if password != confirmation:
            return render_template("error.html", message="Wachtwoorden komen niet overeen.")
        
        # check of username al bestaat
        if User.query.filter_by(username=username).first():
            return render_template("error.html", message="Gebruikersnaam is al in gebruik.")

        # use generate_password_hash to store hash of the password in db
        hash = generate_password_hash(password)
        
        # Create new user
        new_user = User(username=username, hash=hash)
        db.session.add(new_user)

        # we gebruiken dit to commit the current transaction (adding)
        db.session.commit()

        session["user_id"] = new_user.id

        return redirect("/")

    return render_template("register.html")
    

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/login")

@app.route("/")
@login_required
def index():
    """Hier moet ik nog index aan toevoegen!!!!!"""
    user_id = session["user_id"]

    # we halen de user op
    user = User.query.get(user_id)

    # run de template met welkom en verwijzing naa de test
    return render_template("index.html", username=user.username)


@app.route("/question/<int:question_id>", methods=["GET", "POST"])
@login_required
def question(question_id):

    # we halen de user id op
    user_id = session["user_id"]

    # we halen de question op
    question = Question.query.get(question_id)

    # als we de vraag niet vinden
    if question is None:
        return render_template("error.html", message="Vraag niet gevonden.")

    if request.method == "POST":

        # answer_id is het geselecteerde antwoord van de gebruiker
        answer_id = request.form.get("answer_id")

        # als er geen antwoord is geselecteerd door user
        if answer_id is None:
            return render_template("error.html", message="Geen antwoord geselecteerd.")

        # we zoeken op of de gebruiker al eerder deze vraag heeft beantwoord
        old_answer = UserAnswer.query.filter_by(user_id=user_id, question_id=question_id).first()

        # als al eerder beantwoord, wordt deze vervangen door nieuw antwoord
        if old_answer:
            old_answer.answer_id = answer_id

        # als nog niet benatwoord, voegen we dit antwoord toe aan de database
        else:
            new_answer = UserAnswer(user_id=user_id, question_id=question_id, answer_id=answer_id)
            db.session.add(new_answer)

        db.session.commit()

        # we kijken of er een nieuwe vraag is, als dat zo is gaan we naar die, anders gaan we naar uitslag
        next_question = Question.query.filter(Question.id > question_id).first()
        if next_question:
            return redirect(f"/question/{next_question.id}")
        else:
            return redirect("/submit_answers")

    return render_template("questions.html", question=question)

@app.route("/submit_answers", methods=["GET"])
@login_required
def submit_answers():
    """Verwerk de antwoorden van de gebruiker en geef de uitslag weer."""
    user_id = session["user_id"]

    # Haal antwoorden van user op
    user_answers = UserAnswer.query.filter_by(user_id=user_id).all()

    # we maken een lijst voor de user met combi van vraag id en antwoord id
    user_answer_list = []
    for answer in user_answers:
        user_answer_list.append((answer.question_id, answer.answer_id))

    # totale aantal questions is lengte van de lijst
    total_questions = len(user_answer_list)

    # we maken een lege lijst waar we later de matches aan toevoegen
    matches = []

    # we halen alle andere users op
    other_users = User.query.filter(User.id != user_id).all()
    
    # we gaan elke other user afzonderlijk af
    for other_user in other_users:

        # we halen antwoorden van other user op
        other_answers = UserAnswer.query.filter_by(user_id=other_user.id).all()

        # we maken ook een lijst voor de other user met combi van vraag id en antwoord id
        other_user_answer_list = []
        for answer in other_answers:
            other_user_answer_list.append((answer.question_id, answer.answer_id))

        # we tellen de overeenkomsten tussen de twee lijsten
        similar = 0
        for user_answer in user_answer_list:
            if user_answer in other_user_answer_list:
                similar += 1

        # we berekenen het percentage van de antworoden die twee users overeenkomen
        percentage = (similar / total_questions) * 100

        # Voeg de overeenkomsten toe aan de lijst (we ronden percentage af op 2 decimalen)
        matches.append((other_user, round(percentage, 2)))

    # https://stackoverflow.com/questions/10695139/sort-a-list-of-tuples-by-2nd-item-integer-value
    # we sorteren de matches op percentage (element 1)
    matches = sorted(matches, key=lambda x: x[1])

    # we selecteren de beste 3 matches
    top_matches = matches[-3:]

    """Voeg hier nog extra restricties toe voor bijv nul macthes, of meerder met zelfde percentage!!1"""

    # De top matches worden worden doorgegeven aan template. 
    return render_template("submit_answers.html", matches=top_matches)

if __name__ == "__main__":
    app.run()