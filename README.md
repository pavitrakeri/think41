# E-commerce Customer Support Chatbot

A full-stack intelligent customer support chatbot for an e-commerce clothing website. Built with FastAPI backend, React frontend, PostgreSQL database, and powered by Groq's LLM API.

## 🚀 Features

- **Intelligent Chat Interface**: Powered by Groq's LLM API with Llama3 model
- **Product Management**: Query products, check stock levels, view top sellers
- **Order Tracking**: Check order status and tracking information
- **Real-time Chat**: Modern React frontend with real-time messaging
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **Containerized**: Full Docker support with Docker Compose
- **RESTful API**: Complete FastAPI backend with automatic documentation

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **LLM**: Groq API (Llama3-8b-8192)
- **Data Processing**: Pandas

### Frontend
- **Framework**: React 18
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **Markdown**: React Markdown

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL 15

## 📋 Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)
- Groq API key (get from [console.groq.com](https://console.groq.com))

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/pavitrakeri/think41.git
cd think41
```

### 2. Environment Setup

Create a `.env` file in the root directory:

```bash
# Copy the example environment file
cp backend/env_example.txt .env

# Edit the file and add your Groq API key
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Data Setup

Place your CSV files in the `backend/data/` directory:
- `products.csv`
- `orders.csv`
- `order_items.csv`

### 4. Start the Application

```bash
# Start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432

## 📁 Project Structure

```
think41/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database models and configuration
│   ├── models.py            # Pydantic models
│   ├── llm_service.py       # Groq API integration
│   ├── business_logic.py    # Business logic and queries
│   ├── load_data.py         # Data ingestion script
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile          # Backend container
│   └── README.md           # Backend documentation
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.js          # Main app component
│   │   └── index.js        # Entry point
│   ├── package.json        # Node.js dependencies
│   ├── Dockerfile          # Frontend container
│   └── tailwind.config.js  # Tailwind configuration
├── docker-compose.yml      # Service orchestration
└── README.md              # Project documentation
```

## 🔧 Development Setup

### Backend Development

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp env_example.txt .env
# Edit .env with your configuration

# Run the application
python main.py
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## 📊 API Endpoints

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

## 💬 Example Conversations

### Product Queries
```
User: "What are the top 5 most sold products?"
Bot: "Based on our sales data, here are the top 5 most sold products..."

User: "How many Classic T-Shirts are left in stock?"
Bot: "I found that Classic T-Shirts currently have 25 units in stock..."
```

### Order Tracking
```
User: "Show me the status of order ID 12345"
Bot: "Order ID 12345 is currently 'Shipped' and was placed on..."
```

### General Support
```
User: "What can you help me with?"
Bot: "I can help you with product information, order tracking, stock levels..."
```

## 🐳 Docker Commands

```bash
# Build and start all services
docker-compose up --build

# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## 🔍 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL container is running
   - Check database credentials in environment variables

2. **API Key Error**
   - Verify your Groq API key is set correctly
   - Check the `.env` file configuration

3. **Frontend Not Loading**
   - Ensure backend is running on port 8000
   - Check proxy configuration in package.json

4. **Data Loading Issues**
   - Verify CSV files are in the correct format
   - Check file permissions in the data directory

### Logs

```bash
# Backend logs
docker-compose logs backend

# Frontend logs
docker-compose logs frontend

# Database logs
docker-compose logs postgres
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for providing the LLM API
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [React](https://reactjs.org/) for the frontend framework
- [Tailwind CSS](https://tailwindcss.com/) for styling

## 📞 Support

For support and questions, please open an issue in the GitHub repository. 