from pydantic import BaseModel


class SchemaUser(BaseModel):
    username: str

class SchemaMessage(BaseModel):
    username: str
    message: str

