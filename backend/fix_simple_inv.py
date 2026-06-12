with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('@app.post("/inventory/simple"')
end = content.find('\n@app.', start + 10)
if end == -1:
    end = content.find('\n# ---', start + 10)

new_endpoint = '''@app.post("/inventory/simple", tags=["Inventory"])
def add_simple_inventory(body: SimpleInventoryCreate, db: Session = Depends(get_db)):
    warehouse = db.query(Warehouse).filter(
        Warehouse.company_id == body.company_id
    ).first()
    if not warehouse:
        warehouse = Warehouse(
            name=body.warehouse_name or "Main Warehouse",
            company_id=body.company_id,
        )
        db.add(warehouse)
        db.flush()
    product = db.query(Product).filter(Product.name == body.product_name).first()
    if not product:
        import uuid
        sku = body.sku or (body.product_name[:8].upper().replace(" ", "-") + "-" + str(uuid.uuid4())[:4].upper())
        product = Product(name=body.product_name, sku=sku, unit=body.unit or "MT")
        db.add(product)
        db.flush()
    item = InventoryItem(
        product_id=product.id,
        warehouse_id=warehouse.id,
        quantity=body.quantity_on_hand,
        cost_price=body.unit_cost or 0.0,
        reorder_point=body.reorder_point or 20.0,
    )
    db.add(item)
    db.commit()
    return {"message": "SKU added successfully", "product": body.product_name}

'''

content = content[:start] + new_endpoint + content[end:]
open('main.py', 'w', encoding='utf-8').write(content)
print("Done")