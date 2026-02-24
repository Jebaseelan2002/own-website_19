from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ---------------- DATABASE ----------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ------------ TABLE MODEL -----------------
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    message = db.Column(db.Text)


# Create database
with app.app_context():
    db.create_all()


# ---------------- ROUTES ------------------
@app.route("/")
def page():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]

        data = Contact(
            name=name,
            email=email,
            phone=phone,
            message=message
        )

        db.session.add(data)
        db.session.commit()

        return redirect("/")

    return render_template("contact.html")


# View saved data
@app.route("/messages")
def messages():
    all_data = Contact.query.all()
    return render_template("messages.html", messages=all_data)


if __name__ == "__main__":
    app.run(debug=True)