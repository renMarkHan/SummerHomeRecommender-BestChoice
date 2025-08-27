from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import os
import requests
import logging
import shutil
import json
import re
from pathlib import Path
from dotenv import load_dotenv

# Import user creation function and database functions
from user import create_user
from database import get_all_properties, get_connection
from property import get_property
from vectorized_filter import create_vectorized_filter

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(title="Vacation Rentals API", version="1.0.0")

# Add CORS middleware to support frontend cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, this should be restricted to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
# This allows frontend files to be accessed through the FastAPI service
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

class FilterParams(BaseModel):
    budget_range: Optional[List[float]] = None
    features: Optional[List[str]] = None
    property_types: Optional[List[str]] = None
    locations: Optional[List[str]] = None
    case_sensitive: bool = False

class LocationSearchParams(BaseModel):
    query: str
    radius_km: int = 20

@app.get("/")
async def root():
    """Serve the frontend index.html file"""
    return FileResponse("static/index.html")

@app.get("/login")
async def login_page():
    """Serve the login HTML page."""
    return FileResponse("static/login.html")

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

@app.get("/api/properties")
async def get_properties():
    """Get all properties from database"""
    try:
        properties = get_all_properties()
        # Convert Property objects to dictionaries for JSON serialization
        properties_data = []
        for prop in properties:
            prop_dict = {
                "property_id": prop.property_id,
                "location": prop.location,
                "type": prop.ptype,
                "nightly_price": prop.nightly_price,
                "features": ",".join(prop.features) if prop.features else "",
                "tags": ",".join(prop.tags) if prop.tags else "",
                "image_url": prop.image_url,
                "image_alt": prop.image_alt
            }
            properties_data.append(prop_dict)
        
        logger.info(f"Retrieved {len(properties_data)} properties from database")
        return {"properties": properties_data, "count": len(properties_data)}
        
    except Exception as e:
        logger.error(f"Error retrieving properties: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve properties: {str(e)}")

