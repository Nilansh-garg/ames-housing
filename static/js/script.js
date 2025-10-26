// DOM Content Loaded Event
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initNavigation();
    initFormValidation();
    initAnimations();
    initTooltips();
});

// ===== NAVIGATION FUNCTIONALITY =====
function initNavigation() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.color = 'var(--primary-color)';
        }
    });
}

// ===== FORM VALIDATION =====
function initFormValidation() {
    const form = document.getElementById('predictionForm');
    
    if (form) {
        // Real-time validation for numeric inputs
        const numericInputs = form.querySelectorAll('input[type="number"]');
        
        numericInputs.forEach(input => {
            input.addEventListener('input', function() {
                validateNumericInput(this);
            });
            
            input.addEventListener('blur', function() {
                validateNumericInput(this);
            });
        });
        
        // Form submission validation
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                showAlert('Please fill in all fields correctly', 'error');
            }
        });
        
        // Reset form functionality
        const resetButton = form.querySelector('button[type="reset"]');
        if (resetButton) {
            resetButton.addEventListener('click', function() {
                setTimeout(() => {
                    removeAllErrors();
                }, 100);
            });
        }

        // Add dependent field validation
        addDependentFieldValidation();
    }
}

// Validate numeric input
function validateNumericInput(input) {
    const value = parseFloat(input.value);
    const min = parseFloat(input.min);
    const max = parseFloat(input.max);
    
    // Remove previous error
    removeError(input);
    
    if (input.value === '') {
        return;
    }
    
    if (isNaN(value)) {
        showError(input, 'Please enter a valid number');
        return false;
    }
    
    if (min !== undefined && value < min) {
        showError(input, `Value must be at least ${min}`);
        return false;
    }
    
    if (max !== undefined && value > max) {
        showError(input, `Value must be at most ${max}`);
        return false;
    }
    
    return true;
}

// Validate entire form
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (input.type === 'number') {
            if (!validateNumericInput(input) || input.value === '') {
                isValid = false;
            }
        } else if (input.value === '') {
            showError(input, 'This field is required');
            isValid = false;
        }
    });
    
    return isValid;
}

// Show error message
function showError(input, message) {
    const formGroup = input.closest('.form-group');
    
    // Remove existing error
    removeError(input);
    
    // Add error class
    input.style.borderColor = 'var(--error)';
    
    // Create and append error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.style.color = 'var(--error)';
    errorDiv.style.fontSize = '0.875rem';
    errorDiv.style.marginTop = '0.25rem';
    errorDiv.textContent = message;
    
    formGroup.appendChild(errorDiv);
}

// Remove error message
function removeError(input) {
    const formGroup = input.closest('.form-group');
    const errorMessage = formGroup.querySelector('.error-message');
    
    if (errorMessage) {
        errorMessage.remove();
    }
    
    input.style.borderColor = 'var(--border-color)';
}

// Remove all errors
function removeAllErrors() {
    const errorMessages = document.querySelectorAll('.error-message');
    errorMessages.forEach(error => error.remove());
    
    const inputs = document.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.style.borderColor = 'var(--border-color)';
    });
}

// Add dependent field validation (e.g., finished basement should not exceed total basement)
function addDependentFieldValidation() {
    const totalBsmtInput = document.getElementById('Total_Bsmt_SF');
    const finishedBsmtInput = document.getElementById('BsmtFin_SF_1');
    const garageCarInput = document.getElementById('Garage_Cars');
    const garageAreaInput = document.getElementById('Garage_Area');
    
    if (totalBsmtInput && finishedBsmtInput) {
        finishedBsmtInput.addEventListener('blur', function() {
            const total = parseFloat(totalBsmtInput.value);
            const finished = parseFloat(finishedBsmtInput.value);
            
            if (total && finished && finished > total) {
                showError(finishedBsmtInput, 'Finished area cannot exceed total basement area');
            }
        });
        
        totalBsmtInput.addEventListener('input', function() {
            if (finishedBsmtInput.value) {
                finishedBsmtInput.dispatchEvent(new Event('blur'));
            }
        });
    }
    
    // Validate garage area relative to number of cars
    if (garageCarInput && garageAreaInput) {
        garageAreaInput.addEventListener('blur', function() {
            const cars = parseFloat(garageCarInput.value);
            const area = parseFloat(garageAreaInput.value);
            
            if (cars && area) {
                const minAreaPerCar = 200;
                const expectedMinArea = cars * minAreaPerCar;
                
                if (area < expectedMinArea) {
                    showError(garageAreaInput, `Area seems small for ${cars} car(s). Typical minimum: ${expectedMinArea} sq ft`);
                }
            }
        });
    }
}

