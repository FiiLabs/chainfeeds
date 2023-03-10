import dotenv
from pathlib import Path

# read environment variables from .env file
config_dir = Path(__file__).parent.resolve() / "config"
config_env = dotenv.dotenv_values(dotenv_path=config_dir / "conf.env")

openai_api_key = config_env["OPENAI_API_KEY"]
question_limit_per_user = int(config_env["QUESTION_LIMIT_PER_USER"])
sqlalchemy_database_uri = config_env["SQLALCHEMY_DATABASE_URI"]
jwt_secret_key = config_env["JWT_SECRET_KEY"]