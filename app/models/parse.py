import pydantic


class ParseRequest(pydantic.BaseModel):
    text: str
    obj_name: str
