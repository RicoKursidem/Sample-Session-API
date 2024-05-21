from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

class User_Handler:
    
    __users = {1: {'username': 'test', 'password': 'test'}}
    
    def __init__(self) -> None:
        pass
    
    def create_user(self, username: str, password: str):
        user = self.__get_user_by_name(username)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Username {username} already exists",
            )
        new_user_id = len(self.__users) + 1
        new_user = {
            "username": username,
            "password": password
        }
        self.__users[new_user_id] = new_user
        return {"message": "User registered successfully"}

    def authenticate_user(self, credentials: HTTPBasicCredentials = Depends(security)) -> int:
        user_id, user = self.__get_user_by_name(credentials.username)
        if user is None or user["password"] != credentials.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
        print(f"{user_id=}, {user=}")
        return user_id
    
    def get_user_info(self, user_id):
        return self.__users.get(user_id)
    
    def __get_user_by_name(self, username):
        for user_id in self.__users:
            if self.__users.get(user_id)["username"] == username:
                return user_id, self.__users.get(user_id)
        return None