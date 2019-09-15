import sqlite3
from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    # Create function to add users to the database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Create function to find a user by username
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    # Create function to find a user by user id
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
