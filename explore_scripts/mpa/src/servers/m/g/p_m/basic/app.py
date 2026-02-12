from fastapi import FastAPI
import uvicorn
from servers.m.g import server_utils

app = FastAPI()

@app.get("/p_m")
def p_m():
    return {"message": "p_m endpoint active"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6006)
