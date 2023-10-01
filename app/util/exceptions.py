""" Custom Exceptions """

from typing import Optional


class SPAError(Exception):
    def __init__(self, message: Optional[str] = None) -> None:
        if not message:
            message = (
                "Error response from OMDB API"
            )
        super().__init__(message)


class UnknownGenre(SPAError):
    def __init__(self, g: str) -> None:
        super().__init__(f'Uknown Genre: {g}')
