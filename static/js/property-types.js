/**
 * Property Types Filter Module
 * Responsible for managing property type filtering functionality
 */

// Property Types State Management
const propertyTypesState = {
    // All available property types
    allPropertyTypes: [],
    
    // Currently selected property types
    selectedPropertyTypes: new Set(),
    
    // Panel open/close state
    isPanelOpen: false
};

/**
 * Initialize property types module
 */
function initPropertyTypes() {
    console.log('🏠 Initializing Property Types module...');
    
    // Get DOM element references
    getPropertyTypesDOMElements();
    
    // Load unique property types
    loadUniquePropertyTypes();
    
    // Bind event listeners
    bindPropertyTypesEvents();
    
    console.log('🏠 Property Types module initialization complete');
}

/**
 * Get DOM element references for property types
 */
function getPropertyTypesDOMElements() {
    // These will be set when the module initializes
    propertyTypesState.elements = {
        toggle: document.getElementById('propertyTypeToggle'),
        panel: document.getElementById('propertyTypePanel'),
        list: document.getElementById('propertyTypeList'),
        clearBtn: document.getElementById('clearPropertyTypes'),
        countSpan: document.getElementById('selectedPropertyTypesCount')
    };
}

/**
 * Load unique property types from database using vectorized backend
 */
async function loadUniquePropertyTypes() {
    try {
        console.log('🏠 Loading unique property types using vectorized backend...');
        
        // Use vectorized filtering API to get filter options
        if (window.API && window.API.getFilterOptions) {
            const filterOptions = await window.API.getFilterOptions();
            
            if (filterOptions && filterOptions.property_types) {
                console.log('🚀 Vectorized property types loaded:', filterOptions.property_types);
                propertyTypesState.allPropertyTypes = filterOptions.property_types;
                renderPropertyTypesList();
                return;
            }
        }
        
        // Fallback to direct API call
        console.log('🏠 Falling back to direct API call...');
        const response = await fetch('/api/properties');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        const properties = data.properties || [];
        
        if (properties.length > 0) {
            // Extract unique property types
            const allTypes = properties.map(property => property.type || property.ptype).filter(Boolean);
            const uniqueTypes = [...new Set(allTypes)].sort();
            
            propertyTypesState.allPropertyTypes = uniqueTypes;
            console.log('🏠 Fallback property types loaded:', uniqueTypes);
            
            renderPropertyTypesList();
        }
    } catch (error) {
        console.error('🏠 Failed to load unique property types:', error);
        // Fallback to common property types
        propertyTypesState.allPropertyTypes = ['Condo', 'House', 'Villa', 'Apartment', 'Cabin', 'Townhouse'];
        renderPropertyTypesList();
        renderPropertyTypesList();
    }
}

/**
 * Render property types list with checkboxes
 */
function renderPropertyTypesList() {
    const listElement = propertyTypesState.elements.list;
    if (!listElement) return;
    
    listElement.innerHTML = '';
    
    propertyTypesState.allPropertyTypes.forEach(propertyType => {
        const checkboxContainer = document.createElement('div');
        checkboxContainer.className = 'property-type-checkbox';
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = `propertyType_${propertyType.replace(/\s+/g, '_')}`;
        checkbox.value = propertyType;
        checkbox.checked = propertyTypesState.selectedPropertyTypes.has(propertyType);
        
        const label = document.createElement('label');
        label.htmlFor = checkbox.id;
        label.textContent = propertyType;
        
        checkbox.addEventListener('change', (e) => {
            if (e.target.checked) {
                propertyTypesState.selectedPropertyTypes.add(propertyType);
            } else {
                propertyTypesState.selectedPropertyTypes.delete(propertyType);
            }
            
            updateSelectedPropertyTypesCount();
            
            // Enable filter button when property types change
            if (window.Budget && window.Budget.enableFilterButton) {
                window.Budget.enableFilterButton();
            }
        });
        
        checkboxContainer.appendChild(checkbox);
        checkboxContainer.appendChild(label);
        listElement.appendChild(checkboxContainer);
    });
    
    updateSelectedPropertyTypesCount();
}

/**
 * Bind event listeners for property types
 */
function bindPropertyTypesEvents() {
    const { toggle, panel, clearBtn } = propertyTypesState.elements;
    
    if (toggle) {
        toggle.addEventListener('click', togglePropertyTypesPanel);
    }
    
    if (clearBtn) {
        clearBtn.addEventListener('click', clearAllPropertyTypes);
    }
    
    // Close panel when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.property-type-filter')) {
            closePropertyTypesPanel();
        }
    });
}

