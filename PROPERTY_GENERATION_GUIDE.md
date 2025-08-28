# 🏠 AI Property Generation Feature User Guide

## 📋 Feature Overview

Our AI Smart Assistant now has the ability to intelligently recognize user intent. When users request property data generation, it automatically switches to dedicated property generation mode.

## 🎯 Trigger Conditions

When users input the following keywords in the chat box, the system automatically recognizes them as property generation requests:

### **Chinese Keywords**:
- 生成 (generate)
- json
- 数据 (data)
- 房源 (property)

### **English Keywords**:
- property
- generate
- random
- sample

## 💬 Usage Examples

### **Example 1: Chinese Request**
```
User input: 请帮我生成一些随机房源的json文件
(Please help me generate some random property JSON files)
```

### **Example 2: English Request**
```
User input: Can you generate some random property data in JSON format?
```

### **Example 3: Mixed Request**
```
User input: 生成3个度假房源的json数据
(Generate JSON data for 3 vacation properties)
```

## 🔧 Technical Implementation

### **Intelligent Recognition Process**:
1. **User Input Detection**: System automatically detects keywords
2. **AI Generation Attempt**: Calls OpenRouter API to generate property data
3. **Format Validation**: Validates AI-returned JSON format
4. **Template Fallback**: Uses predefined templates if AI fails

### **Data Format**:
```json
[
  {
    "location": "City Name",
    "type": "Property Type",
    "nightly_price": "Price per night",
    "features": ["Feature1", "Feature2", "Feature3"],
    "tags": ["Tag1", "Tag2", "Tag3"]
  }
]
```

### **Data Validation Rules**:
- **location**: Must be a valid Canadian city name
- **type**: Property type (Condo, House, Villa, Apartment, etc.)
- **nightly_price**: Price range 50-500 CAD
- **features**: Feature list (WiFi, Hot Tub, Gym, Pool, etc.)
- **tags**: Tag list (Downtown, Mountain View, etc.)

## 🚀 Response Examples

### **Successful Response**:
```json
[
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
    "features": ["Hot Tub", "Garden", "Pet Friendly"],
    "tags": ["Mountain View", "Quiet", "Spacious"]
  }
]
```

## 🛡️ Error Handling

### **When AI Generation Fails**:
- System automatically falls back to template generation
- Ensures users always receive valid data
- Detailed error logging

### **When Format Validation Fails**:
- Attempts to extract and clean JSON data
- Supports multiple JSON format variants
- Intelligent error recovery

## 📱 Frontend Integration

### **Chat Interface**:
- Floating AI assistant button
- Intelligent intent recognition
- Real-time response display

### **Quick Action Buttons**:
- Preset common questions
- One-click trigger for specific functions
- User-friendly interactive experience

## 🔍 Debug Information

### **Backend Logs**:
- Detailed request processing logs
- AI generation status tracking
- Error cause analysis

### **Frontend Console**:
- Real-time status updates
- Response data display
- Error message prompts

## 🎨 Customization Options

### **Generation Quantity**:
- Default generates 3-5 properties
- Supports user-specified quantities
- Dynamic response adjustment

### **Data Range**:
- Major Canadian cities
- Diverse property types
- Rich features and tags

## 📈 Performance Optimization

### **Response Time**:
- AI generation: Usually 5-15 seconds
- Template generation: Instant response
- Intelligent caching mechanism

### **Resource Usage**:
- Asynchronous request processing
- Timeout protection (30 seconds)
- Error retry mechanism

## 🔮 Future Extensions

### **Planned Features**:
- Support for more countries/regions
- Custom data fields
- Batch data export
- Data quality scoring

### **Integration Options**:
- Direct database insertion
- File download functionality
- API interface expansion
- Third-party service integration

## 📞 Technical Support

If you encounter any issues during use, please:

1. Check if the backend service is running normally
2. View browser console error messages
3. Check backend log files
4. Confirm OpenRouter API key configuration

---

**🎉 Enjoy the intelligent property generation feature!**

