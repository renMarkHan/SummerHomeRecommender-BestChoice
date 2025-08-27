/**
 * Properties Module
 * Responsible for loading and displaying property listings
 */

// Properties data storage
let propertiesData = [];

// Property types with icons mapping
const PROPERTY_TYPE_ICONS = {
    'Apartment': 'fas fa-building',
    'Condo': 'fas fa-building',
    'House': 'fas fa-home',
    'Villa': 'fas fa-home',
    'Loft': 'fas fa-building',
    'Townhouse': 'fas fa-home',
    'Chalet': 'fas fa-mountain',
    'Cabin': 'fas fa-tree',
    'Bungalow': 'fas fa-home'
};

// Environment types with icons mapping
const ENVIRONMENT_ICONS = {
    'mountain': 'fas fa-mountain',
    'lake': 'fas fa-water',
    'beach': 'fas fa-umbrella-beach',
    'city': 'fas fa-city',
    'ski resort': 'fas fa-skiing',
    'harbour': 'fas fa-ship',
    'ocean': 'fas fa-water',
    'garden': 'fas fa-seedling',
    'historic': 'fas fa-landmark',
    'downtown': 'fas fa-city',
    'quiet': 'fas fa-volume-mute'
};

/**
 * Initialize properties module
 */
function initProperties() {
    console.log('Initializing Properties module...');
    loadProperties();
}

/**
 * Load properties data from database via API
 */
async function loadProperties() {
    try {
        console.log('🔄 Starting to load properties from database...');
        showLoading();
        
        // Call the new API endpoint to get properties from database
        const apiUrl = '/api/properties';
        console.log('📡 Calling API endpoint:', apiUrl);
        
        const response = await fetch(apiUrl);
        console.log('📥 API response status:', response.status);
        console.log('📥 API response ok:', response.ok);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('📊 Raw API response data:', data);
        
        propertiesData = data.properties || [];
        console.log('🏠 Properties loaded from database:', propertiesData.length);
        console.log('🏠 Properties data:', propertiesData);
        
        // Update statistics
        updateStatistics();
        
        // Render properties
        renderProperties();
        
        hideLoading();
        
    } catch (error) {
        console.error('❌ Failed to load properties from database:', error);
        hideLoading();
        showNotification('Failed to load properties from database. Please try again later.', 'error');
        
        // Fallback: use sample data for demonstration
        console.log('🔄 Falling back to sample properties...');
        loadSampleProperties();
    }
}

/**
 * Load sample properties data as fallback
 */
function loadSampleProperties() {
    propertiesData = [
        {
            "property_id": 1,
            "location": "Toronto, Canada",
            "type": "Apartment",
            "nightly_price": 120,
            "features": "WiFi,Kitchen,Heating",
            "tags": "Downtown,Close to subway"
        },
        {
            "property_id": 2,
            "location": "Vancouver, Canada",
            "type": "Condo",
            "nightly_price": 150,
            "features": "WiFi,Parking,Balcony",
            "tags": "Sea view,Near park"
        },
        {
            "property_id": 3,
            "location": "Banff, Canada",
            "type": "Cabin",
            "nightly_price": 220,
            "features": "WiFi,Fireplace,Parking",
            "tags": "Mountain view,Near hiking trails"
        }
    ];
    
    updateStatistics();
    renderProperties();
}

/**
 * Update statistics display
 */
function updateStatistics() {
    const totalProperties = propertiesData.length;
    const uniqueLocations = new Set(propertiesData.map(p => p.location.split(',')[0])).size;
    const avgPrice = totalProperties > 0 ? Math.round(propertiesData.reduce((sum, p) => sum + p.nightly_price, 0) / totalProperties) : 0;
    
    // Update DOM elements
    const totalPropertiesEl = document.getElementById('totalProperties');
    const totalLocationsEl = document.getElementById('totalLocations');
    const avgPriceEl = document.getElementById('avgPrice');
    
    if (totalPropertiesEl) totalPropertiesEl.textContent = totalProperties;
    if (totalLocationsEl) totalLocationsEl.textContent = uniqueLocations;
    if (avgPriceEl) avgPriceEl.textContent = `$${avgPrice}`;
}

/**
 * Render properties in the grid
 */
function renderProperties() {
    const propertiesGrid = document.getElementById('propertiesGrid');
    if (!propertiesGrid) {
        console.error('Properties grid not found');
        return;
    }
    
    // Clear existing content
    propertiesGrid.innerHTML = '';
    
    if (propertiesData.length === 0) {
        propertiesGrid.innerHTML = `
            <div class="no-properties">
                <i class="fas fa-home"></i>
                <h3>No Properties Available</h3>
                <p>No properties found in the database. Please check back later.</p>
            </div>
        `;
        return;
    }
    
    // Create property cards
    propertiesData.forEach((property, index) => {
        const propertyCard = createPropertyCard(property, index);
        propertiesGrid.appendChild(propertyCard);
    });
    
    console.log(`Rendered ${propertiesData.length} property cards`);
}

