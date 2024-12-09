from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    hash = db.Column(db.String, nullable=False)

    # relatie tussen user en ingevulde antwoordn
    user_answers = db.relationship("UserAnswer", back_populates="user") 

    # relatie tussen user en profiel
    profile = db.relationship("Profile", back_populates="user")

class UserAnswer(db.Model):
    """Slaat se antwoorden van de User op"""
    __tablename__ = "user_answers"
    id = db.Column(db.Integer, primary_key=True)

    # uiteindelijk hoort elk UserAnswer bij een id van user en de question id en answer id 
    # (die laatste 2 moeten uiteindelijk hetzelfde zijn om te matchen)
    # verwijst naar id uit users
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # verwijst naar id uit questions
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)

    # verwijst naar id uit answers
    answer_id = db.Column(db.Integer, db.ForeignKey("answers.id"), nullable=True)

    # met de relaties kunnen we via UserAnswer de bijbehorende user/question/answer ophalen.
    user = db.relationship("User", back_populates="user_answers")
    question = db.relationship("Question", back_populates="user_answers")
    answer = db.relationship("Answer", back_populates="user_answers")

class Question(db.Model):
    """De vraag die aan de User wordt gesteld"""
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String, nullable=False)

    # met relaties kunnen we via Question naar de bijbehorende (user)answers
    answers = db.relationship("Answer", back_populates="question")
    user_answers = db.relationship("UserAnswer", back_populates="question") 

class Answer(db.Model):
    """De mogelijke antwoorden op Question"""
    __tablename__ = "answers"
    id = db.Column(db.Integer, primary_key=True)
    answer_text = db.Column(db.String, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    question = db.relationship("Question", back_populates="answers")
    user_answers = db.relationship("UserAnswer", back_populates="answer")

class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    bio = db.Column(db.String, nullable=True)
    user = db.relationship("User", back_populates="profile")
    
