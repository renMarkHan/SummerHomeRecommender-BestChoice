from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
import logging
from dotenv import load_dotenv

# Import user creation function
from user import create_user

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(title="Vacation Rentals API", version="1.0.0")

# 添加CORS中间件以支持前端跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
# 这样前端文件就可以通过 FastAPI 服务访问
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    logger.info("Static files directory mounted to /static")
except Exception as e:
    logger.warning(f"Static files directory mount failed: {e}")

# Get API key with better error handling
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    logger.error("OPENROUTER_API_KEY environment variable is not set!")
    logger.error("Please create a .env file with your OpenRouter API key")
    logger.error("Example: OPENROUTER_API_KEY=your_api_key_here")

class Query(BaseModel):
    message: str

class UserProfile(BaseModel):
    name: str
    weighed_location: int = 1
    weighed_type: int = 1
    weighed_features: int = 1
    weighed_price: int = 1

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Vacation Rentals API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

@app.post("/chat")
async def chat(query: Query):
    """Chat endpoint with OpenRouter integration"""
    try:
        # Check if API key is configured
        if not API_KEY:
            raise HTTPException(
                status_code=500, 
                detail="OpenRouter API key not configured. Please set OPENROUTER_API_KEY environment variable."
            )
        
        logger.info(f"Received chat request: {query.message}")
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "tngtech/deepseek-r1t2-chimera:free",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query.message}
            ]
        }
        
        logger.info(f"Making request to OpenRouter API...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        # Log response details for debugging
        logger.info(f"OpenRouter API response status: {response.status_code}")
        
        if response.status_code != 200:
            logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
            raise HTTPException(
                status_code=response.status_code,
                detail=f"OpenRouter API error: {response.text}"
            )
        
        result = response.json()
        logger.info("Successfully received response from OpenRouter API")
        
        return {"reply": result["choices"][0]["message"]["content"]}
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
    except KeyError as e:
        logger.error(f"Response parsing error: {e}")
        raise HTTPException(status_code=500, detail=f"Invalid response format: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/create_user")
async def create_user_endpoint(user_profile: UserProfile):
    """Create a new user profile with weighted preferences"""
    try:
        logger.info(f"Creating user profile: {user_profile.name}")
        
        # Validate weight values
        weights = [user_profile.weighed_location, user_profile.weighed_type, 
                  user_profile.weighed_features, user_profile.weighed_price]
        
        for weight in weights:
            if weight < 1 or weight > 10:
                raise HTTPException(
                    status_code=400, 
                    detail="Weight values must be between 1 and 10"
                )
        
        # Create user in database
        user_id = create_user(
            name=user_profile.name,
            weighed_location=user_profile.weighed_location,
            weighed_type=user_profile.weighed_type,
            weighed_features=user_profile.weighed_features,
            weighed_price=user_profile.weighed_price
        )
        
        logger.info(f"User created successfully with ID: {user_id}")
        
        return {
            "message": "User profile created successfully",
            "user_id": user_id,
            "name": user_profile.name,
            "weights": {
                "location": user_profile.weighed_location,
                "type": user_profile.weighed_type,
                "features": user_profile.weighed_features,
                "price": user_profile.weighed_price
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled exception: {exc}")
    return {"error": "Internal server error", "detail": str(exc)}

# 添加前端页面路由
@app.get("/frontend")
async def serve_frontend():
    """Serve the frontend page"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            content = f.read()
        return {"html": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Frontend page not found")
    except Exception as e:
        logger.error(f"Error serving frontend: {e}")
        raise HTTPException(status_code=500, detail="Error serving frontend")
