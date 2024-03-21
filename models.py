from app import db
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
# Define User model
class User(UserMixin, db.Model):
    # Specify the table name
    __tablename__ = "user"
    # Define the columns for the User table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False, unique=True)
    displayname = db.Column(db.String, default = username, nullable = False)
    streak = db.Column(db.Integer, default = 0, nullable = False)
    sessionsunpaid = db.Column(db.Integer, default = 0, nullable = False)
    usertype = db.Column(db.Integer, default = 0, nullable=False)
    
    # Define the string representation of the User model
    def __repr__(self):
        return '<User %r>' % self.username
# Define UserView for Flask-Admin
class UserView(ModelView):
    # Specify the columns to display in the list view
    column_list = ["displayname", "username", "streak", "sessionsunpaid"]
    # Specify the columns that can be edited directly in the list view
    column_editable_list=["streak", "sessionsunpaid"]
    # Specify the labels for the columns
    column_labels={"displayname": "Name", "username": "Username", "streak":"Streak", "sessionsunpaid":"Sessions Unpaid"}

# Define Expense model
class Expense(db.Model):
    __tablename__ = "expense"
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), nullable = False)
    name = db.Column(db.String(100), unique=True, nullable = False)
    urgency = db.Column(db.Integer, default = 0, nullable = False)
    paid = db.Column(db.Boolean, default = False, nullable = False)
    due = db.Column(db.Date, nullable= False)
    
    def __repr__(self):
        return '<Expense %r>' % self.name
# Define ExpenseView for Flask-Admin
class ExpenseView(ModelView):
    column_list = ["name", "type", "urgency", "paid", "due"]
    column_editable_list = ["name", "type", "urgency", "paid", "due"]
    column_labels={"name":"Name", "type":"Type", "urgency":"Urgency", "paid":"Paid?", "due":"Due Date"}
    form_choices = {
    'type': [
        ('Rent', 'Rent'),
        ('Payroll', 'Payroll'),
        ('Discount', 'Discount'),
        ('Food and Drink', 'Food and Drink'),
        ('Insurance', 'Insurance'),
        ('Maintenance', 'Maintenance'),
        ('Utilities', 'Utilities')
    ],
    'urgency':[
        (0,'0'),
        (1,'1'),
        (2,'2'),
        (3,'3')
        ]
}
    
