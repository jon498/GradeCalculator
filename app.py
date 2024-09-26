import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from login import login_required

# Configure application
app = Flask(__name__)
if __name__ == "main":
    app.run()

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///study.db")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        incorrect = False
        incorrect2 = False
        incorrect3 = False
        if not username:
            incorrect = True
            return render_template("register.html", incorrect = incorrect)

        # Ensure password was submitted
        elif not password:
            incorrect = True
            return render_template("register.html", incorrect = incorrect)

        # Ensure confirmation was submitted
        elif not confirmation:
            incorrect = True
            return render_template("register.html", incorrect = incorrect)

        # Ensure password and confirmation match
        elif password != confirmation:
            incorrect2 = True
            return render_template("register.html", incorrect2 = incorrect2, username = username)

        # Store user infomration into database
        password_hash = generate_password_hash(password)
        try:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, password_hash)
        except:
            incorrect3 = True
            return render_template("register.html", incorrect3 = incorrect3, username = username)

        # Set session as to new_user
        session["user_id"] = new_user

        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        incorrect2 = False
        if not username:
            incorrect2 = True
            return render_template("login.html", incorrect2 = incorrect2)

        # Ensure password was submitted
        elif not password:
            incorrect2 = True
            return render_template("login.html", incorrect2 = incorrect2)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        incorrect = False
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            incorrect = True
            return render_template("login.html", incorrect = incorrect, username = username)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/grades", methods=["GET", "POST"])
def grades():

    if request.method == "POST":

        template = False

        # Get inputted values
        category = request.form.get("category").upper()
        numerator = request.form.get("numerator")
        denominator = request.form.get("denominator")
        weight = request.form.get("weight")
        grades = db.execute("SELECT * FROM grades")

        # Make sure values are inputted
        if not category:
            flash('Please fill out all fields')
            return render_template("grades.html", grades = grades, category = category, numerator = numerator, denominator = denominator, weight = weight, template = template)
        elif not numerator:
            flash('Please fill out all fields')
            return render_template("grades.html", grades = grades, category = category, numerator = numerator, denominator = denominator, weight = weight, template = template)
        elif not denominator:
            flash('Please fill out all fields')
            return render_template("grades.html", grades = grades, category = category, numerator = numerator, denominator = denominator, weight = weight, template = template)
        elif not weight:
            flash('Please fill out all fields')
            return render_template("grades.html", grades = grades, category = category, numerator = numerator, denominator = denominator, weight = weight, template = template)

        # Ensure numbers are positive integers
        try:
            numerator = int(numerator)
        except:
            flash('Numbers must be positive integers')
            return render_template("grades.html", grades = grades, category = category, numerator = numerator, denominator = denominator, weight = weight, template = template)
        try:
            denominator = int(denominator)
        except:
            flash('Numbers must be positive integers')
            return render_template("grades.html", grades = grades, category = category, numerator = numerator, denominator = denominator, weight = weight, template = template)
        try:
            weight = int(weight)
        except:
            flash('Numbers must be positive integers')
            return render_template("grades.html", grades = grades, category = category, numerator = numerator, denominator = denominator, weight = weight, template = template)

        if numerator < 0:
            flash('Numbers must be positive integers')
            return render_template("grades.html", grades = grades, category = category, numerator = numerator, denominator = denominator, weight = weight, template = template)
        if denominator < 0:
            flash('Numbers must be positive integers')
            return render_template("grades.html", grades = grades, category = category, numerator = numerator, denominator = denominator, weight = weight, template = template)
        elif weight < 0:
            flash('Numbers must be positive integers')
            return render_template("grades.html", grades = grades, category = category, numerator = numerator, denominator = denominator, weight = weight, template = template)

        # Check if category is already in table
        if len(grades) > 0:
            x = 0
            for row in grades:
                if category == grades[x]["category"]:
                    flash('Category already used')
                    return render_template("grades.html", grades = grades, category = category, numerator = numerator, denominator = denominator, weight = weight, template = template)
                x += 1

        # Insert new row into table
        db.execute("INSERT INTO grades (category, numerator, denominator, weight) VALUES(?,?,?,?)", category, numerator, denominator, weight)

        # Set auto_id
        grades = db.execute("SELECT * FROM grades")
        if len(grades) > 0:
            x = 1
            for row in grades:
                db.execute("UPDATE grades SET auto_id = (?) WHERE category = (?)", x, category)
                x += 1

        grades = db.execute("SELECT * FROM grades")
        return render_template("grades.html", grades = grades, template = template)

    else:

        # Clear table
        template = False
        grades = db.execute("SELECT * FROM grades")
        for row in grades:
            db.execute("DELETE FROM grades WHERE id = 0")

        return render_template("grades.html", template = template)

@app.route("/grades2", methods=["GET", "POST"])
def grades2():

    if request.method == "POST":

        template = False

        grades = db.execute("SELECT * FROM grades")

        # Check if user inputted category
        if not request.form.get("delete_button"):
            flash('Please input category to be deleted')

        # Get category to be deleted
        delete_button = request.form.get("delete_button")
        print(delete_button)
        x = 0
        for row in grades:
            if delete_button == grades[x]["category"]:

                # Delete grade from table
                db.execute("DELETE FROM grades WHERE category = (?)", delete_button)
                flash('Category deleted')

                # Return the form with category deleted
                grades = db.execute("SELECT * FROM grades")
                return render_template("grades.html", grades = grades, template = template)
            x += 1
        return render_template("grades.html", grades = grades, template = template)

    else:
        grades = db.execute("SELECT * FROM grades")
        return render_template("grades.html", grades = grades, template = template)


@app.route("/grades3", methods=["GET", "POST"])
def grades3():

    if request.method == "POST":

        name = db.execute("SELECT * FROM grades")[0]["course_name"]
        if name == '0':
            template = False
        else:
            template = True
        grades = db.execute("SELECT * FROM grades")

        # Get category and potential grade of assignment
        category = request.form.get("category")
        numerator = request.form.get("numerator")
        denominator = request.form.get("denominator")

        # See if there was already a input selected
        selected2 = False
        x = 0
        for row in grades:
            selected = False
            if category == grades[x]["category"]:
                selected = True
                selected2 = True
            x += 1
            print(selected)

        # Make sure values are inputted
        if len(grades) == 0:
            flash('Please input categories to calculate a grade')
            return render_template("grades.html", grades = grades, selected = selected, numerator = numerator, denominator = denominator, selected2 = selected2, template = template)
        elif not category:
            flash('Please fill out all fields')
            return render_template("grades.html", grades = grades, selected = selected, numerator = numerator, denominator = denominator, selected2 = selected2, template = template)
        elif not numerator:
            flash('Please fill out all fields')
            return render_template("grades.html", grades = grades, selected = selected, numerator = numerator, denominator = denominator, selected2 = selected2, template = template)
        elif not denominator:
            flash('Please fill out all fields')
            return render_template("grades.html", grades = grades, selected = selected, numerator = numerator, denominator = denominator, selected2 = selected2, template = template)

        # Ensure numbers are positive integers
        try:
            numerator = int(numerator)
        except:
            flash('Numbers must be positive integers')
            return render_template("grades.html", grades = grades, selected = selected, numerator = numerator, denominator = denominator, selected2 = selected2, template = template)
        try:
            denominator = int(denominator)
        except:
            flash('Numbers must be positive integers')
            return render_template("grades.html", grades = grades, selected = selected, numerator = numerator, denominator = denominator, selected2 = selected2, template = template)

        if numerator < 0:
            flash('Numbers must be positive integers')
            return render_template("grades.html", grades = grades, selected = selected, numerator = numerator, denominator = denominator, selected2 = selected2, template = template)
        elif denominator < 0:
            flash('Numbers must be positive integers')
            return render_template("grades.html", grades = grades, selected = selected, numerator = numerator, denominator = denominator, selected2 = selected2, template = template)

        # Get new values of numerator and denominator for inputted category
        new_numerator = numerator + int(db.execute("SELECT * FROM grades WHERE category = (?)", category)[0]["numerator"])
        new_denominator = denominator + int(db.execute("SELECT * FROM grades WHERE category = (?)", category)[0]["denominator"])

        # Add all grades together
        final_grade = 0
        x = 0
        for row in grades:
            if grades[x]["category"] == category:

                temp_weight = float(int(db.execute("SELECT * FROM grades WHERE category = (?)", category)[0]["weight"]) / 100.00)
                temp_percent = float(new_numerator / new_denominator)
                temp_total = float(temp_weight * temp_percent)

                final_grade = final_grade + temp_total
                x += 1

            else:

                temp_numerator = int(grades[x]["numerator"])
                temp_denominator = int(grades[x]["denominator"])

                temp_weight = float(int(grades[x]["weight"]) / 100.00)
                if temp_denominator != 0:
                    temp_percent = float(temp_numerator / temp_denominator)
                else:
                    temp_percent = 1
                temp_total = float(temp_weight * temp_percent)

                final_grade = final_grade + temp_total
                x += 1

        final_grade = float("%.2f" % (final_grade * 100.00))
        grades = db.execute("SELECT * FROM grades")
        return render_template("grades.html", grades = grades, final_grade = final_grade, category = category, numerator = numerator, denominator = denominator, template = template)

    else:
        template = False
        grades = db.execute("SELECT * FROM grades")
        return render_template("grades.html", grades = grades, template = template)


