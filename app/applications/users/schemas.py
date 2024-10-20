from pydantic import BaseModel


class SchemaRegister(BaseModel):
    login: str
    username: str
    password_1: str
    password_2: str


class SchemaLogin(BaseModel):
    login: str
    password: str


class SchemaResponseUser(BaseModel):
    user_id: int
    username: str