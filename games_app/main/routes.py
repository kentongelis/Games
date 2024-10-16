from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from datetime import date, datetime
import os

from games_app.main.forms import GameForm, PostForm
from games_app.models import Game, User, Post


# Import app and db from events_app package so that we can run app

from games_app.extensions import app, bcrypt, db

main = Blueprint("main", __name__)


@main.route("/")
def homepage():
    all_games = Game.query.all()
    return render_template("home.html", all_games=all_games)


@main.route("/create_game", methods=["GET", "POST"])
@login_required
def create_game():
    form = GameForm()
    if form.validate_on_submit():

        new_game = Game(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            rating=form.rating.data,
            publisher=current_user,
        )

        uploaded_file = form.image.data
        filename = secure_filename(uploaded_file.filename)
        pic_path = os.path.join(app.config["UPLOAD_PATH"], filename)
        uploaded_file.save(pic_path)
        new_game.image = pic_path
        path_list = pic_path.split("/")[1:]
        new_path = "/".join(path_list)

        new_game.image = new_path
        db.session.add(new_game)
        db.session.commit()

        current_user.games.append(new_game)
        db.session.commit()

        flash("New game was created!")
        return redirect(url_for("main.game_detail", game_id=new_game.id))
    else:
        print(form.errors)
        return render_template("create_game.html", form=form)


@main.route("/game_detail/<game_id>", methods=["GET", "POST"])
def game_detail(game_id):
    game = Game.query.get(game_id)
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            data=form.data.data,
            date=date.today(),
            user_id=current_user.id,
            game_id=game_id,
        )

        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("main.game_detail", game_id=game.id))

    return render_template("game_detail.html", game=game, form=form)


@main.route("/edit_game/<game_id>", methods=["GET", "POST"])
def edit_game(game_id):
    game = Game.query.get(game_id)
    form = GameForm(obj=game)
    if form.validate_on_submit():
        uploaded_file = form.image.data
        filename = secure_filename(uploaded_file.filename)
        pic_path = os.path.join(app.config["UPLOAD_PATH"], filename)
        uploaded_file.save(pic_path)
        path_list = pic_path.split("/")[1:]
        new_path = "/".join(path_list)

        game.title = form.title.data
        game.description = form.description.data
        game.price = form.price.data
        game.image = new_path
        game.rating = form.rating.data

        db.session.commit()

        return redirect(url_for("main.game_detail", game_id=game.id))
    print(form.errors)
    return render_template("edit_game.html", form=form, game=game)


@main.route("/profile/<user_id>")
def profile(user_id):
    user = User.query.get(user_id)

    return render_template("profile.html", user=user)


@main.route("/favorite/<game_id>", methods=["POST"])
@login_required
def favorite_game(game_id):
    game = Game.query.get(game_id)
    current_user.fav_games.append(game)
    db.session.commit()
    return redirect(url_for("main.game_detail", game_id=game.id))


@main.route("/unfavorite/<game_id>", methods=["POST"])
@login_required
def unfavorite_game(game_id):
    game = Game.query.get(game_id)
    current_user.fav_games.remove(game)
    db.session.commit()
    return redirect(url_for("main.game_detail", game_id=game.id))
