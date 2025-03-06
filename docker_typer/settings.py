from environs import env


APP_ENV = env("APP_ENV", default="local")

DEFAULT_ENV_FILE = ".env"