// Show alert message
function showAlert(message, type = 'info') {
    const existingAlert = document.querySelector('.alert');
    if (existingAlert) {
        existingAlert.remove();
    }
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `<strong>${type === 'error' ? 'Error:' : 'Info:'}</strong> ${message}`;
    
    const form = document.querySelector('.prediction-form');
    if (form) {
        form.parentNode.insertBefore(alert, form);
        
        // Scroll to alert
        alert.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            alert.remove();
        }, 5000);
    }
}

// ===== ANIMATIONS =====
function initAnimations() {
    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe feature cards and about cards
    const animatedElements = document.querySelectorAll('.feature-card, .about-card');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });
}

// ===== TOOLTIPS =====
function initTooltips() {
    const inputs = document.querySelectorAll('input[title]');
    
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            showTooltip(this);
        });
        
        input.addEventListener('blur', function() {
            hideTooltip(this);
        });
    });
}

function showTooltip(element) {
    const title = element.getAttribute('title');
    if (!title) return;
    
    const tooltip = document.createElement('div');
    tooltip.className = 'custom-tooltip';
    tooltip.textContent = title;
    tooltip.style.cssText = `
        position: absolute;
        background: var(--text-primary);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.875rem;
        z-index: 1000;
        white-space: nowrap;
        box-shadow: var(--shadow-lg);
        pointer-events: none;
    `;
    
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.top = `${rect.top - tooltip.offsetHeight - 10}px`;
    tooltip.style.left = `${rect.left + (rect.width - tooltip.offsetWidth) / 2}px`;
    
    element.tooltipElement = tooltip;
}

function hideTooltip(element) {
    if (element.tooltipElement) {
        element.tooltipElement.remove();
        element.tooltipElement = null;
    }
}

// ===== UTILITY FUNCTIONS =====

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add loading state to submit button
const forms = document.querySelectorAll('form');
forms.forEach(form => {
    form.addEventListener('submit', function() {
        const submitButton = this.querySelector('button[type="submit"]');
        if (submitButton && validateForm(this)) {
            submitButton.textContent = 'Processing...';
            submitButton.disabled = true;
            submitButton.style.opacity = '0.7';
        }
    });
});

// Auto-format numbers (add commas for thousands)
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Round to 2 decimal places
function roundTo2Decimals(num) {
    return Math.round(num * 100) / 100;
}

// ===== DYNAMIC FEATURES =====

// Add input placeholder animations
const inputs = document.querySelectorAll('input, select');
inputs.forEach(input => {
    input.addEventListener('focus', function() {
        this.style.transform = 'scale(1.02)';
        this.style.transition = 'transform 0.2s ease';
    });
    
    input.addEventListener('blur', function() {
        this.style.transform = 'scale(1)';
    });
});

// Console welcome message
console.log('%c🏠 HomeValue AI', 'color: #4F46E5; font-size: 24px; font-weight: bold;');
console.log('%cPredicting property values with machine learning', 'color: #6B7280; font-size: 14px;');

// Performance monitoring
window.addEventListener('load', function() {
    const loadTime = window.performance.timing.domContentLoadedEventEnd - window.performance.timing.navigationStart;
    console.log(`%cPage loaded in ${loadTime}ms`, 'color: #10B981; font-weight: bold;');
});