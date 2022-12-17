import logging

from app.api import company, job_offer, job_offer_skill, ping, skill, user, user_skill
from app.db import init_db
from fastapi import FastAPI

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router)
    application.include_router(
        company.router,
        prefix="/companies",
        tags=["companies"],
    )
    application.include_router(
        job_offer.router, prefix="/job_offers", tags=["job_offers"]
    )
    application.include_router(user.router, prefix="/users", tags=["users"])
    application.include_router(skill.router, prefix="/skills", tags=["skills"])
    application.include_router(
        user_skill.router, prefix="/user_skills", tags=["user_skills"]
    )
    application.include_router(
        job_offer_skill.router, prefix="/job_offer_skills", tags=["job_offer_skills"]
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
