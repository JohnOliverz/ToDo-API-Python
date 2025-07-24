from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def read_root():
    return {"msg": "Bem-vindo à API de Tarefas!"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000,
                log_level='info', reload=True)