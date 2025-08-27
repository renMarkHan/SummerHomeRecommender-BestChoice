/**
 * UI Module
 * Responsible for handling user interface interactions, animations and state management
 */

// UI State Management
const UI_STATE = {
    // Currently active navigation item
    activeNavItem: 'properties',
    
    // Loading state
    isLoading: false,
    
    // Theme mode
    theme: 'light'
};

/**
 * DOM Element References
 */
const DOM_ELEMENTS = {
    // Navigation elements
    navLinks: null,
    
    // Loading indicator
    loadingOverlay: null,
    
    // Profile modal elements
    profileModal: null,
    profileBtn: null,
    closeProfileBtn: null,
    cancelProfileBtn: null,
    profileForm: null,
    weightSliders: null,
    weightValues: null,
    
    // Floating chat elements
    floatingChatToggle: null,
    floatingChatModal: null,
    minimizeChatBtn: null,
    closeChatBtn: null
};

/**
 * Initialize UI module
 */
function initUI() {
    console.log('Initializing UI module...');
    
    // Check authentication first
    checkAuthentication();
    
    // Get DOM element references
    getDOMElements();
    
    // Debug: Check if profile button was found
    console.log('Profile button found:', DOM_ELEMENTS.profileBtn);
    console.log('Profile modal found:', DOM_ELEMENTS.profileModal);
    
    // Bind event listeners
    bindEventListeners();
    
    // Initialize navigation state
    initNavigation();
    
    // Check backend service status
    checkBackendStatus();
    
    // Update user display
    updateUserDisplay();
    
    // Initialize floating chat functionality
    initFloatingChat();
    
    console.log('UI module initialization complete');
}

/**
 * Get DOM element references
 */
function getDOMElements() {
    DOM_ELEMENTS.navLinks = document.querySelectorAll('.nav-link');
    DOM_ELEMENTS.loadingOverlay = document.getElementById('loadingOverlay');
    DOM_ELEMENTS.profileModal = document.getElementById('profileModal');
    DOM_ELEMENTS.profileBtn = document.getElementById('profileBtn');
    DOM_ELEMENTS.closeProfileBtn = document.getElementById('closeProfileBtn');
    DOM_ELEMENTS.cancelProfileBtn = document.getElementById('cancelProfileBtn');
    DOM_ELEMENTS.profileForm = document.getElementById('profileForm');
    DOM_ELEMENTS.weightSliders = document.querySelectorAll('.weight-slider');
    DOM_ELEMENTS.weightValues = document.querySelectorAll('.weight-value');
    
    // Floating chat elements
    DOM_ELEMENTS.floatingChatToggle = document.getElementById('floatingChatToggle');
    DOM_ELEMENTS.floatingChatModal = document.getElementById('floatingChatModal');
    DOM_ELEMENTS.minimizeChatBtn = document.getElementById('minimizeChatBtn');
    DOM_ELEMENTS.closeChatBtn = document.getElementById('closeChatBtn');
}

/**
 * Bind event listeners
 */
