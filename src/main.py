from fastapi import FastAPI

app = FastAPI(title="Restaurant Table Booking API")


@app.get("/")
async def root():
    return {"message": "Hello World"}