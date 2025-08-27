/**
 * Properties Module
 * Responsible for loading and displaying property listings
 */

// Properties data storage
let propertiesData = [];

// Pagination variables
let currentPage = 1;
let itemsPerPage = 20;
let filteredProperties = [];

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
    console.log('🚀 Initializing Properties module...');
    console.log('📅 Properties.js loaded at:', new Date().toISOString());
    console.log('🔗 This file should use /api/properties endpoint');
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
 * Render properties in the grid with pagination
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
    
    // Set filtered properties to all properties initially
    filteredProperties = [...propertiesData];
    
    // Render current page
    renderCurrentPage();
    
    // Update pagination controls
    updatePagination();
    
    console.log(`🏠 Rendered ${propertiesData.length} properties with pagination`);
}

/**
 * Render current page of properties
 */
function renderCurrentPage() {
    const propertiesGrid = document.getElementById('propertiesGrid');
    if (!propertiesGrid) return;
    
    // Clear existing content
    propertiesGrid.innerHTML = '';
    
    // Calculate start and end indices for current page
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = Math.min(startIndex + itemsPerPage, filteredProperties.length);
    
    // Get properties for current page
    const currentPageProperties = filteredProperties.slice(startIndex, endIndex);
    
    if (currentPageProperties.length === 0) {
        propertiesGrid.innerHTML = `
            <div class="no-properties">
                <i class="fas fa-search"></i>
                <h3>No Properties Found</h3>
                <p>No properties match your current criteria on this page.</p>
            </div>
        `;
        return;
    }
    
    // Create property cards for current page
    currentPageProperties.forEach((property, index) => {
        const propertyCard = createPropertyCard(property, startIndex + index);
        propertiesGrid.appendChild(propertyCard);
    });
    
    console.log(`🏠 Rendered page ${currentPage}: ${currentPageProperties.length} properties (${startIndex + 1}-${endIndex} of ${filteredProperties.length})`);
}

/**
 * Update pagination controls
 */
function updatePagination() {
    const totalPages = Math.ceil(filteredProperties.length / itemsPerPage);
    
    // Update pagination info
    const paginationInfo = document.getElementById('paginationInfo');
    if (paginationInfo) {
        const startIndex = (currentPage - 1) * itemsPerPage + 1;
        const endIndex = Math.min(currentPage * itemsPerPage, filteredProperties.length);
        paginationInfo.textContent = `Showing ${startIndex}-${endIndex} of ${filteredProperties.length} properties`;
    }
    
    // Update pagination buttons
    updatePaginationButtons(totalPages);
    
    // Update page numbers
    updatePageNumbers(totalPages);
}

/**
 * Update pagination button states
 */
function updatePaginationButtons(totalPages) {
    const firstPageBtn = document.getElementById('firstPageBtn');
    const prevPageBtn = document.getElementById('prevPageBtn');
    const nextPageBtn = document.getElementById('nextPageBtn');
    const lastPageBtn = document.getElementById('lastPageBtn');
    
    if (firstPageBtn) firstPageBtn.disabled = currentPage === 1;
    if (prevPageBtn) prevPageBtn.disabled = currentPage === 1;
    if (nextPageBtn) nextPageBtn.disabled = currentPage === totalPages;
    if (lastPageBtn) lastPageBtn.disabled = currentPage === totalPages;
}

/**
 * Update page number buttons
 */
function updatePageNumbers(totalPages) {
    const pageNumbersContainer = document.getElementById('pageNumbers');
    if (!pageNumbersContainer) return;
    
    pageNumbersContainer.innerHTML = '';
    
    // Calculate range of page numbers to show
    let startPage = Math.max(1, currentPage - 2);
    let endPage = Math.min(totalPages, currentPage + 2);
    
    // Adjust range to always show 5 pages if possible
    if (endPage - startPage < 4) {
        if (startPage === 1) {
            endPage = Math.min(totalPages, startPage + 4);
        } else {
            startPage = Math.max(1, endPage - 4);
        }
    }
    
    // Add first page if not in range
    if (startPage > 1) {
        addPageNumber(1, pageNumbersContainer);
        if (startPage > 2) {
            addPageEllipsis(pageNumbersContainer);
        }
    }
    
    // Add page numbers in range
    for (let i = startPage; i <= endPage; i++) {
        addPageNumber(i, pageNumbersContainer);
    }
    
    // Add last page if not in range
    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            addPageEllipsis(pageNumbersContainer);
        }
        addPageNumber(totalPages, pageNumbersContainer);
    }
}

/**
 * Add a page number button
 */
