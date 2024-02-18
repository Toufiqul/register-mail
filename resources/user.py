from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import UserModel
from schemas import UserSchema

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
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the user.")

        return user
