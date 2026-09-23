from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func,ForeignKey
from sqlalchemy.orm import relationship
import bcrypt

from core.core.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(Text, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    tasks = relationship("TaskModel", back_populates="user", cascade="all, delete-orphan")

    # ---------- متدهای رمزنگاری ----------
    def set_password(self, raw_password: str) -> None:
        """پسورد خام رو هش می‌کنه و توی فیلد password می‌ذاره."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(raw_password.encode("utf-8"), salt)
        self.password = hashed.decode("utf-8")

    def verify_password(self, raw_password: str) -> bool:
        """پسورد خام رو با هش ذخیره‌شده مقایسه می‌کنه."""
        if not self.password:
            return False
        return bcrypt.checkpw(
            raw_password.encode("utf-8"),
            self.password.encode("utf-8"),
        )


class TokenModel(Base) :
    __tablename__ = "tokens"

    # ========== ستون‌ها ==========
    id = Column(Integer, primary_key = True, autoincrement = True)
    # شناسه یکتای هر توکن - خودکار زیاد میشه

    user_id = Column(Integer, ForeignKey("users.id"))
    # کلید خارجی به جدول کاربران - صاحب توکن

    token = Column(String, nullable = False, unique = True)
    # خود رشته توکن - نمیتونه خالی باشه و نباید تکراری باشه

    created_date = Column(DateTime, server_default = func.now())
    # تاریخ ساخت توکن - خود دیتابیس پر میکنه

    # ========== رابطه ==========
    user = relationship("UserModel", uselist = False)
    # رابطه با مدل کاربر - uselist=False یعنی یک به یک