from sqlalchemy import text

import models
from database import Base, SessionLocal, engine
from security import hash_password


def init_db():
    """建表 + 给旧表补列 + 生成默认管理员。每次启动时调用,可重复执行。"""
    # 1. 建所有缺失的表(admins 会被建出来)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # 2. readers 表如果是旧表,补上 password_hash 列
        cols = [row[0] for row in db.execute(text("SHOW COLUMNS FROM readers"))]
        if "password_hash" not in cols:
            db.execute(text("ALTER TABLE readers ADD COLUMN password_hash VARCHAR(200) DEFAULT ''"))
            db.commit()

        # 3. 给还没有密码的读者设置默认密码 123456
        no_pwd_readers = db.query(models.Readers).filter(models.Readers.password_hash == "").all()
        for r in no_pwd_readers:
            r.password_hash = hash_password("123456")
        db.commit()

        # 4. 生成默认管理员 admin / admin123
        admin = db.query(models.Admin).filter(models.Admin.username == "admin").first()
        if admin is None:
            db.add(models.Admin(username="admin", password_hash=hash_password("admin123")))
            db.commit()
    finally:
        db.close()
