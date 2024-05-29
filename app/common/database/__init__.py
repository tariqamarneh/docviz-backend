from app.common.database.mongo import get_connection

user_collection = get_connection()["docViz"]["users"]
password_collection = get_connection()["docViz"]["passwords"]
