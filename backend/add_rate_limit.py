with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add rate limiting imports after existing imports
old_imports = 'from fastapi import FastAPI, Depends, HTTPException, Query'
new_imports = '''from fastapi import FastAPI, Depends, HTTPException, Query, Request
from collections import defaultdict
import time'''

content = content.replace(old_imports, new_imports)

# Add rate limiter after app initialization
old = 'app = FastAPI(title="Ayastra API", version="2.0.0")'
new = '''app = FastAPI(title="Ayastra API", version="2.0.0")

# Simple in-memory rate limiter for login attempts
login_attempts: dict = defaultdict(list)

def check_rate_limit(ip: str, max_attempts: int = 5, window: int = 300):
    """Allow max 5 login attempts per IP per 5 minutes."""
    now = time.time()
    attempts = login_attempts[ip]
    # Remove old attempts outside window
    login_attempts[ip] = [t for t in attempts if now - t < window]
    if len(login_attempts[ip]) >= max_attempts:
        raise HTTPException(
            status_code=429,
            detail="Too many login attempts. Please wait 5 minutes."
        )
    login_attempts[ip].append(now)'''

content = content.replace(old, new)

# Add rate limit check to login endpoint
old_login = 'def login(body: LoginRequest, db: Session = Depends(get_db)):'
new_login = 'def login(body: LoginRequest, request: Request, db: Session = Depends(get_db)):\n    check_rate_limit(request.client.host)'

content = content.replace(old_login, new_login)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")