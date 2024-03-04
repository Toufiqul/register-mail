from flask import Flask, request, jsonify
from flask_smorest import Api
import redis
from rq import Queue
from db import db
from resources.user import blp as UserBlueprint

def create_app(db_url=None):
    app = Flask(__name__)

    # redis_url = os.getenv("REDIS_URL", "redis://red-cmqfc0a1hbls73fjcmng:6379")
    # redis_url = "rediss://red-cmqfc0a1hbls73fjcmng:DkI1O3ZoeWetIcAmJPE7FNZfInyyGydU@oregon-redis.render.com:6379"
    redis_url = "rediss://red-cnijnk0l6cac7398rl1g:OySRwc8iMtMerm6gACQasLf2IeML9Pc3@oregon-redis.render.com:6379"
    redis_connection = redis.from_url(redis_url)
    app.email_queue = Queue("emails", connection=redis_connection)
    
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["SQLALCHEMY_DATABASE_URI"]=db_url or "sqlite:///data.db"
    db.init_app(app)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True



    # db.init_app(app)
    api = Api(app)

    with app.app_context():
        db.create_all()
    api.register_blueprint(UserBlueprint)

    return app



