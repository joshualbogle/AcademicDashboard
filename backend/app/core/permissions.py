from fastapi import Depends, HTTPException, status
from app.core.security import get_current_user


def require_group(group_id: str):
    def dependency(current_user=Depends(get_current_user)):
        if group_id not in current_user.get("groups", []):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        return current_user
    return dependency


def require_any_group(group_ids: list[str]):
    def dependency(current_user=Depends(get_current_user)):
        if not any(g in current_user.get("groups", []) for g in group_ids):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        return current_user
    return dependency
