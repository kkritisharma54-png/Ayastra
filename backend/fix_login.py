content = open('main.py', 'r').read()

old = '    # TODO: verify hashed password\n    return LoginResponse(\n        token=f"stub-token-{user.id}",'

new = '''    from passlib.context import CryptContext
    pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not pwd.verify(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    from jose import jwt
    from datetime import datetime, timedelta
    token = jwt.encode({"sub": user.email, "exp": datetime.utcnow() + timedelta(hours=24)}, "ayastra-secret", algorithm="HS256")
    return LoginResponse(
        token=token,'''

result = content.replace(old, new)
open('main.py', 'w').write(result)
print("Done")