from http import HTTPStatus

from fastapi import FastAPI
from sqladmin import Admin

from fast_zero.admin import UserAdmin
from fast_zero.admin_auth import AdminAuth
from fast_zero.database import engine
from fast_zero.routers import auth, users
from fast_zero.schemas import Message
from fast_zero.settings import Settings

app = FastAPI()

# Configuração do SQLAdmin com autenticação
authentication_backend = AdminAuth(secret_key=Settings().SECRET_KEY)
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)

app.include_router(users.router)
app.include_router(auth.router)


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Olá Mundo!"}
