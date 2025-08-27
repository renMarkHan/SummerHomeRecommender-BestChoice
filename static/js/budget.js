/**
 * Budget Management Module
 * Handles budget slider functionality and database operations
 */

// Budget state
let budgetState = {
    minBudget: 0,
    maxBudget: 1000,
    maxPropertyPrice: 1000,
    applyTimeout: null
};

/**
 * Initialize budget module
 */
function initBudget() {
    console.log('💰 Initializing Budget module...');
    
    // Get DOM elements
    const minBudgetSlider = document.getElementById('minBudget');
    const maxBudgetSlider = document.getElementById('maxBudget');
    const minBudgetValue = document.getElementById('minBudgetValue');
    const maxBudgetValue = document.getElementById('maxBudgetValue');
    
    if (!minBudgetSlider || !maxBudgetSlider || !minBudgetValue || !maxBudgetValue) {
        console.error('Budget elements not found');
        return;
    }
    
    // Load max property price and set slider ranges
    loadMaxPropertyPrice();
    
    // Load user's saved budget from database
    loadUserBudget();
    
    // Bind event listeners
    bindBudgetEvents(minBudgetSlider, maxBudgetSlider, minBudgetValue, maxBudgetValue);
    
    console.log('💰 Budget module initialized');
}

/**
 * Load maximum property price from database to set slider range
 */
async function loadMaxPropertyPrice() {
    try {
        const response = await fetch('/api/properties');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        const properties = data.properties || [];
        
        if (properties.length > 0) {
            // Use numpy-like approach to find max price
            const prices = properties.map(p => p.nightly_price);
            budgetState.maxPropertyPrice = Math.max(...prices);
            
            console.log('💰 Max property price:', budgetState.maxPropertyPrice);
            
            // Update slider ranges
            updateSliderRanges();
        }
    } catch (error) {
        console.error('Failed to load max property price:', error);
        // Use default value
        budgetState.maxPropertyPrice = 1000;
    }
}

/**
 * Update slider ranges based on max property price
 */
function updateSliderRanges() {
    const minBudgetSlider = document.getElementById('minBudget');
    const maxBudgetSlider = document.getElementById('maxBudget');
    
    if (minBudgetSlider && maxBudgetSlider) {
        const maxPrice = Math.ceil(budgetState.maxPropertyPrice * 1.1); // Add 10% buffer
        
        minBudgetSlider.max = maxPrice;
        maxBudgetSlider.max = maxPrice;
        
        // Update current values if they exceed new max
        if (budgetState.minBudget > maxPrice) {
            budgetState.minBudget = 0;
            minBudgetSlider.value = 0;
        }
        if (budgetState.maxBudget > maxPrice) {
            budgetState.maxBudget = maxPrice;
            maxBudgetSlider.value = maxPrice;
        }
        
        // Update display
        updateBudgetDisplay();
    }
}

/**
 * Load user's saved budget from database
 */
async function loadUserBudget() {
    try {
        const userId = localStorage.getItem('userId');
        if (!userId) {
            console.log('No user ID found, using default budget');
            return;
        }
        
        // For now, we'll use localStorage as fallback
        // In a real app, you'd fetch from database
        const savedMinBudget = localStorage.getItem('minBudget');
        const savedMaxBudget = localStorage.getItem('maxBudget');
        
        if (savedMinBudget && savedMaxBudget) {
            budgetState.minBudget = parseInt(savedMinBudget);
            budgetState.maxBudget = parseInt(savedMaxBudget);
            
            // Update sliders
            const minBudgetSlider = document.getElementById('minBudget');
            const maxBudgetSlider = document.getElementById('maxBudget');
            
            if (minBudgetSlider && maxBudgetSlider) {
                minBudgetSlider.value = budgetState.minBudget;
                maxBudgetSlider.value = budgetState.maxBudget;
                updateBudgetDisplay();
            }
        }
    } catch (error) {
        console.error('Failed to load user budget:', error);
    }
}

/**
 * Bind budget slider events
 */
function bindBudgetEvents(minSlider, maxSlider, minValue, maxValue) {
    // Min budget slider
    minSlider.addEventListener('input', (e) => {
        const value = parseInt(e.target.value);
        budgetState.minBudget = value;
        
        // Ensure min doesn't exceed max
        if (value > budgetState.maxBudget) {
            budgetState.maxBudget = value;
            maxSlider.value = value;
        }
        
        updateBudgetDisplay();
        
        // Save budget to database only, don't auto-apply filter
        saveBudgetToDatabase();
        
        // Enable filter button when budget changes
        enableFilterButton();
    });
    
    // Max budget slider
    maxSlider.addEventListener('input', (e) => {
        const value = parseInt(e.target.value);
        budgetState.maxBudget = value;
        
        // Ensure max doesn't go below min
        if (value < budgetState.minBudget) {
            budgetState.minBudget = value;
            minSlider.value = value;
        }
        
        updateBudgetDisplay();
        
        // Save budget to database only, don't auto-apply filter
        saveBudgetToDatabase();
        
        // Enable filter button when budget changes
        enableFilterButton();
    });
}

