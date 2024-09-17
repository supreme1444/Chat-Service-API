from typing import Annotated

from pydantic import BaseModel, EmailStr
from annotated_types import MinLen, MaxLen


class CreateUser(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr
