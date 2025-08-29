from fastapi import FastAPI


items = []


app = FastAPI()


@app.get("/")
def main_page():
    return {"message": "Hello"}

