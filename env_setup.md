# Environment Variable Setup Guide

## 🔑 Setting up API Keys

Your project requires API keys for various services. Please follow these steps to set them up:

### OpenRouter API Key

Your API requires an OpenRouter API key to function properly. Please follow these steps to set it up:

### Method 1: Create .env file (Recommended)

1. Create a `.env` file in the project root directory
2. Add the following content:

```bash
# AI Features (Required)
OPENROUTER_API_KEY=your_actual_api_key_here

# Geocoding Services (Optional - only if adding new properties)
HERE_API_KEY=your_here_api_key_here
```

### Method 2: Set system environment variables

#### macOS/Linux:
```bash
export OPENROUTER_API_KEY="your_actual_api_key_here"
# Optional: Only if adding new properties that need geocoding
export HERE_API_KEY="your_here_api_key_here"
```

#### Windows:
```cmd
set OPENROUTER_API_KEY=your_actual_api_key_here
# Optional: Only if adding new properties that need geocoding
set HERE_API_KEY=your_here_api_key_here
```

### Method 3: Set when running uvicorn

```bash
# Required for AI features
OPENROUTER_API_KEY=your_key_here uvicorn api:app --reload

# Optional: Only if you need geocoding for new properties
# OPENROUTER_API_KEY=your_key_here HERE_API_KEY=your_here_key_here uvicorn api:app --reload
```

## 🚀 Getting API Keys

### OpenRouter API Key
1. Visit [OpenRouter](https://openrouter.ai/)
2. Register account and login
3. Create a new API key in the console
4. Copy the key and paste it into any of the methods above

### HERE Maps API Key (Optional)
**Note**: This API key is only needed if you want to add new properties with addresses and need to geocode them to get coordinates. If you're using the existing `properties_simple.json` file, all properties already have coordinates and you don't need this key.

**If you do need it:**
1. Visit [HERE Developer Portal](https://developer.here.com/)
2. Register account and create a project
3. Get your API key from the project console
4. Add it to your `.env` file as `HERE_API_KEY=your_key_here`

## ✅ Verify Setup

After setup, you can verify by:

1. Visit the health check endpoint:
```bash
curl http://127.0.0.1:8000/health
```

2. You should see output similar to:
```json
{
  "status": "healthy",
  "api_key_configured": true,
  "environment": "development"
}
```

## 🐛 Common Issues

- **500 Internal Server Error**: Usually means API key is not set
- **401 Unauthorized**: API key is invalid or expired
- **429 Too Many Requests**: Reached API call limit

## 📝 Notes

- Do not commit `.env` file to version control system
- Ensure `.env` file is in `.gitignore`
- API keys should be kept confidential, do not share with others

## 🗺️ About HERE API Key (Optional)

### **Why is HERE API Key Optional?**

The HERE API key is only required if you need to:
- Add new properties with addresses that need geocoding
- Update coordinates for existing properties
- Use the geocoding scripts (`here_coordinates.py`, `precise_coordinates.py`)

### **If you're using existing data:**

The `properties_simple.json` file already contains:
- ✅ **300 properties** with complete information
- ✅ **Precise coordinates** (latitude/longitude) for all properties
- ✅ **Ready to import** directly into the database

You can simply run:
```bash
python3 import_properties.py
```

This will import all properties with coordinates without needing any geocoding API calls.

### **When you DO need HERE API Key:**

- Adding new properties from addresses
- Updating coordinates for existing properties
- Running geocoding scripts for bulk coordinate updates
