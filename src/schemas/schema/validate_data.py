from pydantic import BaseModel, Field, EmailStr, ConfigDict


class User(BaseModel):
    name: str
    age: int
    email: str


class RegisterFild(BaseModel):
    name: str = Field(max_length=100)
    age: int = Field(ge=0, le=120)
    email: EmailStr
    password: str = Field(max_length=100)
    password_repeat: str = Field(max_length=100)

    model_config = ConfigDict(from_attributes=True)



class RegisterId(RegisterFild):
    id: int


class LoginSchema(BaseModel):
    name: str = Field(max_length=100)
    password: str = Field(max_length=100)

