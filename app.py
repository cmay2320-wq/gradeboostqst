from flask import Flask, render_template, request, redirect, session

import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# =========================
# SECURITY
# =========================

app.secret_key = os.environ.get("SECRET_KEY", "Cmay$0761986009")

ADMIN_PASSWORD = os.environ.get(
    "ADMIN_PASSWORD",
    "admin0760"
)

DATABASE_URL = os.environ.get("DATABASE_URL")

# =========================
# DATABASE SETUP
# =========================

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():

    conn = get_db_connection()

    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS responses (

            id SERIAL PRIMARY KEY,

            name TEXT,
            education_level TEXT,
            institution TEXT,

            hardest_subject TEXT,
            biggest_problem TEXT,

            wanted_feature TEXT,
            study_time TEXT,
            study_style TEXT,

            ai_help TEXT,

            pay_interest TEXT,
            price_range TEXT,

            current_tools TEXT,
            missing_feature TEXT,

            extra TEXT
        )
    """)

    conn.commit()

    c.close()
    conn.close()
init_db()

# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    return render_template("index.html")

# =========================
# FORM SUBMISSION
# =========================

@app.route("/submit", methods=["POST"])
def submit():

    data = (
        request.form.get("name"),
        request.form.get("education_level"),
        request.form.get("institution"),

        request.form.get("hardest_subject"),
        request.form.get("biggest_problem"),

        request.form.get("wanted_feature"),
        request.form.get("study_time"),
        request.form.get("study_style"),

        request.form.get("ai_help"),

        request.form.get("pay_interest"),
        request.form.get("price_range"),

        request.form.get("current_tools"),
        request.form.get("missing_feature"),

        request.form.get("extra")
    )

    conn = get_db_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO responses (

            name,
            education_level,
            institution,

            hardest_subject,
            biggest_problem,

            wanted_feature,
            study_time,
            study_style,

            ai_help,

            pay_interest,
            price_range,

            current_tools,
            missing_feature,

            extra

        )

        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, data)

    conn.commit()
    conn.close()

    return redirect("/thankyou")

# =========================
# THANK YOU PAGE
# =========================

@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

# =========================
# ADMIN LOGIN + RESPONSES
# =========================

@app.route("/admin", methods=["GET", "POST"])
def admin():

    # Login check
    if request.method == "POST":

        password = request.form.get("password")

        if password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/admin")

        else:
            return """
            <h2 style='font-family:Arial;'>Wrong password</h2>
            <a href='/admin'>Try Again</a>
            """

    # Not logged in
    if not session.get("admin"):

        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Admin Login</title>

            <style>
                body{
                    font-family:Arial;
                    background:#0f172a;
                    color:white;
                    display:flex;
                    justify-content:center;
                    align-items:center;
                    height:100vh;
                    margin:0;
                }

                .box{
                    background:#1e293b;
                    padding:40px;
                    border-radius:20px;
                    width:320px;
                    box-shadow:0 0 40px rgba(0,0,0,0.4);
                }

                input{
                    width:100%;
                    padding:14px;
                    border:none;
                    border-radius:10px;
                    margin-top:15px;
                }

                button{
                    width:100%;
                    padding:14px;
                    border:none;
                    border-radius:10px;
                    margin-top:20px;
                    background:#3b82f6;
                    color:white;
                    font-weight:bold;
                    cursor:pointer;
                }

                h2{
                    margin-top:0;
                }
            </style>
        </head>

        <body>

            <div class="box">
                <h2>Admin Login</h2>

                <form method="POST">

                    <input
                        type="password"
                        name="password"
                        placeholder="Enter admin password"
                        required
                    >

                    <button type="submit">
                        Login
                    </button>

                </form>
            </div>

        </body>
        </html>
        """

    # Get all responses
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("""
        SELECT * FROM responses
        ORDER BY id DESC
    """)

    responses = c.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        responses=responses
    )

# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect("/admin")

# =========================
# START APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)