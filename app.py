from boggle import Boggle
from flask import Flask, redirect, render_template, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.pipconfig['SECRET_KEY'] = 'baby15567'

boggle_game = Boggle()

@app.route('/')
def homepage():
    """Show board."""

    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    return render_template('base.html', board=board, highscore=highscore, nplays=nplays)


@app.route('/check-word')
def check_word():
    """Check if word is in dictionary"""

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route('/post-score', methods=["POST"])
def post_score():
    """Recieve score, update nplays, update high score if appropriate."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)