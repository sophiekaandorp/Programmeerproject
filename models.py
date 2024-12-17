from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    hash = db.Column(db.String, nullable=False)
    user_answers = db.relationship("UserAnswer", back_populates="user") 
    profile = db.relationship("Profile", back_populates="user")
    rankings = db.relationship("Ranking", back_populates="user")

class UserAnswer(db.Model):
    """Slaat de antwoorden van de User op"""
    __tablename__ = "user_answers"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey("answers.id"), nullable=True)
    user = db.relationship("User", back_populates="user_answers")
    question = db.relationship("Question", back_populates="user_answers")
    answer = db.relationship("Answer", back_populates="user_answers")

class Question(db.Model):
    """De vraag die aan de User wordt gesteld"""
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String, nullable=False)
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
    instagram = db.Column(db.String, nullable=True)
    user = db.relationship("User", back_populates="profile")
    
class Ranking(db.Model):
    __tablename__ = "rankings"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    song_title = db.Column(db.String, nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    user = db.relationship("User", back_populates="rankings")