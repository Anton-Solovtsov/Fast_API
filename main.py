import asyncio
import logging
import time

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from backend_fastAPI.api.routers.router import api_router
from backend_fastAPI.core.config import get_settings
from backend_fastAPI.core.logging import conf_logging

# @asynccontextmanager
# async def lifespan(_: FastAPI):
#     Base.metadata.create_all(bind=engine)
#     print("БД создана")
#     yield

conf_logging()

settings = get_settings()
app = FastAPI()
app.include_router(router=api_router)

logger = logging.getLogger("app.middelware")

count_request = 0
count_lock = asyncio.Lock()


@app.middleware("http")
async def log_request(request: Request, call_next) -> Response:
    global count_request

    async with count_lock:
        count_request += 1
        cur_num = count_request

    start = time.perf_counter()

    try:
        response: Response = await call_next(request)
        response.headers["X-Request-Nummber"] = str(cur_num)
    except Exception:
        stop = (time.perf_counter() - start) * 1000
        logger.exception(
            "Request failed: %s %s completed_in=%.2f ms",
            request.method,
            request.url.path,
            stop,
        )
        raise

    stop = (time.perf_counter() - start) * 1000
    logger.info(
        "%s %s -> %s (%.2f ms)",
        request.method,
        request.url.path,
        response.status_code,
        stop,
    )

    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_methods=["*"],
)
