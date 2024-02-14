from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import db
from models import UserModel

# def create_app():
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///data.db"
db.init_app(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

with app.app_context():
    db.create_all()


@app.post('/register')
def reg():
    data = request.get_json()
    # return f"{data['id']}, {data['email']},{data['username']}"
    # nUser = {
    #     "username": data["username"],
    #     "mail": data["mail"],
    #     "id": data["id"] 
    # }
    try:
        newUser = UserModel(id=data['id'], email=data['email'],username=data['username'],)

        db.session.add(newUser)
        db.session.commit()
        return jsonify(newUser)
    except Exception as e:
        print(e)
        return jsonify(e)

@app.get('/users')
def get_users():
    return "not implemented "
    # return UserModel.query.all()
    # return app