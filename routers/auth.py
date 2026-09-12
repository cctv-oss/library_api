from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import LoginRequest, TokenResponse
from security import create_token, get_current_user, verify_password

router = APIRouter()


@router.post("/auth/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    # 管理员登录
    if data.role == "admin":
        admin = db.query(models.Admin).filter(models.Admin.username == data.account).first()
        if admin is None or not verify_password(data.password, admin.password_hash):
            raise HTTPException(status_code=401, detail="用户名或密码错误")
        token = create_token(admin.id, "admin")
        return TokenResponse(token=token, role="admin", id=admin.id, name=admin.username)

    # 读者登录(用手机号)
    if data.role == "reader":
        reader = db.query(models.Readers).filter(models.Readers.phone == data.account).first()
        if reader is None or not verify_password(data.password, reader.password_hash):
            raise HTTPException(status_code=401, detail="手机号或密码错误")
        if reader.status != 1:
            raise HTTPException(status_code=403, detail="账号已被停用")
        token = create_token(reader.id, "reader")
        return TokenResponse(token=token, role="reader", id=reader.id, name=reader.name)

    raise HTTPException(status_code=400, detail="角色只能是 admin 或 reader")


@router.get("/auth/me")
def me(user=Depends(get_current_user), db: Session = Depends(get_db)):
    """返回当前登录用户的身份信息"""
    if user["role"] == "admin":
        admin = db.query(models.Admin).filter(models.Admin.id == user["id"]).first()
        return {"id": admin.id, "role": "admin", "name": admin.username}
    reader = db.query(models.Readers).filter(models.Readers.id == user["id"]).first()
    return {
        "id": reader.id, "role": "reader", "name": reader.name,
        "phone": reader.phone, "email": reader.email,
    }
