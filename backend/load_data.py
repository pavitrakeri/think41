import pandas as pd
import os
import sys
from sqlalchemy.orm import Session
from database import SessionLocal, create_tables, Product, Order, OrderItem
from datetime import datetime
import uuid

def load_products(csv_path: str, db: Session):
    """Load products from CSV file"""
    try:
        df = pd.read_csv(csv_path)
        print(f"Loading {len(df)} products...")
        
        for _, row in df.iterrows():
            product = Product(
                product_id=str(row.get('product_id', uuid.uuid4())),
                product_name=str(row.get('product_name', 'Unknown Product')),
                category=str(row.get('category', 'General')),
                price=float(row.get('price', 0.0)),
                stock_quantity=int(row.get('stock_quantity', 0)),
                description=str(row.get('description', ''))
            )
            db.add(product)
        
        db.commit()
        print(f"Successfully loaded {len(df)} products")
        
    except Exception as e:
        print(f"Error loading products: {e}")
        db.rollback()

def load_orders(csv_path: str, db: Session):
    """Load orders from CSV file"""
    try:
        df = pd.read_csv(csv_path)
        print(f"Loading {len(df)} orders...")
        
        for _, row in df.iterrows():
            # Parse order date
            order_date = datetime.now()
            if 'order_date' in row and pd.notna(row['order_date']):
                try:
                    order_date = pd.to_datetime(row['order_date'])
                except:
                    order_date = datetime.now()
            
            order = Order(
                order_id=str(row.get('order_id', uuid.uuid4())),
                customer_id=str(row.get('customer_id', 'unknown')),
                order_date=order_date,
                status=str(row.get('status', 'pending')),
                total_amount=float(row.get('total_amount', 0.0))
            )
            db.add(order)
        
        db.commit()
        print(f"Successfully loaded {len(df)} orders")
        
    except Exception as e:
        print(f"Error loading orders: {e}")
        db.rollback()

def load_order_items(csv_path: str, db: Session):
    """Load order items from CSV file"""
    try:
        df = pd.read_csv(csv_path)
        print(f"Loading {len(df)} order items...")
        
        for _, row in df.iterrows():
            order_item = OrderItem(
                order_id=str(row.get('order_id', '')),
                product_id=str(row.get('product_id', '')),
                quantity=int(row.get('quantity', 1)),
                price=float(row.get('price', 0.0))
            )
            db.add(order_item)
        
        db.commit()
        print(f"Successfully loaded {len(df)} order items")
        
    except Exception as e:
        print(f"Error loading order items: {e}")
        db.rollback()

def main():
    """Main function to load all data"""
    print("Starting data loading process...")
    
    # Create tables
    create_tables()
    print("Database tables created successfully")
    
    db = SessionLocal()
    
    try:
        # Define data directory
        data_dir = "data"
        
        # Load products
        products_file = os.path.join(data_dir, "products.csv")
        if os.path.exists(products_file):
            load_products(products_file, db)
        else:
            print(f"Products file not found at {products_file}")
        
        # Load orders
        orders_file = os.path.join(data_dir, "orders.csv")
        if os.path.exists(orders_file):
            load_orders(orders_file, db)
        else:
            print(f"Orders file not found at {orders_file}")
        
        # Load order items
        order_items_file = os.path.join(data_dir, "order_items.csv")
        if os.path.exists(order_items_file):
            load_order_items(order_items_file, db)
        else:
            print(f"Order items file not found at {order_items_file}")
        
        print("Data loading completed successfully!")
        
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main() 