import pydantic


class UserAuthorizationData(pydantic.BaseModel):
    login: str
    password: str


class UserRegistrationData(pydantic.BaseModel):
    login: str
    password: str
    name: str


class UserRegistrationResponse(pydantic.BaseModel):
    id: int
