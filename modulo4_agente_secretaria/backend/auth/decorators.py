# backend/auth/decorators.py
from fastapi import Depends, HTTPException, status
from functools import wraps
from backend.auth.auth_service import get_current_user
from backend.auth.models import User as UserModel


def User() -> UserModel:
    """
    Dependencia que devuelve el usuario autenticado.
    Se usa igual que Depends(get_current_user), pero con sintaxis compacta.
    """
    return Depends(get_current_user)


# backend/auth/decorators.py


def admin_required(func):
    """
    Decorador para que solo usuarios con role == 'admin' accedan a la ruta.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # current_user se inyecta vía Depends
        current_user: UserModel = kwargs.get("current_user")
        if current_user is None:
            # Si la ruta no lo recibió, pídelo con Depends
            current_user = get_current_user.__call__(*args, **kwargs)

        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo administradores",
            )
        return func(*args, **kwargs)

    return wrapper
