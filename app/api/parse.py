from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.api.dependencies import get_parser
from app.core.security import OAUTH2_SCHEME
from app.core.security import decode_token
from app.models.parse import ParseRequest

router = APIRouter()


@router.post("/netlist")
async def parse(data: ParseRequest, token: str = Depends(OAUTH2_SCHEME)):
    if decode_token(token):
        result = get_parser().execute(data.text, data.obj_name)
        return {"result": result}
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Внутренняя ошибка"}
    )