function bindEventListeners() {
    // Navigation link click events
    DOM_ELEMENTS.navLinks.forEach(link => {
        link.addEventListener('click', handleNavClick);
    });
    
    // Profile modal events
    if (DOM_ELEMENTS.profileBtn) {
        console.log('Binding click event to profile button');
        DOM_ELEMENTS.profileBtn.addEventListener('click', handleProfileBtnClick);
    } else {
        console.error('Profile button not found!');
    }
    
    // Filter button event
    const filterBtn = document.getElementById('filterBtn');
    if (filterBtn) {
        console.log('Binding click event to filter button');
        filterBtn.addEventListener('click', handleFilterClick);
        // Initially disable the filter button
        filterBtn.disabled = true;
        filterBtn.style.opacity = '0.6';
    } else {
        console.error('Filter button not found!');
    }
    
    // Match button event (for vectorized filtering)
    const matchBtn = document.getElementById('matchBtn');
    // Smart Match button event (Matching Method button)
    const smartMatchBtn = document.getElementById('smartMatchBtn');
    if (smartMatchBtn) {
        console.log('Binding click event to smart match button');
        smartMatchBtn.addEventListener('click', handleSmartMatchBtnClick);
    } else {
        console.error('Smart Match button not found!');
    }
    
    // Reset filters button event
    const resetFiltersBtn = document.getElementById('resetFiltersBtn');
    if (resetFiltersBtn) {
        console.log('Binding click event to reset filters button');
        resetFiltersBtn.addEventListener('click', handleResetFilters);
    } else {
        console.error('Reset filters button not found!');
    }
    
    // Logout button event
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        console.log('Binding click event to logout button');
        logoutBtn.addEventListener('click', handleLogout);
    } else {
        console.error('Logout button not found!');
    }
    
    if (DOM_ELEMENTS.closeProfileBtn) {
        console.log('Binding close event to close button');
        DOM_ELEMENTS.closeProfileBtn.addEventListener('click', handleCloseProfileModal);
    } else {
        console.error('Close button not found!');
    }
    
    if (DOM_ELEMENTS.cancelProfileBtn) {
        console.log('Binding cancel event to cancel button');
        DOM_ELEMENTS.cancelProfileBtn.addEventListener('click', handleCloseProfileModal);
    } else {
        console.error('Cancel button not found!');
    }
    
    // Property Details modal events
    const closePropertyDetailsBtn = document.getElementById('closePropertyDetailsBtn');
    if (closePropertyDetailsBtn) {
        console.log('Binding close event to property details close button');
        closePropertyDetailsBtn.addEventListener('click', () => {
            if (window.Properties && window.Properties.closePropertyDetailsModal) {
                window.Properties.closePropertyDetailsModal();
            }
        });
    } else {
        console.error('Property details close button not found!');
    }
    
    // Smart Match modal events
    const closeSmartMatchBtn = document.getElementById('closeSmartMatchBtn');
    const cancelSmartMatchBtn = document.getElementById('cancelSmartMatchBtn');
    const smartMatchForm = document.getElementById('smartMatchForm');
    
    if (closeSmartMatchBtn) {
        console.log('Binding close event to smart match close button');
        closeSmartMatchBtn.addEventListener('click', handleCloseSmartMatchModal);
    } else {
        console.error('Smart Match close button not found!');
    }
    
    if (cancelSmartMatchBtn) {
        console.log('Binding cancel event to smart match cancel button');
        cancelSmartMatchBtn.addEventListener('click', handleCloseSmartMatchModal);
    } else {
        console.error('Smart Match cancel button not found!');
    }
    
    if (smartMatchForm) {
        console.log('Binding submit event to smart match form');
        smartMatchForm.addEventListener('submit', handleSmartMatchFormSubmit);
    } else {
        console.error('Smart Match form not found!');
    }
    
    // Weight slider events
    DOM_ELEMENTS.weightSliders.forEach((slider, index) => {
        slider.addEventListener('input', (e) => handleWeightSliderChange(e, index));
    });
    
    // Floating chat events
    if (DOM_ELEMENTS.floatingChatToggle) {
        DOM_ELEMENTS.floatingChatToggle.addEventListener('click', handleFloatingChatToggle);
    }
    
    if (DOM_ELEMENTS.minimizeChatBtn) {
        DOM_ELEMENTS.minimizeChatBtn.addEventListener('click', handleMinimizeChat);
    }
    
    if (DOM_ELEMENTS.closeChatBtn) {
        DOM_ELEMENTS.closeChatBtn.addEventListener('click', handleCloseChat);
    }
    
    // Page scroll event
    window.addEventListener('scroll', handleScroll);
    
    // Window resize event
    window.addEventListener('resize', handleResize);
}

/**
 * Initialize navigation state
 */
function initNavigation() {
    // Set default active navigation item
    setActiveNavItem('properties');
    
    // Add smooth scrolling
    DOM_ELEMENTS.navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            scrollToSection(targetId);
        });
    });
}

