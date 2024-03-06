from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from db import db
from models import UserModel
from schemas import UserSchema
import bcrypt #for hashing the password
from sqlalchemy.sql import exists


from validate_email import validate_email #to validate the email


from redis import Redis
from rq import Queue,Retry

q = Queue(connection=Redis())

from resources.sendMail import gmail_send_message
blp = Blueprint("Users", "users", description="Operations on users")

@blp.route("/register")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))  # OK Indicates that the request has succeeded
    def get(self):
        try:
            return UserModel.query.all()
        except Exception as e:
            abort(500, message="failed to retriving the list of users", error=e)


    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)  #201 Created Indicates that the request has succeeded and a new resource has been created as a result.
    def post(self, user_data):
        salt = bcrypt.gensalt()
        user = UserModel(
        username=user_data["username"],
        email=user_data["email"],
        password=bcrypt.hashpw(user_data["password"].encode('utf-8'), salt), #salting and hashing the password
        first_name=user_data.get("first_name"),
        last_name=user_data.get("last_name")
    )
        if db.session.query(exists().where(UserModel.email==user_data["email"])):
            abort(409, message=f"{user_data['email']} is already registered. Please Login or register with a diffrent email")
    #409 CONFLICT: Whenever a resource conflict would be caused by fulfilling the request. Duplicate entries, such as trying to create two customers with the same information, and deleting root objects when cascade-delete is not supported are a couple of examples.
        isValid = validate_email(email_address=user_data["email"])
        if not isValid:
            abort(400, message="Invalid email address. Please enter a valid email address")
            # 400 bad request: The request could not be understood by the server due to incorrect syntax. The client SHOULD NOT repeat the request without modifications.

        email_receiver = user_data["email"]
        try:
            db.session.add(user)
            db.session.commit()

            job = current_app.email_queue.enqueue(gmail_send_message, email_receiver,retry=Retry(max=3, interval=[10, 60*60, 24*60*60]))

            return {"message": f"Registration Successful! {job}"}, 200
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the user.")


        return user
