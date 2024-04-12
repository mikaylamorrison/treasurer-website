from app import db
from flask_login import UserMixin, login_required
from flask_admin.contrib.sqla import ModelView
from flask_admin import expose, AdminIndexView
from sqlalchemy import desc

# Define User model
class User(UserMixin, db.Model):
    # Specify the table name
    __tablename__ = "user"
    # Define the columns for the User table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False, unique=True)
    displayname = db.Column(db.String, nullable=False)
    streak = db.Column(db.Integer, default = 0, nullable = False)
    sessionsunpaid = db.Column(db.Integer, default = 0, nullable = False)
    roles = db.relationship("Role", secondary="user_roles", backref='users')
    # Define the string representation of the User model
    def __repr__(self):
        return '<User %r>' % self.username

# making a table for roles

class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique = True)
    
    def __repr__(self):
        return self.name

user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)
# Define UserView for Flask-Admin
class UserView(ModelView):
    # Specify the columns to display in the list view
    column_list = ["displayname", "username", "streak", "sessionsunpaid", "roles"]
    # Specify the columns that can be edited directly in the list view
    column_editable_list=["streak", "sessionsunpaid"]
    # Specify the labels for the columns
    column_labels={"displayname": "Name", "username": "Username", "streak":"Streak", "sessionsunpaid":"Sessions Unpaid", "roles":"Role"}

class HallExpenses(db.Model):
    __tablename__ = "Hall Expenses"
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), nullable = False)
    name = db.Column(db.String(100), unique=True, nullable = False)
    urgency = db.Column(db.Integer, default = 0, nullable = False)
    paid = db.Column(db.Boolean, default = False, nullable = False)
    amount = db.Column(db.Float, default = 0.0, nullable = False)
    due = db.Column(db.Date, nullable= False)
    
    def __repr__(self):
        return '<Hall %r>' % self.name

class HallView(ModelView):
    column_list = ["name", "type", "urgency", "paid", "due","amount"]
    column_editable_list = ["name", "type", "urgency", "paid", "due","amount"]
    column_labels={"name":"Name", "type":"Type", "urgency":"Urgency", "paid":"Paid?", "due":"Due Date","amount":"Amount"}
    form_choices = {
    'type': [
        ('Rent', 'Rent'),
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


class CoachExpenses(db.Model):
    __tablename__ = "Coach Expenses"
         
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), nullable = False)
    name = db.Column(db.String(100), unique=True, nullable = False)
    urgency = db.Column(db.Integer, default = 0, nullable = False)
    paid = db.Column(db.Boolean, default = False, nullable = False)
    amount = db.Column(db.Float, default = 0.0, nullable = False)
    due = db.Column(db.Date, nullable= False)
    
    def __repr__(self):
        return '<Coach %r>' % self.name

class CoachView(ModelView):
    column_list = ["name", "type", "urgency", "paid", "due","amount"]
    column_editable_list = ["name", "type", "urgency", "paid", "due","amount"]
    column_labels={"name":"Name", "type":"Type", "urgency":"Urgency", "paid":"Paid?", "due":"Due Date","amount":"Amount"}
    form_choices = {
    'type': [
        ('Payroll', 'Payroll'),
        ('Equipment', 'Equipment'),
    ],
    'urgency':[
        (0,'0'),
        (1,'1'),
        (2,'2'),
        (3,'3')
        ]
    }
    
class Announcement(db.Model):
    __tablename__ = "announcements"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False)
    title = db.Column(db.String(80), nullable = False)
    body = db.Column(db.String(200), nullable = False)
    date = db.Column(db.Date, nullable = False)
    def __repr__(self):
        return '<Announcement %r>' % self.name


class AnnouncementView(ModelView):
    column_list = ["name", "title", "body", "date"]
    column_editable_list = ["title", "body"]

class Sessions(db.Model):
    __tablename__ = "sessions"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable = False)
    starttime = db.Column(db.Time, nullable = False)
    endtime = db.Column(db.Time, nullable = False)
    attendees = db.relationship("User", secondary="session_attendees", backref='sessions')

    
    def __repr__(self):
        return '<Session %r>' % self.name

session_attendees = db.Table('session_attendees',
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class SessionsView(ModelView):
    column_list = ["id", "date", "attendees"]

class HomeView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        users = User.query.order_by("sessionsunpaid")
        expensesHall = HallExpenses.query.order_by(HallExpenses.paid, desc("urgency"))
        expensesCoach = CoachExpenses.query.order_by(CoachExpenses.paid, desc("urgency"))
        return self.render('admin/index.html', users=users, expensesHall = expensesHall, expensesCoach = expensesCoach)