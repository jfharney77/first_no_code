from fastapi import FastAPI
import uvicorn
from servers.m.g import server_utils

app = FastAPI()

@app.get("/c_s_a_r_m")
def c_s_a_r_m():
    return {"message": "c_s_a_r_m endpoint active"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6013)
