
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import random



class Session_Handler:
    sessions = {280544: {'user_id': 1, 'created': datetime.now()}} # - timedelta(minutes=11) 
    
    def __init__(self) -> None:
        pass

    def get_session(self, session_id: int) -> dict:
        session = self.sessions.get(session_id)
        if session:
            return self.validate_session(session_id, session)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session expired. Please log in again.",
                headers={"WWW-Authenticate": "Basic"},
        )
        
    def create_session(self, user_id: int) -> int:
        session_id = len(self.sessions) + random.randint(0, 1000000)
        self.sessions[session_id] = {'user_id': user_id, 'created': datetime.now()}
        return session_id
    
    def validate_session(self, session_id, session):
        print(f"validate_session(self, {session_id=}, {session=})")
        diff = datetime.now() - session['created']
        if diff > timedelta(seconds=600):
            #TODO: delete Sesson
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session expired. Please log in again.",
                headers={"WWW-Authenticate": "Basic"},
                )
        return session

