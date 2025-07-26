import pandas as pd
import os
import sys
from sqlalchemy.orm import Session
from database import SessionLocal, create_tables, Product, Order, OrderItem, User, InventoryItem, DistributionCenter
from datetime import datetime
import uuid

def load_products(csv_path: str, db: Session):
    """Load products from CSV file"""
    try:
        print(f"Loading products from {csv_path}...")
        
        # Read CSV in chunks to handle large files
        chunk_size = 10000
        total_loaded = 0
        
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
            print(f"Processing chunk with {len(chunk)} products...")
            
            for _, row in chunk.iterrows():
                try:
                    product = Product(
                        id=int(row['id']),
                        cost=float(row.get('cost', 0.0)),
                        category=str(row.get('category', '')),
                        name=str(row.get('name', '')),
                        brand=str(row.get('brand', '')),
                        retail_price=float(row.get('retail_price', 0.0)),
                        department=str(row.get('department', '')),
                        sku=str(row.get('sku', '')),
                        distribution_center_id=int(row.get('distribution_center_id', 0))
                    )
                    db.add(product)
                    total_loaded += 1
                except Exception as e:
                    print(f"Error processing product row: {e}")
                    continue
            
            # Commit each chunk
            db.commit()
            print(f"Committed chunk. Total loaded so far: {total_loaded}")
        
        print(f"Successfully loaded {total_loaded} products")
        
    except Exception as e:
        print(f"Error loading products: {e}")
        db.rollback()

def load_users(csv_path: str, db: Session):
    """Load users from CSV file"""
    try:
        print(f"Loading users from {csv_path}...")
        
        chunk_size = 10000
        total_loaded = 0
        
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
            print(f"Processing chunk with {len(chunk)} users...")
            
            for _, row in chunk.iterrows():
                try:
                    # Parse created_at date
                    created_at = None
                    if 'created_at' in row and pd.notna(row['created_at']):
                        try:
                            created_at = pd.to_datetime(row['created_at'])
                        except:
                            created_at = datetime.now()
                    
                    user = User(
                        id=int(row['id']),
                        first_name=str(row.get('first_name', '')),
                        last_name=str(row.get('last_name', '')),
                        email=str(row.get('email', '')),
                        age=int(row.get('age', 0)) if pd.notna(row.get('age')) else None,
                        country=str(row.get('country', '')),
                        city=str(row.get('city', '')),
                        state=str(row.get('state', '')),
                        postal_code=str(row.get('postal_code', '')),
                        created_at=created_at
                    )
                    db.add(user)
                    total_loaded += 1
                except Exception as e:
                    print(f"Error processing user row: {e}")
                    continue
            
            db.commit()
            print(f"Committed chunk. Total loaded so far: {total_loaded}")
        
        print(f"Successfully loaded {total_loaded} users")
        
    except Exception as e:
        print(f"Error loading users: {e}")
        db.rollback()

def load_orders(csv_path: str, db: Session):
    """Load orders from CSV file"""
    try:
        print(f"Loading orders from {csv_path}...")
        
        chunk_size = 10000
        total_loaded = 0
        
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
            print(f"Processing chunk with {len(chunk)} orders...")
            
            for _, row in chunk.iterrows():
                try:
                    # Parse dates
                    created_at = None
                    returned_at = None
                    shipped_at = None
                    delivered_at = None
                    
                    if 'created_at' in row and pd.notna(row['created_at']):
                        try:
                            created_at = pd.to_datetime(row['created_at'])
                        except:
                            created_at = datetime.now()
                    
                    if 'returned_at' in row and pd.notna(row['returned_at']):
                        try:
                            returned_at = pd.to_datetime(row['returned_at'])
                        except:
                            returned_at = None
                    
                    if 'shipped_at' in row and pd.notna(row['shipped_at']):
                        try:
                            shipped_at = pd.to_datetime(row['shipped_at'])
                        except:
                            shipped_at = None
                    
                    if 'delivered_at' in row and pd.notna(row['delivered_at']):
                        try:
                            delivered_at = pd.to_datetime(row['delivered_at'])
                        except:
                            delivered_at = None
                    
                    order = Order(
                        order_id=int(row['order_id']),
                        user_id=int(row.get('user_id', 0)),
                        status=str(row.get('status', '')),
                        gender=str(row.get('gender', '')),
                        created_at=created_at,
                        returned_at=returned_at,
                        shipped_at=shipped_at,
                        delivered_at=delivered_at,
                        num_of_item=int(row.get('num_of_item', 0))
                    )
                    db.add(order)
                    total_loaded += 1
                except Exception as e:
                    print(f"Error processing order row: {e}")
                    continue
            
            db.commit()
            print(f"Committed chunk. Total loaded so far: {total_loaded}")
        
        print(f"Successfully loaded {total_loaded} orders")
        
    except Exception as e:
        print(f"Error loading orders: {e}")
        db.rollback()

