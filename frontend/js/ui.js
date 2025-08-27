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
    weightValues: null
};

/**
 * Initialize UI module
 */
function initUI() {
    console.log('Initializing UI module...');
    
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
    
    if (DOM_ELEMENTS.profileForm) {
        console.log('Binding submit event to profile form');
        DOM_ELEMENTS.profileForm.addEventListener('submit', handleProfileFormSubmit);
    } else {
        console.error('Profile form not found!');
    }
    
    // Weight slider events
    DOM_ELEMENTS.weightSliders.forEach((slider, index) => {
        slider.addEventListener('input', (e) => handleWeightSliderChange(e, index));
    });
    
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
    const sections = ['properties', 'chat', 'about'];
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
 * Handle profile form submission
 */
function handleProfileFormSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const profileData = {
        name: formData.get('name'),
        locationWeight: parseInt(formData.get('locationWeight')),
        typeWeight: parseInt(formData.get('typeWeight')),
        featuresWeight: parseInt(formData.get('featuresWeight')),
        priceWeight: parseInt(formData.get('priceWeight'))
    };
    
    // Trigger profile save event
    const customEvent = new CustomEvent('saveProfile', { detail: profileData });
    document.dispatchEvent(customEvent);
    
    // Close modal
    handleCloseProfileModal();
    
    // Show success notification
    showNotification('Profile saved successfully!', 'success');
}

// Initialize UI when page loads
document.addEventListener('DOMContentLoaded', initUI);

// Export UI functions
window.UI = {
    showLoading,
    hideLoading,
    showNotification,
    updateBackendStatus,
    checkBackendStatus
};

console.log('UI module loaded:', window.UI);
