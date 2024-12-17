import os
import requests
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, flash, redirect, render_template, request, session, url_for
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

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.hash, password):
            flash("Onjuiste gebruikersnaam of wachtwoord, probeer het opnieuw.")
            return render_template("login.html")
        
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
        
        if password != confirmation:
            flash("Wachtwoorden komen niet overeen.")
            return redirect(url_for("register"))
        
        # check of username al bestaat
        if User.query.filter_by(username=username).first():
            flash("Gebruikersnaam is al in gebruik.")
            return redirect(url_for("register"))

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
    """Home page"""
    user_id = session["user_id"]

    # we halen de user op
    user = User.query.get(user_id)

    # run de template met welkom en verwijzing naar de test en profiel aanpassen
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
            flash("Fout! Vul een antwoord in!")

            return redirect(url_for("question", question_id=question_id))

        # we zoeken op of de gebruiker al eerder deze vraag heeft beantwoord
        old_answer = UserAnswer.query.filter_by(user_id=user_id, question_id=question_id).first()

        # als al eerder beantwoord, wordt deze vervangen door nieuw antwoord
        if old_answer:
            old_answer.answer_id = answer_id

        # als nog niet beantwoord, voegen we dit antwoord toe aan de database
        else:
            new_answer = UserAnswer(user_id=user_id, question_id=question_id, answer_id=answer_id)
            db.session.add(new_answer)

        db.session.commit()

        # we kijken of er een nieuwe vraag is, als dat zo is gaan we naar die, anders gaan we naar ranking
        next_question = Question.query.filter(Question.id > question_id).first()
        if next_question:
            return redirect(f"/question/{next_question.id}")
        else:
            return redirect("/rank")
    return render_template("questions.html", question=question)


@app.route("/matches", methods=["GET"])
@login_required
def matches():
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

    # als de vragen nog niet zijn beantwoord
    if total_questions == 0:
        matches = []
        return render_template("matches.html", matches=matches)

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
        similar_answers = 0
        for user_answer in user_answer_list:
            if user_answer in other_user_answer_list:
                similar_answers += 1

        # we halen de rankings van user op
        user_rankings = Ranking.query.filter_by(user_id=user_id).all()

        # we maken een lijst voor de user met combi van song en ranking voor die song
        user_rank_list = []
        for ranking in user_rankings:
            user_rank_list.append((ranking.song_title, ranking.rank))

        # we halen de rankings van alle andere users op
        other_rankings = Ranking.query.filter_by(user_id=other_user.id).all()

        # we maken een lijst voor de andere usere user met combi van song en ranking voor die song
        other_rank_list = []
        for ranking in other_rankings:
            other_rank_list.append((ranking.song_title, ranking.rank))

        # we tellen de overeenkomsten tussen de twee lijsten
        similar_rankings = 0
        for user_song, user_rank in user_rank_list:
            for other_song, other_rank in other_rank_list:
                if user_song == other_song and user_rank == other_rank:

                    # de ranking van de nummers geven we een gewicht van 0.5 per goede vraag
                    similar_rankings += 0.5

        # we berekenen het percentage van de antworoden die twee users overeenkomen
        # elke vraag van 1 t/m 7 is 1 punt waard, en elke zelfde ranking is 0.5 punt waard
        percentage = ((similar_answers + similar_rankings) / (9.5) ) * 100

        # Voeg de overeenkomsten toe aan de lijst (we ronden percentage af op 2 decimalen)
        matches.append((other_user, round(percentage, 2)))

    # we sorteren de matches op percentage (element 1)
    # Bron: https://stackoverflow.com/questions/10695139/sort-a-list-of-tuples-by-2nd-item-integer-value
    matches = sorted(matches, key=lambda x: x[1], reverse=True)

    # we hebben een match als je voor meer dan 60% met iemand gematcht bent
    final_matches = []
    for match in matches:
        if match[1] > 60:
            final_matches.append(match)

    # we selecteren de beste 3 matches
    top_matches = final_matches[:3]

    # De top matches worden worden doorgegeven aan template. 
    return render_template("matches.html", matches=top_matches)

