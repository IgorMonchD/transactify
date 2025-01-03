from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, crud, schemas, auth
from .database import engine, SessionLocal
from .logger import log_action

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db, user)

@app.post("/login", response_model=schemas.Token)
def login(form_data: auth.OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = auth.create_access_token(data={"user_id": user.id, "username": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/change-password")
def change_password(
    new_password: str,
    token: str = Depends(auth.oauth2_scheme),
    db: Session = Depends(get_db)
):
    user = auth.get_current_user(db, token)
    crud.change_password(db, user.username, new_password)
    log_action(user, f"Changed password for user {user.username}")

    return {"msg": "Password changed successfully"}

@app.post("/verify-token")
def verify_token(token_request: schemas.TokenRequest, db: Session = Depends(get_db)):
    token = token_request.token
    user_data = auth.verify_token(token)
    user = crud.get_user(db, user_data["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Token is valid", "user_data": user_data}





