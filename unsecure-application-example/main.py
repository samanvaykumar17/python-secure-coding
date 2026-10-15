import os
import subprocess
from typing import Optional

from fastapi import Cookie, Depends, FastAPI, HTTPException, Response, status
from fastapi.responses import HTMLResponse
from passlib.context import CryptContext
from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy import Column, Integer, String, create_engine, or_, text
from sqlalchemy.orm import Session, declarative_base, sessionmaker

app = FastAPI(title="User CRUD API")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:password@localhost:3306/bank_users",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class EmailUpdate(BaseModel):
    email: EmailStr


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    hashed_password: str
    model_config = ConfigDict(from_attributes=True)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def ensure_unique_fields(
    db: Session,
    username: Optional[str],
    email: Optional[str],
    exclude_user_id: Optional[int] = None,
) -> None:
    if username is None and email is None:
        return

    filters = []
    if username is not None:
        filters.append(User.username == username)
    if email is not None:
        filters.append(User.email == email)

    query = db.query(User).filter(or_(*filters))
    if exclude_user_id is not None:
        query = query.filter(User.id != exclude_user_id)

    existing_user = query.first()
    if existing_user is None:
        return

    if username is not None and existing_user.username == username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    if email is not None and existing_user.email == email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )


@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserOut:
    ensure_unique_fields(db, payload.username, payload.email)

    new_user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserOut.model_validate(new_user)


@app.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)) -> list[UserOut]:
    user_rows = db.query(User).all()
    return [UserOut.model_validate(user) for user in user_rows]


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserOut:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserOut.model_validate(user)


@app.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)) -> UserOut:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    username = payload.username if payload.username is not None else user.username
    email = payload.email if payload.email is not None else user.email
    ensure_unique_fields(db, username, email, exclude_user_id=user_id)

    user.username = username
    user.email = email
    if payload.password:
        user.hashed_password = hash_password(payload.password)

    db.commit()
    db.refresh(user)
    return UserOut.model_validate(user)


@app.delete("/users/{user_id}", response_model=UserOut)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> UserOut:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    response_user = UserOut.model_validate(user)
    db.delete(user)
    db.commit()
    return response_user


# 79
@app.get("/users/greet-user/{user_id}", response_class=HTMLResponse)
def greet_user(user_id: int, db: Session = Depends(get_db)) -> str:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return f"<h1>Welcome {user.username}</h1>"


# 89
@app.get("/users/search-users")
def search_users(username: str, db: Session = Depends(get_db)) -> dict:
    raw_query = f"SELECT id, username, email FROM users WHERE username = '{username}'"
    rows = db.execute(text(raw_query)).mappings().all()
    return {"query": raw_query, "rows": [dict(row) for row in rows]}


# 352
@app.post("/users/{user_id}/update-email", response_model=UserOut)
def update_email(
    user_id: int,
    payload: EmailUpdate,
    session_user_id: Optional[int] = Cookie(default=None, alias="session_user_id"),
    db: Session = Depends(get_db),
) -> UserOut:

    if session_user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    if session_user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    ensure_unique_fields(db, None, payload.email, exclude_user_id=user_id)
    user.email = payload.email
    db.commit()
    db.refresh(user)
    return UserOut.model_validate(user)


# 862
@app.delete("/admin/users/{user_id}/delete", response_model=UserOut)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> UserOut:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    response_user = UserOut.model_validate(user)
    db.delete(user)
    db.commit()
    return response_user


# 22
@app.get("/files/read-file")
def read_file(path: str) -> dict:
    base_dir = "./user_uploads"
    target_path = os.path.join(base_dir, path)

    # Intentionally vulnerable: no path normalization or traversal checks.
    try:
        with open(target_path, "r", encoding="utf-8") as file_obj:
            content = file_obj.read()
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    return {"path": target_path, "content": content}


# 78
@app.get("/system/run-command")
def run_command(target: str) -> dict:
    command = f"cmd /c echo Checking {target}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


# 94
@app.post("/system/execute-code")
def execute_code(code: str) -> dict:
    execution_scope = {"result": None}
    try:
        exec(code, {}, execution_scope)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    return {
        "status": "executed",
        "result": execution_scope.get("result"),
    }


# 306
@app.post("/admin/reset-all-passwords")
def reset_all_passwords(new_password: str, db: Session = Depends(get_db)) -> dict:
    hashed = hash_password(new_password)
    users = db.query(User).all()
    for user in users:
        user.hashed_password = hashed

    db.commit()
    return {"updated_users": len(users), "status": "all passwords reset"}

# 259
# line 18

# 384
@app.post("/auth/login")
def login(
    username: str,
    response: Response,
    session_id: Optional[str] = Cookie(default=None, alias="session_id"),
    db: Session = Depends(get_db),
) -> dict:
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    active_session_id = session_id if session_id else f"session-{user.id}"
    response.set_cookie("session_id", active_session_id, httponly=True)
    return {
        "status": "logged_in",
        "user_id": user.id,
        "session_id": active_session_id,
    }








