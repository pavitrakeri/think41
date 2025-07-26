from sqlalchemy.orm import Session
from database import Product, Order, OrderItem, User, InventoryItem
from typing import List, Dict, Any
import re
from sqlalchemy import func, desc

class BusinessLogicService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_top_products(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top selling products based on order quantity"""
        try:
            # Query to get products with their total sold quantities
            result = self.db.query(
                Product.id,
                Product.name,
                Product.category,
                Product.brand,
                Product.retail_price,
                Product.department,
                func.count(OrderItem.id).label('total_orders'),
                func.sum(OrderItem.sale_price).label('total_revenue')
            ).join(OrderItem, Product.id == OrderItem.product_id)\
             .filter(OrderItem.status == 'Complete')\
             .group_by(Product.id)\
             .order_by(desc('total_orders'))\
             .limit(limit)\
             .all()
            
            return [
                {
                    "product_id": row.id,
                    "product_name": row.name,
                    "category": row.category,
                    "brand": row.brand,
                    "retail_price": row.retail_price,
                    "department": row.department,
                    "total_orders": row.total_orders,
                    "total_revenue": row.total_revenue
                }
                for row in result
            ]
        except Exception as e:
            print(f"Error getting top products: {e}")
            return []
    
    def get_order_status(self, order_id: str) -> Dict[str, Any]:
        """Get order status by order ID"""
        try:
            order = self.db.query(Order).filter(Order.order_id == int(order_id)).first()
            
            if not order:
                return {"error": "Order not found"}
            
            # Get order items
            order_items = self.db.query(OrderItem).filter(OrderItem.order_id == int(order_id)).all()
            
            # Get user information
            user = self.db.query(User).filter(User.id == order.user_id).first()
            
            return {
                "order_id": order.order_id,
                "user_id": order.user_id,
                "user_name": f"{user.first_name} {user.last_name}" if user else "Unknown",
                "status": order.status,
                "created_at": order.created_at,
                "shipped_at": order.shipped_at,
                "delivered_at": order.delivered_at,
                "returned_at": order.returned_at,
                "num_of_items": order.num_of_item,
                "items": [
                    {
                        "product_id": item.product_id,
                        "status": item.status,
                        "sale_price": item.sale_price,
                        "created_at": item.created_at,
                        "shipped_at": item.shipped_at,
                        "delivered_at": item.delivered_at
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
                product = query.filter(Product.id == int(product_id)).first()
            elif product_name:
                # Case-insensitive search
                product = query.filter(Product.name.ilike(f"%{product_name}%")).first()
            else:
                return {"error": "Product name or ID required"}
            
            if not product:
                return {"error": "Product not found"}
            
            # Get inventory information
            inventory_count = self.db.query(InventoryItem).filter(
                InventoryItem.product_id == product.id,
                InventoryItem.sold_at.is_(None)
            ).count()
            
            return {
                "product_id": product.id,
                "product_name": product.name,
                "category": product.category,
                "brand": product.brand,
                "retail_price": product.retail_price,
                "department": product.department,
                "available_stock": inventory_count,
                "sku": product.sku
            }
        except Exception as e:
            print(f"Error getting product stock: {e}")
            return {"error": "Failed to retrieve product information"}
    
    def search_products(self, query: str) -> List[Dict[str, Any]]:
        """Search products by name, category, or brand"""
        try:
            products = self.db.query(Product).filter(
                (Product.name.ilike(f"%{query}%")) |
                (Product.category.ilike(f"%{query}%")) |
                (Product.brand.ilike(f"%{query}%"))
            ).limit(10).all()
            
            return [
                {
                    "product_id": product.id,
                    "product_name": product.name,
                    "category": product.category,
                    "brand": product.brand,
                    "retail_price": product.retail_price,
                    "department": product.department,
                    "sku": product.sku
                }
                for product in products
            ]
        except Exception as e:
            print(f"Error searching products: {e}")
            return []
    
    def get_low_stock_products(self, threshold: int = 10) -> List[Dict[str, Any]]:
        """Get products with low stock"""
        try:
            # Get products with low available inventory
            result = self.db.query(
                Product.id,
                Product.name,
                Product.category,
                Product.brand,
                Product.retail_price,
                func.count(InventoryItem.id).label('available_stock')
            ).join(InventoryItem, Product.id == InventoryItem.product_id)\
             .filter(InventoryItem.sold_at.is_(None))\
             .group_by(Product.id)\
             .having(func.count(InventoryItem.id) <= threshold)\
             .all()
            
            return [
                {
                    "product_id": row.id,
                    "product_name": row.name,
                    "category": row.category,
                    "brand": row.brand,
                    "retail_price": row.retail_price,
                    "available_stock": row.available_stock
                }
                for row in result
            ]
        except Exception as e:
            print(f"Error getting low stock products: {e}")
            return []
    
    def get_sales_analytics(self) -> Dict[str, Any]:
        """Get sales analytics"""
        try:
            # Total revenue
            total_revenue = self.db.query(func.sum(OrderItem.sale_price))\
                .filter(OrderItem.status == 'Complete').scalar() or 0
            
            # Total orders
            total_orders = self.db.query(func.count(Order.id)).scalar() or 0
            
            # Completed orders
            completed_orders = self.db.query(func.count(Order.id))\
                .filter(Order.status == 'Complete').scalar() or 0
            
            # Top category
            top_category = self.db.query(
                Product.category,
                func.count(OrderItem.id).label('order_count')
            ).join(OrderItem, Product.id == OrderItem.product_id)\
             .filter(OrderItem.status == 'Complete')\
             .group_by(Product.category)\
             .order_by(desc('order_count'))\
             .first()
            
            return {
                "total_revenue": total_revenue,
                "total_orders": total_orders,
                "completed_orders": completed_orders,
                "completion_rate": (completed_orders / total_orders * 100) if total_orders > 0 else 0,
                "top_category": top_category.category if top_category else "N/A",
                "top_category_orders": top_category.order_count if top_category else 0
            }
        except Exception as e:
            print(f"Error getting sales analytics: {e}")
            return {}
    
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
            'jacket', 'hoodie', 'sweater', 'sweatshirt', 'shorts', 'blouse',
            'cap', 'hat', 'accessories', 'shoes', 'sneakers', 'boots'
        ]
        
        message_lower = message.lower()
        
        for term in clothing_terms:
            if term in message_lower:
                return term
        
        return None 