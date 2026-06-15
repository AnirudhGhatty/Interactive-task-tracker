from flask import Flask
from flask import render_template
import mysql.connector
from flask import request, redirect, url_for

db = mysql.connector.connect(
    host="localhost",
    user="Anirudh",
    password="root",
    database="task_tracker"
)

cursor = db.cursor()

app = Flask(__name__)

@app.route("/")
def hello_world():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    cursor.execute("SELECT * FROM schedule")
    schedule = cursor.fetchall()
    return render_template("index.html" , tasks = tasks , schedule = schedule)


@app.route("/about")
def aboutl():
    return render_template("about.html")


@app.route("/goal")
def goals():
    return render_template("goals.html")


@app.route("/add" , methods = ["POST" , "GET"])
def add():
     task = request.form["task"]
     cursor.execute("INSERT INTO tasks (name) VALUES (%s)", (task,))
     db.commit()
     return redirect(url_for("hello_world"))


@app.route("/delete/<int:id>")
def delete(id):
    cursor.execute("DELETE FROM tasks WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for("hello_world"))


@app.route("/update_schedule/<int:id>", methods=["POST"])
def update_schedule(id):
    updated_task = request.form["updated_task"]
    cursor.execute("UPDATE schedule SET task = %s WHERE id = %s", (updated_task, id))
    db.commit()
    return redirect(url_for("hello_world"))


if __name__ == '__main__':
    app.run(debug=True)