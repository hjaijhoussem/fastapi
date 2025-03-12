from fastapi import HTTPException, Response, status, Depends, APIRouter
from typing import Optional, List # For returning a list as response
from .. import modules, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func  # Add this import at the top

router =  APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostVote])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 1, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(modules.Post).filter(modules.Post.title.contains(search)).limit(limit).offset(skip).all() 
    posts = db.query(modules.Post, func.count(modules.Vote.post_id).label("votes")).filter(modules.Post.title.contains(search)).join(modules.Vote, modules.Post.id == modules.Vote.post_id, isouter=True).group_by(modules.Post.id).limit(limit).offset(skip).all()
    return posts



@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = modules.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostVote)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = db.query(modules.Post).filter(modules.Post.id == id).first()
    post = db.query(modules.Post, func.count(modules.Vote.post_id).label("votes")).filter(modules.Post.id == id).join(modules.Vote, modules.Post.id == modules.Vote.post_id, isouter=True).group_by(modules.Post.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post
        


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(modules.Post).filter(modules.Post.id == id)
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model= schemas.PostResponse)
def update_post(id: int, updated_post: schemas.UpdatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(modules.Post).filter(modules.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post
