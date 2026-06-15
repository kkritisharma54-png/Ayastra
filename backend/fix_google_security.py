with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix login to block google-oauth users from password login
old = '''    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not pwd_context.verify(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")'''

new = '''    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Block Google OAuth users from password login
    if user.password_hash == "google-oauth":
        raise HTTPException(status_code=401, detail="Please use Google Sign In for this account")
    
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not pwd_context.verify(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")'''

if old in content:
    content = content.replace(old, new)
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Done")
else:
    print("Pattern not found")