from handlers.exceptions import Error


class ValidationError(Error):
    def __init__(self, message="There were errors in the supplied information.", **extras):
        self.status = 400
        self.code = "VALIDATION_ERROR"
        self.message = message
        self.extras = extras


class NDBEntityNotFoundError(Error):
    def __init__(self, model_name, **extras):
        self.status = 404
        self.code = "ENTITY_NOT_FOUND"
        self.message = "{} entity requested was not found in the datastore.".format(model_name)
        self.extras = extras
