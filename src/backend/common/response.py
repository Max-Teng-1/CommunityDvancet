from typing import Union
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from fastapi import status, HTTPException

# success
def resp_200(*, data: any = None, message: any = "Success") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            'code': 200,
            'message': message,
            'data': data,
        })
    )

# token is expired
def resp_401(*, data: Union[list, dict, str] = None, message: str = "Request Fail") -> Response:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=jsonable_encoder({
            'code': 401,
            'data': data,
            'message': message
        })
    )

# user input error
def resp_400(*, data: Union[list, dict, str] = None, message: Union[list, dict, str] = "Request Fail") -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({
            'code': 400,
            'data': data,
            'message': message,
        })
    )

# user access error
def resp_403(*, data: Union[list, dict, str] = None, message: Union[list, dict, str] = "Request Fail") -> Response:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=jsonable_encoder({
            'code': 403,
            'data': data,
            'message': message,
        })
    )

