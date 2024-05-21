from fastapi import Depends

from backend import session_handler, user_handler

SESSION_HANDLER = session_handler.Session_Handler()
USER_HANDLER = user_handler.User_Handler()

# User 

def signup(username: str, password: str):
    return USER_HANDLER.create_user(username, password)

def authenticate_user(user: dict = Depends(USER_HANDLER.authenticate_user)):
    return user

# Sessions

def create_session(user_id: int):
    return SESSION_HANDLER.create_session(user_id)

# Functions

def get_user_info(session_id: int):
    session = SESSION_HANDLER.get_session(session_id)
    user = USER_HANDLER.get_user_info(session["user_id"])
    return {'userinfo': user, 'sessioninfo': session}
