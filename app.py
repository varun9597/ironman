from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/signin")
def sign_in():
    return render_template('sign_in.html')

@app.route("/signup")
def sign_up():
    return render_template('sign_up.html')

@app.route("/home")
def home():
    return render_template('homepage.html')

if __name__ == "__main__":
    app.run()

