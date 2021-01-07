import logging
import logging.config
from pushbullet import Pushbullet

class PushbulletHandler(logging.StreamHandler):
    def __init__(self,api_key,title):
        super().__init__()
        self.pb = Pushbullet(api_key)
        self.title = title

    def emit(self,record):
        msg = self.format(record)
        self.pb.push_note(self.title,msg)

class ConfDict(dict):
    def set_api_key(self,api_key):
        self["handlers"]["pushbullet_handler"]["api_key"] = api_key

LOGGER_CONFIG = ConfDict({
    "version" : 1,

    "formatters" : {
        "formatter" : {
            "format" : "%(levelname)s : %(message)s"
        }
    },

    "handlers" : {
        "stream_handler" : {
            "class" : "logging.StreamHandler",
            "level" : "DEBUG",
            "formatter" : "formatter"
        },
        "pushbullet_handler" : {
            "class" : "utils.logger.PushbulletHandler",
            "level" : "CRITICAL",
            "formatter" : "formatter",
            "api_key" : None,
            "title" : "BPB log"
        }
    },

    "loggers" : {
        "logger" : {
            "handlers" : ["stream_handler", "pushbullet_handler"]
        }
    }
})
