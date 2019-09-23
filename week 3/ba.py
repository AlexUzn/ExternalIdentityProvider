from flask import Flask, flash, redirect, render_template, request, session, abort, redirect
import os
app = Flask(__name__)
import random

#@app.route("/")
#def ba_login():
 #   return render_template('ba_login.html')

@app.route("/")
def trueme():
    redirecturl = "http://127.0.0.1:5000/"
    return render_template('ba_login.html', redirecturl = redirecturl, client = "BrusselsAirlines") #redirecturl -> which server to go to client --> which client in use

cache = {}
cache['score'] = 0
cache['current_user'] = {}


@app.route("/ask_game")
def ask_game():
    user=request.args.get('user')
    global cache
    cache['score'] = 0
    cache['current_user'] = user
    return render_template("ask_game.html", user=user)
    # highscore=cache["score"].get("highscore",0)
    
@app.route('/question')
def get_question():
    question = request.args.get('question')
    if question == 'capital':
        return render_template('capital.html')
    if question == 'food':
        return render_template('food.html')
    if question == 'person':
        return render_template('person.html') 
    if question == 'landmark':
        return render_template('landmark.html')
    if question == 'greeting':
        return render_template('greeting.html')
    if question == 'score':
        score = cache['score']
        highscore = 4
        return render_template('score.html', score = score, highscore = highscore) 
    return render_template('ask_game.html')

answer_sheet = {
    'capital': 'rome',
    'food': 'pizza',
    'person': 'leonardo da vinci',
    'landmark': 'leaning tower of pisa',
    'greeting': 'ciao'
}

next_question_dict = {
    'capital': 'food',
    'food':'person',
    'person': 'landmark',
    'landmark':'greeting',
    'greeting':'score',
}

@app.route('/answer', methods=['POST'])
def give_answer():
    global cache
    question = request.form.get('question')
    answer = request.form.get('answer')
    correct = False
    if answer == answer_sheet[question]:
        correct = True
        cache['score'] = cache['score'] + 1

    return render_template('answer.html', correct=correct, next_question=next_question_dict[question], cache=cache)

@app.route('/payment')
def choose_flights():
    return render_template('payment.html')

    
if __name__ == '__main__':
    app.run(port=5000, debug=True)