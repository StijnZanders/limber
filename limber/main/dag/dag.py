from typing import Optional
from datetime import timedelta
import inspect


class DAG:

    def __init__(self, dag_id:str, description:Optional[str], default_args:dict, schedule_interval:[str,timedelta]):

        self.dag_id = dag_id
        self.description=description
        self.default_args=default_args
        self.schedule_interval=schedule_interval
        _, filename, line, function, _, _ = inspect.stack()[1]
        self.filename = filename