/**
 * Create a property card element
 */
function createPropertyCard(property, index) {
    const card = document.createElement('div');
    card.className = 'property-card';
    card.setAttribute('data-property-id', property.property_id || index);
    
    // Get property type icon
    const typeIcon = PROPERTY_TYPE_ICONS[property.type] || 'fas fa-home';
    
    // Parse features and tags
    const features = property.features ? property.features.split(',') : [];
    const tags = property.tags ? property.tags.split(',') : [];
    
    // Determine environment type for icon
    const environmentIcon = getEnvironmentIcon(property.location, property.tags);
    
    card.innerHTML = `
        <div class="property-image">
            <div class="image-placeholder">
                <i class="fas fa-image"></i>
                <span>Property Image</span>
            </div>
            <div class="property-type-badge">
                <i class="${typeIcon}"></i>
                ${property.type}
            </div>
            <div class="price-badge">
                $${property.nightly_price}
                <small>/night</small>
            </div>
        </div>
        
        <div class="property-content">
            <div class="property-header">
                <h3 class="property-title">
                    <i class="${environmentIcon}"></i>
                    ${property.location}
                </h3>
                <div class="property-rating">
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <span class="rating-text">5.0</span>
                </div>
            </div>
            
            <div class="property-features">
                ${features.map(feature => `
                    <span class="feature-tag">
                        <i class="fas fa-check"></i>
                        ${feature.trim()}
                    </span>
                `).join('')}
            </div>
            
            <div class="property-tags">
                ${tags.map(tag => `
                    <span class="tag">
                        ${tag.trim()}
                    </span>
                `).join('')}
            </div>
            
            <div class="property-actions">
                <button class="btn btn-outline" onclick="viewPropertyDetails(${property.property_id || index})">
                    <i class="fas fa-eye"></i>
                    View Details
                </button>
                <button class="btn btn-primary" onclick="bookProperty(${property.property_id || index})">
                    <i class="fas fa-calendar-check"></i>
                    Book Now
                </button>
            </div>
        </div>
    `;
    
    return card;
}

/**
 * Get environment icon based on location and tags
 */
function getEnvironmentIcon(location, tags) {
    const locationLower = location.toLowerCase();
    const tagsLower = tags.toLowerCase();
    
    if (tagsLower.includes('mountain') || tagsLower.includes('ski resort')) {
        return ENVIRONMENT_ICONS.mountain;
    } else if (tagsLower.includes('lake') || tagsLower.includes('harbour')) {
        return ENVIRONMENT_ICONS.lake;
    } else if (tagsLower.includes('beach') || tagsLower.includes('ocean') || tagsLower.includes('beachfront')) {
        return ENVIRONMENT_ICONS.beach;
    } else if (tagsLower.includes('downtown') || tagsLower.includes('city center')) {
        return ENVIRONMENT_ICONS.city;
    } else if (tagsLower.includes('garden')) {
        return ENVIRONMENT_ICONS.garden;
    } else if (tagsLower.includes('historic')) {
        return ENVIRONMENT_ICONS.historic;
    } else if (tagsLower.includes('quiet')) {
        return ENVIRONMENT_ICONS.quiet;
    }
    
    // Default to city icon
    return ENVIRONMENT_ICONS.city;
}

/**
 * View property details (placeholder function)
 */
function viewPropertyDetails(propertyId) {
    const property = propertiesData.find(p => p.property_id === propertyId) || propertiesData[propertyId];
    if (property) {
        showNotification(`Viewing details for ${property.location}`, 'info');
        // TODO: Implement detailed view modal
    }
}

/**
 * Book property (placeholder function)
 */
function bookProperty(propertyId) {
    const property = propertiesData.find(p => p.property_id === propertyId) || propertiesData[propertyId];
    if (property) {
        showNotification(`Booking ${property.location} for $${property.nightly_price}/night`, 'success');
        // TODO: Implement booking functionality
    }
}

/**
 * Filter properties by criteria (placeholder for future use)
 */
function filterProperties(criteria) {
    // TODO: Implement filtering functionality
    console.log('Filtering properties by:', criteria);
}

/**
 * Search properties (placeholder for future use)
 */
function searchProperties(query) {
    // TODO: Implement search functionality
    console.log('Searching properties for:', query);
}

// Initialize properties when page loads
document.addEventListener('DOMContentLoaded', initProperties);

// Export properties functions
window.Properties = {
    loadProperties,
    renderProperties,
    filterProperties,
    searchProperties,
    viewPropertyDetails,
    bookProperty
};

console.log('Properties module loaded:', window.Properties);
