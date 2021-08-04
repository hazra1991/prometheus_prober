class ImplementaionError(Exception):
    def __init__(self,message: str = ""):
        msg = "Implementation issue at the given point... "+ message
        super().__init__(self,msg)


class DuplicateMetric(Exception):
    def __init__(self,message:str = ""):
        msg = "Trying to set same metric function more than once (Duplicate metrices) " + message
        super().__init__(msg)
