import os
import groq
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama3-8b-8192"  # Using Llama3 model
    
    def generate_response(self, user_message: str, context: Dict[str, Any] = None) -> str:
        """Generate AI response using Groq API"""
        
        # Build the system prompt
        system_prompt = """You are a helpful customer support chatbot for an e-commerce clothing website. 
        You can help customers with:
        - Product information and availability
        - Order status and tracking
        - Stock levels
        - General customer service questions
        
        Always be polite, helpful, and provide accurate information based on the available data.
        If you don't have enough information to answer a question, ask for clarification."""
        
        # Build the user prompt with context
        user_prompt = f"User message: {user_message}"
        
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
            user_prompt += f"\n\nAvailable context:\n{context_str}"
        
        try:
            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=500
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again later."
    
    def extract_intent(self, message: str) -> Dict[str, Any]:
        """Extract intent and entities from user message"""
        intent_prompt = f"""
        Analyze the following customer message and extract the intent and relevant information:
        
        Message: "{message}"
        
        Return a JSON object with:
        - intent: "product_query", "order_status", "stock_check", "general_help"
        - entities: relevant information like product names, order IDs, etc.
        - requires_clarification: boolean indicating if more info is needed
        """
        
        try:
            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an intent classification system. Return only valid JSON."},
                    {"role": "user", "content": intent_prompt}
                ],
                model=self.model,
                temperature=0.1,
                max_tokens=200
            )
            
            # Parse the response (this is a simplified version)
            response = completion.choices[0].message.content
            
            # Simple intent extraction (in a real system, you'd use proper NLP)
            message_lower = message.lower()
            
            if any(word in message_lower for word in ["order", "status", "tracking"]):
                intent = "order_status"
            elif any(word in message_lower for word in ["stock", "available", "quantity"]):
                intent = "stock_check"
            elif any(word in message_lower for word in ["product", "item", "clothing"]):
                intent = "product_query"
            else:
                intent = "general_help"
            
            return {
                "intent": intent,
                "entities": {},
                "requires_clarification": False
            }
            
        except Exception as e:
            print(f"Error extracting intent: {e}")
            return {
                "intent": "general_help",
                "entities": {},
                "requires_clarification": False
            } 