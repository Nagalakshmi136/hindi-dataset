
from typing import Any


class Singleton(type):
    _instances={}
    def __call__(cls,*args: Any, **kwds: Any) -> Any:
        if cls not in cls._instances:
             cls._instances[cls]=super(Singleton,cls).__call__(*args,**kwds)
        return cls._instances[cls]
    
class VideoData():
    def __init__(self) -> None:
        self.id_store={}
    def store_id(self,video_ids):
        self.id_store.update(video_ids)
    def get_id(self):
        return self.id_store