import requests
from typing import Optional, List
from backend.indeed.config import indeed_config
from backend.indeed.schemas import SearchRequest, SearchResponse, Job
from backend.logger.logger import logger


class IndeedService:
    @staticmethod
    async def search_jobs(request: SearchRequest) -> SearchResponse:
        try:
            params = {
                "q": request.query,
                "l": request.location,
                "radius": request.radius,
                "limit": request.limit,
                "start": request.start,
                "sort": request.sort,
                "filter": request.filter,
                "userip": "1.2.3.4",
                "useragent": "Mozilla/5.0",
            }

            headers = {"Authorization": f"Bearer {indeed_config.INDEED_API_KEY}"}

            response = requests.get(
                f"{indeed_config.INDEED_BASE_URL}/jobs", params=params, headers=headers
            )

            response.raise_for_status()
            data = response.json()

            jobs = [
                Job(
                    job_title=job.get("title", ""),
                    company=job.get("company", ""),
                    location=job.get("location", ""),
                    salary=job.get("salary"),
                    description=job.get("snippet", ""),
                    job_url=job.get("url", ""),
                    date_posted=job.get("date", ""),
                )
                for job in data.get("jobs", [])
            ]

            return SearchResponse(
                jobs=jobs,
                total_jobs=data.get("total", 0),
                search_url=data.get("url", ""),
            )

        except requests.exceptions.RequestException as e:
            logger.warning(f"Error en petición a Indeed: {str(e)}")
            raise Exception(f"Error al buscar empleos: {str(e)}")
