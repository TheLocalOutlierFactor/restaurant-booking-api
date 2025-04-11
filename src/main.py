import time

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.utils.logger import logger
from src.routers import tables, reservations


app = FastAPI(title="Restaurant Table Booking API")
app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(tables.router)
app.include_router(reservations.router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"➡️ {request.method} {request.url}")
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(f"✅ {request.method} {request.url} completed in {process_time:.2f}s with {response.status_code}")
    return response


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")


@app.get("/")
async def root():
    return {"message": "Hello World"}
