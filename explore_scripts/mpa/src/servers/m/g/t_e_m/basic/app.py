from fastapi import FastAPI
import uvicorn
from servers.m.g import server_utils

app = FastAPI()

@app.get("/t_e_m")
def t_e_m():
    return {"message": "t_e_m endpoint active"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6012)
