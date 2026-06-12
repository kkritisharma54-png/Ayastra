new_endpoint = '''
@app.post("/auth/google", tags=["Auth"])
def google_auth(body: dict, db: Session = Depends(get_db)):
    email = body.get("email")
    full_name = body.get("full_name", email)
    
    # Check if user already exists
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        # Create new company and user
        company = Company(name=f"{full_name} Business", industry="Metal Manufacturing")
        db.add(company)
        db.flush()
        
        user = User(
            full_name=full_name,
            email=email,
            password_hash="google-oauth",
            role="admin",
            company_id=company.id,
        )
        db.add(user)
        db.commit()
    
    from jose import jwt
    from datetime import datetime, timedelta
    token = jwt.encode(
        {"sub": user.email, "exp": datetime.utcnow() + timedelta(hours=24)},
        "ayastra-secret-key",
        algorithm="HS256"
    )
    
    return {
        "token": token,
        "user_id": user.id,
        "company_id": user.company_id,
        "full_name": user.full_name,
    }

'''

content = open('main.py', 'r').read()
insert_before = '@app.post("/auth/signup"'
content = content.replace(insert_before, new_endpoint + insert_before)
open('main.py', 'w').write(content)
print("Done")