@app.route("/courses", methods=["GET", "POST"])
@login_required
def courses():

    if request.method == "POST":

        template = False
        grades = db.execute("SELECT * FROM grades")

        # Make sure there is an input
        if not request.form.get("course_name"):
            flash('Please enter a course name')
            return render_template("grades.html", grades = grades, template = template)

        # Check to see if anything was input into grades table
        if len(grades) == 0:
            flash('Insert grades before saving')
            return render_template("grades.html", template = template)
        else:
            user_id = session["user_id"]

            # Get course name
            course_name = request.form.get("course_name").upper()

            # See if course name is already in courses table
            courses = db.execute("SELECT * FROM courses WHERE user_id = (?) AND course_name = (?) order by course_name", user_id, course_name)
            if len(courses) != 0:
                flash('Course already exists')
                return render_template("grades.html", grades = grades, template = template)

            # Check to see how many entries are in courses
            id = 0
            courses = db.execute("SELECT * FROM courses WHERE user_id = (?) order by course_name", user_id)

            if len(courses) == 0:
                id = 0
            else:
                y = 0
                for row in courses:
                    if (courses[y]["id"]) > id:
                        id = courses[y]["id"]


            # Insert values from grades table into courses table
            x = 0
            for row in grades:
                category = grades[x]["category"]
                numerator = grades[x]["numerator"]
                denominator = grades[x]["denominator"]
                weight = grades[x]["weight"]

                # Add values to courses table
                db.execute("INSERT INTO courses (user_id, id, category, numerator, denominator, weight, course_name) VALUES(?,?,?,?,?,?,?)", user_id, id, category, numerator, denominator, weight, course_name)
                x += 1

            # Get unique course names
            uniques = db.execute("SELECT DISTINCT course_name FROM courses WHERE user_id = (?)", user_id)

            # Get all tables for current user
            courses = db.execute("SELECT * FROM courses WHERE user_id = (?) order by course_name", user_id)
            return render_template("grades.html", courses = courses, uniques = uniques, num_courses = len(uniques), template = template)

    else:
        user_id = session["user_id"]
        uniques = db.execute("SELECT DISTINCT course_name FROM courses WHERE user_id = (?)", user_id)
        courses = db.execute("SELECT * FROM courses WHERE user_id = (?) order by course_name", user_id)
        return render_template("courses.html", courses = courses, uniques = uniques, num_courses = len(uniques))


