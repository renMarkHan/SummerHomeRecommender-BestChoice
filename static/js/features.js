/**
 * Features Filter Module
 * Handles feature-based property filtering
 */

// Features state
let featuresState = {
    allFeatures: [],
    selectedFeatures: new Set(),
    isPanelOpen: false
};

/**
 * Initialize features filter module
 */
function initFeatures() {
    console.log('🔧 Initializing Features Filter module...');
    
    // Get DOM elements
    const featuresToggle = document.getElementById('featuresToggle');
    const featuresPanel = document.getElementById('featuresPanel');
    const featuresList = document.getElementById('featuresList');
    const clearFeaturesBtn = document.getElementById('clearFeatures');
    const selectedFeaturesCount = document.getElementById('selectedFeaturesCount');
    
    if (!featuresToggle || !featuresPanel || !featuresList || !clearFeaturesBtn || !selectedFeaturesCount) {
        console.error('Features filter elements not found');
        return;
    }
    
    // Load unique features from database
    loadUniqueFeatures();
    
    // Bind event listeners
    bindFeaturesEvents(featuresToggle, featuresPanel, featuresList, clearFeaturesBtn, selectedFeaturesCount);
    
    console.log('🔧 Features Filter module initialized');
}

/**
 * Load unique features from database properties using vectorized backend
 */
async function loadUniqueFeatures() {
    try {
        console.log('🔍 Loading unique features using vectorized backend...');
        
        // Use vectorized filtering API to get filter options
        if (window.API && window.API.getFilterOptions) {
            const filterOptions = await window.API.getFilterOptions();
            
            if (filterOptions && filterOptions.features) {
                console.log('🚀 Vectorized features loaded:', filterOptions.features);
                featuresState.allFeatures = filterOptions.features;
                renderFeaturesList();
                return;
            }
        }
        
        // Fallback to direct API call
        console.log('🔍 Falling back to direct API call...');
        const response = await fetch('/api/properties');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        const properties = data.properties || [];
        
        if (properties.length > 0) {
            // Extract all features from properties
            const allFeatures = [];
            properties.forEach(property => {
                if (property.features) {
                    // Split features by comma and clean up
                    const propertyFeatures = property.features.split(',').map(f => f.trim());
                    allFeatures.push(...propertyFeatures);
                }
            });
            
            // Remove duplicates (case-insensitive) and sort
            const uniqueFeatures = [...new Set(allFeatures.map(f => f.toLowerCase()))]
                .map(f => f.charAt(0).toUpperCase() + f.slice(1))
                .sort();
            
            featuresState.allFeatures = uniqueFeatures;
            
            console.log('🔧 Fallback features loaded:', uniqueFeatures);
            
            // Render features list
            renderFeaturesList();
        }
    } catch (error) {
        console.error('Failed to load unique features:', error);
        // Use fallback features
        featuresState.allFeatures = ['WiFi', 'Kitchen', 'Parking', 'Heating', 'Air Conditioning', 'Fireplace', 'Balcony', 'Pool', 'Garden'];
        renderFeaturesList();
    }
}

/**
 * Render features list in the dropdown
 */
function renderFeaturesList() {
    const featuresList = document.getElementById('featuresList');
    if (!featuresList) return;
    
    featuresList.innerHTML = '';
    
    featuresState.allFeatures.forEach(feature => {
        const featureItem = document.createElement('div');
        featureItem.className = 'feature-checkbox';
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = `feature-${feature.toLowerCase().replace(/\s+/g, '-')}`;
        checkbox.value = feature;
        checkbox.checked = featuresState.selectedFeatures.has(feature);
        
        const label = document.createElement('label');
        label.htmlFor = `feature-${feature.toLowerCase().replace(/\s+/g, '-')}`;
        label.textContent = feature;
        
        featureItem.appendChild(checkbox);
        featureItem.appendChild(label);
        
        // Add change event listener
        checkbox.addEventListener('change', (e) => {
            if (e.target.checked) {
                featuresState.selectedFeatures.add(feature);
            } else {
                featuresState.selectedFeatures.delete(feature);
            }
            updateSelectedFeaturesCount();
            
            // Enable filter button when features change
            if (window.Budget && window.Budget.enableFilterButton) {
                window.Budget.enableFilterButton();
            }
        });
        
        featuresList.appendChild(featureItem);
    });
}

/**
 * Bind features filter events
 */
function bindFeaturesEvents(toggle, panel, list, clearBtn, countElement) {
    // Toggle dropdown
    toggle.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleFeaturesPanel();
    });
    
    // Close panel when clicking outside
    document.addEventListener('click', (e) => {
        if (!panel.contains(e.target) && !toggle.contains(e.target)) {
            closeFeaturesPanel();
        }
    });
    
    // Clear all features
    clearBtn.addEventListener('click', () => {
        clearAllFeatures();
    });
    
    // Prevent panel clicks from closing it
    panel.addEventListener('click', (e) => {
        e.stopPropagation();
    });
}

