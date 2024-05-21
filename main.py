from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import random
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi import Body
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

from backend import backend

version = "0.1"
description = """
This API provides a Sample for Session Handling and user Authentification.
"""

router = APIRouter(prefix="/api/v0")
app = FastAPI(
    title="Sample API",
    description=description,
    version=version,
    docs_url=None,
    redoc_url=None,
)

#################################################
###
###     Docs
###
#################################################
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


#################################################
###
###     Default
###
#################################################

@app.get("/version")
async def get_data():
    return {"status": 200, "version": version}

#################################################
###
###     Session handling and User Auth
###
#################################################

@router.post("/signup")
def sign_up(username: str = Body(...), password: str = Body(...)):
    return backend.signup(username, password)

@router.post("/login")
def login(user_id: dict = Depends(backend.authenticate_user)):
    session_id = backend.create_session(user_id)
    return {"message": "Logged in successfully", "session_id": session_id}

@router.get("/getusers/me")
def read_current_user(user = Depends(backend.get_user_info)):
    return user

###     Router
app.include_router(router)

if __name__ == "__main__":
    # Don't start normally!
    # Use 'uvicorn main:app --host 127.0.0.1 --port 5000'
    pass