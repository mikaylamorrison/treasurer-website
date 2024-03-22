from app import db
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView


class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False, unique=True)
    displayname = db.Column(db.String, default = username, nullable = False)
    streak = db.Column(db.Integer, default = 0, nullable = False)
    sessionsunpaid = db.Column(db.Integer, default = 0, nullable = False)
    usertype = db.Column(db.Integer, default = 0, nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.username

class UserView(ModelView):
    column_list = ["displayname", "username", "streak", "sessionsunpaid"]
    column_editable_list=["streak", "sessionsunpaid"]
    column_labels={"displayname": "Name", "username": "Username", "streak":"Streak", "sessionsunpaid":"Sessions Unpaid"}


class Expense(db.Model):
    __tablename__ = "expense"
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), nullable = False)
    name = db.Column(db.String(100), unique=True, nullable = False)
    urgency = db.Column(db.Integer, default = 0, nullable = False)
    paid = db.Column(db.Boolean, default = False, nullable = False)
    amount = db.Column(db.Float, default = 0.0, nullable = False)
    due = db.Column(db.Date, nullable= False)
    
    def __repr__(self):
        return '<Expense %r>' % self.name

class ExpenseView(ModelView):
    column_list = ["name", "type", "urgency", "paid", "amount","due"]
    column_editable_list = ["name", "type", "urgency", "paid","amount", "due"]
    column_labels={"name":"Name", "type":"Type", "urgency":"Urgency", "paid":"Paid?", "amount":"Amount","due":"Due Date"}
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
    
