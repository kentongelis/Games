from games_app.extensions import db
from sqlalchemy.orm import backref
from sqlalchemy_utils import URLType
from flask_login import UserMixin
import enum

class FormEnum(enum.Enum):
    """Helper class to make it easier to use enums with forms."""
    @classmethod
    def choices(cls):
        return [(choice.name, choice) for choice in cls]

    def __str__(self):
        return str(self.value)

class Rating(FormEnum):
    EVERYONE = 'Everyone'
    EVERYONETEN = 'Everyone 10+'
    TEEN = 'Teen'
    MATURE = 'Mature'
    ADULTSONLY = 'Adults Only'
    
class Platform(FormEnum):
    PLAYSTATION = 'Playstation'
    XBOX = 'XBOX'
    SWITCH = 'Nintendo Switch'
    PC = 'PC'
    NONE = 'None'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    is_publisher = db.Column(db.Boolean, nullable=False, default=False)
    name = db.Column(db.String(80), nullable=True)
    posts = db.relationship('Post', back_populates = 'user', lazy=True)
    fav_games = db.relationship('Game', secondary='favorite_games', back_populates='users')
    games = db.relationship('Game', back_populates='publisher')
    
    def __repr__(self):
        return f'{self.name}'
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(500), nullable=False)
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='posts')
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    game = db.relationship('Game', back_populates='posts')
    
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(1000))
    price = db.Column(db.Float(precision=2), nullable=True)
    rating = db.Column(db.Enum(Rating))
    publisher_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    publisher = db.relationship('User', back_populates='games')
    image = db.Column(db.String(500))
    posts = db.relationship('Post', back_populates='game', lazy=True)
    users = db.relationship('User', secondary='favorite_games', back_populates='fav_games')
    
favorite_games = db.Table('favorite_games',
        db.Column('game_id', db.Integer, db.ForeignKey('game.id')),
        db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
        )
