/**
 * HamroKotha - Main JavaScript
 * Kathmandu Valley Rental Platform
 */

// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    initMobileMenu();
    initToastNotifications();
    initImagePreview();
    initFavoriteToggle();
    initFormValidation();
    initSearchFilters();
});

/**
 * Mobile Menu Toggle
 */
function initMobileMenu() {
    const menuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (menuBtn && mobileMenu) {
        menuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
}

/**
 * Toast Notifications
 */
function initToastNotifications() {
    const toasts = document.querySelectorAll('.toast');
    
    toasts.forEach(function(toast) {
        // Auto-dismiss after 5 seconds
        setTimeout(function() {
            toast.classList.add('opacity-0');
            setTimeout(function() {
                toast.remove();
            }, 300);
        }, 5000);
        
        // Close button
        const closeBtn = toast.querySelector('.toast-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                toast.remove();
            });
        }
    });
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container') || createToastContainer();
    
    const colors = {
        success: 'bg-green-500',
        error: 'bg-red-500',
        warning: 'bg-yellow-500',
        info: 'bg-blue-500'
    };
    
    const toast = document.createElement('div');
    toast.className = `toast ${colors[type]} text-white px-6 py-3 rounded-lg shadow-lg mb-2 flex items-center justify-between`;
    toast.innerHTML = `
        <span>${message}</span>
        <button class="toast-close ml-4 text-white hover:text-gray-200">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
        </button>
    `;
    
    container.appendChild(toast);
    
    // Auto-dismiss
    setTimeout(function() {
        toast.classList.add('opacity-0');
        setTimeout(function() {
            toast.remove();
        }, 300);
    }, 5000);
    
    // Close button
    toast.querySelector('.toast-close').addEventListener('click', function() {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'fixed top-4 right-4 z-50';
    document.body.appendChild(container);
    return container;
}

/**
 * Image Preview for Upload
 */
function initImagePreview() {
    const imageInput = document.getElementById('property-images');
    const previewContainer = document.getElementById('image-preview');
    
    if (imageInput && previewContainer) {
        imageInput.addEventListener('change', function(e) {
            previewContainer.innerHTML = '';
            
            const files = Array.from(e.target.files);
            
            files.forEach(function(file, index) {
                if (file.type.startsWith('image/')) {
                    const reader = new FileReader();
                    
                    reader.onload = function(event) {
                        const div = document.createElement('div');
                        div.className = 'relative';
                        div.innerHTML = `
                            <img src="${event.target.result}" 
                                 class="w-24 h-24 object-cover rounded-lg border-2 border-gray-200" 
                                 alt="Preview ${index + 1}">
                            ${index === 0 ? '<span class="absolute -top-2 -right-2 bg-blue-500 text-white text-xs px-2 py-1 rounded-full">Primary</span>' : ''}
                        `;
                        previewContainer.appendChild(div);
                    };
                    
                    reader.readAsDataURL(file);
                }
            });
        });
    }
}

/**
 * Favorite Toggle (AJAX)
 */
function initFavoriteToggle() {
    document.addEventListener('click', function(e) {
        const favoriteBtn = e.target.closest('.favorite-btn');
        
        if (favoriteBtn) {
            e.preventDefault();
            
            const propertyId = favoriteBtn.dataset.propertyId;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value 
                           || getCookie('csrftoken');
            
            fetch(`/properties/${propertyId}/favorite/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'added') {
                    favoriteBtn.classList.add('active');
                    showToast('Added to favorites', 'success');
                } else if (data.status === 'removed') {
                    favoriteBtn.classList.remove('active');
                    showToast('Removed from favorites', 'info');
                } else if (data.error === 'login_required') {
                    window.location.href = '/login/?next=' + window.location.pathname;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('Something went wrong', 'error');
            });
        }
    });
}

/**
 * Form Validation
 */
function initFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');
    
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('border-red-500');
                    
                    // Add error message
                    let errorMsg = field.parentElement.querySelector('.error-message');
                    if (!errorMsg) {
                        errorMsg = document.createElement('span');
                        errorMsg.className = 'error-message text-red-500 text-sm mt-1';
                        field.parentElement.appendChild(errorMsg);
                    }
                    errorMsg.textContent = 'This field is required';
                } else {
                    field.classList.remove('border-red-500');
                    const errorMsg = field.parentElement.querySelector('.error-message');
                    if (errorMsg) errorMsg.remove();
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showToast('Please fill in all required fields', 'error');
            }
        });
    });
}

/**
 * Search Filters
 */
function initSearchFilters() {
    const filterToggle = document.getElementById('filter-toggle');
    const filterPanel = document.getElementById('filter-panel');
    
    if (filterToggle && filterPanel) {
        filterToggle.addEventListener('click', function() {
            filterPanel.classList.toggle('hidden');
        });
    }
    
    // District to Areas mapping
    const districtSelect = document.getElementById('district');
    const areaSelect = document.getElementById('area');
    
    if (districtSelect && areaSelect) {
        districtSelect.addEventListener('change', function() {
            const district = this.value;
            
            if (district) {
                fetch(`/properties/api/areas/${district}/`)
                    .then(response => response.json())
                    .then(data => {
                        areaSelect.innerHTML = '<option value="">All Areas</option>';
                        data.areas.forEach(function(area) {
                            areaSelect.innerHTML += `<option value="${area}">${area}</option>`;
                        });
                    });
            } else {
                areaSelect.innerHTML = '<option value="">Select District First</option>';
            }
        });
    }
    
    // Price range slider
    initPriceRangeSlider();
}

/**
 * Price Range Slider
 */
function initPriceRangeSlider() {
    const minPrice = document.getElementById('min-price');
    const maxPrice = document.getElementById('max-price');
    const priceDisplay = document.getElementById('price-display');
    
    if (minPrice && maxPrice && priceDisplay) {
        function updatePriceDisplay() {
            const min = parseInt(minPrice.value) || 0;
            const max = parseInt(maxPrice.value) || 100000;
            priceDisplay.textContent = `NPR ${min.toLocaleString()} - NPR ${max.toLocaleString()}`;
        }
        
        minPrice.addEventListener('input', updatePriceDisplay);
        maxPrice.addEventListener('input', updatePriceDisplay);
    }
}

/**
 * Get CSRF Cookie
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Confirm Dialog
 */
function confirmAction(message) {
    return confirm(message);
}

/**
 * Image Gallery/Lightbox
 */
function initImageGallery() {
    const mainImage = document.getElementById('main-gallery-image');
    const thumbnails = document.querySelectorAll('.gallery-thumbnail');
    
    if (mainImage && thumbnails.length) {
        thumbnails.forEach(function(thumb) {
            thumb.addEventListener('click', function() {
                mainImage.src = this.dataset.fullImage;
                thumbnails.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
            });
        });
    }
}

// Initialize gallery on page load
document.addEventListener('DOMContentLoaded', initImageGallery);

/**
 * Debounce function for search inputs
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Format number as NPR currency
 */
function formatNPR(amount) {
    return 'NPR ' + parseInt(amount).toLocaleString('en-IN');
}