/**
 * Update budget display values
 */
function updateBudgetDisplay() {
    const minBudgetValue = document.getElementById('minBudgetValue');
    const maxBudgetValue = document.getElementById('maxBudgetValue');
    
    if (minBudgetValue && maxBudgetValue) {
        minBudgetValue.textContent = `$${budgetState.minBudget}`;
        maxBudgetValue.textContent = `$${budgetState.maxBudget}`;
    }
}

/**
 * Save budget to database
 */
async function saveBudgetToDatabase() {
    try {
        const userId = localStorage.getItem('userId');
        if (!userId) {
            console.log('No user ID found, saving to localStorage');
            localStorage.setItem('minBudget', budgetState.minBudget);
            localStorage.setItem('maxBudget', budgetState.maxBudget);
            return;
        }
        
        // Save to localStorage for now
        localStorage.setItem('minBudget', budgetState.minBudget);
        localStorage.setItem('maxBudget', budgetState.maxBudget);
        
        console.log('💰 Budget saved:', budgetState);
        
        // Show success notification
        if (window.UI && window.UI.showNotification) {
            window.UI.showNotification('Budget settings saved successfully!', 'success');
        }
        
    } catch (error) {
        console.error('Failed to save budget:', error);
        if (window.UI && window.UI.showNotification) {
            window.UI.showNotification('Failed to save budget settings', 'error');
        }
    }
}

/**
 * Apply budget filter to properties
 */
function applyBudgetFilter() {
    console.log('💰 Applying budget filter:', budgetState);
    
    // Get current features filter state
    const featuresState = window.Features ? window.Features.getFeaturesState() : { selectedFeatures: [] };
    
    // Apply combined filter
    applyCombinedFilter(budgetState.minBudget, budgetState.maxBudget, featuresState.selectedFeatures);
}

/**
 * Reset budget to default values
 */
function resetBudget() {
    budgetState.minBudget = 0;
    budgetState.maxBudget = budgetState.maxPropertyPrice;
    
    const minBudgetSlider = document.getElementById('minBudget');
    const maxBudgetSlider = document.getElementById('maxBudget');
    
    if (minBudgetSlider && maxBudgetSlider) {
        minBudgetSlider.value = budgetState.minBudget;
        maxBudgetSlider.value = budgetState.maxBudget;
        updateBudgetDisplay();
    }
    
    console.log('💰 Budget reset to default');
    
    // Enable filter button after reset
    enableFilterButton();
}

/**
 * Enable filter button when any filter changes
 */
function enableFilterButton() {
    const filterBtn = document.getElementById('filterBtn');
    if (filterBtn) {
        filterBtn.disabled = false;
        filterBtn.style.opacity = '1';
    }
}

/**
 * Disable filter button after filtering is applied
 */
function disableFilterButton() {
    const filterBtn = document.getElementById('filterBtn');
    if (filterBtn) {
        filterBtn.disabled = true;
        filterBtn.style.opacity = '0.6';
    }
}

/**
 * Get current budget state
 */
function getBudgetState() {
    return { ...budgetState };
}

/**
 * Apply combined filter using vectorized backend filtering
 * @param {number} minBudget - Minimum budget
 * @param {number} maxBudget - Maximum budget
 * @param {Array} selectedFeatures - Selected features
 * @param {Array} selectedPropertyTypes - Selected property types
 */
