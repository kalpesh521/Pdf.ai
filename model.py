
from pydantic import BaseModel

class QueryRequest(BaseModel):
    content: list[str]
    query: str
