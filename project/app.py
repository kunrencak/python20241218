from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import random

app = Flask(__name__)

def init_db():
    with sqlite3.connect("participants.db") as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS participants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        conn.commit()

@app.route('/')
def index():
    with sqlite3.connect("participants.db") as conn:
        c = conn.cursor()
        c.execute("SELECT name FROM participants")
        participants = [row[0] for row in c.fetchall()]
    return render_template('index.html', participants=participants) # render_template を使うことで、FlaskはHTMLファイルをテンプレートとして処理

@app.route('/add', methods=['POST'])
def add_participant():
    name = request.form['name']
    if name:
        with sqlite3.connect("participants.db") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO participants (name) VALUES (?)", (name,))
            conn.commit()
    return redirect(url_for('index'))

@app.route('/shuffle')
def shuffle_participants():
    with sqlite3.connect("participants.db") as conn:
        c = conn.cursor()
        c.execute("SELECT name FROM participants")
        participants = [row[0] for row in c.fetchall()]
    random.shuffle(participants)
    return render_template('index.html', participants=participants, shuffled=True)

@app.route('/reset', methods=['POST'])
def reset_participants():
    with sqlite3.connect("participants.db") as conn:
        c = conn.cursor()
        c.execute("DELETE FROM participants")  # すべてのデータを削除
        conn.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
