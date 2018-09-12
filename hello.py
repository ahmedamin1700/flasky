from flask import Flask, render_template
from flask_wtf import Form
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_script import Manager


app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)

class NameForm(Form):
    name = StringField("What's you name?", validators=[Required()])
    submit = SubmitField("Submit")


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/user/<name>")
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    manager.run()