async function applyCombinedFilter(minBudget, maxBudget, selectedFeatures, selectedPropertyTypes) {
    console.log('🚀 Applying vectorized combined filter:', {
        minBudget,
        maxBudget,
        selectedFeatures,
        selectedPropertyTypes
    });
    
    try {
        // Prepare filter parameters for backend
        const filterParams = {
            budget_range: [minBudget, maxBudget],
            features: selectedFeatures && selectedFeatures.length > 0 ? selectedFeatures : null,
            property_types: selectedPropertyTypes && selectedPropertyTypes.length > 0 ? selectedPropertyTypes : null,
            case_sensitive: false
        };
        
        console.log('🚀 Sending filter request to backend:', filterParams);
        
        // Use vectorized filtering API
        if (window.API && window.API.filterProperties) {
            const response = await window.API.filterProperties(filterParams);
            
            console.log('🚀 Vectorized filtering response:', response);
            
            if (response && response.properties) {
                // Update statistics and render filtered properties
                if (window.Properties && window.Properties.updateStatisticsWithData) {
                    window.Properties.updateStatisticsWithData(response.properties);
                    window.Properties.renderPropertiesWithData(response.properties);
                }
                
                // Show success notification
                if (window.UI && window.UI.showNotification) {
                    window.UI.showNotification(
                        `Found ${response.properties.length} matching properties using vectorized filtering!`, 
                        'success'
                    );
                }
            } else {
                console.warn('🚀 No properties returned from vectorized filtering');
                if (window.Properties && window.Properties.updateStatisticsWithData) {
                    window.Properties.updateStatisticsWithData([]);
                    window.Properties.renderPropertiesWithData([]);
                }
            }
        } else {
            console.error('🚀 Vectorized filtering API not available, falling back to client-side filtering');
            applyClientSideFilter(minBudget, maxBudget, selectedFeatures, selectedPropertyTypes);
        }
        
    } catch (error) {
        console.error('🚀 Vectorized filtering failed:', error);
        
        // Fallback to client-side filtering
        console.log('🚀 Falling back to client-side filtering...');
        applyClientSideFilter(minBudget, maxBudget, selectedFeatures, selectedPropertyTypes);
        
        // Show error notification
        if (window.UI && window.UI.showNotification) {
            window.UI.showNotification(
                'Vectorized filtering failed, using client-side filtering instead', 
                'warning'
            );
        }
    }
}

/**
 * Fallback client-side filtering (original implementation)
 */
function applyClientSideFilter(minBudget, maxBudget, selectedFeatures, selectedPropertyTypes) {
    console.log('🔧 Applying client-side filter as fallback');
    
    // Check if there's a location filter state
    let baseProperties = [];
    const locationFilterState = localStorage.getItem('locationFilterState');
    const filteredByLocation = localStorage.getItem('filteredByLocation');
    
    if (locationFilterState && filteredByLocation) {
        try {
            const state = JSON.parse(locationFilterState);
            const locationProperties = JSON.parse(filteredByLocation);
            
            // Check if location filter is still valid (not expired)
            const isExpired = Date.now() - state.timestamp > 24 * 60 * 60 * 1000;
            
            if (!isExpired && locationProperties.length > 0) {
                console.log(`🔧 Using location-filtered properties (${locationProperties.length} properties near ${state.location})`);
                baseProperties = locationProperties;
            } else {
                console.log('🔧 Location filter expired, using all properties');
                baseProperties = window.Properties.getPropertiesData() || [];
                // Clear expired state
                localStorage.removeItem('locationFilterState');
                localStorage.removeItem('filteredByLocation');
            }
        } catch (error) {
            console.error('🔧 Error parsing location filter state, using all properties:', error);
            baseProperties = window.Properties.getPropertiesData() || [];
            // Clear corrupted state
            localStorage.removeItem('locationFilterState');
            localStorage.removeItem('filteredByLocation');
        }
    } else {
        // No location filter, use all properties
        console.log('🔧 No location filter, using all properties');
        baseProperties = window.Properties.getPropertiesData() || [];
    }
    
    if (baseProperties.length === 0) {
        console.error('No properties data available');
        return;
    }
    
    console.log(`🔧 Base properties for filtering: ${baseProperties.length}`);
    
    // Filter properties by budget first
    const budgetFiltered = baseProperties.filter(property => {
        const price = property.nightly_price;
        return price >= minBudget && price <= maxBudget;
    });
    
    console.log('🔧 Properties after budget filter:', budgetFiltered.length);
    
    // Then filter by features
    const featuresFiltered = budgetFiltered.filter(property => {
        return window.Features && window.Features.propertyMatchesFeatures(property, selectedFeatures);
    });
    
    console.log('🔧 Properties after features filter:', featuresFiltered.length);
    
    // Finally filter by property types
    const finalFiltered = featuresFiltered.filter(property => {
        return window.PropertyTypes && window.PropertyTypes.propertyMatchesTypes(property, selectedPropertyTypes);
        });
    
    console.log('🔧 Properties after all filters:', finalFiltered.length);
    
    // Update statistics and render
    if (window.Properties && window.Properties.updateStatisticsWithData) {
        window.Properties.updateStatisticsWithData(finalFiltered);
        window.Properties.renderPropertiesWithData(finalFiltered);
    }
}

// Initialize budget when page loads
document.addEventListener('DOMContentLoaded', initBudget);

// Export budget functions
window.Budget = {
    initBudget,
    getBudgetState,
    applyBudgetFilter,
    resetBudget,
    saveBudgetToDatabase,
    applyCombinedFilter,
    applyClientSideFilter,
    enableFilterButton,
    disableFilterButton
};

console.log('💰 Budget module loaded:', window.Budget);
