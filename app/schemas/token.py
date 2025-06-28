from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    email: str | None = None
    id: str | None = Field(alias="sub")

    model_config = ConfigDict(populate_by_name=True)