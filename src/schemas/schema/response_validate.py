from pydantic import BaseModel, ConfigDict


class UserOut(BaseModel):
    name: str
    age: int
    email: str

    model_config = ConfigDict(from_attributes=True)

class UserOutId(UserOut):
    id: int


