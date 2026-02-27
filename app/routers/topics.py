from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import schemas, models
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/topics", tags=["Topics"])

@router.get("/", response_model=List[schemas.TopicListResponse])
def get_topics(db: Session = Depends(get_db)):
    topics = db.query(models.Topic).order_by(models.Topic.created_at.desc()).all()
    
    result = []
    for topic in topics:
        result.append({
            "id": topic.id,
            "title": topic.title,
            "username": topic.author.username,
            "message_count": len(topic.posts),
            "created_at": topic.created_at
        })
    
    return result

@router.post(
    "/", 
    response_model=schemas.TopicDetailResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": schemas.ErrorResponse}}
)
def create_topic(
    topic_data: schemas.TopicCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if not topic_data.title or not topic_data.content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title and content are required"
        )
    
    db_topic = models.Topic(
        title=topic_data.title,
        content=topic_data.content,
        author_id=current_user.id
    )
    
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    
    return {
        "id": db_topic.id,
        "title": db_topic.title,
        "content": db_topic.content,
        "username": current_user.username,
        "created_at": db_topic.created_at,
        "posts": []
    }

@router.get(
    "/{topic_id}",
    response_model=schemas.TopicDetailResponse,
    responses={404: {"model": schemas.ErrorResponse}}
)
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    
    posts = []
    for post in topic.posts:
        posts.append({
            "id": post.id,
            "content": post.content,
            "username": post.author.username,
            "created_at": post.created_at
        })
    
    return {
        "id": topic.id,
        "title": topic.title,
        "content": topic.content,
        "username": topic.author.username,
        "created_at": topic.created_at,
        "posts": posts
    }