def load_order_items(csv_path: str, db: Session):
    """Load order items from CSV file"""
    try:
        print(f"Loading order items from {csv_path}...")
        
        chunk_size = 10000
        total_loaded = 0
        
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
            print(f"Processing chunk with {len(chunk)} order items...")
            
            for _, row in chunk.iterrows():
                try:
                    # Parse dates
                    created_at = None
                    shipped_at = None
                    delivered_at = None
                    returned_at = None
                    
                    if 'created_at' in row and pd.notna(row['created_at']):
                        try:
                            created_at = pd.to_datetime(row['created_at'])
                        except:
                            created_at = datetime.now()
                    
                    if 'shipped_at' in row and pd.notna(row['shipped_at']):
                        try:
                            shipped_at = pd.to_datetime(row['shipped_at'])
                        except:
                            shipped_at = None
                    
                    if 'delivered_at' in row and pd.notna(row['delivered_at']):
                        try:
                            delivered_at = pd.to_datetime(row['delivered_at'])
                        except:
                            delivered_at = None
                    
                    if 'returned_at' in row and pd.notna(row['returned_at']):
                        try:
                            returned_at = pd.to_datetime(row['returned_at'])
                        except:
                            returned_at = None
                    
                    order_item = OrderItem(
                        order_id=int(row.get('order_id', 0)),
                        user_id=int(row.get('user_id', 0)),
                        product_id=int(row.get('product_id', 0)),
                        inventory_item_id=int(row.get('inventory_item_id', 0)),
                        status=str(row.get('status', '')),
                        created_at=created_at,
                        shipped_at=shipped_at,
                        delivered_at=delivered_at,
                        returned_at=returned_at,
                        sale_price=float(row.get('sale_price', 0.0))
                    )
                    db.add(order_item)
                    total_loaded += 1
                except Exception as e:
                    print(f"Error processing order item row: {e}")
                    continue
            
            db.commit()
            print(f"Committed chunk. Total loaded so far: {total_loaded}")
        
        print(f"Successfully loaded {total_loaded} order items")
        
    except Exception as e:
        print(f"Error loading order items: {e}")
        db.rollback()

def load_inventory_items(csv_path: str, db: Session):
    """Load inventory items from CSV file"""
    try:
        print(f"Loading inventory items from {csv_path}...")
        
        chunk_size = 10000
        total_loaded = 0
        
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
            print(f"Processing chunk with {len(chunk)} inventory items...")
            
            for _, row in chunk.iterrows():
                try:
                    # Parse dates
                    created_at = None
                    sold_at = None
                    
                    if 'created_at' in row and pd.notna(row['created_at']):
                        try:
                            created_at = pd.to_datetime(row['created_at'])
                        except:
                            created_at = datetime.now()
                    
                    if 'sold_at' in row and pd.notna(row['sold_at']):
                        try:
                            sold_at = pd.to_datetime(row['sold_at'])
                        except:
                            sold_at = None
                    
                    inventory_item = InventoryItem(
                        id=int(row['id']),
                        product_id=int(row.get('product_id', 0)),
                        created_at=created_at,
                        sold_at=sold_at,
                        cost=float(row.get('cost', 0.0)),
                        product_category=str(row.get('product_category', '')),
                        product_name=str(row.get('product_name', '')),
                        product_brand=str(row.get('product_brand', '')),
                        product_retail_price=float(row.get('product_retail_price', 0.0)),
                        product_department=str(row.get('product_department', '')),
                        product_sku=str(row.get('product_sku', '')),
                        product_distribution_center_id=int(row.get('product_distribution_center_id', 0))
                    )
                    db.add(inventory_item)
                    total_loaded += 1
                except Exception as e:
                    print(f"Error processing inventory item row: {e}")
                    continue
            
            db.commit()
            print(f"Committed chunk. Total loaded so far: {total_loaded}")
        
        print(f"Successfully loaded {total_loaded} inventory items")
        
    except Exception as e:
        print(f"Error loading inventory items: {e}")
        db.rollback()

def load_distribution_centers(csv_path: str, db: Session):
    """Load distribution centers from CSV file"""
    try:
        df = pd.read_csv(csv_path)
        print(f"Loading {len(df)} distribution centers...")
        
        for _, row in df.iterrows():
            try:
                distribution_center = DistributionCenter(
                    id=int(row['id']),
                    name=str(row.get('name', '')),
                    latitude=float(row.get('latitude', 0.0)),
                    longitude=float(row.get('longitude', 0.0))
                )
                db.add(distribution_center)
            except Exception as e:
                print(f"Error processing distribution center row: {e}")
                continue
        
        db.commit()
        print(f"Successfully loaded {len(df)} distribution centers")
        
    except Exception as e:
        print(f"Error loading distribution centers: {e}")
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
        
        # Load distribution centers first (small file)
        distribution_centers_file = os.path.join(data_dir, "distribution_centers.csv")
        if os.path.exists(distribution_centers_file):
            load_distribution_centers(distribution_centers_file, db)
        else:
            print(f"Distribution centers file not found at {distribution_centers_file}")
        
        # Load products
        products_file = os.path.join(data_dir, "products.csv")
        if os.path.exists(products_file):
            load_products(products_file, db)
        else:
            print(f"Products file not found at {products_file}")
        
        # Load users
        users_file = os.path.join(data_dir, "users.csv")
        if os.path.exists(users_file):
            load_users(users_file, db)
        else:
            print(f"Users file not found at {users_file}")
        
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
        
        # Load inventory items
        inventory_items_file = os.path.join(data_dir, "inventory_items.csv")
        if os.path.exists(inventory_items_file):
            load_inventory_items(inventory_items_file, db)
        else:
            print(f"Inventory items file not found at {inventory_items_file}")
        
        print("Data loading completed successfully!")
        
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main() 