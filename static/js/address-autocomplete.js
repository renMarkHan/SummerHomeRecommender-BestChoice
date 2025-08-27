/**
 * Address Autocomplete Module
 * Provides address suggestions as user types
 */

class AddressAutocomplete {
    constructor() {
        this.searchInput = null;
        this.suggestionsContainer = null;
        this.currentSuggestions = [];
        this.selectedIndex = -1;
        this.isOpen = false;
        this.debounceTimer = null;
        
        this.init();
    }
    
    init() {
        console.log('Initializing Address Autocomplete module...');
        
        // Get DOM elements
        this.searchInput = document.getElementById('locationSearchInput');
        this.suggestionsContainer = this.createSuggestionsContainer();
        
        if (!this.searchInput) {
            console.error('Location search input not found!');
            return;
        }
        
        // Insert suggestions container after the input
        this.searchInput.parentNode.appendChild(this.suggestionsContainer);
        
        // Bind event listeners
        this.bindEvents();
        
        console.log('Address Autocomplete module initialized');
    }
    
    createSuggestionsContainer() {
        const container = document.createElement('div');
        container.className = 'address-suggestions';
        container.style.display = 'none';
        return container;
    }
    
    bindEvents() {
        // Input events
        this.searchInput.addEventListener('input', (e) => this.handleInput(e));
        this.searchInput.addEventListener('keydown', (e) => this.handleKeydown(e));
        this.searchInput.addEventListener('focus', () => this.showSuggestions());
        this.searchInput.addEventListener('blur', () => this.hideSuggestions());
        
        // Click outside to close
        document.addEventListener('click', (e) => {
            if (!this.searchInput.contains(e.target) && !this.suggestionsContainer.contains(e.target)) {
                this.hideSuggestions();
            }
        });
    }
    
    handleInput(e) {
        const query = e.target.value.trim();
        
        // Clear previous debounce timer
        if (this.debounceTimer) {
            clearTimeout(this.debounceTimer);
        }
        
        // Debounce the search to avoid too many API calls
        this.debounceTimer = setTimeout(() => {
            if (query.length >= 2) {
                this.searchAddresses(query);
            } else {
                this.hideSuggestions();
            }
        }, 300);
    }
    
    handleKeydown(e) {
        if (!this.isOpen || this.currentSuggestions.length === 0) return;
        
        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                this.selectNext();
                break;
            case 'ArrowUp':
                e.preventDefault();
                this.selectPrevious();
                break;
            case 'Enter':
                e.preventDefault();
                if (this.selectedIndex >= 0) {
                    this.selectSuggestion(this.currentSuggestions[this.selectedIndex]);
                }
                break;
            case 'Escape':
                this.hideSuggestions();
                break;
        }
    }
    
    async searchAddresses(query) {
        try {
            // Use OpenStreetMap Nominatim for address suggestions
            const response = await fetch(
                `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=5&addressdetails=1&countrycodes=ca,us&bounded=1&viewbox=-141.0,41.7,-52.6,83.3`
            );
            
            if (!response.ok) {
                throw new Error(`Search failed: ${response.status}`);
            }
            
            const data = await response.json();
            this.currentSuggestions = data;
            this.showSuggestions();
            
        } catch (error) {
            console.error('Address search error:', error);
            this.hideSuggestions();
        }
    }
    
    showSuggestions() {
        if (this.currentSuggestions.length === 0) {
            this.hideSuggestions();
            return;
        }
        
        this.renderSuggestions();
        this.suggestionsContainer.style.display = 'block';
        this.isOpen = true;
        this.selectedIndex = -1;
    }
    
    hideSuggestions() {
        this.suggestionsContainer.style.display = 'none';
        this.isOpen = false;
        this.selectedIndex = -1;
    }
    
    renderSuggestions() {
        this.suggestionsContainer.innerHTML = '';
        
        this.currentSuggestions.forEach((suggestion, index) => {
            const item = document.createElement('div');
            item.className = 'suggestion-item';
            item.dataset.index = index;
            
            // Create a formatted display name
            const displayName = this.formatAddress(suggestion);
            
            item.innerHTML = `
                <div class="suggestion-icon">
                    <i class="fas fa-map-marker-alt"></i>
                </div>
                <div class="suggestion-content">
                    <div class="suggestion-main">${displayName.main}</div>
                    <div class="suggestion-details">${displayName.details}</div>
                </div>
            `;
            
            // Add click event
            item.addEventListener('click', () => {
                this.selectSuggestion(suggestion);
            });
            
            // Add hover event
            item.addEventListener('mouseenter', () => {
                this.selectedIndex = index;
                this.updateSelection();
            });
            
            this.suggestionsContainer.appendChild(item);
        });
    }
    
    formatAddress(suggestion) {
        const address = suggestion.address;
        let main = '';
        let details = '';
        
        // Try to create a meaningful main line
        if (address.house_number && address.road) {
            main = `${address.house_number} ${address.road}`;
        } else if (address.road) {
            main = address.road;
        } else if (address.suburb) {
            main = address.suburb;
        } else if (address.city) {
            main = address.city;
        } else {
            main = suggestion.display_name.split(',')[0];
        }
        
        // Create details line
        const detailsParts = [];
        if (address.city && address.city !== main) detailsParts.push(address.city);
        if (address.state) detailsParts.push(address.state);
        if (address.country) detailsParts.push(address.country);
        
        details = detailsParts.join(', ');
        
        return { main, details };
    }
    
    selectNext() {
        this.selectedIndex = Math.min(this.selectedIndex + 1, this.currentSuggestions.length - 1);
        this.updateSelection();
    }
    
    selectPrevious() {
        this.selectedIndex = Math.max(this.selectedIndex - 1, -1);
        this.updateSelection();
    }
    
    updateSelection() {
        // Remove previous selection
        const items = this.suggestionsContainer.querySelectorAll('.suggestion-item');
        items.forEach(item => item.classList.remove('selected'));
        
        // Add selection to current item
        if (this.selectedIndex >= 0 && this.selectedIndex < items.length) {
            items[this.selectedIndex].classList.add('selected');
        }
    }
    
    selectSuggestion(suggestion) {
        // Fill the input with the selected address
        this.searchInput.value = suggestion.display_name;
        
        // Hide suggestions
        this.hideSuggestions();
        
        // Focus the input
        this.searchInput.focus();
        
        // Trigger input event to update validation
        this.searchInput.dispatchEvent(new Event('input'));
        
        // Dispatch custom event for other modules
        const event = new CustomEvent('addressSelected', {
            detail: {
                address: suggestion.display_name,
                coordinates: {
                    lat: parseFloat(suggestion.lat),
                    lon: parseFloat(suggestion.lon)
                },
                fullAddress: suggestion
            }
        });
        document.dispatchEvent(event);
    }
    
    // Public method to clear suggestions
    clearSuggestions() {
        this.currentSuggestions = [];
        this.hideSuggestions();
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.AddressAutocomplete = new AddressAutocomplete();
});

// Export for global access
window.AddressAutocompleteModule = AddressAutocomplete;