/**
 * Handle navigation click events
 */
function handleNavClick(e) {
    const clickedLink = e.currentTarget;
    const targetId = clickedLink.getAttribute('href').substring(1);
    
    // Update active state
    setActiveNavItem(targetId);
    
    // Smooth scroll to target section
    scrollToSection(targetId);
}

/**
 * Set active navigation item
 */
function setActiveNavItem(navId) {
    // Remove all active states
    DOM_ELEMENTS.navLinks.forEach(link => {
        link.classList.remove('active');
    });
    
    // Set current active item
    const activeLink = document.querySelector(`[href="#${navId}"]`);
    if (activeLink) {
        activeLink.classList.add('active');
        UI_STATE.activeNavItem = navId;
    }
}

/**
 * Smooth scroll to specified section
 */
function scrollToSection(sectionId) {
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

/**
 * Handle page scroll events
 */
function handleScroll() {
    // Add scroll effects
    const scrolled = window.pageYOffset;
    const header = document.querySelector('.header');
    
    if (scrolled > 100) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
    
    // Update navigation active state based on scroll position
    updateActiveNavOnScroll();
}

/**
 * Update active navigation based on scroll position
 */
function updateActiveNavOnScroll() {
    const sections = ['properties'];
    const scrollPosition = window.pageYOffset + 100;
    
    for (let i = sections.length - 1; i >= 0; i--) {
        const section = document.getElementById(sections[i]);
        if (section && scrollPosition >= section.offsetTop) {
            setActiveNavItem(sections[i]);
            break;
        }
    }
}

/**
 * Handle window resize events
 */
function handleResize() {
    // Handle responsive adjustments if needed
}

/**
 * Show loading indicator
 */
function showLoading() {
    UI_STATE.isLoading = true;
    if (DOM_ELEMENTS.loadingOverlay) {
        DOM_ELEMENTS.loadingOverlay.classList.add('show');
    }
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    UI_STATE.isLoading = false;
    if (DOM_ELEMENTS.loadingOverlay) {
        DOM_ELEMENTS.loadingOverlay.classList.remove('show');
    }
}

/**
 * Check backend service status
 */
async function checkBackendStatus() {
    try {
        if (window.API && window.API.isServiceAvailable) {
            const isAvailable = await window.API.isServiceAvailable();
            updateBackendStatus(isAvailable);
        }
    } catch (error) {
        console.error('Failed to check backend status:', error);
        updateBackendStatus(false);
    }
}

/**
 * Update backend service status display
 */
function updateBackendStatus(isAvailable) {
    // This function is kept for future use if we need to show backend status
    // For now, it's not actively used in the properties-focused interface
}

/**
 * Show notification message
 */
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Show animation
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Auto-hide
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            if (document.body.contains(notification)) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

/**
 * Handle profile button click
 */
function handleProfileBtnClick() {
    console.log('Profile button clicked!');
    console.log('Profile modal element:', DOM_ELEMENTS.profileModal);
    
    if (DOM_ELEMENTS.profileModal) {
        console.log('Adding show class to profile modal');
        DOM_ELEMENTS.profileModal.classList.add('show');
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
        
        // Auto-fill the profile form
        autoFillProfileForm();
        
        console.log('Profile modal should now be visible');
    } else {
        console.error('Profile modal not found!');
    }
}

/**
 * Handle profile modal close
 */
function handleCloseProfileModal() {
    if (DOM_ELEMENTS.profileModal) {
        DOM_ELEMENTS.profileModal.classList.remove('show');
        document.body.style.overflow = ''; // Restore scrolling
    }
}

/**
 * Handle weight slider changes
 */
function handleWeightSliderChange(event, index) {
    const value = event.target.value;
    if (DOM_ELEMENTS.weightValues && DOM_ELEMENTS.weightValues[index]) {
        DOM_ELEMENTS.weightValues[index].textContent = value;
    }
}

/**
 * Handle Smart Match button click
 */
function handleSmartMatchBtnClick() {
    console.log('Smart Match button clicked!');
    
    const smartMatchModal = document.getElementById('smartMatchModal');
    if (smartMatchModal) {
        console.log('Adding show class to smart match modal');
        smartMatchModal.classList.add('show');
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
        
        // Auto-fill the smart match form
        autoFillSmartMatchForm();
        
        console.log('Smart Match modal should now be visible');
    } else {
        console.error('Smart Match modal not found!');
    }
}

/**
 * Handle Smart Match modal close
 */
function handleCloseSmartMatchModal() {
    const smartMatchModal = document.getElementById('smartMatchModal');
    if (smartMatchModal) {
        smartMatchModal.classList.remove('show');
        document.body.style.overflow = ''; // Restore scrolling
    }
}

/**
 * Handle Smart Match form submission
 */
function handleSmartMatchFormSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const smartMatchData = {
        locationWeight: parseInt(formData.get('locationWeight')),
        typeWeight: parseInt(formData.get('typeWeight')),
        featuresWeight: parseInt(formData.get('featuresWeight')),
        priceWeight: parseInt(formData.get('priceWeight'))
    };
    
    // First: Save the preferences to localStorage for Smart Match
    localStorage.setItem('userWeights', JSON.stringify(smartMatchData));
    
    // Second: Save the preferences to database
    saveSmartMatchPreferences(smartMatchData);
    
    // Third: Execute smart match functionality
    executeSmartMatch();
    
    // Close modal
    handleCloseSmartMatchModal();
    
    // Show success notification
    showNotification('Preferences saved and Smart Match executed!', 'success');
}

