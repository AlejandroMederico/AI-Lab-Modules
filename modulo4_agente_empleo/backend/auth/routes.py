from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.auth import schemas, models, auth_service
from backend.database import get_db
from backend.auth.dependencies import AdminOnly
from backend.auth.decorators import User, admin_required
from backend.auth.schemas import PasswordUpdate
from backend.auth.auth_service import get_password_hash

router = APIRouter(tags=["auth"])


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


@router.post("/register", response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email ya registrado")
    user = models.User(
        email=user_in.email,
        hashed_password=auth_service.get_password_hash(user_in.password),
        role=user_in.role or "user",  # Default role to 'user' if not provided
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = get_user_by_email(db, form_data.username)
    if not user or not auth_service.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas"
        )
    token = auth_service.create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer", "role": user.role}


@router.get("/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(auth_service.get_current_user)):
    return current_user


@router.get("/admin/ping", dependencies=[Depends(AdminOnly)])
def admin_ping():
    return {"msg": "pong", "scope": "admin"}


@router.get("/users", dependencies=[Depends(AdminOnly)])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@router.patch("/users/{user_id}", dependencies=[Depends(AdminOnly)])
def update_user(
    user_id: int, user_data: schemas.UserUpdate, db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if user_data.email is not None:
        user.email = user_data.email
    if user_data.role is not None:
        user.role = user_data.role
    db.commit()
    return {"msg": "Usuario actualizado"}


@router.delete("/users/{user_id}", dependencies=[Depends(AdminOnly)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(user)
    db.commit()
    return {"msg": "Usuario eliminado"}


@router.get("/users/me")
def get_me(current_user: models.User = User()):
    return current_user


@router.post("/users/me/password")
def update_password(
    data: PasswordUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = User(),
):
    current_user.hashed_password = get_password_hash(data.new_password)
    db.commit()
    return {"msg": "Contraseña actualizada"}


@router.get("/admin/test")
@admin_required  # 👈 solo admins
def admin_test(current_user: models.User = User()):
    """
    Ruta de prueba: responde solo si current_user.role == 'admin'.
    """
    return {
        "msg": "Acceso concedido",
        "user": current_user.email,
        "role": current_user.role,
    }
