// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all features
    initSmoothScroll();
    initFormValidation();
    initFormEnhancements();
    initAnimations();
});

// Smooth scrolling for anchor links
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
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
}

// Form validation and enhancements
function initFormValidation() {
    const form = document.getElementById('predictionForm');
    if (!form) return;

    // Add real-time validation
    const inputs = form.querySelectorAll('input[type="number"]');
    
    inputs.forEach(input => {
        // Add input event listener for real-time feedback
        input.addEventListener('input', function() {
            validateInput(this);
        });

        // Add blur event for final validation
        input.addEventListener('blur', function() {
            validateInput(this);
        });
    });

    // Form submission validation
    form.addEventListener('submit', function(e) {
        let isValid = true;
        
        inputs.forEach(input => {
            if (!validateInput(input)) {
                isValid = false;
            }
        });

        if (!isValid) {
            e.preventDefault();
            showNotification('Please fill in all fields correctly', 'error');
            // Scroll to first error
            const firstError = form.querySelector('.input-error');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        } else {
            showLoadingState(true);
        }
    });
}

// Validate individual input
function validateInput(input) {
    const value = parseFloat(input.value);
    const min = parseFloat(input.min);
    const max = parseFloat(input.max);
    const formGroup = input.closest('.form-group');
    
    // Remove existing error
    const existingError = formGroup.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    input.classList.remove('input-error', 'input-success');

    // Check if empty
    if (!input.value || input.value.trim() === '') {
        if (input.hasAttribute('required')) {
            addError(formGroup, input, 'This field is required');
            return false;
        }
        return true;
    }

    // Check if valid number
    if (isNaN(value)) {
        addError(formGroup, input, 'Please enter a valid number');
        return false;
    }

    // Check min value
    if (!isNaN(min) && value < min) {
        addError(formGroup, input, `Value must be at least ${min}`);
        return false;
    }

    // Check max value
    if (!isNaN(max) && value > max) {
        addError(formGroup, input, `Value must be no more than ${max}`);
        return false;
    }

    // Special validations
    if (input.id === 'BsmtFin_SF_1' || input.id === 'Total_Bsmt_SF') {
        const totalBsmt = parseFloat(document.getElementById('Total_Bsmt_SF').value) || 0;
        const finishedBsmt = parseFloat(document.getElementById('BsmtFin_SF_1').value) || 0;
        
        if (finishedBsmt > totalBsmt) {
            addError(formGroup, input, 'Finished basement cannot exceed total basement');
            return false;
        }
    }

    // If we get here, input is valid
    input.classList.add('input-success');
    return true;
}

// Add error message to input
function addError(formGroup, input, message) {
    input.classList.add('input-error');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.style.color = '#ef4444';
    errorDiv.style.fontSize = '0.875rem';
    errorDiv.style.marginTop = '0.25rem';
    errorDiv.textContent = message;
    formGroup.appendChild(errorDiv);
}

// Form enhancements
function initFormEnhancements() {
    const form = document.getElementById('predictionForm');
    if (!form) return;

    // Auto-calculate years since remodel based on remodel year
    const remodYearInput = document.getElementById('year_since_remod');
    if (remodYearInput) {
        // Add helper text about year calculation
        const helperText = remodYearInput.nextElementSibling;
        if (helperText && helperText.tagName === 'SMALL') {
            helperText.textContent = 'Years since last renovation (0 = this year)';
        }
    }

    // Add input formatting
    const inputs = form.querySelectorAll('input[type="number"]');
    inputs.forEach(input => {
        // Add thousand separators on blur (visual only)
        input.addEventListener('focus', function() {
            // Remove formatting when focusing
            this.dataset.rawValue = this.value;
        });
    });

    // Reset button functionality
    const resetButton = form.querySelector('button[type="reset"]');
    if (resetButton) {
        resetButton.addEventListener('click', function(e) {
            e.preventDefault();
            if (confirm('Are you sure you want to reset all fields?')) {
                form.reset();
                // Remove all validation classes
                inputs.forEach(input => {
                    input.classList.remove('input-error', 'input-success');
                    const formGroup = input.closest('.form-group');
                    const errorMsg = formGroup.querySelector('.error-message');
                    if (errorMsg) errorMsg.remove();
                });
            }
        });
    }
}

// Show notification
function showNotification(message, type = 'info') {
    // Remove existing notification
    const existing = document.querySelector('.notification');
    if (existing) {
        existing.remove();
    }

    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        background: ${type === 'error' ? '#ef4444' : type === 'success' ? '#10b981' : '#6366f1'};
        color: white;
        font-weight: 600;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        z-index: 1000;
        animation: slideInRight 0.3s ease-out;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-in';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Loading state for form submission
function showLoadingState(show) {
    const form = document.getElementById('predictionForm');
    if (!form) return;

    const submitButton = form.querySelector('button[type="submit"]');
    
    if (show) {
        submitButton.disabled = true;
        submitButton.innerHTML = `
            <span style="display: inline-flex; align-items: center; gap: 0.5rem;">
                <span class="spinner"></span>
                Predicting...
            </span>
        `;
        
        // Add spinner styles if not already present
        if (!document.getElementById('spinner-styles')) {
            const style = document.createElement('style');
            style.id = 'spinner-styles';
            style.textContent = `
                .spinner {
                    width: 16px;
                    height: 16px;
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    border-top-color: white;
                    border-radius: 50%;
                    animation: spin 0.6s linear infinite;
                }
                @keyframes spin {
                    to { transform: rotate(360deg); }
                }
                @keyframes slideInRight {
                    from {
                        opacity: 0;
                        transform: translateX(100px);
                    }
                    to {
                        opacity: 1;
                        transform: translateX(0);
                    }
                }
                @keyframes slideOutRight {
                    from {
                        opacity: 1;
                        transform: translateX(0);
                    }
                    to {
                        opacity: 0;
                        transform: translateX(100px);
                    }
                }
                .input-error {
                    border-color: #ef4444 !important;
                }
                .input-success {
                    border-color: #10b981 !important;
                }
            `;
            document.head.appendChild(style);
        }
    } else {
        submitButton.disabled = false;
        submitButton.textContent = 'Predict House Price';
    }
}

// Initialize scroll animations
function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe feature cards and other animated elements
    const animatedElements = document.querySelectorAll('.feature-card, .about-card, .use-case');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease-out';
        observer.observe(el);
    });
}

// Add tooltip functionality for form fields
function addTooltips() {
    const formGroups = document.querySelectorAll('.form-group');
    
    formGroups.forEach(group => {
        const label = group.querySelector('label');
        const input = group.querySelector('input');
        
        if (label && input && input.title) {
            label.style.cursor = 'help';
            label.title = input.title;
        }
    });
}

// Call tooltip function on load
document.addEventListener('DOMContentLoaded', addTooltips);

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const form = document.getElementById('predictionForm');
        if (form && document.activeElement.tagName === 'INPUT') {
            form.requestSubmit();
        }
    }
});

// Scroll to top button
function addScrollToTop() {
    const scrollBtn = document.createElement('button');
    scrollBtn.innerHTML = '↑';
    scrollBtn.className = 'scroll-to-top';
    scrollBtn.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: var(--primary-color);
        color: white;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s;
        z-index: 999;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    `;

    document.body.appendChild(scrollBtn);

    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            scrollBtn.style.opacity = '1';
            scrollBtn.style.visibility = 'visible';
        } else {
            scrollBtn.style.opacity = '0';
            scrollBtn.style.visibility = 'hidden';
        }
    });

    scrollBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Initialize scroll to top button
document.addEventListener('DOMContentLoaded', addScrollToTop);