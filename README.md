# 🏝️ Cozy DoDo - Vacation Home Assistant

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive AI-powered vacation property recommendation platform that combines advanced AI technology with a rich property database to provide personalized travel planning and property recommendations.

> **🚀 New User?** Start with our [One-Command Setup](#-alternative-one-command-setup) for the easiest experience!

## 📸 **Application Screenshots**

### **Main Interface**
<img width="1429" height="840" alt="Screenshot 2025-08-27 at 16 45 15" src="https://github.com/user-attachments/assets/51954898-6198-429b-afd6-c898f97bff34" />

*Beautiful property browsing interface with advanced filtering options*
<img width="1354" height="827" alt="Screenshot 2025-08-27 at 16 45 52" src="https://github.com/user-attachments/assets/bd93420a-3702-45ec-b3a9-c16fe9514bd9" />


### **Property Details**
<img width="1283" height="665" alt="Screenshot 2025-08-27 at 16 45 36" src="https://github.com/user-attachments/assets/f4020ffa-4e52-41c9-8080-04c26fa1d9b7" />

*Detailed property information with high-quality images and amenities*

## ✨ Features

### 🏠 **Smart Property Browsing**
- **Beautiful Property Cards**: Each property displays with:
  - Location with environment-specific icons (mountain, beach, city, etc.)
  - High-quality property images
  - Detailed amenities and features
  - Pricing information
  - Interactive elements

### 🔍 **Advanced Filtering System**
- **Location-Based Search**: Radius-based property discovery
- **Multi-Criteria Filtering**: Budget, property type, features, amenities
- **Smart Persistence**: Filter state maintained across page refreshes
- **Real-time Updates**: Dynamic filtering without page reload

### 🤖 **AI Travel Planning Assistant**
- **Multi-Turn Conversations**: Natural language interaction
- **Intelligent Information Extraction**: AI-powered data collection
- **Personalized Recommendations**: Property suggestions based on preferences
- **Context-Aware Conversations**: Maintains conversation state
- **OpenRouter Integration**: Powered by deepseek-r1t2-chimera:free

### 🗺️ **Geographic Intelligence**
- **Coordinate System**: GPS coordinates for all properties
- **Primary Service**: Nominatim (OpenStreetMap) - Free geocoding service
- **Advanced Service**: HERE Maps API - High-precision geocoding (250,000 free requests/month)
- **Smart Location Matching**: Intelligent address parsing and geocoding
- **Distance Calculations**: Radius-based property filtering

### 📊 **Data Management**
- **SQLite Database**: Lightweight, efficient data storage
- **Property Database**: 300+ curated vacation properties
- **User Profiles**: Personalized preference management
- **Image Management**: Property photo uploads and management

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/SummerHomeRecommender-BestChoice.git
   cd SummerHomeRecommender-BestChoice
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (Optional for basic usage)**
   ```bash
   # Create .env file with OpenRouter API key (required for AI features)
   echo "OPENROUTER_API_KEY=your_api_key_here" > .env
   
   # HERE API key is optional - only needed if adding new properties
   # echo "HERE_API_KEY=your_here_api_key" >> .env
   ```

   **Note**: 
   - **OpenRouter API Key**: Required for AI features - get from [OpenRouter](https://openrouter.ai/)
   - **HERE API Key**: Optional - only needed for geocoding new properties

5. **Import property data (Required for first run)**
   ```bash
   # The database will be automatically created and populated
   python3 import_properties.py --auto-import
   ```

6. **Run the application**
   ```bash
   # Option 1: Use the startup script (Recommended)
   ./run.sh
   
   # Option 2: Manual start
   python3 -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload
   ```

7. **Open your browser**
   - Main application: http://localhost:8000/
   - API documentation: http://localhost:8000/docs

8. **Login to the application**
   > **🔑 Login Credentials**
   > - **Username**: `Team18`
   > - **Password**: `Team18`
   > - Navigate to http://localhost:8000/static/login.html

### **🚀 Alternative: One-Command Setup**

If you prefer a simpler approach, you can use our automated startup script:

```bash
# Make the script executable (first time only)
chmod +x run.sh

# Run everything with one command
./run.sh
```

The script will automatically:
- ✅ Check and create virtual environment
- ✅ Install dependencies
- ✅ Detect missing .env file and guide you
- ✅ Import property data if database is empty
- ✅ Start the application

**After startup, login with:**
- **Username**: `Team18`
- **Password**: `Team18`

## 🏗️ Project Architecture

### **Frontend Layer**
```
static/
├── index.html              # Main application page (27KB, 564 lines)
├── login.html              # Authentication page (7.2KB, 233 lines)
├── css/
│   └── style.css           # Main stylesheet (65KB, 3203 lines)
├── js/
│   ├── ui.js               # UI interactions (38KB, 1157 lines)
│   ├── chat.js             # Chat functionality (24KB, 843 lines)
│   ├── properties.js       # Property display (29KB, 908 lines)
│   ├── budget.js           # Budget filtering (15KB, 460 lines)
│   ├── location-search.js  # Location search (11KB, 285 lines)
│   ├── address-autocomplete.js # Address completion (8.5KB, 269 lines)
│   ├── property-types.js   # Property type handling (9.9KB, 324 lines)
│   ├── features.js         # Feature management (11KB, 339 lines)
│   └── api.js              # API communication (7.1KB, 261 lines)
└── images/
    └── properties/         # Property images
```

### **Backend Layer**
```
├── api.py                  # FastAPI application (49KB, 1257 lines)
├── database.py             # Database operations (3.1KB, 106 lines)
├── property.py             # Property data model (2.4KB, 67 lines)
├── user.py                 # User management (9.3KB, 252 lines)
├── main.py                 # CLI application (7.4KB, 216 lines)
└── vectorized_filter.py    # Advanced filtering (13KB, 363 lines)
```

### **AI Intelligence Layer**
```
├── travel_planning.py      # AI conversation management (21KB, 482 lines)
├── travel_recommendation_engine.py # Recommendation logic (11KB, 241 lines)
├── smart_match_engine.py   # Smart matching algorithms (12KB, 322 lines)
```

### **Geographic Services**
```
├── add_coordinates.py      # Coordinate addition script (8.3KB, 239 lines)
├── here_coordinates.py     # HERE API integration (6.1KB, 198 lines)
├── precise_coordinates.py  # HERE API coordinate service (6.1KB, 201 lines)
├── complete_coordinates.py # Coordinate completion utility (5.6KB, 170 lines)
└── add_coordinates_to_db.py # Database coordinate management (2.7KB, 83 lines)
```

### **Data Management**
```
├── seed_data.py            # Database seeding (2.2KB, 78 lines)
├── add_sample_images.py    # Image management (2.3KB, 64 lines)
├── bulk_upload_images.py   # Bulk image operations (7.5KB, 223 lines)
└── properties_300.json     # Property data (72KB, 2102 lines)
```

### **Testing & Development**
```
├── test_*.py               # Comprehensive test suite (20+ test files)
├── debug_*.py              # Debugging utilities
├── test_*.html             # Frontend testing pages
└── requirements.txt         # Python dependencies
```

## 🏗️ **Detailed Architecture Overview**

### **Overall Architecture Overview**

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend Layer                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌──────────┐  │
│  │   HTML5     │ │   CSS3      │ │  Vanilla    │ │  Font    │  │
│  │  Semantic   │ │  Variables  │ │ JavaScript  │ │ Awesome  │  │
│  │   Markup    │ │  & Grid     │ │  Modules    │ │  Icons   │  │
│  └─────────────┘ └─────────────┘ └─────────────┘ └──────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     API Gateway Layer                           │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    FastAPI (api.py)                        │ │
│  │  • RESTful API endpoints                                   │ │
│  │  • Static file serving                                     │ │
│  │  • CORS handling                                           │ │
│  │  • Request/Response validation                             │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌──────────┐  │
│  │   Travel    │ │  Property   │ │   User      │ │  Smart   │  │
│  │ Planning    │ │ Management  │ │ Management  │ │ Matching │  │
│  │   (AI)      │ │             │ │             │ │ Engine   │  │
│  └─────────────┘ └─────────────┘ └─────────────┘ └──────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Data Access Layer                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌──────────┐  │
│  │   SQLite    │ │   Pandas    │ │   NumPy     │ │  Geopy   │  │
│  │  Database   │ │  DataFrame  │ │  Arrays     │ │Geocoding │  │
│  │             │ │             │ │             │ │          │  │
│  └─────────────┘ └─────────────┘ └─────────────┘ └──────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    External Services Layer                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌──────────┐  │
│  │ OpenRouter  │ │  HERE Maps  │ │Nominatim    │ │  File    │  │
│  │     AI      │ │   API       │ │OpenStreetMap│ │  System  │  │
│  │  Service    │ │             │ │             │ │          │  │
│  └─────────────┘ └─────────────┘ └─────────────┘ └──────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### **Layered Architecture Details**

#### **1. Frontend Layer**

##### **Technology Stack**
- **HTML5**: Semantic markup, responsive design
- **CSS3**: Custom properties system, Flexbox/Grid layout
- **Vanilla JavaScript**: Modular architecture, no framework dependencies

##### **Architecture Features**
- **Modular Design**: Each functionality in independent JS files
- **Event-Driven**: Loosely coupled component communication
- **State Management**: Centralized UI state management
- **Responsive Design**: Mobile-first design philosophy

#### **2. API Gateway Layer**

##### **Core Component: `api.py` (1257 lines)**
```python
# FastAPI application instance
app = FastAPI(
    title="Cozy DoDo - Vacation Home Assistant",
    description="AI-powered vacation property recommendation platform",
    version="1.0.0"
)

# Main endpoints
@app.get("/")                    # Main page
@app.get("/api/properties")      # Get all properties
@app.post("/api/search_by_location") # Location search
@app.post("/chat")               # AI chat
@app.post("/api/travel_planning") # Travel planning
```

##### **Features**
- **RESTful API**: Standardized API design
- **Static File Serving**: Frontend resource distribution
- **CORS Support**: Cross-origin request handling
- **Request Validation**: Data input validation
- **Error Handling**: Unified error responses

#### **3. Business Logic Layer**

##### **A. AI Travel Planning Module (`travel_planning.py` - 482 lines)**
```python
class TravelPlanningSession:
    """Travel planning session management"""
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.collected_info = {}
        self.current_step = "initial"
        self.step_completion = {}

# Core functionality
- Multi-turn conversation management
- Information extraction and storage
- Step state tracking
- AI-driven question generation
```

##### **B. Property Recommendation Engine (`travel_recommendation_engine.py` - 241 lines)**
```python
class TravelRecommendationEngine:
    """Intelligent property recommendation engine"""
    
    def filter_properties_for_travel_planning(self, session):
        """Filter properties based on session information"""
        
    def score_properties_by_preferences(self, properties, session):
        """Score properties based on user preferences"""
        
    def generate_travel_recommendations(self, session):
        """Generate travel recommendations"""
```

##### **C. Smart Matching Engine (`smart_match_engine.py` - 322 lines)**
```python
class SmartMatchEngine:
    """Intelligent property matching engine"""
    
    def calculate_similarity_score(self, property1, property2):
        """Calculate property similarity score"""
        
    def find_best_matches(self, target_property, properties, top_n=5):
        """Find best matches"""
```

#### **4. Data Access Layer**

##### **A. Database Management (`database.py` - 106 lines)**
```python
# SQLite database operations
def create_tables():
    """Create database table structure"""
    
def get_connection():
    """Get database connection"""
    
def get_all_properties():
    """Get all property data"""
```

##### **B. Property Data Model (`property.py` - 67 lines)**
```python
class Property:
    """Property data model"""
    def __init__(self, property_id, location, ptype, 
                 nightly_price, features, tags, 
                 image_url=None, image_alt=None, 
                 latitude=None, longitude=None):
        # Property attributes initialization
```

##### **C. Vectorized Filtering (`vectorized_filter.py` - 363 lines)**
```python
class VectorizedFilter:
    """High-performance vectorized filtering"""
    
    def prepare_dataframe(self, properties):
        """Prepare Pandas DataFrame"""
        
    def filter_by_criteria(self, df, filters):
        """Filter by criteria"""
```

#### **5. External Services Layer**

##### **A. AI Service Integration**
```python
# OpenRouter API integration
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "tngtech/deepseek-r1t2-chimera:free"

async def generate_response_with_ai(prompt):
    """Call AI service to generate response"""
```

##### **B. Geocoding Services**
```python
# Multi-API geocoding
- Nominatim (OpenStreetMap): Free service
- HERE Maps API: High-precision service (250,000 free requests/month)
- Intelligent address parsing and coordinate acquisition
```

### **Data Flow Architecture**

#### **1. User Request Flow**
```
User Action → Frontend JS → API Endpoint → Business Logic → Data Access → Database/External Services
    ↓
Response Data ← API Endpoint ← Business Logic ← Data Access ← Database/External Services
    ↓
Frontend Rendering ← Frontend JS ← Response Data
```

#### **2. AI Travel Planning Flow**
```
User Input → Chat Interface → Intent Recognition → Information Extraction → Session Management
    ↓
AI Q&A Generation ← Recommendation Engine ← Property Filtering ← Database Query
    ↓
Personalized Recommendations → Chat Response → User Interface
```

#### **3. Property Search Flow**
```
Location Input → Geocoding → Coordinate Acquisition → Radius Search → Property Filtering
    ↓
Result Sorting ← Preference Scoring ← Feature Matching ← Database Query
    ↓
Property Cards ← Frontend Rendering ← Filtered Results
```

### **Architecture Design Principles**

#### **1. Layered Architecture**
- **Separation of Concerns**: Each layer focuses on specific responsibilities
- **Loose Coupling**: Layers communicate through interfaces
- **High Cohesion**: Related functionality is organized together

#### **2. Modular Design**
- **Single Responsibility**: Each module is responsible for one function
- **Reusability**: Modules can be reused in different scenarios
- **Testability**: Independent modules facilitate unit testing

#### **3. Event-Driven Architecture**
- **Loose Coupling Communication**: Components communicate through events
- **Asynchronous Processing**: Non-blocking operation handling
- **Scalability**: Easy to add new event handlers

#### **4. Microservices Mindset**
- **Service-Oriented**: Break functionality into independent services
- **API-First**: Service-to-service communication through APIs
- **Independent Deployment**: Each service can be updated independently

### **Architecture Advantages**

#### **1. Maintainability**
- Clear code organization structure
- Modular functionality design
- Unified coding standards

#### **2. Scalability**
- Easy to add new functional modules
- Support for horizontal scaling
- Plugin-based architecture design

#### **3. Performance Optimization**
- Vectorized data processing
- Intelligent caching strategies
- Asynchronous operation support

#### **4. Development Efficiency**
- Complete test coverage
- Detailed documentation
- Standardized development process

### **Architecture Evolution Roadmap**

#### **Short-term Optimization**
- Add Redis caching layer
- Implement database connection pooling
- Optimize static resource loading

#### **Medium-term Expansion**
- Introduce message queue system
- Implement microservice separation
- Add monitoring and logging systems

#### **Long-term Planning**
- Containerized deployment
- Cloud-native architecture
- Distributed system design

## 🔧 Core Workflows

### **Property Discovery Flow**
1. **Location Search**: User enters desired location
2. **Radius Filtering**: Properties within specified distance
3. **Advanced Filtering**: Budget, type, features, amenities
4. **Results Display**: Interactive property cards
5. **State Persistence**: Filter preferences saved

### **AI Travel Planning Flow**
1. **Conversation Initiation**: User requests travel planning
2. **Information Collection**: AI asks sequential questions
3. **Preference Analysis**: Natural language understanding
4. **Property Matching**: Database filtering and scoring
5. **Recommendations**: Personalized property suggestions

### **Data Management Flow**
1. **Property Addition**: Admin adds new properties
2. **Image Upload**: Property photos and descriptions
3. **Coordinate Generation**: Geographic data enrichment
4. **Quality Assurance**: Data validation and verification

## 🎯 Advanced Features

### **AI-Powered Travel Planning**
- **Natural Language Understanding**: Conversational AI interface
- **Multi-Turn Conversations**: Context-aware interactions
- **Intelligent Recommendations**: AI-driven property matching
- **Preference Learning**: User preference adaptation

### **Smart Property Matching**
- **Vectorized Filtering**: High-performance data processing
- **Scoring Algorithms**: Multi-factor property ranking
- **Geographic Intelligence**: Location-based optimization
- **Feature Matching**: Amenity and requirement alignment

### **Geographic Intelligence**
- **Multi-API Fallback**: HERE Maps integration for high-precision geocoding
- **Address Parsing**: Intelligent location extraction
- **Coordinate Management**: GPS data storage and retrieval
- **Distance Calculations**: Radius-based property filtering

### **Data Management**
- **SQLite Database**: Efficient local data storage
- **Image Management**: Property photo organization
- **Bulk Operations**: Batch data processing
- **Data Validation**: Quality assurance systems

## 🛠️ Technical Implementation

### **Backend Technologies**
- **FastAPI**: Modern, fast web framework
- **SQLite**: Lightweight database
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Geopy**: Geographic calculations

### **Frontend Technologies**
- **Vanilla JavaScript**: No framework dependencies
- **CSS3**: Modern styling with custom properties
- **HTML5**: Semantic markup
- **Font Awesome**: Icon library
- **Google Fonts**: Typography

### **AI Integration**
- **OpenRouter API**: AI language model access
- **Natural Language Processing**: Intent recognition
- **Structured Output**: JSON generation and validation
- **Fallback Systems**: Template-based responses

### **Performance Features**
- **Static File Serving**: Efficient asset delivery
- **Database Indexing**: Optimized queries
- **Caching Strategies**: Response optimization
- **Async Operations**: Non-blocking I/O

## 🗄️ Property Database

### **Data Structure**
- **300+ Properties**: Curated vacation rentals
- **Geographic Coverage**: Canada-wide locations
- **Property Types**: Houses, condos, cabins, etc.
- **Rich Metadata**: Features, amenities, pricing

### **Database Schema**
```sql
properties (
    property_id, location, type, nightly_price,
    features, tags, image_url, image_alt,
    latitude, longitude
)

users (
    user_id, name, group_size, preferred_env,
    budget_min, budget_max, travel_dates,
    weight_preferences
)
```

### **Data Sources**
- **Property Listings**: Curated vacation rentals
- **Geographic Data**: HERE Maps API integration
- **Image Assets**: High-quality property photos
- **Feature Tags**: Comprehensive amenity descriptions

### **Data Import & Setup**
> **Important Note**: We initially started with `properties_300.json` as input data and ran `add_coordinates_to_db.py` to add latitude and longitude coordinates for each property in the database. However, **you can now directly import `properties_simple.json` without needing to add your HERE API key** - all properties already include complete coordinate data.

**Available Import Options:**
- **`properties_simple.json`**: Complete property data with coordinates (recommended for direct import)
- **`exported_properties.json`**: Full export with metadata (includes export information)
- **Import Scripts**: Use `import_properties.py` for automated database import

## 🎨 Design Philosophy

### **UX Principles**
- **User-Centric Design**: Intuitive navigation and interactions
- **Responsive Layout**: Mobile-first design approach
- **Performance Focus**: Fast loading and smooth interactions
- **Accessibility**: Inclusive design considerations

### **Visual Design Elements**
- **Modern Aesthetics**: Clean, professional appearance
- **Color System**: Consistent brand identity
- **Typography**: Readable, elegant fonts
- **Iconography**: Meaningful visual elements
- **Spacing**: Balanced layout composition

## 🧪 Development & Testing

### **Testing Strategy**
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **Frontend Testing**: UI interaction validation
- **API Testing**: Backend endpoint verification

### **Development Workflow**
- **Version Control**: Git-based development
- **Code Quality**: Consistent coding standards
- **Documentation**: Comprehensive code comments
- **Error Handling**: Robust error management

## 🚀 Deployment & Operations

### **Environment Setup**
- **Python Environment**: Virtual environment management
- **Dependencies**: Requirements.txt management
- **Configuration**: Environment variable setup
- **Database**: SQLite file management

### **Performance Optimization**
- **Static Assets**: Efficient file serving
- **Database Queries**: Optimized SQL operations
- **Caching**: Response caching strategies
- **Compression**: Asset compression

## 🔮 Future Roadmap

### **Phase 1: Core Features** ✅
- [x] Property browsing and filtering
- [x] AI travel planning assistant
- [x] Geographic intelligence
- [x] User profile management

### **Phase 2: Enhanced AI** 🚧
- [ ] Advanced recommendation algorithms
- [ ] Machine learning integration
- [ ] Predictive analytics
- [ ] Natural language improvements

### **Phase 3: Platform Expansion** 📋
- [ ] Multi-language support
- [ ] Mobile application
- [ ] Advanced analytics dashboard
- [ ] Integration APIs

### **Phase 4: Enterprise Features** 📋
- [ ] Multi-tenant architecture
- [ ] Advanced security features
- [ ] Performance monitoring
- [ ] Scalability improvements

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

### **Development Setup**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### **Code Standards**
- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add comprehensive docstrings
- Include error handling
- Write unit tests for new features

### **Commit Guidelines**
- Use clear, descriptive commit messages
- Reference issues in commit messages
- Keep commits focused and atomic
- Test before committing

## 📚 Documentation

### **User Guides**
- [Travel Planning Usage](TRAVEL_PLANNING_USAGE.md) - AI assistant guide
- [Property Generation Guide](PROPERTY_GENERATION_GUIDE.md) - Property creation
- [Image Upload Guide](IMAGE_UPLOAD_GUIDE.md) - Media management
- [API Setup Guide](API_SETUP_GUIDE.md) - Service configuration

### **Developer Resources**
- [API Documentation](http://localhost:8000/docs) - Interactive API docs
- [Code Comments](api.py) - Comprehensive code documentation
- [Test Examples](test_*.py) - Usage examples and patterns
- [Database Schema](database.py) - Data structure documentation

## 🐛 Troubleshooting

### **Common Issues**

#### **Backend Issues**
- **Port already in use**: Change port or kill existing process
- **Database errors**: Check file permissions and paths
- **API key errors**: Verify environment variables
- **Import errors**: Check virtual environment activation
- **Empty database**: Run `python3 import_properties.py --auto-import` to populate data

#### **Frontend Issues**
- **Static files not loading**: Check file paths and permissions
- **JavaScript errors**: Check browser console for details
- **Styling issues**: Verify CSS file loading
- **Image loading**: Check image file paths
- **Login issues**: Use username `Team18` and password `Team18`

#### **Performance Issues**
- **Slow loading**: Check database query optimization
- **Memory usage**: Monitor Python process memory
- **Response times**: Check API endpoint performance
- **File sizes**: Optimize image and asset sizes

#### **Debug Mode**
- **Enable logging**: Check console output
- **API testing**: Use `/docs` endpoint
- **Database inspection**: Use SQLite browser
- **Network monitoring**: Check browser network tab

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

### **Open Source Libraries**
- **FastAPI**: Modern web framework
- **SQLite**: Database engine
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing
- **Geopy**: Geographic calculations

### **External Services**
- **OpenRouter**: AI language model access
- **HERE Technologies**: Geographic data and mapping (250,000 free requests/month)
- **Nominatim**: OpenStreetMap free geocoding service

### **Community Support**
- **OpenStreetMap**: Free geographic data
- **Font Awesome**: Icon library
- **Google Fonts**: Typography resources

## 📞 Support & Contact

### **Getting Help**
- **Documentation**: Check this README and guides
- **Issues**: Report bugs via GitHub issues
- **Discussions**: Join community discussions
- **Email**: Contact the development team

### **Community**
- **GitHub**: [Project Repository](https://github.com/yourusername/SummerHomeRecommender-BestChoice)
- **Issues**: [Bug Reports](https://github.com/yourusername/SummerHomeRecommender-BestChoice/issues)
- **Discussions**: [Community Forum](https://github.com/yourusername/SummerHomeRecommender-BestChoice/discussions)

---

**Built with ❤️ by the Cozy DoDo team**

*Empowering travelers to discover their perfect vacation homes through intelligent AI and comprehensive property data.*
