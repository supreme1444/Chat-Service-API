import asyncio
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
import models, schemas, auth
from jose import JWTError, jwt

from telegram_bot import notify_new_message, start_bot

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
@app.on_event("startup")
async def startup():
    asyncio.create_task(start_bot())
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html") as f:
        return f.read()
@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    try:
        auth.create_user(db, user)
        return {"detail": "User  created successfully"}
    except HTTPException as e:
        raise e

@app.post("/token")
def login(form_data: auth.OAuth2PasswordRequestForm = Depends(), db: Session = Depends(auth.get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"token_type": "bearer","access_token": access_token }

@app.post("/messages")
async def create_message(message: schemas.MessageCreate, db: Session = Depends(auth.get_db), token: str = Depends(auth.oauth2_scheme)):
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")

        sender = db.query(models.User).filter(models.User.username == username).first()
        if not sender:
            raise HTTPException(status_code=404, detail="Sender not found")

        recipient = db.query(models.User).filter(models.User.username == message.recipient_username).first()
        if not recipient:
            raise HTTPException(status_code=404, detail="Recipient not found")

        new_message = models.MessageUser (
            sender_id=sender.id,
            recipient_id=recipient.id,
            message=message.content )
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        await notify_new_message(f'Новое сообщение от {username}')
        return {"detail": "Message created", "message_id": new_message.id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/messages/history/{recipient_username}", response_model=List[schemas.MessageSch])
async def get_message_history(recipient_username: str, token: str = Depends(auth.oauth2_scheme), db: Session = Depends(auth.get_db)):
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")

        sender = db.query(models.User).filter(models.User.username == username).first()
        if not sender:
            raise HTTPException(status_code=404, detail="Sender not found")

        recipient = db.query(models.User).filter(models.User.username == recipient_username).first()
        if not recipient:
            raise HTTPException(status_code=404, detail="Recipient not found")

        messages = db.query(models.MessageUser).filter(
            or_(
                (models.MessageUser.sender_id == sender.id) & (models.MessageUser.recipient_id == recipient.id),
                (models.MessageUser.sender_id == recipient.id) & (models.MessageUser.recipient_id == sender.id)
            )
        ).order_by(models.MessageUser.datetime).all()
        return [schemas.MessageSch(
           sender_id=message.sender_id,
            recipient_id=message.recipient_id,
            message=message.message,
            timestamp=message.datetime
        ) for message in messages]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/messages/history/{refresh}")
async def get_refresh(recipient_username: str,token: str = Depends(auth.oauth2_scheme), db: Session = Depends(auth.get_db)):
        sender = db.query(models.User).filter(models.User.token == token).first()
        recipient = db.query(models.User).filter(models.User.username == recipient_username).first()
        messages = db.query(models.MessageUser).filter(
            or_(
                (models.MessageUser.sender_id == sender.id) & (models.MessageUser.recipient_id == recipient.id),
                (models.MessageUser.sender_id == recipient.id) & (models.MessageUser.recipient_id == sender.id)
            )
        ).order_by(models.MessageUser.datetime).all()

        return [schemas.MessageSch(
            sender_id=message.sender_id,
            recipient_id=message.recipient_id,
            message=message.message,
            timestamp=message.datetime
        ) for message in messages]

def root():
    return {"message": "Welcome to the chat service!"}


