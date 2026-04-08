from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# create table
conn = sqlite3.connect('todo.db')
conn.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, content TEXT, completed INTEGER DEFAULT 0)')
conn.close()

# connect db
def get_db():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row
    return conn

# home
@app.route('/')
def index():
    conn = get_db()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# add task
@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    conn = get_db()
    conn.execute('INSERT INTO tasks (content) VALUES (?)', (task,))
    conn.commit()
    conn.close()
    return redirect('/')

# delete task
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# ✅ complete task (VERY IMPORTANT FIX)
@app.route('/complete/<int:id>')
def complete(id):
    conn = get_db()
    conn.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)