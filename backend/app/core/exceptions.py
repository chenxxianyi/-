"""Custom exceptions for the application."""


class AppException(Exception):
    """Base application exception."""

    def __init__(self, code: int = 400, message: str = "Bad Request"):
        self.code = code
        self.message = message
        super().__init__(self.message)


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(code=401, message=message)


class ForbiddenException(AppException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(code=403, message=message)


class NotFoundException(AppException):
    def __init__(self, message: str = "Not Found"):
        super().__init__(code=404, message=message)


class ConflictException(AppException):
    def __init__(self, message: str = "Conflict"):
        super().__init__(code=409, message=message)


class ValidationException(AppException):
    def __init__(self, message: str = "Validation Error"):
        super().__init__(code=422, message=message)
