from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.auth import schemas, models, auth_service
from backend.database import get_db
from backend.auth.dependencies import AdminOnly
from backend.auth.decorators import User, admin_required
from backend.auth.schemas import PasswordUpdate
from backend.auth.auth_service import get_password_hash
from backend.logger.logger import logger

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
        role=user_in.role or "user",
        auth_provider="local",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info(f"Usuario registrado exitosamente: {user.email}")
    return user


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = get_user_by_email(db, form_data.username)
    if not user:
        logger.warning(f"Login fallido: usuario no encontrado ({form_data.username})")
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    if user.auth_provider != "local":
        logger.warning(f"Login con método incorrecto para {form_data.username}")
        raise HTTPException(
            status_code=400,
            detail="Este correo fue registrado con autenticación de Google",
        )

    if not auth_service.verify_password(form_data.password, user.hashed_password):
        logger.warning(
            f"Login fallido: contraseña incorrecta para {form_data.username}"
        )
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    logger.info(f"Login exitoso para {user.email} (rol: {user.role})")
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
        logger.warning(f"Usuario no encontrado con el ID: {user_id} para actualización")
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
        logger.warning(f"Usuario no encontrado con el ID: {user_id} para eliminación")
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


@router.post("/auth/google", response_model=schemas.Token)
def login_with_google(
    google_data: schemas.GoogleLoginSchema, db: Session = Depends(get_db)
):
    try:
        decoded_token = auth_service.verificar_token_google(google_data.id_token)
        firebase_uid = decoded_token["uid"]
        email = decoded_token.get("email")

        if email is None:
            logger.error("Token de Google válido pero sin email")
            raise HTTPException(status_code=400, detail="Email no encontrado en token")

        user = db.query(models.User).filter(models.User.email == email).first()

        # ❌ Ya existe pero no es de Google
        if user and user.auth_provider != "google":
            logger.warning(f"Intento de login con Google para cuenta local: {email}")
            raise HTTPException(
                status_code=400,
                detail="Este correo ya está registrado con otro método de autenticación",
            )

        # ✅ No existe: crear nuevo usuario con auth_provider='google'
        if not user:
            user = models.User(
                email=email,
                firebase_uid=firebase_uid,
                role="user",
                auth_provider="google",
                hashed_password="firebase",  # dummy
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"Usuario registrado por Google: {user.email}")

        # Emitir token JWT normal del sistema
        token = auth_service.create_access_token(
            data={"sub": str(user.id), "role": user.role}
        )

        logger.info(f"Login exitoso con Google para {user.email} (rol: {user.role})")
        return {"access_token": token, "token_type": "bearer", "role": user.role}

    except Exception as e:
        logger.error(f"Error al verificar token de Google: {e}")
        raise HTTPException(status_code=401, detail=f"Token de Google inválido: {e}")
