new_model = '''
class SimpleInventoryCreate(BaseModel):
    product_name: str
    sku: Optional[str] = ""
    warehouse_name: Optional[str] = "Main Warehouse"
    quantity_on_hand: float
    unit: Optional[str] = "MT"
    unit_cost: Optional[float] = 0.0
    reorder_point: Optional[float] = 20.0
    status: Optional[str] = "ok"
    company_id: int

'''

new_endpoint = '''
@app.post("/inventory/simple", tags=["Inventory"])
def add_simple_inventory(body: SimpleInventoryCreate, db: Session = Depends(get_db)):
    from models import Inventory, Product, Warehouse
    
    # Find or create product
    product = db.query(Product).filter(
        Product.name == body.product_name,
        Product.company_id == body.company_id
    ).first()
    
    if not product:
        product = Product(
            name=body.product_name,
            sku=body.sku or body.product_name[:10].upper().replace(" ", "-"),
            company_id=body.company_id,
            unit=body.unit,
            cost_price=body.unit_cost,
        )
        db.add(product)
        db.flush()
    
    # Find or create warehouse
    warehouse = db.query(Warehouse).filter(
        Warehouse.name == body.warehouse_name,
        Warehouse.company_id == body.company_id
    ).first()
    
    if not warehouse:
        warehouse = Warehouse(
            name=body.warehouse_name,
            company_id=body.company_id,
        )
        db.add(warehouse)
        db.flush()
    
    # Create inventory item
    item = Inventory(
        product_id=product.id,
        warehouse_id=warehouse.id,
        quantity=body.quantity_on_hand,
        cost_price=body.unit_cost,
        reorder_point=body.reorder_point,
    )
    db.add(item)
    db.commit()
    
    return {"message": "SKU added successfully", "product": body.product_name}

'''

content = open('main.py', 'r').read()

# Add SimpleInventoryCreate model before InventoryCreate
insert_before = 'class InventoryCreate(BaseModel):'
content = content.replace(insert_before, new_model + insert_before)

# Add endpoint before existing inventory endpoint
insert_before2 = '@app.get("/inventory"'
content = content.replace(insert_before2, new_endpoint + insert_before2, 1)

open('main.py', 'w').write(content)
print("Done")