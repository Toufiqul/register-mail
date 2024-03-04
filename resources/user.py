from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from db import db
from models import UserModel
from schemas import UserSchema

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
        user = UserModel(**user_data)
        email_receiver = user_data["email"]
        try:
            db.session.add(user)
            db.session.commit()
            send_mail(email_receiver)
            job = current_app.email_queue.enqueue(send_mail, email_receiver)
            # print(job.result())
            return {"message": f"Registration Successful! {job}"}, 200
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the user.")
        except Exception as e:
            print(e)

        return user
