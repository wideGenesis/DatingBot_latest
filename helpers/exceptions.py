class ValidationError(ValueError):
    pass


class ObjectDoesNotExist(ValueError):
    pass


class BadRequest(ValueError):
    pass


class RequestAborted(ValueError):
    pass


class AuthError(ValueError):
    pass


class EmptyResultSet(ValueError):
    pass


class DropReply(KeyError):
    pass
