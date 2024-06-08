import logging
import datetime

from app.common.database.mongo import get_connection
from app.common.schemas.logging_schema import LoggingSchema


class MongoHandler(logging.Handler):

    def __init__(self, connection=None, database="docViz", collection="logs"):
        super().__init__()
        self.connection = connection
        self.database = self.connection[database]
        self.collection = self.database[collection]
        self.setLevel(logging.DEBUG)

    def emit(self, record):
        self.collection.insert_one(
            LoggingSchema(
                when=datetime.datetime.now(),
                filename=record.filename,
                funcName=record.funcName,
                levelname=record.levelname,
                message=str(record.msg),
            ).model_dump()
        )


class MongoRouteHandler(logging.Handler):

    def __init__(self, connection=None, database="docViz", collection="route_logs"):
        super().__init__()
        self.connection = connection
        self.database = self.connection[database]
        self.collection = self.database[collection]
        self.setLevel(logging.DEBUG)

    def emit(self, record):
        self.collection.insert_one(record.msg)


connection = get_connection()

mongo_logger = logging.getLogger("docViz")
mongo_logger.setLevel(logging.DEBUG)
mongo_logger.addHandler(MongoHandler(database="docViz", connection=connection))

mongo_route_logger = logging.getLogger("docViz-route")
mongo_route_logger.setLevel(logging.DEBUG)
mongo_route_logger.addHandler(
    MongoRouteHandler(database="docViz", connection=connection, collection="route_logs")
)