/**
 * Toggle property types panel open/close
 */
function togglePropertyTypesPanel() {
    if (propertyTypesState.isPanelOpen) {
        closePropertyTypesPanel();
    } else {
        openPropertyTypesPanel();
    }
}

/**
 * Open property types panel
 */
function openPropertyTypesPanel() {
    const { toggle, panel } = propertyTypesState.elements;
    
    if (toggle && panel) {
        propertyTypesState.isPanelOpen = true;
        toggle.classList.add('active');
        panel.classList.add('show');
    }
}

/**
 * Close property types panel
 */
function closePropertyTypesPanel() {
    const { toggle, panel } = propertyTypesState.elements;
    
    if (toggle && panel) {
        propertyTypesState.isPanelOpen = false;
        toggle.classList.remove('active');
        panel.classList.remove('show');
    }
}

/**
 * Clear all selected property types
 */
function clearAllPropertyTypes() {
    propertyTypesState.selectedPropertyTypes.clear();
    
    // Uncheck all checkboxes
    const checkboxes = document.querySelectorAll('.property-type-checkbox input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
    });
    
    updateSelectedPropertyTypesCount();
    
    // Enable filter button when property types change
    if (window.Budget && window.Budget.enableFilterButton) {
        window.Budget.enableFilterButton();
    }
}

/**
 * Update selected property types count display
 */
function updateSelectedPropertyTypesCount() {
    const countElement = propertyTypesState.elements.countSpan;
    if (!countElement) return;
    
    const count = propertyTypesState.selectedPropertyTypes.size;
    
    if (count === 0) {
        countElement.textContent = 'All';
    } else if (count === 1) {
        countElement.textContent = '1 Type';
    } else {
        countElement.textContent = `${count} Types`;
    }
}

/**
 * Apply property types filter to properties
 */
function applyPropertyTypesFilter() {
    console.log('🏠 Applying property types filter:', Array.from(propertyTypesState.selectedPropertyTypes));
    
    // Get current budget and features filter state
    const budgetState = window.Budget ? window.Budget.getBudgetState() : { minBudget: 0, maxBudget: 10000 };
    const featuresState = window.Features ? window.Features.getFeaturesState() : { selectedFeatures: [] };
    
    console.log('🏠 Current filter states:', { budgetState, featuresState });
    
    // Apply combined filter
    if (window.Budget && typeof window.Budget.applyCombinedFilter === 'function') {
        console.log('🏠 Calling combined filter with property types...');
        window.Budget.applyCombinedFilter(
            budgetState.minBudget, 
            budgetState.maxBudget, 
            Array.from(featuresState.selectedFeatures),
            Array.from(propertyTypesState.selectedPropertyTypes)
        );
    } else {
        console.error('🏠 Budget module or applyCombinedFilter not available');
    }
}

/**
 * Check if a property matches selected property types
 */
function propertyMatchesTypes(property, selectedTypes) {
    console.log('🏠 Checking property type match:', {
        property: property.location || 'Unknown',
        propertyType: property.type || property.ptype,
        selectedTypes: selectedTypes
    });
    
    if (!selectedTypes || selectedTypes.length === 0) {
        console.log('🏠 No types selected, showing all properties');
        return true; // No types selected means show all
    }
    
    if (!property.type && !property.ptype) {
        console.log('🏠 Property has no type');
        return false;
    }
    
    const propertyType = (property.type || property.ptype).toLowerCase();
    const selectedTypesLower = selectedTypes.map(t => t.toLowerCase());
    
    console.log('🏠 Type comparison:', {
        propertyType,
        selectedTypesLower
    });
    
    const matches = selectedTypesLower.includes(propertyType);
    console.log('🏠 Type match result:', matches);
    
    return matches;
}

/**
 * Get current property types state
 */
function getPropertyTypesState() {
    return {
        allPropertyTypes: [...propertyTypesState.allPropertyTypes],
        selectedPropertyTypes: Array.from(propertyTypesState.selectedPropertyTypes)
    };
}

// Initialize property types when page loads
document.addEventListener('DOMContentLoaded', initPropertyTypes);

// Export property types functions
window.PropertyTypes = {
    initPropertyTypes,
    getPropertyTypesState,
    applyPropertyTypesFilter,
    propertyMatchesTypes,
    clearAllPropertyTypes
};

console.log('🏠 Property Types module loaded:', window.PropertyTypes);
