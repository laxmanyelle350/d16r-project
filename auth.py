from fastapi import Cookie, HTTPException
import jwt

SECRET_KEY = "abcdefghijklmnopqrstuvwxyz"
ALGORITHM = "HS256"


def verify_admin(access_token: str = Cookie(None)):
    if access_token is None:
        raise HTTPException(
            status_code=401,
            detail="Login Required"
        )

    try:
        payload = jwt.decode(
            access_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload["is_admin"] != True:
            raise HTTPException(
                status_code=403,
                detail="Admin Access Only"
            )

        return payload

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )