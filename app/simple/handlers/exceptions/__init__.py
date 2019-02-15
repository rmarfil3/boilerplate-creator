class Error(Exception):
    status = 500
    code = "ERROR"

    def __str__(self):
        return str(self.message)


class GenericError(Error):
    def __init__(self, code=Error.code, message="Something occurred unexpectedly. Please try again."):
        self.code = code or Error.code
        self.message = message


class UnknownError(Error):
    def __init__(self, message="An unknown error occurred."):
        self.code = "UNKNOWN_ERROR"
        self.message = message


class SendGridError(Error):
    def __init__(self, message="SendGrid failed to send email.", response_object=None):
        self.code = "SENDGRID_ERROR"
        self.message = message
        self.response_object = response_object
