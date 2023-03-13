from flask import Flask
from api import api_v1
from router.mainoutlines import *
from router.suboutlines import *
from router.content.articles import *
from router.account.login import *
import config
from flask_apscheduler import APScheduler
from datetime import datetime
from router.feeds import parse_feeds_background
from model.database import DataBase

from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)
app.register_blueprint(api_v1)

class Config:
    """App configuration."""

    JOBS = [{"id": "job1", "func": parse_feeds_background, "trigger": "interval", "seconds": 60*60*2}]

    # SCHEDULER_JOBSTORES = {
    #     "default": SQLAlchemyJobStore(url="sqlite:///flask_context.db")
    # }

    SCHEDULER_API_ENABLED = True
 



app.config['SQLALCHEMY_DATABASE_URI'] = config.sqlalchemy_database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = config.jwt_secret_key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=5)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config.from_object(Config())
jwt = JWTManager(app)

db = DataBase.instance().db
db.app = app
db.init_app(app)

def init_models():
    import model.users
    import model.feeds

init_models()

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    for job in scheduler.get_jobs():
        job.modify(next_run_time=datetime.now())
    print("scheduler started")
    app.run(debug=True)