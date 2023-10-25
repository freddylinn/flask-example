import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, inspect
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dynamic.db"
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Butterfly(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    image = db.Column(db.Text)

@app.route('/', methods=["GET", "POST"])
def hello_world():  # put application's code here
    if request.method == "POST":
        return render_template("template.html", var=[1,2,3], form=int(request.form["num"]))
    else:
        return render_template("template.html", var=[1,2,3], form=None)

@app.route('/butterflies', methods=["GET"])
def db_testing():
    with db.engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM butterfly;"))
        butterflies = [row._mapping for row in result]
    return render_template("butterflies.html", butter=butterflies)

@app.route('/admin', methods=["GET","POST"])
def admin_page():
    if request.method == "POST":
        file = request.files['file']
        with db.engine.connect() as conn:
            to_execute = f"INSERT INTO butterfly (id,name,image) VALUES ({request.form['id']},\"{request.form['name']}\", \"{file.filename}\");"
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
            conn.execute(text(to_execute))
            conn.commit()
    return render_template("admin.html")
        
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()