class ImplementaionError(Exception):
    def __init__(self, message: str = ""):
        msg = "Implementation issue at the given point... "+ message
        super().__init__(msg)


class DuplicateMetric(Exception):
    def __init__(self, message: str = ""):
        msg = "Trying to set same metric function more than once (Duplicate metrices) " + message
        super().__init__(msg)


class DuplicateProberError(Exception):
    def __init__(self, message: str = ""):
        msg = "Multiple probers cannot be defined with the same name " + message
        super().__init__(msg)


class JobError(Exception):
    def __init__(self, message: str = ""):
        msg = "Unable to start the JOB ." + message
        super().__init__(msg)


class JobNotFoundError(Exception):
    def __init__(self, message: str = ""):
        msg = "No build job found \nEnsure the project should have a successful job stage named build." + message
        super().__init__(msg)


class RetryTimedOut(Exception):
    def __init__(self,message: str = ""):
        msg = "Timed out .. " + message
        super().__init__(msg)


class InvalidLoggingLevel(Exception):
    def __init__(self,message:str = ""):
        msg = "The log level provided is not valid :--" + message
        super().__init__(msg)

