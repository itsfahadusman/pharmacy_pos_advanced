# Quick Start Guide - Advanced Pharmacy POS

## Installation (3 Simple Steps)

### Step 1: Install Python Dependencies
```bash
pip install flask werkzeug
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Open in Browser
Navigate to: **http://localhost:5002**

---

## Default Login
- **Username:** admin
- **Password:** admin123

**⚠️ Change password immediately after first login!**

---

## Key Features at a Glance

### 🛒 Point of Sale
- Fast cart-based selling
- Barcode scanner support
- Multiple payment methods
- Automatic invoice generation

### 📦 Inventory
- Low stock alerts
- Expiry tracking
- Batch management
- Location tracking

### 👥 Customer & Supplier
- Customer profiles
- Purchase history
- Supplier management
- PO system

### 📊 Reports & Analytics
- Sales reports
- Top selling items
- Category analysis
- Export to CSV

---

## Common Tasks

### Add a Medicine
1. Go to **Medicines** → **Add Medicine**
2. Fill required fields (Name, Brand, Price, Expiry)
3. Click **Save**

### Make a Sale
1. Go to **Point of Sale**
2. Search medicine or scan barcode
3. Click **+** to add to cart
4. Adjust quantity/discount if needed
5. Click **Process Sale**

### View Low Stock
1. Go to **Inventory** → **Low Stock**
2. View items below reorder level
3. Create purchase orders as needed

### Generate Sales Report
1. Go to **Sales Report**
2. Select date range
3. Click **Filter**
4. Export to CSV if needed

---

## File Structure
```
pharmacy_pos_advanced/
├── app.py              # Main application
├── pharmacy.db         # Database (auto-created)
├── templates/          # HTML files
├── static/
│   ├── css/
│   └── js/
└── README.md           # Full documentation
```

---

## Database
- Automatically created on first run
- SQLite database (pharmacy.db)
- No manual setup required

---

## Troubleshooting

### Port Already in Use?
Edit app.py last line, change port:
```python
app.run(debug=True, port=5003)  # Change to any free port
```

### Can't Login?
Use default credentials: admin / admin123

### Database Errors?
Delete pharmacy.db and restart app (will recreate)

---

## Next Steps
1. ✅ Change default admin password
2. ✅ Add your medicines
3. ✅ Add customers/suppliers
4. ✅ Configure tax rate if needed
5. ✅ Start making sales!

---

## Need Help?
See full README.md for detailed documentation

**Version:** 2.0.0 | **Status:** Production Ready ✅