@app.route("/profile/me", methods=["GET", "POST"])
@login_required
def my_profile():
    """eigen profiel bekijken/aanpassen"""

    # we halen het profiel op
    profile = Profile.query.filter_by(user_id=session["user_id"]).first()

    if request.method == "POST":

        # we vragen om de bio en instagram
        bio = request.form.get("bio")
        instagram = request.form.get("instagram")

        # als er al een profiel is, vervangen we de bio en instagram
        if profile:
            profile.bio = bio
            profile.instagram = instagram

        # anders voegen we de bio en instagram toe aan het profiel, we creeren dus het profiel
        else:
            profile = Profile(user_id=session["user_id"], bio=bio, instagram=instagram)
            db.session.add(profile)

        db.session.commit()

        # we hebben de profielgegevens opgeslagen en gaan terug naar home page
        flash("Profielgegevens succesvol opgeslagen.")
        return redirect("/")

    return render_template("my_profile.html", profile=profile)

@app.route("/profile/<int:user_id>", methods=["GET"])
@login_required
def view_profile(user_id):
    """profielen van anderen bekijken"""

    # we halen het profiel op
    profile = Profile.query.filter_by(user_id=user_id).first()

    # we geven een flashbericht als de gebruiker nog geen profielgegevens heeft ingevuld.
    if not profile or profile.bio == "":
        flash("Deze gebruiker heeft nog geen profiel aangemaakt.")
        return redirect(url_for("matches"))
    
    # we geven het profiel van de user weer
    user = User.query.get(user_id)
    return render_template("profile.html", profile=profile, username=user.username)

@app.route('/rank', methods=['GET', 'POST'])
@login_required
def rank():
    """nummers ranken"""

    user_id = session["user_id"]
    if request.method == 'POST':

        # hier gaan we de ranks aan toevoegen
        ranks = []

        # vraag van elke song de rank op
        rank_1 = request.form.get("rank1")
        rank_2 = request.form.get("rank2")
        rank_3 = request.form.get("rank3")
        rank_4 = request.form.get("rank4")
        rank_5 = request.form.get("rank5")

        # als de rank is opgegeven, voegen we deze toe aan ranks
        if rank_1:
            ranks.append(int(rank_1))

        if rank_2:
            ranks.append(int(rank_2))

        if rank_3:
            ranks.append(int(rank_3))

        if rank_4:
            ranks.append(int(rank_4))

        if rank_5:
            ranks.append(int(rank_5))

        # we checken of elke ranking (uniek) is ingevuld
        # Bron: https://stackoverflow.com/questions/12282232/how-do-i-count-occurrence-of-unique-values-inside-a-list
        if len(ranks) != len(set(ranks)) or len(ranks)!=5:
            flash("Fout: Zorg ervoor dat elke nummer een unieke rang heeft!")
            return redirect(url_for('rank'))

        # we verwijderen eerst de ranking van user (zodat deze vervangen wordt als dit nodig is)
        Ranking.query.filter_by(user_id=user_id).delete()

        # We voegen de nummers toe
        song_titles = ["Shape of You", "Don't Stop Believin'", "God's Plan", "Bad Guy", "Another One Bites The Dust"]

        # we voegen aan de ranking van user de nummers met de ranking toe
        for index in range(len(song_titles)):
            db.session.add(Ranking(user_id=user_id, song_title=song_titles[index], rank=ranks[index]))

        db.session.commit()

        # hierna gaan we door naar de uitslag
        return redirect(url_for("matches"))

    return render_template('rank_songs.html')


@app.route('/website_instagram/<int:profile_id>')
def website_instagram(profile_id):
    """Naar Instagram"""

    # we halen het profiel op
    profile = Profile.query.get(profile_id)

    # als de gebruiker geen instagram account heeft ingevuld.
    if not profile or not profile.instagram:
        flash("Deze gebruiker heeft geen Instagram profiel opgegeven.")
        return render_template("profile.html", profile=profile, username=profile.user.username)
    
    # Als het profiel bestaat, gaan we naar het instagram account
    return redirect(f"http://www.instagram.com/{profile.instagram}/")

if __name__ == "__main__":
    app.run()