@app.route("/courses1", methods=["POST"])
@login_required
def courses1():

    # Make sure the user inputted a category
    user_id = session["user_id"]
    courses = db.execute("SELECT * FROM courses WHERE user_id = (?) order by course_name", user_id)
    uniques = db.execute("SELECT DISTINCT course_name FROM courses WHERE user_id = (?)", user_id)
    if not request.form.get("course_name"):
        flash('Please select a course')
        return render_template("courses.html", courses = courses, uniques = uniques, num_courses = len(uniques))

    # Get course that the user wants to update
    user_id = session["user_id"]
    course = request.form.get("course_name")
    courses1 = db.execute("SELECT * FROM courses WHERE user_id = (?) AND course_name = (?) order by course_name", user_id, course)

    # Delete any values in update table
    x = 0
    if len(courses) > 0:
        for row in courses1:
            db.execute("DELETE FROM update1 WHERE id = (?)", 0)

    # Insert course into update table
    x = 0
    if len(courses1) > 0:
        for row in courses1:
            category = courses1[x]["category"]
            numerator = courses1[x]["numerator"]
            denominator = courses1[x]["denominator"]
            weight = courses1[x]["weight"]
            db.execute("INSERT INTO update1 (user_id, course_name, category, numerator, denominator, weight) VALUES(?,?,?,?,?,?)", user_id, course, category, numerator, denominator, weight)
            x += 1

    edit = False
    updates = db.execute("SELECT * FROM update1")
    course_name = db.execute("SELECT * FROM update1")[0]["course_name"]
    return render_template("update.html", updates = updates, edit = edit)


@app.route("/courses2", methods=["POST"])
@login_required
def courses2():

    # Make sure the user inputted a category
    user_id = session["user_id"]
    courses = db.execute("SELECT * FROM courses WHERE user_id = (?) order by course_name", user_id)
    uniques = db.execute("SELECT DISTINCT course_name FROM courses WHERE user_id = (?)", user_id)
    if not request.form.get("course_name"):
        flash('Please select a course')
        return render_template("courses.html", courses = courses, uniques = uniques, num_courses = len(uniques))

    # Delete the course
    user_id = session["user_id"]
    course = request.form.get("course_name")
    courses1 = db.execute("SELECT * FROM courses WHERE user_id = (?) AND course_name = (?) order by course_name", user_id, course)
    for row in courses1:
        db.execute("DELETE FROM courses WHERE user_id = (?) AND course_name = (?)", user_id, course)

    courses = db.execute("SELECT * FROM courses WHERE user_id = (?) order by course_name", user_id)
    uniques = db.execute("SELECT DISTINCT course_name FROM courses WHERE user_id = (?)", user_id)
    return render_template("courses.html", courses = courses, uniques = uniques, num_courses = len(uniques))


@app.route("/update", methods=["POST"])
@login_required
def update():

    edit = True

    # Get inputted values
    updates = db.execute("SELECT * FROM update1")
    course_name = db.execute("SELECT * FROM update1")[0]["course_name"]
    category = request.form.get("category")
    numerator = request.form.get("numerator")
    denominator = request.form.get("denominator")
    weight = request.form.get("weight")

    # Make sure values are inputted
    if not numerator:
        flash('Please fill out all fields')
        return render_template("update.html", updates = updates, course_name = course_name, edit = edit, numerator = numerator, denominator = denominator, weight = weight)
    elif not denominator:
        flash('Please fill out all fields')
        return render_template("update.html", updates = updates, course_name = course_name, edit = edit, numerator = numerator, denominator = denominator, weight = weight)
    elif not weight:
        flash('Please fill out all fields')
        return render_template("update.html", updates = updates, course_name = course_name, edit = edit, numerator = numerator, denominator = denominator, weight = weight)

    # Ensure numbers are positive integers
    try:
        numerator = int(numerator)
    except:
        flash('Numbers must be positive integers')
        return render_template("update.html", updates = updates, course_name = course_name, edit = edit, numerator = numerator, denominator = denominator, weight = weight)
    try:
        denominator = int(denominator)
    except:
        flash('Numbers must be positive integers')
        return render_template("update.html", updates = updates, course_name = course_name, edit = edit, numerator = numerator, denominator = denominator, weight = weight)
    try:
        weight = int(weight)
    except:
        flash('Numbers must be positive integers')
        return render_template("update.html", updates = updates, course_name = course_name, edit = edit, numerator = numerator, denominator = denominator, weight = weight)

    if numerator < 0:
        flash('Numbers must be positive integers')
        return render_template("update.html", updates = updates, course_name = course_name, edit = edit, numerator = numerator, denominator = denominator, weight = weight)
    if denominator < 0:
        flash('Numbers must be positive integers')
        return render_template("update.html", updates = updates, course_name = course_name, edit = edit, numerator = numerator, denominator = denominator, weight = weight)
    elif weight < 0:
        flash('Numbers must be positive integers')
        return render_template("update.html", updates = updates, course_name = course_name, edit = edit, numerator = numerator, denominator = denominator, weight = weight)

    # Update values in update1 table
    db.execute("UPDATE update1 SET numerator = (?) WHERE category = (?)", numerator, category)
    db.execute("UPDATE update1 SET denominator = (?) WHERE category = (?)", denominator, category)
    db.execute("UPDATE update1 SET weight = (?) WHERE category = (?)", weight, category)

    # Update values in courses table
    db.execute("UPDATE courses SET numerator = (?) WHERE category = (?)", numerator, category)
    db.execute("UPDATE courses SET denominator = (?) WHERE category = (?)", denominator, category)
    db.execute("UPDATE courses SET weight = (?) WHERE category = (?)", weight, category)

    updates = db.execute("SELECT * FROM update1")
    return render_template("update.html", updates = updates, course_name = course_name, edit = edit)


@app.route("/update1", methods=["POST"])
@login_required
def update1():

    # Get inputted values
    updates = db.execute("SELECT * FROM update1")
    user_id = session["user_id"]
    course_name = db.execute("SELECT * FROM update1")[0]["course_name"]
    category = request.form.get("category").upper()
    numerator = request.form.get("numerator")
    denominator = request.form.get("denominator")
    weight = request.form.get("weight")

    # Make sure values are inputted
    if not category:
        flash('Please fill out all fields')
        return render_template("update.html", updates = updates, category = category, numerator = numerator, denominator = denominator, weight = weight)
    elif not numerator:
        flash('Please fill out all fields')
        return render_template("update.html", updates = updates, category = category, numerator = numerator, denominator = denominator, weight = weight)
    elif not denominator:
        flash('Please fill out all fields')
        return render_template("update.html", updates = updates, category = category, numerator = numerator, denominator = denominator, weight = weight)
    elif not weight:
        flash('Please fill out all fields')
        return render_template("update.html", updates = updates, category = category, numerator = numerator, denominator = denominator, weight = weight)

    # Ensure numbers are positive integers
    try:
        numerator = int(numerator)
    except:
        flash('Numbers must be positive integers')
        return render_template("update.html", updates = updates, category = category, numerator = numerator, denominator = denominator, weight = weight)
    try:
        denominator = int(denominator)
    except:
        flash('Numbers must be positive integers')
        return render_template("update.html", updates = updates, category = category, numerator = numerator, denominator = denominator, weight = weight)
    try:
        weight = int(weight)
    except:
        flash('Numbers must be positive integers')
        return render_template("update.html", updates = updates, category = category, numerator = numerator, denominator = denominator, weight = weight)

    if numerator < 0:
        flash('Numbers must be positive integers')
        return render_template("update.html", updates = updates, category = category, numerator = numerator, denominator = denominator, weight = weight)
    if denominator < 0:
        flash('Numbers must be positive integers')
        return render_template("update.html", updates = updates, category = category, numerator = numerator, denominator = denominator, weight = weight)
    elif weight < 0:
        flash('Numbers must be positive integers')
        return render_template("update.html", updates = updates, category = category, numerator = numerator, denominator = denominator, weight = weight)

    # Check if category is already in table
    x = 0
    for row in updates:
        if category == updates[x]["category"]:
            flash('Category already used')
            return render_template("update.html", updates = updates, course_name = course_name, numerator = numerator, denominator = denominator, weight = weight)
        x += 1

    db.execute("INSERT INTO courses (user_id, id, course_name, category, numerator, denominator, weight) VALUES(?,?,?,?,?,?,?)", user_id, 0, course_name, category, numerator, denominator, weight)
    db.execute("INSERT INTO update1 (user_id, course_name, category, numerator, denominator, weight) VALUES(?,?,?,?,?,?)", user_id, course_name, category, numerator, denominator, weight)

    updates = db.execute("SELECT * FROM update1")
    return render_template("update.html", updates = updates)


@app.route("/update2", methods=["POST"])
@login_required
def update2():

    # Make sure the user inputted a category
    user_id = session["user_id"]
    updates = db.execute("SELECT * FROM update1")
    if not request.form.get("category"):
        flash('Please choose a category')
        return render_template("update.html", updates = updates)

    # Delete the category
    category = request.form.get("category")
    course_name = db.execute("SELECT * FROM update1")[0]["course_name"]
    db.execute("DELETE FROM courses WHERE user_id = (?) AND course_name = (?) AND category = (?)", user_id, course_name, category)
    db.execute("DELETE FROM update1 WHERE course_name = (?) AND category = (?)", course_name, category)

    updates = db.execute("SELECT * FROM update1")
    return render_template("update.html", updates = updates)


@app.route("/edit", methods=["POST"])
@login_required
def edit():

    edit = True
    updates = db.execute("SELECT * FROM update1")
    course_name = db.execute("SELECT * FROM update1")[0]["course_name"]
    return render_template("update.html", updates = updates, edit = edit, course_name = course_name)


@app.route("/back", methods=["POST"])
@login_required
def back():

    edit = False
    user_id = session["user_id"]
    uniques = db.execute("SELECT DISTINCT course_name FROM courses WHERE user_id = (?)", user_id)
    courses = db.execute("SELECT * FROM courses WHERE user_id = (?) order by course_name", user_id)
    return render_template("courses.html", courses = courses, edit = edit, uniques = uniques, num_courses = len(uniques))


@app.route("/back2", methods=["POST"])
@login_required
def back2():

    edit = False
    updates = db.execute("SELECT * FROM update1")
    return render_template("update.html", updates = updates, edit = edit)


@app.route("/use", methods=["POST"])
@login_required
def use():

    # Get course values
    user_id = session["user_id"]
    course_name = request.form.get("course_name")
    courses = db.execute("SELECT * FROM courses WHERE user_id = (?) AND course_name = (?)", user_id, course_name)

    # Clear grades
    db.execute("DELETE FROM grades WHERE id = 0")

    # Insert into grades
    x = 0
    for row in courses:
        category = courses[x]["category"]
        numerator = courses[x]["numerator"]
        denominator = courses[x]["denominator"]
        weight = courses[x]["weight"]
        db.execute("INSERT INTO grades (auto_id, category, numerator, denominator, weight, course_name) VALUES(?,?,?,?,?,?)", (x + 1), category, numerator, denominator, weight, course_name)
        x += 1

    template = True
    grades = db.execute("SELECT * FROM grades")
    return render_template("grades.html", grades = grades, template = template)