from datetime import date, datetime, timedelta

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, MetaData, Table
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)

from app import create_app, db
from models import User, Expense, UserView, ExpenseView

app = create_app()


with app.app_context():
    # Get a list of all tables in the database
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    # Check if the Expense table exists
    if 'expense' not in tables:
        # Create the Expense table
        Expense.__table__.create(bind=db.engine)

    start_date = date(date.today().year, 3, 1)  # March 1 of the current year

    for id in range(1, 25):  # Loop from 1 to 24
        due_date = start_date + timedelta(weeks=2 * (id - 1))
        paid = False

        # Try to get the Expense instance with the given id
        expense = db.session.get(Expense, id)

        if expense is None:
            # If the Expense instance doesn't exist, create a new one
            expense = Expense(id=id, type="Payroll", name=f"Liam{id}", urgency=0, paid=paid, due=due_date, amount=50)
            # Add the new Expense to the session
            db.session.add(expense)
        else:
            # If the Expense instance exists, update its fields
            expense.type = "Payroll"
            expense.name = f"Liam{id}"
            expense.urgency = 0
            expense.paid = paid
            expense.due = due_date
            expense.amount = 50

        # Set the urgency based on the due_date and paid status
        if paid:
            expense.urgency = 0
        elif due_date < date.today() and not paid:
            expense.urgency = 3
        elif date.today() <= due_date <= date.today() + timedelta(days=14) and not paid:
            expense.urgency = 2
        elif due_date > date.today() + timedelta(days=7) and not paid:
            expense.urgency = 1

    # Commit the changes to the database
    db.session.commit()

# code for button to pay
def pay_expense(expense_id, amount_paid):
    # Try to get the Expense instance with the given id
    expense = db.session.get(Expense, expense_id)

    if expense is not None:
        # If the Expense instance exists, update its paid status and amount
        expense.paid = True
        expense.amount -= amount_paid

        # Commit the changes to the database
        db.session.commit()