@app.get("/api/properties/{property_id}")
async def get_property_by_id(property_id: int):
    """Get a specific property by ID"""
    try:
        property_data = get_property(property_id)
        if not property_data:
            raise HTTPException(status_code=404, detail="Property not found")
        
        # Convert database row to Property object
        from property import Property
        prop = Property(
            property_id=property_data[0],
            location=property_data[1],
            ptype=property_data[2],
            nightly_price=property_data[3],
            features=property_data[4].split(",") if property_data[4] else [],
            tags=property_data[5].split(",") if property_data[5] else [],
            image_url=property_data[6] if len(property_data) > 6 else None,
            image_alt=property_data[7] if len(property_data) > 7 else None
        )
        
        # Convert to dictionary
        prop_dict = {
            "property_id": prop.property_id,
            "location": prop.location,
            "type": prop.ptype,
            "nightly_price": prop.nightly_price,
            "features": ",".join(prop.features) if prop.features else "",
            "tags": ",".join(prop.tags) if prop.tags else "",
            "image_url": prop.image_url,
            "image_alt": prop.image_alt
        }
        
        return prop_dict
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving property {property_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve property: {str(e)}")

@app.post("/chat")
async def chat(query: Query):
    """Chat endpoint with OpenRouter integration and smart property generation"""
    try:
        # Check if API key is configured
        if not API_KEY:
            raise HTTPException(
                status_code=500, 
                detail="OpenRouter API key not configured. Please set OPENROUTER_API_KEY environment variable."
            )
        
        logger.info(f"Received chat request: {query.message}")
        
        # Smart detection: Check if user wants to generate property data or travel planning
        user_message = query.message.lower()
        
        # Check for property generation
        is_property_generation = any(keyword in user_message for keyword in [
            "generate", "json", "data", "property", "generate", "random", "sample"
        ])
        
        # Check for travel planning
        is_travel_planning = any(keyword in user_message for keyword in [
            "travel", "plan", "planning", "trip", "vacation", "weekend", "holiday",
            "travel", "plan", "planning", "weekend", "holiday", "vacation"
        ])
        
        if is_property_generation:
            logger.info("Detected property generation request, using specialized logic")
            return await generate_property_json()
        elif is_travel_planning:
            logger.info("Detected travel planning request, using specialized logic")
            return await handle_travel_planning_request(query.message)
        else:
            logger.info("Using normal chat response")
            return await normal_chat_response(query.message)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

async def normal_chat_response(user_message: str):
    """Normal chat response using OpenRouter API"""
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "tngtech/deepseek-r1t2-chimera:free",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
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
        
        # Parse response
        try:
            response_data = response.json()
            ai_message = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            if not ai_message:
                raise ValueError("No AI message content in response")
            
            logger.info(f"AI response generated successfully")
            return {"response": ai_message}
            
        except (KeyError, ValueError, IndexError) as e:
            logger.error(f"Failed to parse OpenRouter API response: {e}")
            logger.error(f"Response content: {response.text}")
            raise HTTPException(
                status_code=500,
                detail="Failed to parse AI response"
            )
            
    except HTTPException:
        raise
    except requests.exceptions.Timeout:
        logger.error("OpenRouter API request timed out")
        raise HTTPException(
            status_code=408,
            detail="AI service request timed out. Please try again."
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"OpenRouter API request failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"AI service request failed: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error in normal chat: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

async def generate_property_json():
    """Generate property JSON data using AI + template fallback"""
    try:
        logger.info("Generating property JSON data...")
        
        # Try AI generation first
        ai_response = await generate_property_with_ai()
        
        if ai_response:
            # Validate and clean the AI response
            cleaned_json = validate_and_clean_json(ai_response)
            if cleaned_json:
                logger.info("AI-generated JSON is valid, returning...")
                return {"response": json.dumps(cleaned_json, indent=2, ensure_ascii=False)}
        
        # Fallback to template generation if AI fails
        logger.info("AI generation failed, using template fallback...")
        template_data = generate_template_property_data()
        return {"response": json.dumps(template_data, indent=2, ensure_ascii=False)}
        
    except Exception as e:
        logger.error(f"Error in generate_property_json: {e}")
        # Final fallback
        template_data = generate_template_property_data()
        return {"response": json.dumps(template_data, indent=2, ensure_ascii=False)}

# ===== Travel Planning Functions =====

async def handle_travel_planning_request(user_message: str):
    """Handle travel planning request - simplified version, asks one question at a time"""
    try:
        logger.info(f"Handling travel planning request: {user_message}")
        
        # Create new travel planning session
        from travel_planning import TravelPlanningSession, generate_next_question_with_ai
        session = TravelPlanningSession()
        
        # Generate first question
        first_question = await generate_next_question_with_ai(session)
        
        # Store session
        global travel_sessions
        travel_sessions[session.session_id] = session
        
        # Record conversation
        session.add_conversation_entry(user_message, first_question)
        
        return {
            "response": first_question,
            "session_id": session.session_id,
            "current_step": session.current_step,
            "completion_percentage": session.get_completion_percentage()
        }
        
    except Exception as e:
        logger.error(f"Travel planning request handling failed: {e}")
        return {
            "response": "Sorry, I encountered an issue while processing your travel planning request. Please try again later.",
            "error": str(e)
        }

@app.post("/api/update_user_weights")
async def update_user_weights_endpoint(weights_data: dict):
    """Update user's weighted preferences"""
    try:
        user_id = weights_data.get("user_id")
        weighed_location = weights_data.get("weighed_location")
        weighed_type = weights_data.get("weighed_type")
        weighed_features = weights_data.get("weighed_features")
        weighed_price = weights_data.get("weighed_price")
        
        # Validate weight values (1-10 range)
        weights = [weighed_location, weighed_type, weighed_features, weighed_price]
        for weight in weights:
            if weight is not None and (weight < 1 or weight > 10):
                raise HTTPException(
                    status_code=400,
                    detail="Weight values must be between 1 and 10"
                )
        
        # Update user weights in database
        from user import update_user_weights
        update_user_weights(
            user_id=user_id,
            weighed_location=weighed_location,
            weighed_type=weighed_type,
            weighed_features=weighed_features,
            weighed_price=weighed_price
        )
        
        logger.info(f"User {user_id} weights updated successfully")
        return {"success": True, "message": "User weights updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user weights: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update user weights: {str(e)}")

@app.post("/create_user")
async def create_user_endpoint(user_profile: UserProfile):
    """Create a new user profile with weighted preferences"""
    try:
        # Validate weight values (1-10 range)
        weights = [
            user_profile.weighed_location,
            user_profile.weighed_type,
            user_profile.weighed_features,
            user_profile.weighed_price
        ]
        
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
        
        logger.info(f"User profile created successfully with ID: {user_id}")
        return {
            "message": "User profile created successfully",
            "user_id": user_id,
            "name": user_profile.name
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating user profile: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create user profile: {str(e)}"
        )

@app.post("/api/smart_match")
async def smart_match_endpoint(smart_match_params: dict):
    """Smart Match endpoint using weighted scoring system"""
    try:
        # Get all properties
        properties = get_all_properties()
        
        # Convert to DataFrame
        properties_data = []
        for prop in properties:
            prop_dict = {
                "property_id": prop.property_id,
                "location": prop.location,
                "ptype": prop.ptype,
                "nightly_price": prop.nightly_price,
                "features": prop.features if prop.features else [],
                "tags": prop.tags if prop.tags else [],
                "image_url": prop.image_url,
                "image_alt": prop.image_alt,
                "latitude": prop.latitude,
                "longitude": prop.longitude
            }
            properties_data.append(prop_dict)
        
        # Create DataFrame
        import pandas as pd
        properties_df = pd.DataFrame(properties_data)
        
        # Import Smart Match engine
        from smart_match_engine import smart_match_engine
        
        # Execute Smart Match
        result_df = smart_match_engine.calculate_total_scores(
            properties_df=properties_df,
            selected_types=smart_match_params.get("selected_types", []),
            selected_features=smart_match_params.get("selected_features", []),
            center_location=smart_match_params.get("center_location", "Toronto"),
            radius=smart_match_params.get("radius", 50),
            min_budget=smart_match_params.get("min_budget", 0),
            max_budget=smart_match_params.get("max_budget", 1000),
            location_weight=smart_match_params.get("location_weight", 1),
            type_weight=smart_match_params.get("type_weight", 1),
            features_weight=smart_match_params.get("features_weight", 1),
            price_weight=smart_match_params.get("price_weight", 1)
        )
        
        if result_df.empty:
            return {"properties": [], "count": 0, "message": "No properties found matching criteria"}
        
        # Convert to list of dictionaries
        result_properties = result_df.to_dict('records')
        
        logger.info(f"Smart Match completed: {len(result_properties)} properties found")
        
        return {
            "properties": result_properties,
            "count": len(result_properties),
            "message": "Smart Match completed successfully"
        }
        
    except Exception as e:
        logger.error(f"Smart Match failed: {e}")
        raise HTTPException(status_code=500, detail=f"Smart Match failed: {str(e)}")

@app.post("/api/filter_properties")
async def filter_properties(filter_params: FilterParams):
    """Filter properties using vectorized operations"""
    try:
        # Get all properties from database
        properties = get_all_properties()
        
        # Convert Property objects to dictionaries for filtering
        properties_data = []
        for prop in properties:
            prop_dict = {
                "property_id": prop.property_id,
                "location": prop.location,
                "ptype": prop.ptype,
                "nightly_price": prop.nightly_price,
                "features": prop.features if prop.features else [],
                "tags": prop.tags if prop.tags else [],
                "image_url": prop.image_url,
                "image_alt": prop.image_alt
            }
            properties_data.append(prop_dict)
        
        # Create vectorized filter instance
        filter_instance = create_vectorized_filter(properties_data)
        
        # Apply filters
        filtered_df = filter_instance.apply_combined_filters(
            budget_range=filter_params.budget_range,
            features=filter_params.features,
            property_types=filter_params.property_types,
            locations=filter_params.locations,
            case_sensitive=filter_params.case_sensitive
        )
        
        # Convert filtered DataFrame back to list of dictionaries
        filtered_properties = []
        if not filtered_df.empty:
            filtered_properties = filtered_df.to_dict('records')
        
        # Get filter statistics
        stats = filter_instance.get_filter_statistics(filtered_df)
        
        logger.info(f"Vectorized filtering completed: {len(filtered_properties)} properties match criteria")
        
        return {
            "properties": filtered_properties,
            "count": len(filtered_properties),
            "statistics": stats
        }
        
    except Exception as e:
        logger.error(f"Error in vectorized filtering: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Filtering failed: {str(e)}"
        )

@app.post("/api/search_by_location")
async def search_by_location(search_params: LocationSearchParams):
    """Search properties by location and radius"""
    try:
        from geopy.geocoders import Nominatim
        from geopy.distance import geodesic
        
        # Initialize geocoder
        geolocator = Nominatim(user_agent="vacation_rentals_app")
        
        # Geocode the search query
        location = geolocator.geocode(search_params.query)
        
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        
        search_coordinates = (location.latitude, location.longitude)
        
        # Get all properties
        all_properties = get_all_properties()
        
        # Filter properties by distance
        nearby_properties = []
        for prop in all_properties:
            # For now, we'll use a simple text-based matching
            # In a real application, you'd want to store coordinates for each property
            property_location = prop.location.lower()
            search_location = location.address.lower()
            
            # Check if the property location contains the search location or vice versa
            is_nearby = (property_location in search_location or 
                        search_location.split(',')[0] in property_location)
            
            if is_nearby:
                nearby_properties.append(prop)
        
        # Convert Property objects to dictionaries for JSON serialization
        properties_data = []
        for prop in nearby_properties:
            prop_dict = {
                "property_id": prop.property_id,
                "location": prop.location,
                "type": prop.ptype,
                "nightly_price": prop.nightly_price,
                "features": ",".join(prop.features) if prop.features else "",
                "tags": ",".join(prop.tags) if prop.tags else "",
                "image_url": prop.image_url,
                "image_alt": prop.image_alt
            }
            properties_data.append(prop_dict)
        
        logger.info(f"Location search found {len(properties_data)} properties near {search_params.query}")
        
        return {
            "properties": properties_data,
            "total_count": len(properties_data),
            "search_location": {
                "query": search_params.query,
                "address": location.address,
                "coordinates": search_coordinates,
                "radius_km": search_params.radius_km
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in location search: {e}")
        raise HTTPException(status_code=500, detail=f"Location search failed: {str(e)}")

@app.get("/api/filter_options")
async def get_filter_options():
    """Get available filter options (unique features, types, locations)"""
    try:
        # Get all properties from database
        properties = get_all_properties()
        
        # Convert Property objects to dictionaries for filtering
        properties_data = []
        for prop in properties:
            prop_dict = {
                "property_id": prop.property_id,
                "location": prop.location,
                "ptype": prop.ptype,
                "nightly_price": prop.nightly_price,
                "features": prop.features if prop.features else [],
                "tags": prop.tags if prop.tags else [],
                "image_url": prop.image_url,
                "image_alt": prop.image_alt
            }
            properties_data.append(prop_dict)
        
        # Create vectorized filter instance
        filter_instance = create_vectorized_filter(properties_data)
        
        # Get unique values for each filter category
        filter_options = {
            "features": filter_instance.get_unique_features(case_sensitive=False),
            "property_types": filter_instance.get_unique_property_types(case_sensitive=False),
            "locations": filter_instance.get_unique_locations(case_sensitive=False),
            "price_range": {
                "min": min(prop["nightly_price"] for prop in properties_data),
                "max": max(prop["nightly_price"] for prop in properties_data)
            }
        }
        
        logger.info(f"Filter options retrieved: {len(filter_options['features'])} features, {len(filter_options['property_types'])} types, {len(filter_options['locations'])} locations")
        
        return filter_options
        
    except Exception as e:
        logger.error(f"Error getting filter options: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get filter options: {str(e)}"
        )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled exception: {exc}")
    return {"error": "Internal server error", "detail": str(exc)}

# Add frontend page routes
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

# Image management endpoints
@app.get("/image-manager")
async def serve_image_manager():
    """Serve the image manager page"""
    try:
        return FileResponse("static/image-manager.html")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Image manager page not found")
    except Exception as e:
        logger.error(f"Error serving image manager: {e}")
        raise HTTPException(status_code=500, detail="Error serving image manager")

@app.post("/api/upload_property_image")
async def upload_property_image(
    image: UploadFile = File(...),
    property_id: int = Form(...)
):
    """Upload an image for a specific property"""
    try:
        # Validate file type
        if not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Validate file size (5MB limit)
        if image.size > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size must be less than 5MB")
        
        # Create images directory if it doesn't exist
        images_dir = Path("static/images/properties")
        images_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        file_extension = Path(image.filename).suffix
        filename = f"property_{property_id}_{int(os.urandom(4).hex(), 16)}{file_extension}"
        file_path = images_dir / filename
        
        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        # Update database with image URL
        image_url = f"/static/images/properties/{filename}"
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE properties SET image_url = ?, image_alt = ? WHERE property_id = ?",
            (image_url, f"Property {property_id} image", property_id)
        )
        conn.commit()
        conn.close()
        
        logger.info(f"Image uploaded for property {property_id}: {filename}")
        
        return {
            "success": True,
            "message": "Image uploaded successfully",
            "image_url": image_url,
            "filename": filename
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading image for property {property_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

@app.delete("/api/remove_property_image/{property_id}")
async def remove_property_image(property_id: int):
    """Remove image for a specific property"""
    try:
        # Get current image URL from database
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT image_url FROM properties WHERE property_id = ?", (property_id,))
        result = cursor.fetchone()
        
        if not result or not result[0]:
            raise HTTPException(status_code=404, detail="No image found for this property")
        
        image_url = result[0]
        
        # Remove image file if it's a local file
        if image_url.startswith('/static/images/properties/'):
            file_path = Path("static") / image_url.lstrip('/')
            if file_path.exists():
                file_path.unlink()
                logger.info(f"Image file removed: {file_path}")
        
        # Update database to remove image reference
        cursor.execute(
            "UPDATE properties SET image_url = NULL, image_alt = NULL WHERE property_id = ?",
            (property_id,)
        )
        conn.commit()
        conn.close()
        
        logger.info(f"Image removed for property {property_id}")
        
        return {
            "success": True,
            "message": "Image removed successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing image for property {property_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to remove image: {str(e)}")

@app.get("/api/property_images")
async def get_property_images():
    """Get all property images status"""
    try:
        properties = get_all_properties()
        image_status = []
        
        for prop in properties:
            has_image = prop.image_url is not None
            is_local = has_image and prop.image_url.startswith('/static/images/properties/')
            
            image_status.append({
                "property_id": prop.property_id,
                "location": prop.location,
                "type": prop.ptype,
                "has_image": has_image,
                "is_local": is_local,
                "image_url": prop.image_url,
                "image_alt": prop.image_alt
            })
        
        return {
            "properties": image_status,
            "total_properties": len(image_status),
            "properties_with_images": sum(1 for p in image_status if p["has_image"]),
            "properties_with_local_images": sum(1 for p in image_status if p["is_local"])
        }
        
    except Exception as e:
        logger.error(f"Error getting property images status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get property images status: {str(e)}")

# ===== Property Generation Functions =====

async def generate_property_with_ai():
    """Generate property data using AI with enhanced prompt"""
    try:
        logger.info("Generating property data with AI...")
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Enhanced system prompt for property generation
        enhanced_prompt = """You are a professional vacation property data generator. Please generate 3-5 vacation property entries in the following JSON format:

[
  {
    "location": "City name (e.g., Toronto, Vancouver, Montreal)",
    "type": "Property type (e.g., Condo, House, Villa, Apartment)",
    "nightly_price": "Price per night (number between 50-500)",
    "features": ["Feature1", "Feature2", "Feature3"],
    "tags": ["Tag1", "Tag2", "Tag3"]
  }
]

Requirements:
1. Return ONLY valid JSON, no additional text
2. Use realistic Canadian city names
3. Price range: $50-$500 per night
4. Features should include: WiFi, Hot Tub, Gym, Pool, Pet Friendly, Kitchen, etc.
5. Tags should describe: Downtown, Mountain View, Beach Front, Family Friendly, etc.
6. Generate 3-5 different properties
7. Ensure all fields are properly filled"""
        
        data = {
            "model": "tngtech/deepseek-r1t2-chimera:free",
            "messages": [
                {"role": "system", "content": enhanced_prompt},
                {"role": "user", "content": "Please generate vacation property data in JSON format."}
            ]
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            response_data = response.json()
            ai_message = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
            logger.info("AI response received successfully")
            return ai_message
        else:
            logger.error(f"AI generation failed: {response.status_code}")
            return None
            
    except Exception as e:
        logger.error(f"Error in AI property generation: {e}")
        return None

def validate_and_clean_json(ai_response: str):
    """Validate and clean AI-generated JSON response"""
    try:
        # Try direct JSON parsing first
        return json.loads(ai_response)
    except json.JSONDecodeError:
        logger.info("Direct JSON parsing failed, attempting to extract JSON...")
        
        # Look for JSON array pattern
        json_match = re.search(r'\[.*\]', ai_response, re.DOTALL)
        if json_match:
            try:
                extracted_json = json_match.group()
                # Clean up common issues
                cleaned_json = extracted_json.replace('\n', '').replace('\r', '')
                return json.loads(cleaned_json)
            except json.JSONDecodeError:
                logger.info("JSON extraction failed")
                pass
        
        # Look for individual property objects
        property_matches = re.findall(r'\{[^}]*\}', ai_response)
        if property_matches:
            try:
                properties = []
                for match in property_matches:
                    # Clean up the property object
                    cleaned_property = match.replace('\n', '').replace('\r', '')
                    property_data = json.loads(cleaned_property)
                    if validate_property_data(property_data):
                        properties.append(property_data)
                
                if properties:
                    logger.info(f"Extracted {len(properties)} valid properties")
                    return properties
            except Exception as e:
                logger.error(f"Error processing extracted properties: {e}")
        
        return None

def validate_property_data(property_data: dict):
    """Validate individual property data"""
    try:
        required_fields = ["location", "type", "nightly_price", "features", "tags"]
        
        # Check required fields
        for field in required_fields:
            if field not in property_data:
                logger.info(f"Missing required field: {field}")
                return False
        
        # Validate price
        try:
            price = int(property_data["nightly_price"])
            if not (50 <= price <= 500):
                logger.info(f"Invalid price range: {price}")
                return False
        except (ValueError, TypeError):
            logger.info(f"Invalid price format: {property_data['nightly_price']}")
            return False
        
        # Validate features and tags are lists
        if not isinstance(property_data.get("features"), list):
            logger.info("Features must be a list")
            return False
        
        if not isinstance(property_data.get("tags"), list):
            logger.info("Tags must be a list")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error validating property data: {e}")
        return False

def generate_template_property_data():
    """Generate template property data as fallback"""
    logger.info("Generating template property data...")
    
    template_properties = [
        {
            "location": "Toronto",
            "type": "Condo",
            "nightly_price": 180,
            "features": ["WiFi", "Gym", "Pool", "Kitchen"],
            "tags": ["Downtown", "Modern", "Family Friendly"]
        },
        {
            "location": "Vancouver",
            "type": "House",
            "nightly_price": 250,
            "features": ["Hot Tub", "Garden", "Pet Friendly", "Fireplace"],
            "tags": ["Mountain View", "Quiet", "Spacious"]
        },
        {
            "location": "Montreal",
            "type": "Apartment",
            "nightly_price": 120,
            "features": ["WiFi", "Balcony", "Air Conditioning", "Washing Machine"],
            "tags": ["Historic District", "Walkable", "Cultural"]
        },
        {
            "location": "Calgary",
            "type": "Villa",
            "nightly_price": 300,
            "features": ["Private Pool", "BBQ Area", "Mountain View", "Garage"],
            "tags": ["Luxury", "Scenic", "Private"]
        }
    ]
    
    return template_properties

# ===== Travel Planning Functions =====

# Session storage (in production, should use Redis or database)
travel_sessions = {}

@app.post("/api/travel_planning")
async def travel_planning_endpoint(request_data: dict):
    """Travel planning endpoint"""
    try:
        user_message = request_data.get("message", "")
        session_id = request_data.get("session_id")
        
        logger.info(f"Received travel planning request: {user_message}, Session ID: {session_id}")
        
        # Get or create session
        from travel_planning import TravelPlanningSession
        session = None
        
        if session_id and session_id in travel_sessions:
            session = travel_sessions[session_id]
            # Check if session is expired
            if session.is_expired():
                del travel_sessions[session_id]
                session = None
        
        if not session:
            if session_id:
                # Create session using user-provided session_id
                session = TravelPlanningSession(session_id)
                travel_sessions[session_id] = session
            else:
                # Create new session
                session = TravelPlanningSession()
                travel_sessions[session.session_id] = session
        
        # Classify user intent
        from travel_planning import classify_user_intent, extract_information_with_ai, generate_next_question_with_ai
        intent = classify_user_intent(user_message)
        
        if intent == "start_planning":
            # Start new planning session
            session.reset_session()
            next_question = await generate_next_question_with_ai(session)
            session.add_conversation_entry(user_message, next_question)
            
            return {
                "response": next_question,
                "session_id": session.session_id,
                "current_step": session.current_step,
                "completion_percentage": session.get_completion_percentage()
            }
        
        elif intent == "provide_information":
            # User provides information
            current_step = session.current_step
            logger.info(f"Current step: {current_step}")
            
            print(f"🔍 DEBUG: Starting information extraction")
            print(f"🔍 DEBUG: user_message = '{user_message}'")
            print(f"🔍 DEBUG: current_step = '{current_step}'")
            
            # Simple test
            print(f"🔍 DEBUG: Testing function call...")
            try:
                test_result = await extract_information_with_ai("Toronto", "destination", session)
                print(f"🔍 DEBUG: Test call result: {test_result}")
            except Exception as e:
                print(f"🔍 DEBUG: Test call exception: {e}")
            
            extracted_info = await extract_information_with_ai(user_message, current_step, session)
            print(f"🔍 DEBUG: extract_information_with_ai returned: {extracted_info}")
            
            logger.info(f"Extracted information: {extracted_info}")
            
            # Use step mapping table to determine which field to store to
            from travel_planning import TRAVEL_PLANNING_STEPS
            step_info = TRAVEL_PLANNING_STEPS.get(current_step, {})
            target_field = step_info.get("field")
            logger.info(f"Target field: {target_field}")
            
            if target_field:
                update_success = session.update_collected_info(target_field, extracted_info)
                logger.info(f"Field updated successfully: {update_success}")
                logger.info(f"Session info after update: {session.collected_info}")
            else:
                # For steps without corresponding fields (like initial), handle manually
                if current_step == "initial":
                    # Initial step usually provides destination information
                    update_success = session.update_collected_info("destination", extracted_info)
                    logger.info(f"initial step updated successfully: {update_success}")
                    logger.info(f"Session info after update: {session.collected_info}")
                else:
                    update_success = True
                    logger.info(f"No field step, default success: {update_success}")
            
            if update_success:
                # Move to next step
                from travel_planning import TRAVEL_PLANNING_STEPS
                session.current_step = TRAVEL_PLANNING_STEPS[current_step]["next"]
                
                # Check if sufficient information has been collected
                if session.has_sufficient_information():
                    # Generate recommendations
                    from travel_recommendation_engine import TravelRecommendationEngine
                    engine = TravelRecommendationEngine()
                    recommendations = engine.generate_travel_recommendations(session)
                    
                    if recommendations["type"] == "recommendations":
                        response_text = recommendations["recommendation_text"]
                        session.current_step = "complete"
                    else:
                        response_text = recommendations["message"]
                    
                    session.add_conversation_entry(user_message, response_text)
                    
                    return {
                        "response": response_text,
                        "session_id": session.session_id,
                        "current_step": session.current_step,
                        "completion_percentage": session.get_completion_percentage(),
                        "recommendations": recommendations
                    }
                else:
                    # Continue collecting information
                    next_question = await generate_next_question_with_ai(session)
                    session.add_conversation_entry(user_message, next_question)
                    
                    return {
                        "response": next_question,
                        "session_id": session.session_id,
                        "current_step": session.current_step,
                        "completion_percentage": session.get_completion_percentage()
                    }
            else:
                # Information update failed
                error_message = f"Sorry, I cannot understand your information about '{current_step}'. Please re-enter."
                session.add_conversation_entry(user_message, error_message)
                
                return {
                    "response": error_message,
                    "session_id": session.session_id,
                    "current_step": session.current_step,
                    "completion_percentage": session.get_completion_percentage()
                }
        
        elif intent == "modify_information":
            # User modifies information
            response_text = "Okay, please tell me what information you want to modify?"
            session.add_conversation_entry(user_message, response_text)
            
            return {
                "response": response_text,
                "session_id": session.session_id,
                "current_step": session.current_step,
                "completion_percentage": session.get_completion_percentage()
            }
        
        elif intent == "ask_for_recommendations":
            # User requests recommendations
            if session.has_sufficient_information():
                from travel_recommendation_engine import TravelRecommendationEngine
                engine = TravelRecommendationEngine()
                recommendations = engine.generate_travel_recommendations(session)
                
                if recommendations["type"] == "recommendations":
                    response_text = recommendations["recommendation_text"]
                else:
                    response_text = recommendations["message"]
                
                session.add_conversation_entry(user_message, response_text)
                
                return {
                    "response": response_text,
                    "session_id": session.session_id,
                    "current_step": session.current_step,
                    "completion_percentage": session.get_completion_percentage(),
                    "recommendations": recommendations
                }
            else:
                # Insufficient information, continue collecting
                next_question = await generate_next_question_with_ai(session)
                session.add_conversation_entry(user_message, next_question)
                
                return {
                    "response": f"I still need some information to recommend properties for you. {next_question}",
                    "session_id": session.session_id,
                    "current_step": session.current_step,
                    "completion_percentage": session.get_completion_percentage()
                }
        
        else:
            # Other cases, treat as providing information
            current_step = session.current_step
            extracted_info = await extract_information_with_ai(user_message, current_step, session)
            
            # Use step mapping table to determine which field to store to
            from travel_planning import TRAVEL_PLANNING_STEPS
            step_info = TRAVEL_PLANNING_STEPS.get(current_step, {})
            target_field = step_info.get("field")
            
            if target_field:
                update_success = session.update_collected_info(target_field, extracted_info)
            else:
                update_success = False
            
            if update_success:
                from travel_planning import TRAVEL_PLANNING_STEPS
                session.current_step = TRAVEL_PLANNING_STEPS[current_step]["next"]
                next_question = await generate_next_question_with_ai(session)
                session.add_conversation_entry(user_message, next_question)
                
                return {
                    "response": next_question,
                    "session_id": session.session_id,
                    "current_step": session.current_step,
                    "completion_percentage": session.get_completion_percentage()
                }
            else:
                response_text = "Sorry, I did not understand your request. Please re-enter."
                session.add_conversation_entry(user_message, response_text)
                
                return {
                    "response": response_text,
                    "session_id": session.session_id,
                    "current_step": session.current_step,
                    "completion_percentage": session.get_completion_percentage()
                }
                
    except Exception as e:
        logger.error(f"Travel planning processing failed: {e}")
        return {
            "response": "Sorry, I encountered an issue while processing your request. Please try again later.",
            "error": str(e)
        }

@app.get("/api/travel_planning/session/{session_id}")
async def get_travel_session(session_id: str):
    """Get travel planning session information"""
    try:
        if session_id in travel_sessions:
            session = travel_sessions[session_id]
            return {
                "session_id": session.session_id,
                "current_step": session.current_step,
                "completion_percentage": session.get_completion_percentage(),
                "collected_info": session.collected_info,
                "conversation_count": len(session.conversation_history)
            }
        else:
            raise HTTPException(status_code=404, detail="Session not found")
            
    except Exception as e:
        logger.error(f"Failed to get session info: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get session info: {str(e)}")

@app.delete("/api/travel_planning/session/{session_id}")
async def delete_travel_session(session_id: str):
    """Delete travel planning session"""
    try:
        if session_id in travel_sessions:
            del travel_sessions[session_id]
            return {"message": "Session deleted"}
        else:
            raise HTTPException(status_code=404, detail="Session not found")
            
    except Exception as e:
        logger.error(f"Failed to delete session: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete session: {str(e)}")
