from flask import (
    render_template,
    redirect,
    flash,
    url_for,
    session
)

from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError

from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

from flask_login import (
    login_user,
    logout_user,
    login_required,
)

from app import create_app,db,login_manager,bcrypt
from models import User
from forms import login_form,register_form

# Define user loader for flask-login
@login_manager.user_loader
def load_user(user_id):
    # Return the user object for the given user_id
    return User.query.get(int(user_id))

# Create an instance of the Flask application
app = create_app()

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
    
    return render_template("index.html",title="Home")

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
# Define the route for the logout page
@app.route("/logout")
# Require the user to be logged in to access this route
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
    