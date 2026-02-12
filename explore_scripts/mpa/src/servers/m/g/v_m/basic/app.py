from fastapi import FastAPI
import uvicorn
from servers.m.g import server_utils

app = FastAPI()

@app.get("/v_m")
def v_m():
    return {"message": "v_m endpoint active"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6014)
