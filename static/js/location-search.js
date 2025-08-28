/**
 * Location Search Module
 * Handles location-based property search and filtering
 */

class LocationSearch {
    constructor() {
        this.searchInput = null;
        this.radiusSelect = null;
        this.searchBtn = null;
        this.searchStatus = null;
        this.currentLocation = null;
        this.currentRadius = 20; // Default 20km
        
        this.init();
    }
    
    init() {
        console.log('Initializing Location Search module...');
        
        // Get DOM elements
        this.searchInput = document.getElementById('locationSearchInput');
        this.radiusSelect = document.getElementById('radiusSelect');
        this.searchBtn = document.getElementById('locationSearchBtn');
        this.searchStatus = document.getElementById('searchStatus');
        
        if (!this.searchInput || !this.radiusSelect || !this.searchBtn || !this.searchStatus) {
            console.error('Location search elements not found!');
            return;
        }
        
        // Bind event listeners
        this.bindEvents();
        
        // Set initial radius
        this.currentRadius = parseInt(this.radiusSelect.value);
        
        // Restore location filter state from localStorage if exists
        this.restoreLocationFilterState();
        
        console.log('Location Search module initialized');
    }
    
    bindEvents() {
        // Search button click
        this.searchBtn.addEventListener('click', () => this.performSearch());
        
        // Enter key in search input
        this.searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.performSearch();
            }
        });
        
        // Radius change
        this.radiusSelect.addEventListener('change', (e) => {
            this.currentRadius = parseInt(e.target.value);
            console.log(`Radius changed to ${this.currentRadius}km`);
        });
        
        // Input change for real-time validation
        this.searchInput.addEventListener('input', () => {
            this.validateInput();
        });
        
        // Listen for address selection from autocomplete
        document.addEventListener('addressSelected', (e) => {
            console.log('Address selected from autocomplete:', e.detail);
            // Auto-trigger search when address is selected
            setTimeout(() => this.performSearch(), 100);
        });
    }
    
    validateInput() {
        const query = this.searchInput.value.trim();
        const isValid = query.length >= 2;
        
        this.searchBtn.disabled = !isValid;
        
        if (isValid) {
            this.searchStatus.className = 'search-status';
            this.searchStatus.querySelector('.status-text').textContent = 'Ready to search';
        } else {
            this.searchStatus.className = 'search-status error';
            this.searchStatus.querySelector('.status-text').textContent = 'Please enter at least 2 characters';
        }
    }
    
    async performSearch() {
        const query = this.searchInput.value.trim();
        
        if (query.length < 2) {
            this.showError('Please enter a valid location');
            return;
        }
        
        try {
            this.setSearchingState();
            
            // Use backend API for location search
            const response = await fetch('/api/search_by_location', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: query,
                    radius_km: this.currentRadius
                })
            });
            
            if (!response.ok) {
                if (response.status === 404) {
                    this.showError('Location not found. Please try a different search term.');
                } else {
                    throw new Error(`Search failed: ${response.status}`);
                }
                return;
            }
            
            const data = await response.json();
            
            if (data.properties && data.properties.length > 0) {
                this.currentLocation = data.search_location;
                this.showSuccess(`Found ${data.total_count} properties near ${query}`);
                
                // Save location filter state to localStorage
                const locationFilterState = {
                    location: data.search_location,
                    radius: this.currentRadius,
                    query: query,
                    filteredCount: data.total_count,
                    timestamp: Date.now()
                };
                localStorage.setItem('locationFilterState', JSON.stringify(locationFilterState));
                
                // Save filtered properties for secondary filtering
                localStorage.setItem('filteredByLocation', JSON.stringify(data.properties));
                
                // Update properties display with filtered results
                if (window.Properties && window.Properties.renderPropertiesWithData) {
                    window.Properties.renderPropertiesWithData(data.properties);
                }
                
                // Dispatch custom event for other modules
                const event = new CustomEvent('locationFilterApplied', {
                    detail: {
                        location: data.search_location,
                        radius: this.currentRadius,
                        filteredCount: data.total_count,
                        totalCount: window.PROPERTIES_DATA ? window.PROPERTIES_DATA.length : 0
                    }
                });
                document.dispatchEvent(event);
                
            } else {
                this.showError(`No properties found near ${query}`);
            }
            
        } catch (error) {
            console.error('Search error:', error);
            this.showError('Search failed. Please try again.');
        }
    }
    

    
    setSearchingState() {
        this.searchStatus.className = 'search-status searching';
        this.searchStatus.querySelector('.status-text').textContent = 'Searching...';
        this.searchBtn.disabled = true;
    }
    
    showSuccess(message) {
        this.searchStatus.className = 'search-status success';
        this.searchStatus.querySelector('.status-text').textContent = message;
        this.searchBtn.disabled = false;
    }
    
    showError(message) {
        this.searchStatus.className = 'search-status error';
        this.searchStatus.querySelector('.status-text').textContent = message;
        this.searchBtn.disabled = false;
    }
    
    // Method to clear location filter
    clearLocationFilter() {
        this.searchInput.value = '';
        this.currentLocation = null;
        this.searchStatus.className = 'search-status';
        this.searchStatus.querySelector('.status-text').textContent = 'Ready to search';
        this.searchBtn.disabled = true;
        
        // Clear location filter state from localStorage
        localStorage.removeItem('locationFilterState');
        localStorage.removeItem('filteredByLocation');
        
        // Show all properties - safely handle undefined data
        if (window.Properties && window.Properties.renderPropertiesWithData) {
            // Check if PROPERTIES_DATA exists and has properties
            if (window.PROPERTIES_DATA && Array.isArray(window.PROPERTIES_DATA) && window.PROPERTIES_DATA.length > 0) {
                window.Properties.renderPropertiesWithData(window.PROPERTIES_DATA);
            } else {
                // If no data available, try to reload properties
                console.log('No properties data available, attempting to reload...');
                if (window.Properties.loadProperties) {
                    window.Properties.loadProperties();
                }
            }
        }
        
        // Dispatch clear event
        const event = new CustomEvent('locationFilterCleared');
        document.dispatchEvent(event);
    }
    
    // Get current search state
    getSearchState() {
        return {
            location: this.currentLocation,
            radius: this.currentRadius,
            query: this.searchInput.value.trim()
        };
    }
    
    // Get current location state for Smart Match
    getLocationState() {
        return {
            location: this.searchInput.value.trim() || 'Toronto',
            radius: this.currentRadius
        };
    }
    
    // Restore location filter state from localStorage
    restoreLocationFilterState() {
        try {
            const savedState = localStorage.getItem('locationFilterState');
            const savedProperties = localStorage.getItem('filteredByLocation');
            
            if (savedState && savedProperties) {
                const state = JSON.parse(savedState);
                const properties = JSON.parse(savedProperties);
                
                // Check if saved state is not too old (24 hours)
                const isExpired = Date.now() - state.timestamp > 24 * 60 * 60 * 1000;
                
                if (!isExpired && properties.length > 0) {
                    // Restore the state
                    this.currentLocation = state.location;
                    this.searchInput.value = state.query;
                    this.currentRadius = state.radius;
                    this.radiusSelect.value = state.radius;
                    
                    // Update UI to show restored state
                    this.showSuccess(`Restored: ${properties.length} properties near ${state.location}`);
                    
                    // Update properties display
                    if (window.Properties && window.Properties.renderPropertiesWithData) {
                        window.Properties.renderPropertiesWithData(properties);
                    }
                    
                    console.log('Location filter state restored from localStorage');
                } else {
                    // Clear expired state
                    localStorage.removeItem('locationFilterState');
                    localStorage.removeItem('filteredByLocation');
                }
            }
        } catch (error) {
            console.error('Error restoring location filter state:', error);
            // Clear corrupted state
            localStorage.removeItem('locationFilterState');
            localStorage.removeItem('filteredByLocation');
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.LocationSearch = new LocationSearch();
});

// Export for global access
window.LocationSearchModule = LocationSearch;
