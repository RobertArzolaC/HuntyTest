from typing import List, Union

from app.models.jobs import JobOffer, JobOfferSchema
from app.schema.job_offer import JobOfferPayloadSchema


async def add_job_offer(payload: JobOfferPayloadSchema) -> JobOfferSchema:
    job_offer = JobOffer(
        name=payload.name,
        currency=payload.currency,
        salary=payload.salary,
        url=payload.url,
        company_id=payload.company_id,
    )
    await job_offer.save()
    return job_offer


async def get_job_offer(id: str) -> Union[dict, None]:
    return await JobOffer.filter(id=id).first().values() or None


async def get_job_offers() -> List:
    return await JobOffer.all().values()


async def remove_job_offer(id: str) -> int:
    return await JobOffer.filter(id=id).first().delete()


async def edit_job_offer(id: str, payload: JobOfferPayloadSchema) -> Union[dict, None]:
    job_offer = await JobOffer.filter(id=id).update(
        name=payload.name,
        currency=payload.currency,
        salary=payload.salary,
        url=payload.url,
        company_id=payload.company_id,
    )
    if job_offer:
        updated_job_offer = await JobOffer.filter(id=id).first().values()
        return updated_job_offer
    return None


async def get_job_offers_by_ids(job_offer_id_list) -> List:
    return await JobOffer.filter(id__in=job_offer_id_list).values()
