from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from .. import modules, utils, oauth2, schemas

router = APIRouter(
    tags=["Authentication"]
)

"""
OAuth2PasswordRequestForm : takes username and password dynamically
- it doesn't care if is email or username, just it will take username and store it in username field
- it return : {
                "username": "username",
                "password": "password"
            }
- the username and password for the login, they should not be passed in the body of the request,
  they should be passed in the body of the request in the form of the request.
"""


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(modules.User).filter(modules.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
    
    