/**
 * Save Smart Match preferences to database
 */
async function saveSmartMatchPreferences(preferences) {
    try {
        // Get current user ID (assuming we have one stored)
        const userId = localStorage.getItem('userId') || 1; // Default to user 1 for now
        
        // Call API to save preferences
        const response = await fetch('/api/update_user_weights', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: userId,
                weighed_location: preferences.locationWeight,
                weighed_type: preferences.typeWeight,
                weighed_features: preferences.featuresWeight,
                weighed_price: preferences.priceWeight
            })
        });
        
        if (!response.ok) {
            throw new Error(`Failed to save preferences: ${response.status}`);
        }
        
        console.log('Smart Match preferences saved successfully');
        
    } catch (error) {
        console.error('Error saving Smart Match preferences:', error);
        showNotification('Failed to save preferences', 'error');
    }
}

/**
 * Execute Smart Match functionality (same as clicking Smart Match button)
 */
async function executeSmartMatch() {
    console.log('🎯 Executing Smart Match after saving preferences...');
    
    try {
        // Get current filter states
        const budgetState = window.Budget ? window.Budget.getBudgetState() : { minBudget: 0, maxBudget: 1000 };
        const featuresState = window.Features ? window.Features.getFeaturesState() : { selectedFeatures: [] };
        const propertyTypesState = window.PropertyTypes ? window.PropertyTypes.getPropertyTypesState() : { selectedPropertyTypes: [] };
        const locationState = window.LocationSearch ? window.LocationSearch.getLocationState() : { location: 'Toronto', radius: 50 };
        
        // Get user weights from profile data (stored when saving preferences)
        const userWeights = JSON.parse(localStorage.getItem('userWeights') || '{}');
        const locationWeight = userWeights.locationWeight || 1;
        const typeWeight = userWeights.typeWeight || 1;
        const featuresWeight = userWeights.featuresWeight || 1;
        const priceWeight = userWeights.priceWeight || 1;
        
        console.log('🎯 Smart Match parameters:', {
            budget: budgetState,
            features: featuresState.selectedFeatures,
            propertyTypes: propertyTypesState.selectedPropertyTypes,
            location: locationState.location,
            radius: locationState.radius,
            weights: { locationWeight, typeWeight, featuresWeight, priceWeight }
        });
        
        // Debug: Check the actual data being sent
        console.log('🔍 DEBUG - Selected Property Types:', Array.from(propertyTypesState.selectedPropertyTypes));
        console.log('🔍 DEBUG - Selected Features:', Array.from(featuresState.selectedFeatures));
        
        // Call Smart Match API
        const response = await fetch('/api/smart_match', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                selected_types: Array.from(propertyTypesState.selectedPropertyTypes),
                selected_features: Array.from(featuresState.selectedFeatures),
                center_location: locationState.location,
                radius: locationState.radius,
                min_budget: budgetState.minBudget,
                max_budget: budgetState.maxBudget,
                location_weight: locationWeight,
                type_weight: typeWeight,
                features_weight: featuresWeight,
                price_weight: priceWeight
            })
        });
        
        if (!response.ok) {
            throw new Error(`Smart Match API error: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('🎯 Smart Match API response:', result);
        
        // Display Smart Match results
        if (result.properties && result.properties.length > 0) {
            // Log detailed scores for each property
            console.log('🎯 === SMART MATCH DETAILED SCORES ===');
            result.properties.forEach((property, index) => {
                console.log(`🏆 #${index + 1} - ${property.ptype} in ${property.location}`);
                console.log(`   💰 Price: $${property.nightly_price}/night`);
                console.log(`   📊 Scores:`);
                console.log(`      Type: ${(property.type_score * 100).toFixed(1)}% (${property.type_score})`);
                console.log(`      Features: ${(property.features_score * 100).toFixed(1)}% (${property.features_score})`);
                console.log(`      Location: ${(property.location_score * 100).toFixed(1)}% (${property.location_score})`);
                console.log(`      Price: ${(property.price_score * 100).toFixed(1)}% (${property.price_score})`);
                console.log(`   🎯 TOTAL SCORE: ${(property.total_score * 100).toFixed(1)}% (${property.total_score})`);
                console.log(`   📍 Coordinates: (${property.latitude}, ${property.longitude})`);
                console.log('   ──────────────────────────────────────────────');
            });
            console.log('🎯 === END OF SMART MATCH SCORES ===');
            
            displaySmartMatchResults(result.properties);
            showNotification(`Smart Match found ${result.properties.length} properties!`, 'success');
        } else {
            showNotification('No properties found matching your Smart Match criteria', 'info');
        }
        
    } catch (error) {
        console.error('Error executing Smart Match:', error);
        showNotification('Failed to execute Smart Match', 'error');
    }
}

