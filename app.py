from flask import Flask, render_template, redirect, request, flash, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "1234"

# Moved the database connection setup inside the respective routes

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form['user_name']
        password = request.form['user_password']
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row  # Set row_factory to fetch results as dictionaries
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE name=? AND password=?", (name, password))
        data = cur.fetchone()
        conn.close()

        if data:
            session["name"] = data["name"]
            session["password"] = data["password"]
            return redirect(url_for("customer"))
        else:
            flash("Username and Password Mismatch")
            return redirect(url_for("index"))

    return render_template("index.html")

@app.route("/customer")
def customer():
    if "name" in session and "password" in session:
        return render_template("customer.html")
    else:
        return redirect(url_for("index"))

@app.route("/Register", methods=['GET', 'POST'])
def Register():
    if request.method == 'POST':
        try:
            name = request.form['name']
            contact = request.form['contact']
            email = request.form['mail']
            password = request.form['create_password']
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO user(name, contact, email, password) VALUES (?, ?, ?, ?)", (name, contact, email, password))
            conn.commit()
            flash("Record Added Successfully")
        except sqlite3.Error as e:
            flash("Error in Insert Operation: {}".format(str(e)), "danger")
        finally:
            conn.close()
            return redirect(url_for("index"))

    return render_template("Register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)


