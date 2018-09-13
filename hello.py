from flask import (Flask, render_template, session, redirect, url_for, flash)
from flask_wtf import FlaskForm
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.config["SECRET_KEY"] = "hard to guess my name"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://shrnzflrxqeive:31e46c2221f786ec755fa703c5b27c2c6eeb209e8e2f8aa4465a8a25f174a931@ec2-184-72-247-70.compute-1.amazonaws.com:5432/da32rk10cpahb6"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ahmedamin1700@gmail.com'
app.config['MAIL_PASSWORD'] = 'Ahmed@6695659'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)
mail = Mail(app)

""" Helpers """
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))

""" Forms """
class NameForm(FlaskForm):
    name = StringField("What's you name?", validators=[Required()])
    submit = SubmitField("Submit")

""" Models """
class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return "<Role %r>" % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __repr__(self):
        return '<User %r>' % self.username

""" Routes """
@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session["known"] = False
        else:
            session["known"] = True
        session["name"] = form.name.data
        form.name.data = ''
        return redirect(url_for("index"))
    return render_template('index.html',
        form=form, name=session.get("name"),
        known=session.get("known", False))

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
