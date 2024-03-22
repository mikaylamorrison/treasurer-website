from flask import (
    render_template,
    redirect,
    flash,
    url_for,
    session
)
from  datetime import date,datetime,timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from datetime import date, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

from flask_login import (
    login_user,
    logout_user,
    login_required,
)
from sqlalchemy import MetaData, create_engine

from app import create_app,db
from models import User, Expense,UserView,ExpenseView

app = create_app()

with app.app_context():
    start_date = date(date.today().year, 3, 1)  # March 1 of the current year

    for id in range(1, 25):  # Loop from 1 to 24
        due_date = start_date + timedelta(weeks=2 * (id - 1))
        paid = False

        # Create a new Expense instance
        expense = Expense(id=id, type="Payroll", name=f"Liam{id}",urgency=0,paid=paid, due=due_date, amount=50)

        # Set the urgency based on the due_date and paid status
        if paid:
            expense.urgency = 0
        elif due_date < date.today() and not paid:
            expense.urgency = 3
        elif date.today() <= due_date <= date.today() + timedelta(days=14) and not paid:
            expense.urgency = 2
        elif due_date > date.today() + timedelta(days=7) and not paid:
            expense.urgency = 1

        # Add the new Expense to the session
        db.session.add(expense)

    # Commit the session to apply the changes to the database
    db.session.commit()
