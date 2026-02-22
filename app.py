from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL connection
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="admin",          # change if needed
        password="root",  # your MySQL password
        database="study_planner"
    )

@app.route("/", methods=["GET", "POST"])
def index():
    db = get_db()
    cursor = db.cursor()

    if request.method == "POST":
        query = """
        INSERT INTO tasks (subject, topic, date, priority)
        VALUES (%s, %s, %s, %s)
        """
        values = (
            request.form["subject"],
            request.form["topic"],
            request.form["date"],
            request.form["priority"]
        )
        cursor.execute(query, values)
        db.commit()
        return redirect("/")

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (id,))
    db.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
