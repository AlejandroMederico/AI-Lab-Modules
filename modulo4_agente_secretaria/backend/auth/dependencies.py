from fastapi import Depends, HTTPException, status
from backend.auth.auth_service import get_current_user
from backend.auth.models import User


def AdminOnly(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependencia para rutas que solo puede usar un rol 'admin'.
    Si el usuario no es admin lanza 403.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Solo administradores."
        )
    return current_user  # se devuelve para uso opcional en la ruta


def User():
    return Depends(get_current_user)
