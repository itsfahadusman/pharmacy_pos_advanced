// Sidebar Toggle
document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.querySelector('.main-content');
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
            mainContent.classList.toggle('expanded');
        });
    }
    
    // Auto-dismiss alerts
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

// Format currency
function formatCurrency(amount) {
    return '₨ ' + parseFloat(amount).toFixed(2);
}

// Confirm delete
function confirmDelete(itemName) {
    return confirm(`Are you sure you want to delete "${itemName}"?`);
}

// Print functionality
function printPage() {
    window.print();
}

// Export table to CSV
function exportTableToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    for (let i = 0; i < rows.length; i++) {
        const row = [], cols = rows[i].querySelectorAll('td, th');
        
        for (let j = 0; j < cols.length; j++) {
            row.push(cols[j].innerText);
        }
        
        csv.push(row.join(','));
    }
    
    downloadCSV(csv.join('\n'), filename);
}

function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = 'none';
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

// Search functionality
function searchTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toUpperCase();
    const table = document.getElementById(tableId);
    const tr = table.getElementsByTagName('tr');
    
    for (let i = 1; i < tr.length; i++) {
        let txtValue = tr[i].textContent || tr[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = '';
        } else {
            tr[i].style.display = 'none';
        }
    }
}

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return false;
    }
    return true;
}

// Number input validation
function validateNumber(input, min = 0) {
    const value = parseFloat(input.value);
    if (isNaN(value) || value < min) {
        input.value = min;
    }
}

// Date validation
function validateDate(dateString) {
    const date = new Date(dateString);
    return date instanceof Date && !isNaN(date);
}

// Show loading spinner
function showLoading(buttonId) {
    const button = document.getElementById(buttonId);
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
}

// Hide loading spinner
function hideLoading(buttonId, originalText) {
    const button = document.getElementById(buttonId);
    button.disabled = false;
    button.innerHTML = originalText;
}

// Toast notification
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) {
        const container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
    
    const toastId = 'toast-' + Date.now();
    const toast = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    document.getElementById('toastContainer').insertAdjacentHTML('beforeend', toast);
    const toastElement = new bootstrap.Toast(document.getElementById(toastId));
    toastElement.show();
}

// Barcode scanner simulation
function handleBarcodeInput(inputId, callbackFunction) {
    let barcode = '';
    let reading = false;
    
    document.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            if (barcode.length > 0) {
                callbackFunction(barcode);
                barcode = '';
                reading = false;
            }
        } else {
            barcode += e.key;
            reading = true;
        }
        
        setTimeout(function() {
            if (reading) {
                barcode = '';
                reading = false;
            }
        }, 100);
    });
}

// Calculate total with discount and tax
function calculateTotal(price, quantity, discount = 0, taxRate = 0) {
    const subtotal = price * quantity;
    const discountAmount = subtotal * (discount / 100);
    const taxableAmount = subtotal - discountAmount;
    const tax = taxableAmount * (taxRate / 100);
    return taxableAmount + tax;
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
}

// Check expiry status
function checkExpiryStatus(expiryDate) {
    const today = new Date();
    const expiry = new Date(expiryDate);
    const diffTime = expiry - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays < 0) {
        return { status: 'expired', class: 'danger', text: 'Expired' };
    } else if (diffDays <= 30) {
        return { status: 'expiring', class: 'warning', text: `${diffDays} days left` };
    } else {
        return { status: 'valid', class: 'success', text: 'Valid' };
    }
}

// Auto-complete for search
function setupAutocomplete(inputId, dataSource) {
    const input = document.getElementById(inputId);
    const resultsContainer = document.createElement('div');
    resultsContainer.className = 'autocomplete-results';
    input.parentNode.appendChild(resultsContainer);
    
    input.addEventListener('input', function() {
        const value = this.value.toLowerCase();
        resultsContainer.innerHTML = '';
        
        if (value.length > 0) {
            const matches = dataSource.filter(item => 
                item.toLowerCase().includes(value)
            ).slice(0, 10);
            
            matches.forEach(match => {
                const div = document.createElement('div');
                div.textContent = match;
                div.addEventListener('click', function() {
                    input.value = match;
                    resultsContainer.innerHTML = '';
                });
                resultsContainer.appendChild(div);
            });
        }
    });
}
