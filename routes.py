from flask import (
    render_template,
    redirect,
    flash,
    url_for,
    session,
    request
)
from functools import wraps
from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from sqlalchemy.orm import sessionmaker

from werkzeug.routing import BuildError

from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
)

from sqlalchemy import inspect, func
from flask_admin import Admin, AdminIndexView, expose
from app import create_app,db,login_manager,bcrypt
from models import *
from forms import login_form,register_form
from datetime import datetime, timedelta
from random import randint, choice
from faker import Faker


# Define user loader for flask-login
@login_manager.user_loader
def load_user(user_id):
    # Return the user object for the given user_id
    return User.query.get(int(user_id))

# Create an instance of the Flask application
app = create_app()

with app.app_context():
    # Get a list of all tables in the database
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    

    admin = Admin(name = "Coin Keeper", template_mode= "bootstrap3", index_view=HomeView())
    admin.add_view(UserView(User, db.session, endpoint = "user"))
    admin.add_view(CoachView(CoachExpenses, db.session, endpoint = "coach"))
    admin.add_view(HallView(HallExpenses, db.session, endpoint = "hall"))
    admin.add_view(AnnouncementView(Announcement, db.session, endpoint = "announcement"))
    admin.add_view(SessionsView(Sessions, db.session, endpoint = "sessions"))
    
    admin.init_app(app)
    
    # fakes info
    fake = Faker()
    
    # TEST DATA FOR ROLES
    role_user = Role(name = "user")
    role_treasurer = Role(name = "treasurer")
    role_coach = Role(name = "coach")
    
    for i in [role_user, role_treasurer, role_coach]:
        role = i.name
        existing_role = Role.query.filter_by(name=role).first()
        if existing_role is None:
            db.session.add(i)
    db.session.commit()
    
    # TEST DATA FOR USERS
    
    role_user = Role.query.filter_by(name="user").first()
    role_treasurer = Role.query.filter_by(name="treasurer").first()
    role_coach = Role.query.filter_by(name="coach").first()
    
    user_admin = User(username = "admin", pwd = bcrypt.generate_password_hash("admin123"), displayname = "Admin")
    user_admin.roles = [role_treasurer, role_coach]
    
    user_treasurer = User(username = "treasurer", pwd = bcrypt.generate_password_hash("treasurer123"), displayname = "Treasurer")
    user_treasurer.roles = [role_treasurer]
    
    user_coach = User(username = "coach", pwd = bcrypt.generate_password_hash("coach123"), displayname = "Coach")
    user_coach.roles = [role_coach]

    for i in range(10):
        name = f"user{i}"
        # Check if the username already exists in the table
        existing_user = User.query.filter_by(username=name).first()
        if existing_user is None:
            # If the username doesn't exist, create a new user
            user_user = User(username=name, pwd=bcrypt.generate_password_hash(f"user{i}pwd"), displayname = fake.name() , streak = randint(0,3), sessionsunpaid = randint(0,3))
            user_user.roles = [role_user]
            db.session.add(user_user)
    
    for i in [user_admin, user_treasurer, user_coach]:
        name = i.username
        existing_user = User.query.filter_by(username=name).first()
        if existing_user is None:
            db.session.add(i)
    db.session.commit()
    
    

    # TEST DATA FOR COACH EXPENSES
    if CoachExpenses.query.count() < 10:
        for _ in range(10 - CoachExpenses.query.count()):
            coach_expense = CoachExpenses(
                type=choice(['Payroll', 'Equipment']),
                name=fake.company(),
                urgency=randint(0, 3),
                paid=fake.boolean(),
                amount=randint(100, 1000),
                due=fake.date_between(start_date='-1y', end_date='+1y')
            )
            db.session.add(coach_expense)

    
    # TEST DATA FOR HALL EXPENSES
    if HallExpenses.query.count() < 10:
        for _ in range(10 - HallExpenses.query.count()):
            hall_expense = HallExpenses(
                type=choice(['Rent', 'Food and Drink', 'Insurance', 'Maintenance', 'Utilities']),
                name=fake.company(),
                urgency=randint(0, 3),
                paid=fake.boolean(),
                amount=randint(100, 1000),
                due=fake.date_between(start_date='-1y', end_date='+1y')
            )
            db.session.add(hall_expense)

    
    # TEST DATA FOR ANNOUNCEMENTS
    if Announcement.query.count() < 3:
        for _ in range(3 - Announcement.query.count()):
            announcement = Announcement(
                name=fake.name(),
                title=fake.sentence(),
                body=fake.paragraph(),
                date=fake.date_between(start_date='-1y', end_date='+1y')
            )
            db.session.add(announcement)


    
    # TEST DATA FOR SESSIONS (WEEKLY)
    if Sessions.query.count() < 10:
        start_date = datetime.now().date() - timedelta(days=7 * 10)  # 10 weeks ago
        for i in range(10 - Sessions.query.count()):
            session_date = start_date + timedelta(days=7 * i)
            
            starthour = randint(10,18)
            starttime = datetime.strptime(f"{starthour}:00", "%H:%M").time()
            endtime = (datetime.combine(datetime.min, starttime) + timedelta(hours=1)).time()
            session = Sessions(date=session_date, starttime=starttime, endtime=endtime )
            # Add random attendees (users)
            attendees = User.query.filter(User.roles.any(name="user")).order_by(func.random()).limit(randint(1, 5)).all()
            session.attendees.extend(attendees)
            db.session.add(session)
    
    db.session.commit()

# Define a function to be run before each request
@app.before_request
def session_handler():
    # Set the session to be permanent
    session.permanent = True
    # Set the lifetime of the session to be 1 minute
    app.permanent_session_lifetime = timedelta(minutes=1)

# Define the route for the index page
@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    return render_template("index.html",title="Home", announcements = Announcement.query.all(), sessions = Sessions.query.all())

# Define the route for the login page
@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    # Create an instance of the login form
    form = login_form()
    # If the form is submitted and validated    
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                if user.username == "admin" or user.username == "treasurer" or user.username == "coach":
                    return redirect(url_for("admin"))
                else:
                    return redirect(url_for('index'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template("auth.html",
        form=form,
        text="Login",
        title="Login",
        btn_action="Login"
        )

# Register route
@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    # Create an instance of the registration form
    form = register_form()
    # If the form is submitted and validated
    if form.validate_on_submit():
        try:
            # Get the password, username, and display name from the form data
            pwd = form.pwd.data
            pwd = form.pwd.data
            # Create a new user with the form data and hashed password
            username = form.username.data
            displayname = form.displayname.data
            newuser = User(
                username=username,
                pwd=bcrypt.generate_password_hash(pwd),
                displayname=displayname
            )
            newuser.roles = [Role.query.filter_by(name = "user").first()]
            # Add the new user to the session and commit the session to the database
            db.session.add(newuser)
            db.session.commit()
            flash(f"Account Succesfully created", "success")
            # Redirect to the login page
            return redirect(url_for("login"))
        # Handle various exceptions 
        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occured !", "danger")
    # Render the registration page with the form
    return render_template("auth.html",
        form=form,
        text="Create account",
        title="Register",
        btn_action="Register account"
        )

@app.route("/admin/", methods=("GET", "POST"), strict_slashes=False)
def admin():
    return render_template("/admin",title="Admin",)

@app.route('/pay_hall', methods=['POST'])
def pay_hall_expense():
    expense_id = request.form['pay_to']
    amount_paid = float(request.form['Pay_Amount'])

    # Call your function to pay the hall expense
    pay_hallexpense(expense_id, amount_paid)

    return redirect(url_for("admin"))

@app.route('/pay_coach', methods=['POST'])
def pay_coach_expense():
    expense_id = request.form['pay_to']
    amount_paid = float(request.form['Pay_Amount'])

    # Call your function to pay the coach expense
    pay_coachexpense(expense_id, amount_paid)

    return redirect(url_for("admin"))

# Define the route for the logout page
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

def pay_hallexpense(expense_id, amount_paid):
    # Try to get the Expense instance with the given id
    expense = db.session.get(HallExpenses, expense_id)
    
    if expense is not None:
        # If the Expense instance exists, update its paid status and amount
        if expense.amount <= amount_paid:
            expense.paid = True
            expense.amount = 0
        else:
            expense.amount -= amount_paid

        # Commit the changes to the database
        db.session.commit()

def pay_coachexpense(expense_id, amount_paid):
    expense = db.session.get(CoachExpenses, expense_id)
    
    if expense is not None:
        # If the Expense instance exists, update its paid status and amount
        if expense.amount <= amount_paid:
            expense.paid = True
            expense.amount = 0
        else:
            expense.amount -= amount_paid

        # Commit the changes to the database
        db.session.commit()