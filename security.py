from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, Header, HTTPException

SECRET_KEY = "library-secret-key-2026"  # 签名密钥(生产环境要放环境变量,不能写死)
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24


# ---- 密码加密 ----
def hash_password(password: str) -> str:
    """把明文密码加密成一串哈希(数据库只存这串,不存明文)"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """校验用户输入的密码和库里存的哈希是否匹配"""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False


# ---- token 签发与解析 ----
def create_token(user_id: int, role: str) -> str:
    """登录成功后,发一张带身份信息的"通行证"(token)"""
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRE_HOURS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    """解析通行证,还原身份;过期或无效就报错"""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="登录已过期,请重新登录")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效的登录凭证")


# ---- 鉴权依赖(给接口"上锁"用) ----
def get_current_user(authorization: str = Header(None)):
    """从请求头取 token,校验后返回当前登录用户 {id, role}"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未登录")
    token = authorization[7:]  # 去掉 "Bearer " 前缀
    payload = decode_token(token)
    return {"id": int(payload["sub"]), "role": payload["role"]}


def require_admin(user=Depends(get_current_user)):
    """只放行管理员"""
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return user


def require_reader(user=Depends(get_current_user)):
    """只放行读者(管理员也放行)"""
    if user["role"] not in ("reader", "admin"):
        raise HTTPException(status_code=403, detail="需要读者权限")
    return user
