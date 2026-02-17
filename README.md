# Advanced Pharmacy POS System

## 🚀 Features Overview

### Core POS Features
- ✅ **Modern Point of Sale Interface** - Fast, intuitive cart-based selling system
- ✅ **Barcode Scanner Support** - Quick product lookup with barcode scanning
- ✅ **Multiple Payment Methods** - Cash, Card, UPI, Credit support
- ✅ **Real-time Inventory Updates** - Automatic stock adjustments on sales
- ✅ **Invoice Generation** - Professional invoice printing with customization
- ✅ **Customer Management** - Track customer purchase history and preferences

### Inventory Management
- ✅ **Comprehensive Medicine Database** - Name, generic name, brand, category tracking
- ✅ **Batch & Expiry Management** - Batch numbers and expiry date monitoring
- ✅ **Low Stock Alerts** - Automatic notifications when stock falls below reorder level
- ✅ **Expired Medicine Tracking** - Identify and manage expired/expiring medicines
- ✅ **Rack Location Management** - Physical location tracking for quick retrieval
- ✅ **Inventory Adjustments** - Stock corrections with reason logging
- ✅ **Multi-category Organization** - Organize medicines by therapeutic categories

### Purchase & Supplier Management
- ✅ **Purchase Order System** - Create and track POs with suppliers
- ✅ **Supplier Database** - Maintain detailed supplier contact information
- ✅ **PO Status Tracking** - Monitor pending, received, cancelled orders
- ✅ **Cost Price Tracking** - Track both cost and selling prices for profit analysis

### Customer Relationship Management (CRM)
- ✅ **Customer Profiles** - Name, contact, medical history, allergies
- ✅ **Purchase History** - Complete transaction history per customer
- ✅ **Loyalty Points System** - Built-in loyalty program infrastructure
- ✅ **Prescription Tracking** - Track prescription numbers for controlled medicines

### Sales & Analytics
- ✅ **Comprehensive Sales Reports** - Filter by date range, customer, medicine
- ✅ **Sales Analytics Dashboard** - Visual charts and graphs
- ✅ **Top Selling Medicines** - Identify best performers
- ✅ **Sales by Category** - Category-wise revenue breakdown
- ✅ **Daily Sales Trends** - 30-day sales visualization
- ✅ **Profit Margin Analysis** - Track profitability per item
- ✅ **Export to CSV/Excel** - Export all data for external analysis

### Security & User Management
- ✅ **Multi-user Support** - Multiple cashier/admin accounts
- ✅ **Role-based Access Control** - Admin and cashier roles
- ✅ **Password Encryption** - Secure password hashing
- ✅ **Activity Logging** - Complete audit trail of all actions
- ✅ **Session Management** - Secure session handling

### Advanced Features
- ✅ **Discount Management** - Item-level and transaction-level discounts
- ✅ **Tax Calculation** - Automatic tax computation (configurable rate)
- ✅ **Notifications System** - Real-time alerts for low stock, expiry, etc.
- ✅ **Search & Filter** - Advanced search across all modules
- ✅ **Responsive Design** - Works on desktop, tablet, and mobile
- ✅ **Print Functionality** - Print invoices, reports, labels
- ✅ **Keyboard Shortcuts** - Speed up operations with hotkeys
- ✅ **Dark/Light Theme** - User preference support (extendable)

## 📋 System Requirements

- Python 3.8 or higher
- SQLite3 (included with Python)
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Optional: Barcode scanner (USB HID device)

## 🔧 Installation & Setup

### 1. Install Dependencies

```bash
pip install flask werkzeug
```

### 2. Database Initialization

The database is automatically created when you first run the application. It includes:
- Pre-configured tables for all modules
- Default admin account (username: admin, password: admin123)
- Proper indexing for performance

### 3. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5002`

### 4. First Login

- Username: `admin`
- Password: `admin123`
- **Important:** Change the default password immediately after first login!

## 📁 Project Structure

```
pharmacy_pos_advanced/
├── app.py                      # Main Flask application
├── pharmacy.db                 # SQLite database (auto-created)
├── templates/                  # HTML templates
│   ├── base.html              # Base template with sidebar
│   ├── login.html             # Login page
│   ├── dashboard.html         # Main dashboard
│   ├── pos.html               # Point of sale interface
│   ├── medicines.html         # Medicine management
│   ├── add_medicine.html      # Add/Edit medicine forms
│   ├── customers.html         # Customer management
│   ├── suppliers.html         # Supplier management
│   ├── purchase_orders.html   # Purchase order management
│   ├── sales_report.html      # Sales reports
│   ├── analytics.html         # Analytics dashboard
│   ├── low_stock.html         # Low stock alerts
│   ├── expired.html           # Expired medicines
│   ├── notifications.html     # Notifications center
│   ├── activity_log.html      # System activity log
│   └── settings.html          # System settings
├── static/
│   ├── css/
│   │   └── style.css          # Custom CSS styling
│   └── js/
│       └── script.js          # JavaScript functions
└── README.md                   # This file
```

