class ZaifApiError(Exception):
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return self._message


class ZaifApiNonceError(ZaifApiError):
    pass


class ZaifApiValidationError(ZaifApiError):
    pass


class ZaifServerException(ZaifApiError):
    pass
