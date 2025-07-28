from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from api.tasks import router as tasks_router
from api.auth import router as auth_router
from api.users import router as users_router
from common.exceptions import (
    validation_exception_handler,
    integrity_error_handler,
    http_exception_handler,
    general_exception_handler
)

app = FastAPI(
    title="ToDo API",
    description="API para gerenciamento de tarefas com autenticação JWT",
    version="1.0.0",
    contact={
        "name": "ToDo API Support",
        "email": "support@todoapi.com",
    },
    license_info={
        "name": "MIT",
    },
)

# Exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Routers
app.include_router(auth_router, tags=["Autenticação"])
app.include_router(users_router, tags=["Usuários"])
app.include_router(tasks_router, tags=["Tarefas"])

@app.get("/")
def read_root():
    return {"msg": "Bem-vindo à API de Tarefas!"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000,
                log_level='info', reload=True)