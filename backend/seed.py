from database import Base, SessionLocal, engine, Base
from models import Product, BrassPrice, ScrapInventory
from datetime import datetime, timedelta

Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()

    products = [
        Product(name="Brass Ganesh Statue", category="statue",
                weight_kg=4.240, stock=100,
                price_type="per_kg", price=1200),

        Product(name="Copper Glass", category="kitchenware",
                weight_kg=None, stock=100,
                price_type="per_piece", price=400),

        Product(name="Brass Glass", category="kitchenware",
                weight_kg=None, stock=100,
                price_type="per_piece", price=425),

        Product(name="Brass Glass Set", category="kitchenware",
                weight_kg=None, stock=100,
                price_type="per_piece", price=400),

        Product(name="Brass Bail Gadi", category="decor",
                weight_kg=None, stock=100,
                price_type="per_piece", price=450),

        Product(name="Brass Durga Mata Statue", category="statue",
                weight_kg=1.080, stock=100,
                price_type="per_kg", price=1150),
    ]

    brass_prices = [
        BrassPrice(price_per_kg=510, recorded_at=datetime.now() - timedelta(days=6)),
        BrassPrice(price_per_kg=515, recorded_at=datetime.now() - timedelta(days=5)),
        BrassPrice(price_per_kg=508, recorded_at=datetime.now() - timedelta(days=4)),
        BrassPrice(price_per_kg=520, recorded_at=datetime.now() - timedelta(days=3)),
        BrassPrice(price_per_kg=518, recorded_at=datetime.now() - timedelta(days=2)),
        BrassPrice(price_per_kg=525, recorded_at=datetime.now() - timedelta(days=1)),
        BrassPrice(price_per_kg=522, recorded_at=datetime.now()),
    ]

    # Some scrap inventory
    scrap = [
        ScrapInventory(weight_kg=45.5, quality="clean"),
        ScrapInventory(weight_kg=30.0, quality="mixed"),
    ]

    db.add_all(products)
    db.add_all(brass_prices)
    db.add_all(scrap)
    db.commit()
    db.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()

#Base.metadata.create_all : Creates the actual .db file and tables
#SessionLocal() :Opens a connection to the database
#db.add_all() :Queues all records to be inserted
#db.commit() : Actually saves them to the database
#db.close() :Closes the connection cleanly