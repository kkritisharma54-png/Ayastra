with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add get_current_user helper after rate limiter
old = '# Simple in-memory rate limiter for login attempts'
new = '''# ---------------------------------------------------------------------------
# Auth helper - get current user from JWT token
# ---------------------------------------------------------------------------
def get_current_user_id(authorization: str = None, db: Session = None):
    """Extract and verify JWT token, return user."""
    return None  # Optional auth for now

def verify_token(token: str) -> dict:
    """Verify JWT and return payload."""
    from jose import jwt, JWTError
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-change-in-production")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def get_token_from_header(request: Request) -> str:
    """Extract Bearer token from Authorization header."""
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    return auth.split(" ")[1]

def get_current_company_id(request: Request, db: Session = Depends(get_db)) -> int:
    """Get company_id from JWT token."""
    token = get_token_from_header(request)
    payload = verify_token(token)
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user.company_id

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """Get current user from JWT token."""
    token = get_token_from_header(request)
    payload = verify_token(token)
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Simple in-memory rate limiter for login attempts'''

content = content.replace(old, new)

# Fix PATCH inventory - verify ownership
old_patch_inv = '''def update_inventory(item_id: int, body: InventoryUpdate, db: Session = Depends(get_db)):
    """Update quantity / cost / reorder for a specific inventory row."""
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")'''

new_patch_inv = '''def update_inventory(item_id: int, body: InventoryUpdate, request: Request, db: Session = Depends(get_db)):
    """Update quantity / cost / reorder for a specific inventory row."""
    current_user = get_current_user(request, db)
    item = db.query(InventoryItem).join(Warehouse).filter(
        InventoryItem.id == item_id,
        Warehouse.company_id == current_user.company_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found or access denied")'''

content = content.replace(old_patch_inv, new_patch_inv)

# Fix DELETE inventory - verify ownership
old_del_inv = '''def delete_inventory(item_id: int, db: Session = Depends(get_db)):
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")'''

new_del_inv = '''def delete_inventory(item_id: int, request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user(request, db)
    item = db.query(InventoryItem).join(Warehouse).filter(
        InventoryItem.id == item_id,
        Warehouse.company_id == current_user.company_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found or access denied")'''

content = content.replace(old_del_inv, new_del_inv)

# Fix PATCH order status - verify ownership
old_patch_order = '''def update_order_status(order_id: int, body: OrderStatusUpdate, db: Session = Depends(get_db)):
    """Update order status (pending → confirmed → processing → dispatched → delivered)."""
    valid = ["pending", "confirmed", "processing", "dispatched", "delivered"]
    if body.status not in valid:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {valid}")
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")'''

new_patch_order = '''def update_order_status(order_id: int, body: OrderStatusUpdate, request: Request, db: Session = Depends(get_db)):
    """Update order status (pending → confirmed → processing → dispatched → delivered)."""
    current_user = get_current_user(request, db)
    valid = ["pending", "confirmed", "processing", "dispatched", "delivered"]
    if body.status not in valid:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {valid}")
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.company_id == current_user.company_id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found or access denied")'''

content = content.replace(old_patch_order, new_patch_order)

# Fix GET/PATCH profile - verify user owns their own profile
old_get_profile = '''def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")'''

new_get_profile = '''def get_profile(user_id: int, request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user(request, db)
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")'''

content = content.replace(old_get_profile, new_get_profile)

# Fix PATCH profile
old_patch_profile = '''def update_profile(user_id: int, body: ProfileUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")'''

new_patch_profile = '''def update_profile(user_id: int, body: ProfileUpdate, request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user(request, db)
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")'''

content = content.replace(old_patch_profile, new_patch_profile)

# Fix GET company settings
old_get_company = '''def get_company(company_id: int, db: Session = Depends(get_db)):
    c = db.query(Company).filter(Company.id == company_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Company not found")'''

new_get_company = '''def get_company(company_id: int, request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user(request, db)
    if current_user.company_id != company_id:
        raise HTTPException(status_code=403, detail="Access denied")
    c = db.query(Company).filter(Company.id == company_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Company not found")'''

content = content.replace(old_get_company, new_get_company)

# Fix PATCH company settings
old_patch_company = '''def update_company(company_id: int, body: CompanyUpdate, db: Session = Depends(get_db)):
    c = db.query(Company).filter(Company.id == company_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Company not found")'''

new_patch_company = '''def update_company(company_id: int, body: CompanyUpdate, request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user(request, db)
    if current_user.company_id != company_id:
        raise HTTPException(status_code=403, detail="Access denied")
    c = db.query(Company).filter(Company.id == company_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Company not found")'''

content = content.replace(old_patch_company, new_patch_company)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done - IDOR fixes applied")