import unittest
import app

from datetime import date
from games_app.extensions import app, db, bcrypt
from games_app.models import User, Post, Game

'''
python -m unittest games_app.tests
'''

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_user():
    # Creates a user with username 'me1' and password of 'password'
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()
    
def create_publisher():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me2', password=password_hash, is_publisher = True, name='me2')
    db.session.add(user)
    db.session.commit()
    
    
def create_game():
    game = Game(title='Fortnite')
    db.session.add(game)
    db.session.commit()
    
class Tests(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        
    def test_homepage(self):
        create_game()
        
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        response_text = response.get_data(as_text=True)
        
        self.assertIn('Fortnite', response_text)
        self.assertIn('Sign Up', response_text)
        self.assertIn('Log In', response_text)
        
    def test_create_game(self):
        create_game()
        create_publisher()
        login(self.app, 'me2', 'password')
    
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        response_text = response.get_data(as_text=True)
        
        self.assertIn('Create Game', response_text)
        self.assertIn('me2', response_text)
        
    def test_post_not_logged_in(self):
        create_game()
        
        response = self.app.get('/game_detail/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        response_text = response.get_data(as_text=True)

        self.assertIn('Fortnite', response_text)
        self.assertIn('Please log in or sign up to view and leave comments', response_text)
        self.assertNotIn('Leave a comment!', response_text)
        
    def test_post(self):
        create_game()
        create_user()
        login(self.app, 'me1', 'password')
        
        post_data = {
            'data' : 'Great Game',
            'user_id': 1,
            'game_id' : 1
        }
        self.app.get('/game_detail/1', follow_redirects=True)
        response = self.app.post('/game_detail/1', data=post_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        response_text = response.get_data(as_text=True)
        
        self.assertIn('Fortnite', response_text)
        self.assertIn('Great Game', response_text)
        self.assertIn('me1', response_text)
        
    def test_publisher_profile(self):
        create_game()
        create_publisher()
        login(self.app, 'me2', 'password')
        
        response = self.app.get('/profile/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        response_text = response.get_data(as_text=True)
        
        self.assertIn('me2',response_text)
        self.assertIn('Games published', response_text)
        
    def test_user_profile(self):
        create_user()
        login(self.app, 'me1', 'password')
        
        response = self.app.get('/profile/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        response_text = response.get_data(as_text=True)
        
        self.assertIn('me1', response_text)
        self.assertIn('Favorite Games', response_text)