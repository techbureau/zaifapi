class ZaifApiError(Exception):
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return self._message


class ZaifApiNonceError(Exception):
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return self._message