/**
 * Toggle features panel
 */
function toggleFeaturesPanel() {
    const toggle = document.getElementById('featuresToggle');
    const panel = document.getElementById('featuresPanel');
    
    if (featuresState.isPanelOpen) {
        closeFeaturesPanel();
    } else {
        openFeaturesPanel();
    }
}

/**
 * Open features panel
 */
function openFeaturesPanel() {
    const toggle = document.getElementById('featuresToggle');
    const panel = document.getElementById('featuresPanel');
    
    featuresState.isPanelOpen = true;
    toggle.classList.add('active');
    panel.classList.add('show');
}

/**
 * Close features panel
 */
function closeFeaturesPanel() {
    const toggle = document.getElementById('featuresToggle');
    const panel = document.getElementById('featuresPanel');
    
    featuresState.isPanelOpen = false;
    toggle.classList.remove('active');
    panel.classList.remove('show');
}

/**
 * Clear all selected features
 */
function clearAllFeatures() {
    featuresState.selectedFeatures.clear();
    
    // Update checkboxes
    featuresState.allFeatures.forEach(feature => {
        const checkbox = document.getElementById(`feature-${feature.toLowerCase().replace(/\s+/g, '-')}`);
        if (checkbox) {
            checkbox.checked = false;
        }
    });
    
    updateSelectedFeaturesCount();
    
    // Enable filter button when features change
    if (window.Budget && window.Budget.enableFilterButton) {
        window.Budget.enableFilterButton();
    }
}

/**
 * Update selected features count display
 */
function updateSelectedFeaturesCount() {
    const countElement = document.getElementById('selectedFeaturesCount');
    if (!countElement) return;
    
    const count = featuresState.selectedFeatures.size;
    if (count === 0) {
        countElement.textContent = 'All';
    } else if (count === 1) {
        countElement.textContent = '1 Feature';
    } else {
        countElement.textContent = `${count} Features`;
    }
}

/**
 * Apply features filter to properties
 */
function applyFeaturesFilter() {
    console.log('🔧 Applying features filter:', Array.from(featuresState.selectedFeatures));
    
    // Get current budget and property types filter state
    const budgetState = window.Budget ? window.Budget.getBudgetState() : { minBudget: 0, maxBudget: 10000 };
    const propertyTypesState = window.PropertyTypes ? window.PropertyTypes.getPropertyTypesState() : { selectedPropertyTypes: [] };
    
    console.log('🔧 Current filter states:', { budgetState, propertyTypesState });
    
    // Apply combined filter
    if (window.Budget && typeof window.Budget.applyCombinedFilter === 'function') {
        console.log('🔧 Calling combined filter...');
        window.Budget.applyCombinedFilter(
            budgetState.minBudget, 
            budgetState.maxBudget, 
            Array.from(featuresState.selectedFeatures),
            propertyTypesState.selectedPropertyTypes
        );
    } else {
        console.error('🔧 Budget module or applyCombinedFilter not available');
        console.log('🔧 Available Budget methods:', window.Budget ? Object.keys(window.Budget) : 'Budget module not found');
    }
}

/**
 * Get current features state
 */
function getFeaturesState() {
    return {
        allFeatures: [...featuresState.allFeatures],
        selectedFeatures: Array.from(featuresState.selectedFeatures)
    };
}

/**
 * Check if a property matches selected features
 */
function propertyMatchesFeatures(property, selectedFeatures) {
    console.log('🔧 Checking property features match:', {
        property: property.location || 'Unknown',
        propertyFeatures: property.features,
        selectedFeatures: selectedFeatures
    });
    
    if (!selectedFeatures || selectedFeatures.length === 0) {
        console.log('🔧 No features selected, showing all properties');
        return true; // No features selected means show all
    }
    
    if (!property.features) {
        console.log('🔧 Property has no features');
        return false;
    }
    
    const propertyFeatures = property.features.split(',').map(f => f.trim().toLowerCase());
    const selectedFeaturesLower = selectedFeatures.map(f => f.toLowerCase());
    
    console.log('🔧 Processed features:', {
        propertyFeatures,
        selectedFeaturesLower
    });
    
    // Property must have at least one of the selected features
    const matches = selectedFeaturesLower.some(selected => 
        propertyFeatures.some(propertyFeature => 
            propertyFeature.includes(selected) || selected.includes(propertyFeature)
        )
    );
    
    console.log('🔧 Features match result:', matches);
    return matches;
}

// Initialize features when page loads
document.addEventListener('DOMContentLoaded', initFeatures);

// Export features functions
window.Features = {
    initFeatures,
    getFeaturesState,
    propertyMatchesFeatures,
    applyFeaturesFilter,
    clearAllFeatures
};

console.log('🔧 Features Filter module loaded:', window.Features);
