import pydantic


class UserInfo(pydantic.BaseModel):
    username: str
    email: str


class UserResult(pydantic.BaseModel):
    data: str
    timestamp: int


class UserPasswords(pydantic.BaseModel):
    old: str
    new: str


class UserAuthLog(pydantic.BaseModel):
    auth_at: int
