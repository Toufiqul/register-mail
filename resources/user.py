from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from db import db
from models import UserModel
from schemas import UserSchema
import bcrypt


from redis import Redis
from rq import Queue

q = Queue(connection=Redis())

from resources.sendMail import send_mail
blp = Blueprint("Users", "users", description="Operations on users")

@blp.route("/register")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        # print(user_data["username"])
        # print(user_data["first_name"])
        # print(user_data["second_name"])
        # print(user_data["password"])
        salt = bcrypt.gensalt()
        user = UserModel(
        username=user_data["username"],
        email=user_data["email"],
        password=bcrypt.hashpw(user_data["password"].encode('utf-8'), salt),
        first_name=user_data.get("first_name"),
        last_name=user_data.get("last_name")
    )
        email_receiver = user_data["email"]
        try:
            db.session.add(user)
            db.session.commit()

            # job = current_app.email_queue.enqueue(send_mail, email_receiver)

            # return {"message": f"Registration Successful! {job}"}, 200
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the user.")
        except Exception as e:
            print(e)

        return user