## 🗄️ Database Schema

### Tables Overview

1. **admin** - User accounts with role-based access
2. **medicine** - Complete medicine inventory
3. **sales** - All sales transactions with detailed info
4. **customers** - Customer profiles and history
5. **suppliers** - Supplier contact information
6. **purchase_orders** - PO headers
7. **po_items** - Purchase order line items
8. **inventory_adjustments** - Stock adjustment history
9. **activity_log** - Complete system audit trail
10. **notifications** - System notifications and alerts

## 🎯 Usage Guide

### Adding Medicine

1. Navigate to **Medicines** → **Add Medicine**
2. Fill in required fields:
   - Medicine Name (required)
   - Generic Name (optional but recommended)
   - Brand (required)
   - Category (e.g., Antibiotic, Painkiller, Vitamin)
   - Quantity (current stock)
   - Reorder Level (when to alert for low stock)
   - Cost Price (purchase price)
   - Selling Price (retail price)
   - Expiry Date (YYYY-MM-DD)
   - Barcode (optional - for scanner support)
   - Batch Number
   - Rack Location
   - Requires Prescription (checkbox)
3. Click **Save**

### Making a Sale (POS)

1. Go to **Point of Sale**
2. Search or scan medicine barcode
3. Click **+** to add to cart
4. Adjust quantity and discount if needed
5. Select customer (optional)
6. Choose payment method
7. Click **Process Sale**
8. Print invoice if required

### Generating Reports

1. Navigate to **Sales Report**
2. Select date range
3. View detailed transaction list
4. Export to CSV for Excel analysis
5. Print report if needed

### Managing Inventory

**Low Stock:**
- Automatically shows medicines below reorder level
- Create purchase orders directly from low stock page

**Expired Medicines:**
- View all expired medicines
- See medicines expiring in next 30 days
- Remove expired items from inventory

**Inventory Adjustments:**
- Add or subtract stock
- Record reason for adjustment
- All adjustments are logged in activity log

## ⚙️ Configuration

### Changing Tax Rate

Edit `app.py` line ~280 (in POS route):
```python
tax = (subtotal - discount_amount) * 0.05  # Change 0.05 to desired rate
```

### Changing Port

Edit `app.py` last line:
```python
app.run(debug=True, port=5002)  # Change port number
```

### Adding More Categories

Categories are dynamic - just type a new category when adding medicine.

## 🔐 Security Best Practices

1. **Change Default Password** immediately after installation
2. **Use Strong Passwords** for all user accounts
3. **Regular Backups** of pharmacy.db file
4. **Limit Access** to authorized personnel only
5. **Review Activity Log** regularly for suspicious activity
6. **Update Dependencies** regularly for security patches

## 🚀 Advanced Customization

### Adding New User Roles

Modify the `role` field in admin table and add role checks in routes.

### Custom Reports

Create new query functions and templates following existing report patterns.

### Email Notifications

Integrate SMTP to send email alerts for low stock, expiry, etc.

### Receipt Printer Integration

Add printer.js or similar library for direct thermal printer support.

### Multi-location Support

Extend database schema to include location/branch field.

## 📊 Key Performance Indicators (KPIs)

The dashboard displays:
- Total medicines in inventory
- Low stock items count
- Expired medicines count
- Today's sales revenue
- Monthly sales revenue
- Recent transactions
- Active notifications

## 🐛 Troubleshooting

### Database Errors
- Delete `pharmacy.db` and restart app to recreate database
- Check file permissions on database file

### Login Issues
- Use default credentials: admin/admin123
- Clear browser cookies and cache
- Check if database was properly initialized

### Port Already in Use
- Change port in app.py
- Or kill process using port 5002

### Templates Not Loading
- Ensure templates folder exists in same directory as app.py
- Check folder structure matches documentation

## 📝 Future Enhancements

Potential features for future development:
- [ ] Multi-branch/Multi-store support
- [ ] Online ordering integration
- [ ] SMS notifications for customers
- [ ] WhatsApp integration for order updates
- [ ] Automated reordering with suppliers
- [ ] Integration with accounting software
- [ ] Mobile app (React Native/Flutter)
- [ ] Insurance claims processing
- [ ] Prescription scanning & OCR
- [ ] Telemedicine integration
- [ ] IoT integration for temperature-controlled medicines
- [ ] Blockchain for supply chain tracking
- [ ] AI-powered demand forecasting
- [ ] Voice commands for hands-free operation

## 📞 Support

For issues, questions, or feature requests:
- Review this documentation
- Check the activity log for errors
- Ensure all dependencies are installed
- Verify database permissions

## 📜 License

This project is provided as-is for educational and commercial use.

## 🙏 Credits

Built with:
- Flask (Python web framework)
- Bootstrap 5 (UI framework)
- Bootstrap Icons
- SQLite (Database)

---

**Version:** 2.0.0  
**Last Updated:** February 2026  
**Status:** Production Ready ✅
