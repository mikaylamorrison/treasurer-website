from flask import Flask, render_template

# app is the current module name ig??
app = Flask(__name__)


# @app.route, decorates a view function to register it with the given URL
# idk look at documentation idk what this does yet
@app.route('/')
def index():
    # Don't need to say the path file, render template knows to look for index.html
    # this is rendering the page.
    # render template prolly just renders the html file.
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
    