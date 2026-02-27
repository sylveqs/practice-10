from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional, List

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Auth schemas
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None

# Post schemas
class PostBase(BaseModel):
    content: str

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    username: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Topic schemas
class TopicBase(BaseModel):
    title: str
    content: str

class TopicCreate(TopicBase):
    pass

class TopicListResponse(BaseModel):
    id: int
    title: str
    username: str
    message_count: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class TopicDetailResponse(TopicBase):
    id: int
    username: str
    created_at: datetime
    posts: List[PostResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

# Error response
class ErrorResponse(BaseModel):
    detail: str