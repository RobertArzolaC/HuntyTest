import logging

from fastapi import FastAPI

from app.api import ping, company, job_offer, user, skill
from app.db import init_db

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router)
    application.include_router(
        company.router, prefix="/companies", tags=["companies"],
    )
    application.include_router(
        job_offer.router, prefix="/job_offers", tags=["job_offers"]
    )
    application.include_router(
        user.router, prefix="/users", tags=["users"]
    )
    application.include_router(
        skill.router, prefix="/skills", tags=["skills"]
    )

    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
