from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/msg")
def read_root():
    return JSONResponse(content={"message": "Hello from FastAPI on Vercel!"})


@app.get("/teste")
def read_roo2t():
    return JSONResponse(content={"a":"!!!!!"})