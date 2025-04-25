import pydantic


class UserRegistrationData(pydantic.BaseModel):
    username: str
    password: str
    email: str


class UserRegistrationResponse(pydantic.BaseModel):
    id: int
