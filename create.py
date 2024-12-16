import os

from flask import Flask, render_template, request
from models import *

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    db.create_all()

def add_questions():
    """We voegen de questions en bijbehorende antwoorden toe aan de database."""
    user = User.query.first()
    if user is None:
        raise ValueError("Geen gebruikers gevonden om vragen aan toe te voegen.")

    question_1 = Question(question_text="Bij welk soort evenement zou je het liefst live muziek willen horen?")
    question_2 = Question(question_text="Als je een tijdperk van muziek opnieuw zou kunnen beleven, welk tijdperk zou dat zijn?")
    question_3 = Question(question_text="Hoe belangrijk zijn songteksten voor jou in muziek?")
    question_4 = Question(question_text="Hoe ontdek je nieuwe muziek?")
    question_5 = Question(question_text="Hoe vaak luister je naar muziek?")
    question_6 = Question(question_text="Als je een concert mocht bijwonen van een overleden artiest, wie zou dat dan zijn?")
    question_7 = Question(question_text="Als je een soundtrack voor je leven moest kiezen, welke zou dat dan zijn?")

    db.session.add_all([question_1, question_2, question_3, question_4, question_5, question_6, question_7])
    db.session.commit()

    answer_1_1 = Answer(answer_text="Intiem café met singer-songwriter.", question=question_1)
    answer_1_2 = Answer(answer_text="Groot festival met meerdere artiesten.", question=question_1)
    answer_1_3 = Answer(answer_text="Jazzclub.", question=question_1)
    answer_1_4 = Answer(answer_text="Klassiek concert in een theater.", question=question_1)

    answer_2_1 = Answer(answer_text="De jaren '60.", question=question_2)
    answer_2_2 = Answer(answer_text="De jaren '80.", question=question_2)
    answer_2_3 = Answer(answer_text="De jaren '90.", question=question_2)
    answer_2_4 = Answer(answer_text="De jaren 2000.", question=question_2)

    answer_3_1 = Answer(answer_text="Heel belangrijk, ik let altijd op de woorden.", question=question_3)
    answer_3_2 = Answer(answer_text="Soms, als het goed geschreven is.", question=question_3)
    answer_3_3 = Answer(answer_text="Niet zo belangrijk, het gaat meer om de melodie.", question=question_3)
    answer_3_4 = Answer(answer_text="Helemaal niet, ik luister alleen naar de sfeer.", question=question_3)

    answer_4_1 = Answer(answer_text="Via Spotify of andere streamingplatforms.", question=question_4)
    answer_4_2 = Answer(answer_text="Aanbevelingen van vrienden.", question=question_4)
    answer_4_3 = Answer(answer_text="Radio of televisie.", question=question_4)
    answer_4_4 = Answer(answer_text="Optredens of festivals.", question=question_4)

    answer_5_1 = Answer(answer_text="De hele dag door.", question=question_5)
    answer_5_2 = Answer(answer_text="Een paar uur per dag.", question=question_5)
    answer_5_3 = Answer(answer_text="Alleen als ik onderweg ben.", question=question_5)
    answer_5_4 = Answer(answer_text="Af en toe als ik er zin in heb.", question=question_5)

    answer_6_1 = Answer(answer_text="Freddie Mercury.", question=question_6)
    answer_6_2 = Answer(answer_text="Tupac.", question=question_6)
    answer_6_3 = Answer(answer_text="Kurt Cobain.", question=question_6)
    answer_6_4 = Answer(answer_text="Michael Jackson.", question=question_6)

    answer_7_1 = Answer(answer_text="Een episch en groots nummer.", question=question_7)
    answer_7_2 = Answer(answer_text="Een vrolijk en feelgood nummer.", question=question_7)
    answer_7_3 = Answer(answer_text="Een rustig en diepgaand nummer.", question=question_7)
    answer_7_4 = Answer(answer_text="Een intens en energiek nummer.", question=question_7)

    db.session.add_all([
        answer_1_1, answer_1_2, answer_1_3, answer_1_4,
        answer_2_1, answer_2_2, answer_2_3, answer_2_4,
        answer_3_1, answer_3_2, answer_3_3, answer_3_4,
        answer_4_1, answer_4_2, answer_4_3, answer_4_4,
        answer_5_1, answer_5_2, answer_5_3, answer_5_4,
        answer_6_1, answer_6_2, answer_6_3, answer_6_4,
        answer_7_1, answer_7_2, answer_7_3, answer_7_4,
    ])
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()
        add_questions()
