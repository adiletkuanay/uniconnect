// Main JavaScript file for UniConnect Kazakhstan

// Initialize all tooltips
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Initialize all popovers
document.addEventListener('DOMContentLoaded', function() {
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });

    return isValid;
}

// File upload preview
function previewImage(input, previewId) {
    const preview = document.getElementById(previewId);
    if (!preview) return;

    const file = input.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        }
        reader.readAsDataURL(file);
    }
}

// Dynamic form fields
function addFormField(containerId, template) {
    const container = document.getElementById(containerId);
    if (!container || !template) return;

    const newField = template.cloneNode(true);
    newField.classList.remove('d-none');
    container.appendChild(newField);
}

// Remove form field
function removeFormField(button) {
    const field = button.closest('.form-field');
    if (field) {
        field.remove();
    }
}

// Character counter for textareas
function updateCharacterCount(textarea, counterId, maxLength) {
    const counter = document.getElementById(counterId);
    if (!counter) return;

    const remaining = maxLength - textarea.value.length;
    counter.textContent = `${remaining} characters remaining`;
    
    if (remaining < 20) {
        counter.classList.add('text-danger');
    } else {
        counter.classList.remove('text-danger');
    }
}

// Smooth scroll to element
function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;

    element.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// Toggle password visibility
function togglePasswordVisibility(inputId, toggleId) {
    const input = document.getElementById(inputId);
    const toggle = document.getElementById(toggleId);
    if (!input || !toggle) return;

    if (input.type === 'password') {
        input.type = 'text';
        toggle.innerHTML = '<i class="bi bi-eye-slash"></i>';
    } else {
        input.type = 'password';
        toggle.innerHTML = '<i class="bi bi-eye"></i>';
    }
}

// Format currency
function formatCurrency(amount, currency = 'KZT') {
    return new Intl.NumberFormat('kk-KZ', {
        style: 'currency',
        currency: currency
    }).format(amount);
}

// Format date
function formatDate(date) {
    return new Intl.DateTimeFormat('kk-KZ', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
}

// Handle form submission with AJAX
function handleFormSubmit(formId, successCallback, errorCallback) {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        if (!validateForm(formId)) {
            return;
        }

        const formData = new FormData(form);
        
        fetch(form.action, {
            method: form.method,
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (successCallback) successCallback(data);
        })
        .catch(error => {
            if (errorCallback) errorCallback(error);
        });
    });
}

// Get CSRF token from cookies
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