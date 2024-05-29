from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")


# OpenAI
OPENAI_API_KEY = config["AZURE_OPENAI"]["AZURE_OPENAI_API_KEY"]
AZURE_ENDPOINT = config["AZURE_OPENAI"]["AZURE_OPENAI_ENDPOINT"]

# Mongo
MONGO_CONNECTION_STRING = config["MONGO"]["MONGO_CONNECTION_STRING"]

# Auth
SECRET_KEY = config["AUTH"]["SECRET_KEY"]
ALGORITHM = config["AUTH"]["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = config["AUTH"]["ACCESS_TOKEN_EXPIRE_MINUTES"]
