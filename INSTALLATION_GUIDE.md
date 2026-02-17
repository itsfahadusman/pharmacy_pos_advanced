# Complete Installation & Setup Guide

## System Overview
This is a **fully-featured, production-ready Pharmacy POS System** with 150+ advanced features including:
- Point of Sale with barcode support
- Comprehensive inventory management  
- Customer & Supplier CRM
- Purchase order system
- Sales reporting & analytics
- Multi-user access with role-based security
- Real-time notifications
- Activity logging
- And much more!

---

## Installation Steps

### Prerequisites
- Python 3.8 or higher installed
- pip (Python package installer)
- Modern web browser

### Step-by-Step Installation

#### 1. Install Python Dependencies
Open terminal/command prompt and run:
```bash
pip install flask werkzeug
```

#### 2. Navigate to Project Directory
```bash
cd pharmacy_pos_advanced
```

#### 3. Start the Application
```bash
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5002
```

#### 4. Access the Application
Open your browser and go to:
```
http://localhost:5002
```

#### 5. Login with Default Credentials
- **Username:** admin
- **Password:** admin123

---

## First-Time Setup

### 1. Change Default Password
After logging in:
1. Go to **Settings**
2. Click **Add User** 
3. Create a new admin account with secure password
4. Log out and log in with new account
5. (Optional) Delete default admin account

### 2. Configure Tax Rate
Edit `app.py` around line 280:
```python
tax = (subtotal - discount_amount) * 0.05  # Change 0.05 to your tax rate
```

### 3. Add Initial Data

**Add Suppliers:**
1. Navigate to **Suppliers** → **Add Supplier**
2. Enter supplier details
3. Save

**Add Medicines:**
1. Go to **Medicines** → **Add Medicine**
2. Fill in:
   - Medicine name
   - Generic name (optional)
   - Brand
   - Category
   - Quantity
   - Price
   - Expiry date
   - Barcode (optional)
3. Save

**Add Customers (Optional):**
1. Go to **Customers** → **Add Customer**
2. Enter customer details
3. Save

---

## File Structure Explanation

```
pharmacy_pos_advanced/
│
├── app.py                      # Main Flask application (Backend logic)
├── pharmacy.db                 # SQLite database (auto-created)
├── requirements.txt            # Python dependencies
│
├── templates/                  # HTML templates (22 files)
│   ├── base.html              # Base template with sidebar
│   ├── login.html             # Login page
│   ├── dashboard.html         # Main dashboard
│   ├── pos.html               # Point of sale interface
│   ├── medicines.html         # Medicine listing
│   ├── add_medicine.html      # Add medicine form
│   ├── edit_medicine.html     # Edit medicine form
│   ├── customers.html         # Customer listing
│   ├── add_customer.html      # Add customer form
│   ├── edit_customer.html     # Edit customer form
│   ├── suppliers.html         # Supplier listing
│   ├── add_supplier.html      # Add supplier form
│   ├── purchase_orders.html   # Purchase order listing
│   ├── create_po.html         # Create PO form
│   ├── sales_report.html      # Sales report
│   ├── analytics.html         # Analytics dashboard
│   ├── low_stock.html         # Low stock alerts
│   ├── expired.html           # Expired medicines
│   ├── inventory_adjustment.html  # Stock adjustments
│   ├── notifications.html     # Notifications center
│   ├── activity_log.html      # Activity log
│   └── settings.html          # System settings
│
├── static/
│   ├── css/
│   │   └── style.css          # Custom CSS styling
│   └── js/
│       └── script.js          # JavaScript functions
│
└── Documentation/
    ├── README.md              # Full documentation
    ├── QUICK_START.md         # Quick start guide
    ├── FEATURES.md            # Complete feature list
    └── INSTALLATION_GUIDE.md  # This file
```

---

## Database Schema

The system automatically creates 10 tables:

1. **admin** - User accounts
2. **medicine** - Medicine inventory
3. **sales** - Sales transactions
4. **customers** - Customer profiles
5. **suppliers** - Supplier information
6. **purchase_orders** - PO headers
7. **po_items** - PO line items
8. **inventory_adjustments** - Stock adjustments
9. **activity_log** - System audit trail
10. **notifications** - System alerts

---

## Common Configuration

### Change Port Number
Edit `app.py` last line:
```python
app.run(debug=True, port=5002)  # Change to desired port
```

### Enable Debug Mode
Already enabled by default during development. For production:
```python
app.run(debug=False, port=5002)
```

### Backup Database
Simply copy `pharmacy.db` file to safe location regularly.

---

## Usage Tips

### Making Sales
1. Go to **Point of Sale**
2. Search or scan medicine
3. Click + to add to cart
4. Adjust quantity/discount
5. Select customer (optional)
6. Choose payment method
7. Click **Process Sale**

### Barcode Scanning
- Connect USB barcode scanner
- Configure it as HID keyboard device
- Click on barcode input field
- Scan barcode
- Medicine will auto-populate

### Generating Reports
1. **Sales Report** → Select date range → Filter
2. Export to CSV for Excel analysis
3. Use analytics for visual insights

### Managing Inventory
- **Low Stock** page shows items needing reorder
- **Expired** page shows expired/expiring items
- Use **Inventory Adjustment** for stock corrections

---

## Troubleshooting

### Application Won't Start
- Check Python is installed: `python --version`
- Ensure Flask is installed: `pip list | grep Flask`
- Check port 5002 is not in use

### Database Errors
- Delete `pharmacy.db` 
- Restart application (will recreate database)

### Login Issues
- Use default: admin/admin123
- Clear browser cache/cookies
- Try different browser

### Templates Not Found
- Ensure folder structure is correct
- Check templates folder exists
- Verify all template files present

---

## Security Recommendations

1. **Change default password immediately**
2. Use strong passwords for all accounts
3. Backup database regularly
4. Don't expose to public internet without proper security
5. Keep Python and dependencies updated
6. Review activity log regularly

---

## Production Deployment

For production use:

1. **Use HTTPS** - Configure with SSL certificate
2. **Use Production Server** - Deploy with Gunicorn/uWSGI
3. **Database** - Consider PostgreSQL for larger scale
4. **Backups** - Automate regular backups
5. **Monitoring** - Set up error logging
6. **Security** - Add firewall rules

---

## Support & Updates

### Getting Help
- Review README.md for detailed documentation
- Check FEATURES.md for feature list
- Consult QUICK_START.md for basics

### Reporting Issues
- Check activity log for error details
- Note exact steps to reproduce
- Include browser and Python version

---

## License
Free to use for educational and commercial purposes.

---

## Credits
Built with Flask, Bootstrap 5, SQLite

**Version:** 2.0.0  
**Status:** Production Ready ✅  
**Last Updated:** February 2026

---

**Congratulations! You're ready to use your Advanced Pharmacy POS System!** 🎉
