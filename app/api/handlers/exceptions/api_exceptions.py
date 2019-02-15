from handlers.exceptions import Error


class UnauthorizedAccess(Error):
    def __init__(self, message="No valid authentication details were provided. Access is denied."):
        self.status = 401
        self.code = "UNAUTHORIZED_ACCESS"
        self.message = message


class ForbiddenAccess(Error):
    def __init__(self, message="Account is blocked from accessing this resource. Please contact the administrator."):
        self.status = 403
        self.code = "FORBIDDEN_ACCESS"
        self.message = message


class ValidationError(Error):
    def __init__(self, message="There were errors in the supplied information."):
        self.status = 400
        self.code = "VALIDATION_ERROR"
        self.message = message
