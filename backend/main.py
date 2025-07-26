from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
import os

from database import get_db, create_tables, Conversation
from models import ChatRequest, ChatResponse, ProductResponse, OrderResponse
from llm_service import LLMService
from business_logic import BusinessLogicService

app = FastAPI(title="E-commerce Chatbot API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM service
llm_service = LLMService()

@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    create_tables()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "E-commerce Chatbot API is running!"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """Main chat endpoint"""
    try:
        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Initialize business logic service
        business_logic = BusinessLogicService(db)
        
        # Extract intent and entities
        intent_info = llm_service.extract_intent(request.message)
        intent = intent_info.get("intent", "general_help")
        
        # Build context based on intent
        context = {}
        
        if intent == "order_status":
            order_id = business_logic.extract_order_id(request.message)
            if order_id:
                order_info = business_logic.get_order_status(order_id)
                if "error" not in order_info:
                    context["order_info"] = order_info
                else:
                    context["order_error"] = order_info["error"]
        
        elif intent == "stock_check":
            product_name = business_logic.extract_product_name(request.message)
            if product_name:
                stock_info = business_logic.get_product_stock(product_name=product_name)
                if "error" not in stock_info:
                    context["stock_info"] = stock_info
                else:
                    context["stock_error"] = stock_info["error"]
        
        elif intent == "product_query":
            # Check for top products query
            if "top" in request.message.lower() and ("product" in request.message.lower() or "sold" in request.message.lower()):
                top_products = business_logic.get_top_products(5)
                context["top_products"] = top_products
            else:
                # Search for specific products
                products = business_logic.search_products(request.message)
                context["products"] = products
        
        # Generate AI response
        ai_response = llm_service.generate_response(request.message, context)
        
        # Save conversation to database
        conversation = Conversation(
            conversation_id=conversation_id,
            user_message=request.message,
            ai_response=ai_response
        )
        db.add(conversation)
        db.commit()
        
        return ChatResponse(
            response=ai_response,
            conversation_id=conversation_id,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/products", response_model=list[ProductResponse])
async def get_products(db: Session = Depends(get_db)):
    """Get all products"""
    try:
        from database import Product
        products = db.query(Product).limit(100).all()  # Limit to prevent overwhelming response
        return [
            ProductResponse(
                product_id=str(product.id),
                product_name=product.name,
                category=product.category,
                price=product.retail_price,
                stock_quantity=0,  # Will be calculated dynamically
                description=f"{product.brand} - {product.department}"
            )
            for product in products
        ]
    except Exception as e:
        print(f"Error getting products: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve products")

@app.get("/api/products/top")
async def get_top_products(limit: int = 5, db: Session = Depends(get_db)):
    """Get top selling products"""
    try:
        business_logic = BusinessLogicService(db)
        products = business_logic.get_top_products(limit)
        return {"products": products}
    except Exception as e:
        print(f"Error getting top products: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve top products")

@app.get("/api/orders/{order_id}")
async def get_order_status(order_id: str, db: Session = Depends(get_db)):
    """Get order status by order ID"""
    try:
        business_logic = BusinessLogicService(db)
        order_info = business_logic.get_order_status(order_id)
        return order_info
    except Exception as e:
        print(f"Error getting order status: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve order information")

@app.get("/api/products/stock/{product_name}")
async def get_product_stock(product_name: str, db: Session = Depends(get_db)):
    """Get stock information for a product"""
    try:
        business_logic = BusinessLogicService(db)
        stock_info = business_logic.get_product_stock(product_name=product_name)
        return stock_info
    except Exception as e:
        print(f"Error getting product stock: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve product information")

@app.get("/api/analytics/sales")
async def get_sales_analytics(db: Session = Depends(get_db)):
    """Get sales analytics"""
    try:
        business_logic = BusinessLogicService(db)
        analytics = business_logic.get_sales_analytics()
        return analytics
    except Exception as e:
        print(f"Error getting sales analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve analytics")

@app.get("/api/products/low-stock")
async def get_low_stock_products(threshold: int = 10, db: Session = Depends(get_db)):
    """Get products with low stock"""
    try:
        business_logic = BusinessLogicService(db)
        products = business_logic.get_low_stock_products(threshold)
        return {"products": products}
    except Exception as e:
        print(f"Error getting low stock products: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve low stock products")

@app.get("/api/conversations")
async def get_conversations(db: Session = Depends(get_db)):
    """Get recent conversations"""
    try:
        conversations = db.query(Conversation).order_by(Conversation.created_at.desc()).limit(50).all()
        return [
            {
                "id": conv.id,
                "conversation_id": conv.conversation_id,
                "user_message": conv.user_message,
                "ai_response": conv.ai_response,
                "created_at": conv.created_at
            }
            for conv in conversations
        ]
    except Exception as e:
        print(f"Error getting conversations: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve conversations")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 