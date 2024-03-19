from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# app is the current module name ig??
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customerInfo.db'
db = SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    displayName = db.Column(db.String, default = username)
    streak = db.Column(db.Integer, default = 0)
    sessionsUnpaid = db.Column(db.Integer, default = 0)
    
    def __repr__(self) -> str:
        return '<User %r' % self.id
    

# @app.route, decorates a view function to register it with the given URL
# idk look at documentation idk what this does yet
@app.route('/')
def index():
    # Don't need to say the path file, render template knows to look for index.html
    # this is rendering the page.
    # render template prolly just renders the html file.
    return render_template('index.html')



# RUNNING APP
if __name__ == "__main__":
    app.run(debug=True)
    