/**
 * Display Smart Match results
 */
function displaySmartMatchResults(properties) {
    // Get the properties container
    const propertiesGrid = document.getElementById('propertiesGrid');
    if (!propertiesGrid) return;
    
    // Clear existing properties
    propertiesGrid.innerHTML = '';
    
    // Add Smart Match header
    const headerDiv = document.createElement('div');
    headerDiv.className = 'smart-match-header';
    headerDiv.innerHTML = `
        <div class="smart-match-title">
            <i class="fas fa-magic"></i>
            <h3>Smart Match Results</h3>
            <p>Top ${properties.length} properties based on your preferences</p>
        </div>
    `;
    propertiesGrid.appendChild(headerDiv);
    
    // Display each property with its scores
    properties.forEach((property, index) => {
        const propertyCard = createSmartMatchPropertyCard(property, index + 1);
        propertiesGrid.appendChild(propertyCard);
    });
}

/**
 * Create a property card for Smart Match results
 */
function createSmartMatchPropertyCard(property, rank) {
    const card = document.createElement('div');
    card.className = 'property-card smart-match-card';
    
    // Format scores for display
    const typeScore = (property.type_score * 100).toFixed(0);
    const featuresScore = (property.features_score * 100).toFixed(0);
    const locationScore = (property.location_score * 100).toFixed(0);
    const priceScore = (property.price_score * 100).toFixed(0);
    const totalScore = (property.total_score * 100).toFixed(0);
    
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
            <div class="rank-badge">#${rank}</div>
            <div class="total-score-badge">${totalScore}%</div>
        </div>
        
        <div class="property-content">
            <div class="property-header">
                <div class="property-title">
                    <i class="fas fa-home"></i>
                    ${property.ptype} in ${property.location}
                </div>
                <div class="property-price">
                    $${property.nightly_price}/night
                </div>
            </div>
            
            <div class="smart-match-scores">
                <div class="score-item">
                    <span class="score-label">Type:</span>
                    <span class="score-value type-score">${typeScore}%</span>
                </div>
                <div class="score-item">
                    <span class="score-label">Features:</span>
                    <span class="score-value features-score">${featuresScore}%</span>
                </div>
                <div class="score-item">
                    <span class="score-label">Location:</span>
                    <span class="score-value location-score">${locationScore}%</span>
                </div>
                <div class="score-item">
                    <span class="score-label">Price:</span>
                    <span class="score-value price-score">${priceScore}%</span>
                </div>
            </div>
            
            <div class="property-features">
                ${property.features && property.features.length > 0 ? 
                    property.features.slice(0, 5).map(feature => 
                        `<span class="feature-tag"><i class="fas fa-check"></i>${feature}</span>`
                    ).join('') : 
                    '<span class="no-features">No features listed</span>'
                }
            </div>
            
            <div class="property-actions">
                <button class="btn btn-primary">View Details</button>
                <button class="btn btn-outline">Save</button>
            </div>
        </div>
    `;
    
    return card;
}

/**
 * Auto-fill smart match form with user data
 */
function autoFillSmartMatchForm() {
    // Set up weight slider events for smart match form
    const smartMatchWeightSliders = document.querySelectorAll('#smartMatchModal .weight-slider');
    const smartMatchWeightValues = document.querySelectorAll('#smartMatchModal .weight-value');
    
    smartMatchWeightSliders.forEach((slider, index) => {
        slider.addEventListener('input', (e) => {
            const value = e.target.value;
            if (smartMatchWeightValues[index]) {
                smartMatchWeightValues[index].textContent = value;
            }
        });
    });
}

/**
 * Auto-fill profile form with user data
 */
function autoFillProfileForm() {
    const username = localStorage.getItem('username') || 'Team18';
    const nameInput = document.getElementById('profileName');
    if (nameInput) {
        nameInput.value = username;
        nameInput.readOnly = true; // Make name field read-only since it's Team18
    }
}

// Initialize UI when page loads
document.addEventListener('DOMContentLoaded', initUI);

/**
 * Check if user is authenticated
 */
function checkAuthentication() {
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    if (!isLoggedIn) {
        // Redirect to login page
        window.location.href = '/static/login.html';
        return;
    }
}

/**
 * Update user display information
 */
function updateUserDisplay() {
    // Username display has been removed from the interface
    // This function is kept for backward compatibility
    console.log('User display updated (username element removed from interface)');
}

/**
 * Handle filter button click
 */
function handleFilterClick() {
    console.log('🔍 Filter button clicked!');
    
    try {
        // Get current filter states
        const budgetState = window.Budget ? window.Budget.getBudgetState() : { minBudget: 0, maxBudget: 1000 };
        const featuresState = window.Features ? window.Features.getFeaturesState() : { selectedFeatures: [] };
        const propertyTypesState = window.PropertyTypes ? window.PropertyTypes.getPropertyTypesState() : { selectedPropertyTypes: [] };
        
        console.log('🔍 Applying client-side filters:', {
            budget: budgetState,
            features: featuresState.selectedFeatures,
            propertyTypes: propertyTypesState.selectedPropertyTypes
        });
        
        // Apply client-side filtering (original method)
        if (window.Budget && window.Budget.applyClientSideFilter) {
            window.Budget.applyClientSideFilter(
                budgetState.minBudget,
                budgetState.maxBudget,
                Array.from(featuresState.selectedFeatures),
                Array.from(propertyTypesState.selectedPropertyTypes)
            );
            
            // Disable filter button after filtering
            if (window.Budget && window.Budget.disableFilterButton) {
                window.Budget.disableFilterButton();
            }
            
            // Show success notification
            showNotification('Client-side filters applied successfully!', 'success');
        } else {
            console.error('Budget module not available');
            showNotification('Filter functionality not available', 'error');
        }
        
    } catch (error) {
        console.error('Error applying filters:', error);
        showNotification('Failed to apply filters', 'error');
    }
}



/**
 * Handle reset filters button click
 */
function handleResetFilters() {
    console.log('🔄 Reset filters button clicked!');
    
    try {
        // Reset budget to default values
        if (window.Budget && window.Budget.resetBudget) {
            window.Budget.resetBudget();
        }
        
        // Reset features selection
        if (window.Features && window.Features.clearAllFeatures) {
            window.Features.clearAllFeatures();
        }
        
        // Reset property types selection
        if (window.PropertyTypes && window.PropertyTypes.clearAllPropertyTypes) {
            window.PropertyTypes.clearAllPropertyTypes();
        }
        
        // Reset location search
        if (window.LocationSearch && window.LocationSearch.clearLocationFilter) {
            window.LocationSearch.clearLocationFilter();
        }
        
        // Enable filter button
        if (window.Budget && window.Budget.enableFilterButton) {
            window.Budget.enableFilterButton();
        }
        
        // Show success notification
        showNotification('All filters have been reset!', 'success');
        
    } catch (error) {
        console.error('Error resetting filters:', error);
        showNotification('Failed to reset filters', 'error');
    }
}

/**
 * Handle logout
 */
function handleLogout() {
    // Clear local storage
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('username');
    localStorage.removeItem('userId');
    
    // Redirect to login page
    window.location.href = '/static/login.html';
}

/**
 * Handle floating chat toggle
 */
function handleFloatingChatToggle() {
    console.log('🤖 Floating chat toggle clicked');
    
    if (DOM_ELEMENTS.floatingChatModal) {
        const isVisible = DOM_ELEMENTS.floatingChatModal.classList.contains('show');
        
        if (isVisible) {
            DOM_ELEMENTS.floatingChatModal.classList.remove('show');
        } else {
            DOM_ELEMENTS.floatingChatModal.classList.add('show');
            DOM_ELEMENTS.floatingChatModal.classList.remove('minimized');
            
            // Hide notification badge
            const notification = document.getElementById('chatNotification');
            if (notification) {
                notification.style.display = 'none';
            }
        }
    }
}

/**
 * Handle minimize chat
 */
function handleMinimizeChat() {
    console.log('🤖 Minimizing chat');
    
    if (DOM_ELEMENTS.floatingChatModal) {
        DOM_ELEMENTS.floatingChatModal.classList.add('minimized');
    }
}

/**
 * Handle close chat
 */
function handleCloseChat() {
    console.log('🤖 Closing chat');
    
    if (DOM_ELEMENTS.floatingChatModal) {
        DOM_ELEMENTS.floatingChatModal.classList.remove('show');
        DOM_ELEMENTS.floatingChatModal.classList.remove('minimized');
    }
}

/**
 * Initialize floating chat functionality
 */
function initFloatingChat() {
    console.log('🤖 Initializing floating chat functionality...');
    
    // Get floating chat input elements
    const floatingChatInput = document.getElementById('floatingChatInput');
    const floatingSendButton = document.getElementById('floatingSendButton');
    
    if (floatingChatInput && floatingSendButton) {
        console.log('🤖 Binding floating chat input events...');
        
        // Auto resize textarea and enable/disable send button
        floatingChatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
            
            // Enable/disable send button based on input
            const hasText = this.value.trim().length > 0;
            floatingSendButton.disabled = !hasText;
        });
        
        // Enter key to send (Shift+Enter for new line)
        floatingChatInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendFloatingChatMessage();
            }
        });
        
        // Send button click
        floatingSendButton.addEventListener('click', function() {
            console.log('🤖 Send button clicked');
            sendFloatingChatMessage();
        });
        
        // Quick action buttons
        const quickActionBtns = document.querySelectorAll('.floating-chat-input-container .quick-action-btn');
        quickActionBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const prompt = this.getAttribute('data-prompt');
                if (prompt) {
                    floatingChatInput.value = prompt;
                    floatingChatInput.focus();
                    floatingSendButton.disabled = false;
                    // Auto resize
                    floatingChatInput.style.height = 'auto';
                    floatingChatInput.style.height = floatingChatInput.scrollHeight + 'px';
                }
            });
        });
        
        console.log('🤖 Floating chat input events bound successfully');
    } else {
        console.error('🤖 Floating chat input/send button not found!');
    }
}

/**
 * Send floating chat message
 */
function sendFloatingChatMessage() {
    const floatingChatInput = document.getElementById('floatingChatInput');
    const floatingSendButton = document.getElementById('floatingSendButton');
    
    if (!floatingChatInput || !floatingChatInput.value.trim()) {
        console.log('🤖 No message to send');
        return;
    }
    
    const message = floatingChatInput.value.trim();
    console.log('🤖 Sending floating chat message:', message);
    
    // Clear input
    floatingChatInput.value = '';
    floatingChatInput.style.height = 'auto';
    
    // Disable send button
    if (floatingSendButton) {
        floatingSendButton.disabled = true;
    }
    
    // Add user message to floating chat
    addFloatingChatMessage(message, 'user');
    
    // Add typing indicator
    addFloatingTypingIndicator();
    
    // Send to API
    if (window.API && window.API.sendChatMessage) {
        window.API.sendChatMessage(message)
            .then(response => {
                removeFloatingTypingIndicator();
                if (response && response.response) {
                    addFloatingChatMessage(response.response, 'bot');
                } else {
                    addFloatingChatMessage('Sorry, I didn\'t receive a response. Please try again.', 'bot');
                }
            })
            .catch(error => {
                removeFloatingTypingIndicator();
                console.error('🤖 API error:', error);
                addFloatingChatMessage('Sorry, I encountered an error. Please try again.', 'bot');
            });
    } else {
        // Fallback if API is not available
        setTimeout(() => {
            removeFloatingTypingIndicator();
            addFloatingChatMessage('API is not available. This is a test response.', 'bot');
        }, 1000);
    }
}

/**
 * Add message to floating chat
 */
function addFloatingChatMessage(message, type) {
    const floatingChatMessages = document.getElementById('floatingChatMessages');
    if (!floatingChatMessages) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    avatarDiv.innerHTML = type === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    textDiv.textContent = message;
    
    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = new Date().toLocaleTimeString();
    
    contentDiv.appendChild(textDiv);
    contentDiv.appendChild(timeDiv);
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    
    floatingChatMessages.appendChild(messageDiv);
    floatingChatMessages.scrollTop = floatingChatMessages.scrollHeight;
}

/**
 * Add typing indicator to floating chat
 */
function addFloatingTypingIndicator() {
    const floatingChatMessages = document.getElementById('floatingChatMessages');
    if (!floatingChatMessages) return;
    
    // Remove existing typing indicator
    removeFloatingTypingIndicator();
    
    const typingDiv = document.createElement('div');
    typingDiv.id = 'floatingTypingIndicator';
    typingDiv.className = 'message bot-message typing-indicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="message-text">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    `;
    
    floatingChatMessages.appendChild(typingDiv);
    floatingChatMessages.scrollTop = floatingChatMessages.scrollHeight;
}

/**
 * Remove typing indicator from floating chat
 */
function removeFloatingTypingIndicator() {
    const typingIndicator = document.getElementById('floatingTypingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Export UI functions
window.UI = {
    showLoading,
    hideLoading,
    showNotification,
    updateBackendStatus,
    checkBackendStatus,
    checkAuthentication,
    updateUserDisplay,
    handleLogout,
    // Floating chat functions
    sendFloatingChatMessage,
    addFloatingChatMessage,
    addFloatingTypingIndicator,
    removeFloatingTypingIndicator
};

console.log('UI module loaded:', window.UI);
