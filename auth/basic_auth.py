from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from users.models import UserModel
from core.core.database import get_db
from sqlalchemy.orm import Session

security = HTTPBasic()


# این خط یه نمونه از کلاس HTTPBasic میسازه
# FastAPI از این استفاده میکنه تا هدر Authorization رو بخونه
# و username/password رو استخراج کنه


# ========== تابع وابستگی برای گرفتن کاربر فعلی ==========
def get_current_username(
        credentials: HTTPBasicCredentials = Depends(security),
        db: Session = Depends(get_db)
) :
    """
    این تابع یه Dependency هست که:
    1. اطلاعات Basic Auth رو از هدر درخواست میگیره
    2. کاربر رو از دیتابیس پیدا میکنه
    3. رمز عبور رو بررسی میکنه
    4. اگه همه چی درست بود، آبجکت کاربر رو برمیگردونه
    """

    # ========== مرحله 1: پیدا کردن کاربر توی دیتابیس ==========
    user_obj = db.query(UserModel).filter_by(
        username = credentials.username
    ).one_or_none()
    # credentials.username از هدر Authorization استخراج شده
    # one_or_none() یعنی یا یه کاربر پیدا کن یا None برگردون

    # ========== مرحله 2: اگه کاربر پیدا نشد ==========
    if not user_obj :
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers = {"WWW-Authenticate" : "Basic"},  # ← این هدر حیاتیه!
        )
        # این هدر باعث میشه مرورگر پنجره لاگین رو نشون بده
        # و علامت قفل 🔒 بیاد

    # ========== مرحله 3: بررسی رمز عبور ==========
    if not user_obj.verify_password(credentials.password) :
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers = {"WWW-Authenticate" : "Basic"},
        )
        # verify_password یه متد توی مدل UserModel هست
        # که رمز وارد شده رو با رمز هش شده توی دیتابیس مقایسه میکنه

    # ========== مرحله 4: همه چی درست بود ==========
    return user_obj
    # آبجکت کاربر رو برمیگردونه تا توی مسیرها استفاده بشه