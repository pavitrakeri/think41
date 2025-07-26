from sqlalchemy.orm import Session
from database import Product, Order, OrderItem
from typing import List, Dict, Any
import re

class BusinessLogicService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_top_products(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top selling products based on order quantity"""
        try:
            # Query to get products with their total sold quantities
            result = self.db.query(
                Product.product_id,
                Product.product_name,
                Product.category,
                Product.price,
                Product.stock_quantity,
                Product.description
            ).join(OrderItem, Product.product_id == OrderItem.product_id)\
             .group_by(Product.product_id)\
             .order_by(OrderItem.quantity.desc())\
             .limit(limit)\
             .all()
            
            return [
                {
                    "product_id": row.product_id,
                    "product_name": row.product_name,
                    "category": row.category,
                    "price": row.price,
                    "stock_quantity": row.stock_quantity,
                    "description": row.description
                }
                for row in result
            ]
        except Exception as e:
            print(f"Error getting top products: {e}")
            return []
    
    def get_order_status(self, order_id: str) -> Dict[str, Any]:
        """Get order status by order ID"""
        try:
            order = self.db.query(Order).filter(Order.order_id == order_id).first()
            
            if not order:
                return {"error": "Order not found"}
            
            # Get order items
            order_items = self.db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
            
            return {
                "order_id": order.order_id,
                "customer_id": order.customer_id,
                "order_date": order.order_date,
                "status": order.status,
                "total_amount": order.total_amount,
                "items": [
                    {
                        "product_id": item.product_id,
                        "quantity": item.quantity,
                        "price": item.price
                    }
                    for item in order_items
                ]
            }
        except Exception as e:
            print(f"Error getting order status: {e}")
            return {"error": "Failed to retrieve order information"}
    
    def get_product_stock(self, product_name: str = None, product_id: str = None) -> Dict[str, Any]:
        """Get stock information for a product"""
        try:
            query = self.db.query(Product)
            
            if product_id:
                product = query.filter(Product.product_id == product_id).first()
            elif product_name:
                # Case-insensitive search
                product = query.filter(Product.product_name.ilike(f"%{product_name}%")).first()
            else:
                return {"error": "Product name or ID required"}
            
            if not product:
                return {"error": "Product not found"}
            
            return {
                "product_id": product.product_id,
                "product_name": product.product_name,
                "category": product.category,
                "price": product.price,
                "stock_quantity": product.stock_quantity,
                "description": product.description
            }
        except Exception as e:
            print(f"Error getting product stock: {e}")
            return {"error": "Failed to retrieve product information"}
    
    def search_products(self, query: str) -> List[Dict[str, Any]]:
        """Search products by name or category"""
        try:
            products = self.db.query(Product).filter(
                (Product.product_name.ilike(f"%{query}%")) |
                (Product.category.ilike(f"%{query}%"))
            ).limit(10).all()
            
            return [
                {
                    "product_id": product.product_id,
                    "product_name": product.product_name,
                    "category": product.category,
                    "price": product.price,
                    "stock_quantity": product.stock_quantity,
                    "description": product.description
                }
                for product in products
            ]
        except Exception as e:
            print(f"Error searching products: {e}")
            return []
    
    def get_low_stock_products(self, threshold: int = 10) -> List[Dict[str, Any]]:
        """Get products with low stock"""
        try:
            products = self.db.query(Product).filter(Product.stock_quantity <= threshold).all()
            
            return [
                {
                    "product_id": product.product_id,
                    "product_name": product.product_name,
                    "category": product.category,
                    "price": product.price,
                    "stock_quantity": product.stock_quantity,
                    "description": product.description
                }
                for product in products
            ]
        except Exception as e:
            print(f"Error getting low stock products: {e}")
            return []
    
    def extract_order_id(self, message: str) -> str:
        """Extract order ID from message"""
        # Look for patterns like "order 12345" or "order ID 12345"
        patterns = [
            r'order\s+(?:id\s+)?(\d+)',
            r'order\s+#(\d+)',
            r'(\d{5,})'  # 5+ digit number
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message.lower())
            if match:
                return match.group(1)
        
        return None
    
    def extract_product_name(self, message: str) -> str:
        """Extract product name from message"""
        # Common clothing terms
        clothing_terms = [
            't-shirt', 'tshirt', 'shirt', 'pants', 'jeans', 'dress', 'skirt',
            'jacket', 'hoodie', 'sweater', 'sweatshirt', 'shorts', 'blouse'
        ]
        
        message_lower = message.lower()
        
        for term in clothing_terms:
            if term in message_lower:
                return term
        
        return None 