from pydantic import BaseModel
from typing import Optional

# Token model

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]