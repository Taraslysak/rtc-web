# flake8: noqa F402

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import auth_router, ws_router
from app.utils.custom_generate_unique_id import custom_generate_unique_id


app = FastAPI(
    generate_unique_id_function=custom_generate_unique_id,
    root_path="/api",
    # openapi_prefix="/api",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(ws_router)


@app.get("/", tags=["main"])
def root():
    SAMPLE_ENV_VAR = settings.SAMPLE_ENV_VAR
    return {"ENV": SAMPLE_ENV_VAR}
