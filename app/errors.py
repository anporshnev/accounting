from typing import Annotated, Any
from annotated_doc import Doc
from fastapi import HTTPException

class AddingException(HTTPException):
    def __init__(self, detail) -> None:
        super().__init__(500, f"При сохранении возникла ошибка: {detail}")
        
class UpdateException(HTTPException):
    def __init__(self, detail) -> None:
        super().__init__(500, f"При обновлении возникла ошибка: {detail}")