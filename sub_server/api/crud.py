from sqlalchemy.orm import Session
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from fastapi import Depends, FastAPI, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import StreamingResponse

import api.models as models
import api.schemas as schemas
import actions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def test_action():
    result = actions.getWin()
    return result

def get_ss_action(keyword):
    im = actions.ss_action(keyword)
    return {"img": im}

def get_window_action(time):
    name = actions.window_action(time)
    return {"name": name}

def set_item(item):
    try:
        result = actions.setYaml('item', {item['name']: item})
        return { 'status': result, 'item': item }
    except Exception as e:
        print(e)
        return { 'status': False }

def get_item():
    item = actions.getYaml('item')
    return { 'items': item }



def create_convert(file):
    filepath = save_upload_file_tmp(file)
    try:
        img = cv2.imread(str(filepath))
        _, img_enc = cv2.imencode('.png', img)
        return img_enc
    except Exception as e:
        raise False
    finally:
        filepath.unlink()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, name=user.name, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def fake_decode_token(token):
    return models.User(
        name=token + "fakedecoded", email="john@example.com"
    )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user

def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp_path
