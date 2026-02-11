from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/pr_m")
def pr_m():
    return {"message": "pr_m endpoint active"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6007)
