from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/w_mj")
def w_mj():
    return {"message": "w_mj endpoint active"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6008)
