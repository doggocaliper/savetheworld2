import random
from flask import Flask, redirect, url_for, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS matches
                     (n_id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     sex TEXT NOT NULL,
                     birthyear INTEGER(4) NOT NULL,
                     classs INTEGER(4) NOT NULL,
                     ighandle TEXT NOT NULL,
                     sexuality TEXT NOT NULL,
                     interests TEXT NOT NULL,
                     mbti TEXT NOT NULL,
                     matchedmbti TEXT NOT NULL)''')

    conn.commit()
    conn.close()

@app.route("/")
def homepage():
  return render_template('index.html')

@app.route("/matchme.html", methods=['GET', 'POST'])
def matchme():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    name = ''
    sex = ''
    birthyear = ''
    classs = ''
    sexuality = ''
    ighandle = ''
    interests = ''
    mbti = ''
    matchedmbti = ''
    if request.method == 'POST':
        name = request.form.get('name')
        sex = request.form.get('sex')
        birthyear = request.form.get('birthyear')
        classs = request.form.get('classs')
        sexuality = request.form.get('sexuality')
        ighandle = request.form.get('ighandle')
        interests = request.form.get('interests')
        mbti = request.form.get('mbti')
        matchedmbti = request.form.get('matchedmbti')

        cur.execute("INSERT INTO matches (name, sex, birthyear, classs, sexuality, ighandle, interests, mbti, matchedmbti) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, sex, birthyear, classs, sexuality, ighandle, interests, mbti, matchedmbti))

        conn.commit()
        return redirect(url_for('matchme'))
    cur.execute(""" 
                    SELECT name, sex, birthyear, classs, ighandle, sexuality, interests, mbti, matchedmbti
                    FROM matches;""")
    matches = cur.fetchall()
    conn.close()
    return render_template('matchme.html', name=name, sex=sex, birthyear=birthyear, classs=classs, sexuality=sexuality, ighandle=ighandle, interests=interests, mbti=mbti, matchedmbti=matchedmbti)
    # , name=name, sex=sex, birthyear=birthyear, classs=classs, sexuality=sexuality, ighandle=ighandle, interests=interests, mbti=mbti, matchedmbti=matchedmbti

@app.route("/tips.html")
def tips():
  with open('data.txt') as f:
       tips = [tip.strip() for tip in f.readlines()]
       tip = random.choice(tips)
  return render_template('tips.html', tip=tip)

@app.route("/chatgpt.html")
def chatgpt():
  return render_template('chatgpt.html')

@app.route("/typetest.html")
def typetest():
  return render_template('typetest.html')

@app.route("/index.html")
def admin():
  return redirect(url_for("homepage"))

@app.route('/matchwith.html')
def matchwith():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(""" 
                    SELECT name, sex, birthyear, classs, ighandle, sexuality, interests, mbti, matchedmbti
                    FROM matches;""")
  
    matches = cur.fetchall()
    conn.close()
    return render_template('matchwith.html', matches=matches)

@app.route('/chatgpt.html', methods=['POST'])

def get_bot_response():
    user_input = request.form['user_input']
    print(user_input)
    messages.append({'role': 'user', 'content': user_input})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ai_response = completion.choices[0].message['content']
    print(ai_response)
    messages.append({'role': 'assistant', 'content': ai_response})
    print(messages)
    return  Markup(markdown.markdown(ai_response, extensions=['fenced_code', 'codehilite']))
@app.route('/reset')
def reset():
    global messages
    messages = []
    return "Conversation history has been reset."

  
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=81)
