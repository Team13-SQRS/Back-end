from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.security.tokens import verify_access_token
from app.database.crud import get_user_by_username
from app.database.database import get_db
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """Dependency to get the authenticated user from JWT token.
    Args:
        token: JWT access token from Authorization header
        db: Database session
    Returns:
        User: Authenticated user object
    Raises:
        HTTPException: 401 if token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_access_token(token)
    if not payload:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user
