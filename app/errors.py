#!/usr/bin/env python3


class ApplicationError(Exception):
    def __init__(self, message, app=None):
        super().__init__(message)

        if app:
            app.logger.error(message)


class ApiConnectionError(ApplicationError):
    def __init__(self, message, app=None):
        super().__init__(app, message)