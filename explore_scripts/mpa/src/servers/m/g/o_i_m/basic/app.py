from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/o_i_m")
def o_i_m():
    return {"message": "o_i_m endpoint active"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6011)