function addPageNumber(pageNum, container) {
    const pageBtn = document.createElement('button');
    pageBtn.className = `page-number ${pageNum === currentPage ? 'active' : ''}`;
    pageBtn.textContent = pageNum;
    pageBtn.addEventListener('click', () => goToPage(pageNum));
    container.appendChild(pageBtn);
}

/**
 * Add page ellipsis
 */
function addPageEllipsis(container) {
    const ellipsis = document.createElement('span');
    ellipsis.className = 'page-ellipsis';
    ellipsis.textContent = '...';
    ellipsis.style.padding = 'var(--spacing-sm) var(--spacing-md)';
    ellipsis.style.color = 'var(--text-light)';
    container.appendChild(ellipsis);
}

/**
 * Navigate to specific page
 */
function goToPage(pageNum) {
    if (pageNum < 1 || pageNum > Math.ceil(filteredProperties.length / itemsPerPage)) {
        return;
    }
    
    currentPage = pageNum;
    renderCurrentPage();
    updatePagination();
    
    // Scroll to top of properties section
    const propertiesSection = document.getElementById('properties');
    if (propertiesSection) {
        propertiesSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

/**
 * Navigate to next page
 */
function goToNextPage() {
    const totalPages = Math.ceil(filteredProperties.length / itemsPerPage);
    if (currentPage < totalPages) {
        goToPage(currentPage + 1);
    }
}

/**
 * Navigate to previous page
 */
function goToPrevPage() {
    if (currentPage > 1) {
        goToPage(currentPage - 1);
    }
}

/**
 * Navigate to first page
 */
function goToFirstPage() {
    goToPage(1);
}

/**
 * Navigate to last page
 */
function goToLastPage() {
    const totalPages = Math.ceil(filteredProperties.length / itemsPerPage);
    goToPage(totalPages);
}

/**
 * Change items per page
 */
function changeItemsPerPage(newItemsPerPage) {
    itemsPerPage = parseInt(newItemsPerPage);
    currentPage = 1; // Reset to first page
    renderCurrentPage();
    updatePagination();
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
    
    // Debug logging for image URLs
    console.log(`Property ${property.property_id}: image_url = "${property.image_url}"`);
    
    card.innerHTML = `
        <div class="property-image">
            ${property.image_url ? `
                <img src="${property.image_url}" alt="${property.image_alt || property.location}" class="property-img" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                <div class="image-placeholder" style="display: none;">
                    <i class="fas fa-image"></i>
                    <span>Property Image</span>
                </div>
            ` : `
            <div class="image-placeholder">
                <i class="fas fa-image"></i>
                <span>Property Image</span>
            </div>
            `}
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
 * View property details in modal
 */
function viewPropertyDetails(propertyId) {
    const property = propertiesData.find(p => p.property_id === propertyId) || propertiesData[propertyId];
    if (!property) {
        showNotification('Property not found', 'error');
        return;
    }
    
    // Populate modal with property details
    populatePropertyDetailsModal(property);
    
    // Show modal
    const modal = document.getElementById('propertyDetailsModal');
    if (modal) {
        modal.classList.add('show');
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }
}

/**
 * Populate property details modal with data
 */
function populatePropertyDetailsModal(property) {
    const modalBody = document.getElementById('propertyDetailsBody');
    if (!modalBody) return;
    
    // Parse features and tags
    const features = property.features ? (Array.isArray(property.features) ? property.features : property.features.split(',')) : [];
    const tags = property.tags ? (Array.isArray(property.tags) ? property.tags : property.tags.split(',')) : [];
    
    // Generate Airbnb-style description
    const description = generatePropertyDescription(property, features, tags);
    
    modalBody.innerHTML = `
        <!-- Property Image Gallery -->
        <div class="property-image-gallery">
            ${property.image_url ? `
                <img src="${property.image_url}" alt="${property.image_alt || property.location}" class="main-property-image" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                <div class="image-placeholder-large" style="display: none;">
                    <i class="fas fa-image"></i>
                    <span>Property Image</span>
                </div>
            ` : `
                <div class="image-placeholder-large">
                    <i class="fas fa-image"></i>
                    <span>Property Image</span>
                </div>
            `}
        </div>
        
        <!-- Location Section -->
        <div class="property-info-section">
            <h4><i class="fas fa-map-marker-alt"></i> Location</h4>
            <div class="location-details">
                <i class="fas fa-map-marker-alt location-icon"></i>
                <span class="location-text">${property.location}</span>
            </div>
        </div>
        
        <!-- Features Section -->
        <div class="property-info-section">
            <h4><i class="fas fa-star"></i> Amenities & Features</h4>
            <div class="features-grid">
                ${features.length > 0 ? features.map(feature => `
                    <div class="feature-item">
                        <i class="fas fa-check"></i>
                        <span>${feature.trim()}</span>
                    </div>
                `).join('') : '<p>No features listed</p>'}
            </div>
        </div>
        
        <!-- Price Section -->
        <div class="property-info-section">
            <h4><i class="fas fa-dollar-sign"></i> Pricing</h4>
            <div class="price-details">
                <div>
                    <span class="price-amount">$${property.nightly_price}</span>
                    <span class="price-period">/night</span>
                </div>
            </div>
            <div class="price-breakdown">
                <div class="price-breakdown-item">
                    <span>Nightly Rate</span>
                    <span>$${property.nightly_price}</span>
                </div>
                <div class="price-breakdown-item">
                    <span>Service Fee</span>
                    <span>$${Math.round(property.nightly_price * 0.12)}</span>
                </div>
                <div class="price-breakdown-item">
                    <span>Total per Night</span>
                    <span>$${Math.round(property.nightly_price * 1.12)}</span>
                </div>
            </div>
        </div>
        
        <!-- Description Section -->
        <div class="property-info-section">
            <h4><i class="fas fa-info-circle"></i> About This Property</h4>
            <div class="description-content">
                ${description}
            </div>
        </div>
        
        <!-- Property Actions -->
        <div class="property-actions-modal">
            <button class="btn btn-primary" onclick="bookProperty(${property.property_id})">
                <i class="fas fa-calendar-check"></i>
                Book Now
            </button>
            <button class="btn btn-outline" onclick="saveProperty(${property.property_id})">
                <i class="fas fa-heart"></i>
                Save to Wishlist
            </button>
            <button class="btn btn-secondary" onclick="closePropertyDetailsModal()">
                <i class="fas fa-times"></i>
                Close
            </button>
        </div>
    `;
}

/**
 * Generate Airbnb-style property description
 */
function generatePropertyDescription(property, features, tags) {
    const location = property.location;
    const type = property.ptype || property.type;
    const price = property.nightly_price;
    
    let description = `<p>Welcome to this beautiful ${type.toLowerCase()} located in the heart of ${location}. This exceptional property offers the perfect blend of comfort, style, and convenience for your vacation experience.</p>`;
    
    if (features.length > 0) {
        const topFeatures = features.slice(0, 5);
        description += `<p>This ${type.toLowerCase()} comes equipped with premium amenities including ${topFeatures.map(f => f.trim()).join(', ')} to ensure your stay is nothing short of extraordinary.</p>`;
    }
    
    if (tags.length > 0) {
        const topTags = tags.slice(0, 3);
        description += `<p>Nestled in a ${topTags.map(t => t.trim()).join(', ')} area, this property provides the perfect setting for both relaxation and adventure.</p>`;
    }
    
    description += `<p>At just $${price} per night, this ${type.toLowerCase()} offers exceptional value for money, making it an ideal choice for travelers seeking quality accommodation without compromising on comfort or location.</p>`;
    
    description += `<p>Whether you're planning a romantic getaway, a family vacation, or a business trip, this ${type.toLowerCase()} provides the perfect home base for exploring ${location} and creating unforgettable memories.</p>`;
    
    return description;
}

/**
 * Close property details modal
 */
function closePropertyDetailsModal() {
    const modal = document.getElementById('propertyDetailsModal');
    if (modal) {
        modal.classList.remove('show');
        document.body.style.overflow = ''; // Restore scrolling
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
 * Save property to wishlist (placeholder function)
 */
function saveProperty(propertyId) {
    const property = propertiesData.find(p => p.property_id === propertyId) || propertiesData[propertyId];
    if (property) {
        showNotification(`${property.location} added to your wishlist!`, 'success');
        // TODO: Implement wishlist functionality
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

/**
 * Filter properties by budget range
 */
function filterPropertiesByBudget(minBudget, maxBudget) {
    console.log('🏠 Filtering properties by budget:', minBudget, '-', maxBudget);
    
    // Filter properties based on budget
    const filteredProperties = propertiesData.filter(property => {
        const price = property.nightly_price;
        return price >= minBudget && price <= maxBudget;
    });
    
    console.log('🏠 Properties after budget filter:', filteredProperties.length);
    
    // Update statistics with filtered data
    updateStatisticsWithData(filteredProperties);
    
    // Render filtered properties
    renderPropertiesWithData(filteredProperties);
}

/**
 * Filter properties by selected features
 */
function filterPropertiesByFeatures(selectedFeatures) {
    console.log('🏠 Filtering properties by features:', selectedFeatures);
    
    // Filter properties based on features
    const filteredProperties = propertiesData.filter(property => {
        return window.Features && window.Features.propertyMatchesFeatures(property, selectedFeatures);
    });
    
    console.log('🏠 Properties after features filter:', filteredProperties.length);
    
    // Update statistics with filtered data
    updateStatisticsWithData(filteredProperties);
    
    // Render filtered properties
    renderPropertiesWithData(filteredProperties);
}

/**
 * Update statistics with specific data
 */
function updateStatisticsWithData(properties) {
    const totalProperties = properties.length;
    const uniqueLocations = new Set(properties.map(p => p.location.split(',')[0])).size;
    const avgPrice = totalProperties > 0 ? Math.round(properties.reduce((sum, p) => sum + p.nightly_price, 0) / totalProperties) : 0;
    
    // Update DOM elements
    const totalPropertiesEl = document.getElementById('totalProperties');
    const totalLocationsEl = document.getElementById('totalLocations');
    const avgPriceEl = document.getElementById('avgPrice');
    
    if (totalPropertiesEl) totalPropertiesEl.textContent = totalProperties;
    if (totalLocationsEl) totalLocationsEl.textContent = uniqueLocations;
    if (avgPriceEl) avgPriceEl.textContent = `$${avgPrice}`;
}

/**
 * Render properties with specific data
 */
function renderPropertiesWithData(properties) {
    const propertiesGrid = document.getElementById('propertiesGrid');
    if (!propertiesGrid) {
        console.error('Properties grid not found');
        return;
    }
    
    // Clear existing content
    propertiesGrid.innerHTML = '';
    
    // Safely handle undefined or null properties
    if (!properties || !Array.isArray(properties)) {
        console.warn('renderPropertiesWithData: Invalid properties data:', properties);
        propertiesGrid.innerHTML = `
            <div class="no-properties">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>Data Error</h3>
                <p>Unable to load properties. Please refresh the page.</p>
            </div>
        `;
        return;
    }
    
    if (properties.length === 0) {
        propertiesGrid.innerHTML = `
            <div class="no-properties">
                <i class="fas fa-search"></i>
                <h3>No Properties Found</h3>
                <p>No properties match your current criteria. Try adjusting your filters.</p>
            </div>
        `;
        return;
    }
    
    // Update filtered properties and reset to first page
    filteredProperties = [...properties];
    currentPage = 1;
    
    // Render current page
    renderCurrentPage();
    
    // Update pagination controls
    updatePagination();
    
    console.log(`🏠 Rendered ${properties.length} filtered properties with pagination`);
}

// Initialize properties when page loads
document.addEventListener('DOMContentLoaded', () => {
    initProperties();
    initPagination();
});

// Listen for budget changes
document.addEventListener('budgetChanged', (event) => {
    console.log('🏠 Budget changed, filtering properties:', event.detail);
    filterPropertiesByBudget(event.detail.minBudget, event.detail.maxBudget);
});

// Listen for features changes
document.addEventListener('featuresChanged', (event) => {
    console.log('🏠 Features changed, filtering properties:', event.detail);
    filterPropertiesByFeatures(event.detail.selectedFeatures);
});

/**
 * Initialize pagination event listeners
 */
function initPagination() {
    // First page button
    const firstPageBtn = document.getElementById('firstPageBtn');
    if (firstPageBtn) {
        firstPageBtn.addEventListener('click', goToFirstPage);
    }
    
    // Previous page button
    const prevPageBtn = document.getElementById('prevPageBtn');
    if (prevPageBtn) {
        prevPageBtn.addEventListener('click', goToPrevPage);
    }
    
    // Next page button
    const nextPageBtn = document.getElementById('nextPageBtn');
    if (nextPageBtn) {
        nextPageBtn.addEventListener('click', goToNextPage);
    }
    
    // Last page button
    const lastPageBtn = document.getElementById('lastPageBtn');
    if (lastPageBtn) {
        lastPageBtn.addEventListener('click', goToLastPage);
    }
    
    // Items per page selector
    const itemsPerPageSelect = document.getElementById('itemsPerPage');
    if (itemsPerPageSelect) {
        itemsPerPageSelect.addEventListener('change', (e) => {
            changeItemsPerPage(e.target.value);
        });
    }
    
    console.log('🏠 Pagination initialized');
}

/**
 * Get properties data for external use
 */
function getPropertiesData() {
    return propertiesData;
}

// Export properties functions
window.Properties = {
    loadProperties,
    renderProperties,
    filterProperties,
    searchProperties,
    viewPropertyDetails,
    bookProperty,
    saveProperty,
    closePropertyDetailsModal,
    getPropertiesData,
    updateStatisticsWithData,
    renderPropertiesWithData,
    // Pagination functions
    goToPage,
    goToNextPage,
    goToPrevPage,
    goToFirstPage,
    goToLastPage,
    changeItemsPerPage
};

console.log('Properties module loaded:', window.Properties);
