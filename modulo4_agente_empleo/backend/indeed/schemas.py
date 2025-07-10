from pydantic import BaseModel
from typing import List, Optional

class Job(BaseModel):
    job_title: str
    company: str
    location: str
    salary: Optional[str]
    description: str
    job_url: str
    date_posted: str


class SearchRequest(BaseModel):
    query: str
    location: str
    radius: Optional[int] = 25  # en kilómetros
    limit: Optional[int] = 50
    start: Optional[int] = 0
    sort: Optional[str] = "date"  # date o relevance
    filter: Optional[int] = 0  # 0: todos, 1: últimos 24h, 2: últimos 3 días, 3: últimos 7 días


class SearchResponse(BaseModel):
    jobs: List[Job]
    total_jobs: int
    search_url: str
