from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")


# OpenAI
OPENAI_API_KEY = config["AZURE_OPENAI"]["AZURE_OPENAI_API_KEY"]
AZURE_ENDPOINT = config["AZURE_OPENAI"]["AZURE_OPENAI_ENDPOINT"]

# Mongo
MONGO_CONNECTION_STRING = config["MONGO"]["MONGO_CONNECTION_STRING"]