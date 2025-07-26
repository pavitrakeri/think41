# E-commerce Chatbot Backend

A FastAPI-based backend service for an intelligent customer support chatbot for an e-commerce clothing website.

## Features

- **Intelligent Chat Interface**: Powered by Groq's LLM API
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **Business Logic**: Product queries, order tracking, stock management
- **RESTful API**: Complete API endpoints for all functionality
- **Conversation History**: Persistent chat history storage

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **LLM**: Groq API (Llama3 model)
- **Data Processing**: Pandas

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Database Setup

1. Install PostgreSQL on your system
2. Create a database named `ecommerce_chatbot`
3. Update the `DATABASE_URL` in your environment variables

### 3. Environment Configuration

Copy `env_example.txt` to `.env` and update the values:

```bash
cp env_example.txt .env
```

Required environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `GROQ_API_KEY`: Your Groq API key (get from console.groq.com)

### 4. Data Loading

Place your CSV files in a `data/` directory:
- `products.csv`
- `orders.csv`
- `order_items.csv`

Run the data loading script:

```bash
python load_data.py
```

### 5. Start the Server

```bash
python main.py
```

Or using uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Chat Endpoint
- **POST** `/api/chat` - Main chat interface

### Product Endpoints
- **GET** `/api/products` - Get all products
- **GET** `/api/products/top` - Get top selling products
- **GET** `/api/products/stock/{product_name}` - Get stock for specific product

### Order Endpoints
- **GET** `/api/orders/{order_id}` - Get order status

### Conversation Endpoints
- **GET** `/api/conversations` - Get recent conversations

## Example Usage

### Chat with the bot:
```bash
curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "What are the top 5 most sold products?"}'
```

### Check order status:
```bash
curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Show me the status of order ID 12345"}'
```

### Check product stock:
```bash
curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "How many Classic T-Shirts are left in stock?"}'
```

## Database Schema

### Products Table
- `id`: Primary key
- `product_id`: Unique product identifier
- `product_name`: Product name
- `category`: Product category
- `price`: Product price
- `stock_quantity`: Available stock
- `description`: Product description

### Orders Table
- `id`: Primary key
- `order_id`: Unique order identifier
- `customer_id`: Customer identifier
- `order_date`: Order date
- `status`: Order status
- `total_amount`: Order total

### Order Items Table
- `id`: Primary key
- `order_id`: Foreign key to orders
- `product_id`: Foreign key to products
- `quantity`: Item quantity
- `price`: Item price

### Conversations Table
- `id`: Primary key
- `conversation_id`: Unique conversation identifier
- `user_message`: User's message
- `ai_response`: AI's response
- `created_at`: Timestamp

## Development

The backend is structured with the following components:

- **`main.py`**: FastAPI application and endpoints
- **`database.py`**: Database models and configuration
- **`models.py`**: Pydantic models for API schemas
- **`llm_service.py`**: Groq API integration
- **`business_logic.py`**: Business logic and database queries
- **`load_data.py`**: Data ingestion script

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc 