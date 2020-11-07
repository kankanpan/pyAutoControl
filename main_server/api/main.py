import sys
import uvicorn
from typing import List
from fastapi import Depends, FastAPI, HTTPException, UploadFile, File, Response, BackgroundTasks, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from api.database import SessionLocal, engine

import api.crud as crud
import api.models as models
import api.schemas as schemas
import api.request as request

class Server():
    def __init__(self, status={'value': 0}, ep=None):
        models.Base.metadata.create_all(bind=engine)
        self.app = FastAPI()
        self.ep = ep
        self.status = status

        origins = [
            "http://localhost:8200",
            "http://localhost"
        ]
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def start(self, **kwargs):
        self.setApi()
        uvicorn.run(self.app, host="0.0.0.0", port=kwargs['port'])

    async def end(self):
        status = await self.ep.recv()
        print(status)
        if status != 'quit':
            self.end()
        else:
            sys.exit(0)

    def setApi(self):
        @self.app.on_event("startup")
        def startup_event():
            background_tasks = BackgroundTasks()
            background_tasks.add_task(self.end)
            return True

        @self.app.on_event("shutdown")
        def shutdown_event():
            print("*** shutdown server ***")

        @self.app.get("/test/")
        async def test_action():
            return {'value': self.status.value}

        @self.app.get("/ss/")
        async def ss_action(keyword: str = ''):
            return crud.get_ss_action(keyword)

        @self.app.get("/sub/ss/")
        async def call_ss_action(keyword: str = ''):
            result = request.callGet("/ss/", keyword)
            if result:
                return result
            else:
                return False

        @self.app.get("/window/")
        async def get_window(time: float = 1):
            return crud.get_window_action(time)

        @self.app.get("/sub/window/")
        async def call_get_window(time: str = '1'):
            result = request.callGet("/window/", time)
            if result:
                return result
            else:
                return False

        @self.app.post("/item/")
        async def create_item(item: schemas.ItemCreate):
            return crud.set_item(item)

        @self.app.get("/item/")
        async def get_item():
            return crud.get_item()

        """

        @self.app.websocket("/ws_sub")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            while True:
                data = await websocket.receive_text()
                print('connecting', data)
                time.sleep(5)
                await websocket.send_text("ok!")

        @self.app.get("/ws/")
        async def start_ws(background_tasks: BackgroundTasks):
            background_tasks.add_task(crud.start_ws)
            return True

        @self.app.post("/convert")
        async def convert(file: UploadFile = File(...)):
            img_enc = crud.create_convert(file)
            if img_enc:
                return Response(content=img_enc.tostring(), media_type='image/png')
            else:
                return HTTPException(status_code=500, detail='Failed to convert an image.')

        @self.app.post("/users/", response_model=schemas.User)
        def create_user(user: schemas.UserCreate, db: Session = Depends(self._get_db)):
            db_user = crud.get_user_by_email(db, email=user.email, name=user.name)
            if db_user:
                raise HTTPException(status_code=400, detail="Email already registered")
            return crud.create_user(db=db, user=user)


        @self.app.get("/users/", response_model=List[schemas.User])
        def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(self._get_db)):
            users = crud.get_users(db, skip=skip, limit=limit)
            return users


        @self.app.get("/users/{user_id}", response_model=schemas.User)
        def read_user(user_id: int, db: Session = Depends(self._get_db)):
            db_user = crud.get_user(db, user_id=user_id)
            if db_user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return db_user


        @self.app.post("/users/{user_id}/items/", response_model=schemas.Item)
        def create_item_for_user(
            user_id: int, item: schemas.ItemCreate, db: Session = Depends(self._get_db)
        ):
            return crud.create_user_item(db=db, item=item, user_id=user_id)


        @self.app.get("/items/", response_model=List[schemas.Item])
        def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(self._get_db)):
            items = crud.get_items(db, skip=skip, limit=limit)
            return items

        @self.app.get("/tokens/")
        async def read_token(token: str = Depends(self.oauth2_scheme)):
            return {"token": token}

        @self.app.get("/users/me")
        async def read_users_me(current_user: models.User = Depends(crud.get_current_user)):
            return current_user
        """

    def _get_db(self):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

if __name__ == "__main__":
    app = Server()
    app.start(port=8123)
