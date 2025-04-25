import pydantic


class UserInfo(pydantic.BaseModel):
    login: str
    name: str


class UserHistory(pydantic.BaseModel):
    data: str
    timestamp: int


class UserPasswords(pydantic.BaseModel):
    old: str
    new: str


class UserAuthLog(pydantic.BaseModel):
    auth_at: int
