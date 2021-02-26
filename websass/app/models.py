from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournament.id"))
    player_name = db.Column(db.String(64), index=True, unique=True)
    is_bye = db.Column(db.Boolean, default=False)
    recieved_bye = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Player {self.player_name}>"


class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    organizer = db.Column(db.Integer, db.ForeignKey("user.id"))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    rounds = db.relationship("Round", backref="t", lazy="dynamic")
    players = db.relationship("Player", backref="t", lazy="dynamic")

    def __repr__(self):
        return f"<Tournament {self.name}>"


class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournament = db.Column(db.Integer, db.ForeignKey("tournament.id"))
    round_num = db.Column(db.Integer)
    matches = db.relationship("Match", backref="r", lazy="dynamic")

    def __repr__(self):
        return f"<Round {self.round_num}: Tournament {self.tournament}>"


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round = db.Column(db.Integer, db.ForeignKey("round.id"))
    corp_player = db.Column(db.Integer, db.ForeignKey("player.id"))
    runner_player = db.Column(db.Integer, db.ForeignKey("player.id"))
    corp_score = db.Column(db.Integer, default=0)
    runner_score = db.Column(db.Integer, default=0)
    elim_game = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Corp {self.corp_player}: Runner {self.corp_player}>"

