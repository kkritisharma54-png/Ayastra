content = open('main.py', 'r').read()

old = '''    from models import Inventory, Product, Warehouse
    
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
    
    return {"message": "SKU added successfully", "product": body.product_name}'''

new = '''    # Find or create product
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
    item = InventoryItem(
        product_id=product.id,
        warehouse_id=warehouse.id,
        quantity=body.quantity_on_hand,
        cost_price=body.unit_cost,
        reorder_point=body.reorder_point,
    )
    db.add(item)
    db.commit()
    
    return {"message": "SKU added successfully", "product": body.product_name}'''

result = content.replace(old, new)
open('main.py', 'w').write(result)
print("Done" if old in content else "Pattern not found")