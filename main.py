from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, Response
import sqlite3
from datetime import datetime, timedelta
from functools import wraps
import csv
import io
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'pharmacy_advanced_secret_key_2024')

# Use /tmp for Vercel (only writable directory in serverless)
UPLOAD_FOLDER = '/tmp/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Use /tmp for SQLite on Vercel (only writable directory)
DB = '/tmp/pharmacy.db'

# === Database Helper ===
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, args)
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return (result[0] if result else None) if one else result

def init_db():
    """Initialize database with all required tables"""
    conn = get_db()
    c = conn.cursor()
    
    # Admin table with enhanced fields
    c.execute('''CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        full_name TEXT,
        email TEXT,
        role TEXT DEFAULT 'admin',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP
    )''')
    
    # Medicine table with enhanced fields
    c.execute('''CREATE TABLE IF NOT EXISTS medicine (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        generic_name TEXT,
        brand TEXT,
        category TEXT,
        supplier_id INTEGER,
        quantity INTEGER DEFAULT 0,
        reorder_level INTEGER DEFAULT 10,
        cost_price REAL,
        price REAL,
        expiry_date DATE,
        barcode TEXT UNIQUE,
        batch_number TEXT,
        rack_location TEXT,
        description TEXT,
        image_url TEXT,
        requires_prescription INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
    )''')
    
    # Sales table with customer info
    c.execute('''CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_number TEXT UNIQUE,
        customer_id INTEGER,
        medicine_id INTEGER,
        quantity INTEGER,
        unit_price REAL,
        discount REAL DEFAULT 0,
        tax REAL DEFAULT 0,
        total_price REAL,
        payment_method TEXT,
        sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        cashier_id INTEGER,
        prescription_required INTEGER DEFAULT 0,
        prescription_number TEXT,
        FOREIGN KEY (medicine_id) REFERENCES medicine(id),
        FOREIGN KEY (customer_id) REFERENCES customers(id),
        FOREIGN KEY (cashier_id) REFERENCES admin(id)
    )''')
    
    # Customers table
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        email TEXT,
        address TEXT,
        date_of_birth DATE,
        medical_history TEXT,
        allergies TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        loyalty_points INTEGER DEFAULT 0
    )''')
    
    # Suppliers table
    c.execute('''CREATE TABLE IF NOT EXISTS suppliers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact_person TEXT,
        phone TEXT,
        email TEXT,
        address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Purchase orders table
    c.execute('''CREATE TABLE IF NOT EXISTS purchase_orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        po_number TEXT UNIQUE,
        supplier_id INTEGER,
        order_date DATE,
        expected_delivery DATE,
        status TEXT DEFAULT 'pending',
        total_amount REAL,
        notes TEXT,
        created_by INTEGER,
        FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
        FOREIGN KEY (created_by) REFERENCES admin(id)
    )''')
    
    # Purchase order items
    c.execute('''CREATE TABLE IF NOT EXISTS po_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        po_id INTEGER,
        medicine_id INTEGER,
        quantity INTEGER,
        unit_price REAL,
        FOREIGN KEY (po_id) REFERENCES purchase_orders(id),
        FOREIGN KEY (medicine_id) REFERENCES medicine(id)
    )''')
    
    # Inventory adjustments
    c.execute('''CREATE TABLE IF NOT EXISTS inventory_adjustments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicine_id INTEGER,
        adjustment_type TEXT,
        quantity_change INTEGER,
        reason TEXT,
        adjusted_by INTEGER,
        adjustment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (medicine_id) REFERENCES medicine(id),
        FOREIGN KEY (adjusted_by) REFERENCES admin(id)
    )''')
    
    # Activity log
    c.execute('''CREATE TABLE IF NOT EXISTS activity_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        details TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES admin(id)
    )''')
    
    # Notifications
    c.execute('''CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        message TEXT,
        is_read INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Create default admin if not exists
    c.execute("SELECT * FROM admin WHERE username='admin'")
    if not c.fetchone():
        hashed_pw = generate_password_hash('admin123')
        c.execute('''INSERT INTO admin (username, password, full_name, email, role) 
                     VALUES (?, ?, ?, ?, ?)''',
                 ('admin', hashed_pw, 'System Administrator', 'admin@pharmacy.com', 'admin'))
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# === Login Required Decorator ===
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# === Log Activity ===
def log_activity(action, details=''):
    if 'admin_id' in session:
        query_db('''INSERT INTO activity_log (user_id, action, details) 
                    VALUES (?, ?, ?)''', (session['admin_id'], action, details))

# === Create Notification ===
def create_notification(type, message):
    query_db('''INSERT INTO notifications (type, message) VALUES (?, ?)''', (type, message))

# === Routes ===

@app.route('/', methods=['GET', 'POST'])
def login():
    if 'admin_id' in session:
        return redirect(url_for('dashboard'))
    
    error = None
    if request.method == 'POST':
        user = query_db("SELECT * FROM admin WHERE username=?", 
                        (request.form['username'],), one=True)
        if user and check_password_hash(user['password'], request.form['password']):
            session['admin_id'] = user['id']
            session['admin'] = user['username']
            session['role'] = user['role']
            session['full_name'] = user['full_name']
            
            # Update last login
            query_db("UPDATE admin SET last_login=? WHERE id=?", 
                    (datetime.now(), user['id']))
            
            log_activity('Login', f"User {user['username']} logged in")
            flash(f'Welcome back, {user["full_name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid credentials'
            flash(error, 'danger')
    
    return render_template('login.html', error=error)

@app.route('/dashboard')
@login_required
def dashboard():
    # Get statistics
    total_medicines = query_db("SELECT COUNT(*) as count FROM medicine", one=True)['count']
    low_stock = query_db("SELECT COUNT(*) as count FROM medicine WHERE quantity < reorder_level", one=True)['count']
    
    today = datetime.today().strftime('%Y-%m-%d')
    expired = query_db("SELECT COUNT(*) as count FROM medicine WHERE expiry_date < ?", (today,), one=True)['count']
    expiring_soon = query_db("SELECT COUNT(*) as count FROM medicine WHERE expiry_date BETWEEN ? AND ?", 
                             (today, (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')), one=True)['count']
    
    # Sales statistics
    today_sales = query_db('''SELECT COALESCE(SUM(total_price), 0) as total 
                              FROM sales 
                              WHERE DATE(sale_date) = ?''', (today,), one=True)['total']
    
    month_start = datetime.today().replace(day=1).strftime('%Y-%m-%d')
    month_sales = query_db('''SELECT COALESCE(SUM(total_price), 0) as total 
                              FROM sales 
                              WHERE DATE(sale_date) >= ?''', (month_start,), one=True)['total']
    
    # Recent sales
    recent_sales = query_db('''
        SELECT s.*, m.name, c.name as customer_name 
        FROM sales s
        JOIN medicine m ON s.medicine_id = m.id
        LEFT JOIN customers c ON s.customer_id = c.id
        ORDER BY s.sale_date DESC
        LIMIT 10
    ''')
    
    # Unread notifications
    notifications = query_db("SELECT * FROM notifications WHERE is_read=0 ORDER BY created_at DESC LIMIT 5")
    
    return render_template('dashboard.html',
                         total_medicines=total_medicines,
                         low_stock=low_stock,
                         expired=expired,
                         expiring_soon=expiring_soon,
                         today_sales=today_sales,
                         month_sales=month_sales,
                         recent_sales=recent_sales,
                         notifications=notifications)

# === Medicine Management ===

@app.route('/medicines')
@login_required
def medicines():
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()
    sort_by = request.args.get('sort', 'name')
    order = request.args.get('order', 'ASC')
    
    base_query = "SELECT * FROM medicine WHERE 1=1"
    args = []
    
    if search:
        base_query += " AND (name LIKE ? OR brand LIKE ? OR generic_name LIKE ? OR barcode LIKE ?)"
        search_term = f'%{search}%'
        args.extend([search_term, search_term, search_term, search_term])
    
    if category:
        base_query += " AND category = ?"
        args.append(category)
    
    # Sorting
    allowed_sorts = ['name', 'brand', 'quantity', 'price', 'expiry_date']
    if sort_by in allowed_sorts:
        base_query += f" ORDER BY {sort_by} {order}"
    
    meds = query_db(base_query, args)
    categories = query_db("SELECT DISTINCT category FROM medicine WHERE category IS NOT NULL")
    
    return render_template('medicines.html', 
                         medicines=meds, 
                         categories=categories, 
                         selected_category=category, 
                         search=search,
                         sort_by=sort_by,
                         order=order)

@app.route('/add_medicine', methods=['GET', 'POST'])
@login_required
def add_medicine():
    if request.method == 'POST':
        query_db('''INSERT INTO medicine 
                    (name, generic_name, brand, category, supplier_id, quantity, reorder_level,
                     cost_price, price, expiry_date, barcode, batch_number, rack_location, 
                     description, requires_prescription)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                 (request.form['name'], request.form.get('generic_name'),
                  request.form['brand'], request.form['category'],
                  request.form.get('supplier_id') or None,
                  request.form['quantity'], request.form.get('reorder_level', 10),
                  request.form.get('cost_price'), request.form['price'],
                  request.form['expiry_date'], request.form.get('barcode'),
                  request.form.get('batch_number'), request.form.get('rack_location'),
                  request.form.get('description'), 
                  1 if request.form.get('requires_prescription') else 0))
        
        log_activity('Add Medicine', f"Added medicine: {request.form['name']}")
        flash(f"Medicine '{request.form['name']}' added successfully!", 'success')
        return redirect(url_for('medicines'))
    
    suppliers = query_db("SELECT * FROM suppliers ORDER BY name")
    return render_template('add_medicine.html', suppliers=suppliers)

@app.route('/edit_medicine/<int:med_id>', methods=['GET', 'POST'])
@login_required
def edit_medicine(med_id):
    if request.method == 'POST':
        query_db('''UPDATE medicine
                    SET name=?, generic_name=?, brand=?, category=?, supplier_id=?, 
                        quantity=?, reorder_level=?, cost_price=?, price=?, expiry_date=?, 
                        barcode=?, batch_number=?, rack_location=?, description=?,
                        requires_prescription=?, updated_at=?
                    WHERE id=?''',
                 (request.form['name'], request.form.get('generic_name'),
                  request.form['brand'], request.form['category'],
                  request.form.get('supplier_id') or None,
                  request.form['quantity'], request.form.get('reorder_level', 10),
                  request.form.get('cost_price'), request.form['price'],
                  request.form['expiry_date'], request.form.get('barcode'),
                  request.form.get('batch_number'), request.form.get('rack_location'),
                  request.form.get('description'),
                  1 if request.form.get('requires_prescription') else 0,
                  datetime.now(), med_id))
        
        log_activity('Edit Medicine', f"Updated medicine ID: {med_id}")
        flash('Medicine updated successfully!', 'success')
        return redirect(url_for('medicines'))
    
    medicine = query_db('SELECT * FROM medicine WHERE id=?', (med_id,), one=True)
    suppliers = query_db("SELECT * FROM suppliers ORDER BY name")
    return render_template('edit_medicine.html', medicine=medicine, suppliers=suppliers)

@app.route('/delete_medicine/<int:med_id>')
@login_required
def delete_medicine(med_id):
    medicine = query_db("SELECT name FROM medicine WHERE id=?", (med_id,), one=True)
    query_db("DELETE FROM medicine WHERE id=?", (med_id,))
    log_activity('Delete Medicine', f"Deleted medicine: {medicine['name']}")
    flash(f"Medicine '{medicine['name']}' deleted successfully!", 'success')
    return redirect(url_for('medicines'))

# === Point of Sale ===

@app.route('/pos', methods=['GET', 'POST'])
@login_required
def pos():
    if request.method == 'POST':
        data = request.get_json()
        
        # Generate invoice number
        invoice_number = f"INV{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        total_amount = 0
        customer_id = data.get('customer_id') or None
        payment_method = data.get('payment_method', 'cash')
        
        conn = get_db()
        c = conn.cursor()
        
        try:
            for item in data['items']:
                medicine_id = item['medicine_id']
                quantity = int(item['quantity'])
                discount = float(item.get('discount', 0))
                
                # Get medicine details
                c.execute("SELECT * FROM medicine WHERE id=?", (medicine_id,))
                med = c.fetchone()
                
                if not med:
                    conn.close()
                    return jsonify({'success': False, 'message': 'Medicine not found'}), 400
                
                if med['quantity'] < quantity:
                    conn.close()
                    return jsonify({'success': False, 'message': f'Insufficient stock for {med["name"]}'}), 400
                
                # Calculate prices
                unit_price = med['price']
                subtotal = unit_price * quantity
                discount_amount = subtotal * (discount / 100)
                tax = (subtotal - discount_amount) * 0.05  # 5% tax
                total_price = subtotal - discount_amount + tax
                total_amount += total_price
                
                # Update stock
                c.execute("UPDATE medicine SET quantity = quantity - ? WHERE id = ?", (quantity, medicine_id))
                
                # Insert sale record
                c.execute('''INSERT INTO sales 
                            (invoice_number, customer_id, medicine_id, quantity, unit_price, 
                             discount, tax, total_price, payment_method, cashier_id)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                         (invoice_number, customer_id, medicine_id, quantity, unit_price,
                          discount, tax, total_price, payment_method, session['admin_id']))
                
                # Check if stock is low
                if med['quantity'] - quantity < med['reorder_level']:
                    create_notification('low_stock', f"{med['name']} is running low (Stock: {med['quantity'] - quantity})")
            
            conn.commit()
            conn.close()
            
            log_activity('Sale', f"Invoice: {invoice_number}, Amount: {total_amount:.2f}")
            
            return jsonify({
                'success': True, 
                'message': 'Sale completed successfully',
                'invoice_number': invoice_number,
                'total_amount': total_amount
            })
            
        except Exception as e:
            conn.rollback()
            conn.close()
            return jsonify({'success': False, 'message': str(e)}), 500
    
    # GET request
    medicines = query_db("SELECT * FROM medicine WHERE quantity > 0 AND expiry_date >= date('now') ORDER BY name")
    customers = query_db("SELECT * FROM customers ORDER BY name")
    return render_template('pos.html', medicines=medicines, customers=customers)

# === Sales Reports ===

@app.route('/sales_report')
@login_required
def sales_report():
    start_date = request.args.get('start_date', datetime.today().replace(day=1).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', datetime.today().strftime('%Y-%m-%d'))
    
    sales = query_db('''
        SELECT s.*, m.name as medicine_name, c.name as customer_name, a.full_name as cashier_name
        FROM sales s
        JOIN medicine m ON s.medicine_id = m.id
        LEFT JOIN customers c ON s.customer_id = c.id
        LEFT JOIN admin a ON s.cashier_id = a.id
        WHERE DATE(s.sale_date) BETWEEN ? AND ?
        ORDER BY s.sale_date DESC
    ''', (start_date, end_date))
    
    # Calculate totals
    total_sales = sum(sale['total_price'] for sale in sales)
    total_items = sum(sale['quantity'] for sale in sales)
    
    return render_template('sales_report.html', 
                         sales=sales, 
                         start_date=start_date, 
                         end_date=end_date,
                         total_sales=total_sales,
                         total_items=total_items)

# === Inventory Management ===

@app.route('/low_stock')
@login_required
def low_stock():
    low_stock_meds = query_db('''
        SELECT m.*, s.name as supplier_name 
        FROM medicine m
        LEFT JOIN suppliers s ON m.supplier_id = s.id
        WHERE m.quantity < m.reorder_level
        ORDER BY m.quantity ASC
    ''')
    return render_template('low_stock.html', medicines=low_stock_meds)

@app.route('/expired')
@login_required
def expired_medicines():
    today = datetime.today().strftime('%Y-%m-%d')
    expired = query_db("SELECT * FROM medicine WHERE expiry_date < ? ORDER BY expiry_date", (today,))
    
    thirty_days = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')
    expiring_soon = query_db("SELECT * FROM medicine WHERE expiry_date BETWEEN ? AND ? ORDER BY expiry_date", 
                            (today, thirty_days))
    
    return render_template('expired.html', expired=expired, expiring_soon=expiring_soon)

@app.route('/inventory_adjustment', methods=['GET', 'POST'])
@login_required
def inventory_adjustment():
    if request.method == 'POST':
        medicine_id = request.form['medicine_id']
        adjustment_type = request.form['adjustment_type']
        quantity_change = int(request.form['quantity_change'])
        reason = request.form['reason']
        
        # Update medicine quantity
        if adjustment_type == 'add':
            query_db("UPDATE medicine SET quantity = quantity + ? WHERE id = ?", (quantity_change, medicine_id))
        else:
            query_db("UPDATE medicine SET quantity = quantity - ? WHERE id = ?", (quantity_change, medicine_id))
        
        # Log adjustment
        query_db('''INSERT INTO inventory_adjustments 
                    (medicine_id, adjustment_type, quantity_change, reason, adjusted_by)
                    VALUES (?, ?, ?, ?, ?)''',
                (medicine_id, adjustment_type, quantity_change, reason, session['admin_id']))
        
        log_activity('Inventory Adjustment', f"Medicine ID: {medicine_id}, Type: {adjustment_type}, Qty: {quantity_change}")
        flash('Inventory adjusted successfully!', 'success')
        return redirect(url_for('medicines'))
    
    medicines = query_db("SELECT * FROM medicine ORDER BY name")
    return render_template('inventory_adjustment.html', medicines=medicines)

# === Customer Management ===

@app.route('/customers')
@login_required
def customers():
    customers = query_db("SELECT * FROM customers ORDER BY name")
    return render_template('customers.html', customers=customers)

@app.route('/add_customer', methods=['GET', 'POST'])
@login_required
def add_customer():
    if request.method == 'POST':
        query_db('''INSERT INTO customers (name, phone, email, address, date_of_birth, medical_history, allergies)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (request.form['name'], request.form.get('phone'), request.form.get('email'),
                 request.form.get('address'), request.form.get('date_of_birth'),
                 request.form.get('medical_history'), request.form.get('allergies')))
        
        log_activity('Add Customer', f"Added customer: {request.form['name']}")
        flash(f"Customer '{request.form['name']}' added successfully!", 'success')
        return redirect(url_for('customers'))
    
    return render_template('add_customer.html')

@app.route('/edit_customer/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def edit_customer(customer_id):
    if request.method == 'POST':
        query_db('''UPDATE customers
                    SET name=?, phone=?, email=?, address=?, date_of_birth=?, medical_history=?, allergies=?
                    WHERE id=?''',
                (request.form['name'], request.form.get('phone'), request.form.get('email'),
                 request.form.get('address'), request.form.get('date_of_birth'),
                 request.form.get('medical_history'), request.form.get('allergies'), customer_id))
        
        log_activity('Edit Customer', f"Updated customer ID: {customer_id}")
        flash('Customer updated successfully!', 'success')
        return redirect(url_for('customers'))
    
    customer = query_db('SELECT * FROM customers WHERE id=?', (customer_id,), one=True)
    return render_template('edit_customer.html', customer=customer)

# === Supplier Management ===

@app.route('/suppliers')
@login_required
def suppliers():
    suppliers = query_db("SELECT * FROM suppliers ORDER BY name")
    return render_template('suppliers.html', suppliers=suppliers)

@app.route('/add_supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if request.method == 'POST':
        query_db('''INSERT INTO suppliers (name, contact_person, phone, email, address)
                    VALUES (?, ?, ?, ?, ?)''',
                (request.form['name'], request.form.get('contact_person'),
                 request.form.get('phone'), request.form.get('email'), request.form.get('address')))
        
        log_activity('Add Supplier', f"Added supplier: {request.form['name']}")
        flash(f"Supplier '{request.form['name']}' added successfully!", 'success')
        return redirect(url_for('suppliers'))
    
    return render_template('add_supplier.html')

# === Purchase Orders ===

@app.route('/purchase_orders')
@login_required
def purchase_orders():
    pos = query_db('''
        SELECT po.*, s.name as supplier_name, a.full_name as created_by_name
        FROM purchase_orders po
        JOIN suppliers s ON po.supplier_id = s.id
        LEFT JOIN admin a ON po.created_by = a.id
        ORDER BY po.order_date DESC
    ''')
    return render_template('purchase_orders.html', purchase_orders=pos)

@app.route('/create_po', methods=['GET', 'POST'])
@login_required
def create_po():
    if request.method == 'POST':
        data = request.get_json()
        
        # Generate PO number
        po_number = f"PO{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        conn = get_db()
        c = conn.cursor()
        
        try:
            # Create purchase order
            c.execute('''INSERT INTO purchase_orders 
                        (po_number, supplier_id, order_date, expected_delivery, status, total_amount, notes, created_by)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                     (po_number, data['supplier_id'], data['order_date'], data['expected_delivery'],
                      'pending', data['total_amount'], data.get('notes'), session['admin_id']))
            
            po_id = c.lastrowid
            
            # Add items
            for item in data['items']:
                c.execute('''INSERT INTO po_items (po_id, medicine_id, quantity, unit_price)
                            VALUES (?, ?, ?, ?)''',
                         (po_id, item['medicine_id'], item['quantity'], item['unit_price']))
            
            conn.commit()
            conn.close()
            
            log_activity('Create PO', f"PO Number: {po_number}")
            return jsonify({'success': True, 'po_number': po_number})
            
        except Exception as e:
            conn.rollback()
            conn.close()
            return jsonify({'success': False, 'message': str(e)}), 500
    
    suppliers = query_db("SELECT * FROM suppliers ORDER BY name")
    medicines = query_db("SELECT * FROM medicine ORDER BY name")
    return render_template('create_po.html', suppliers=suppliers, medicines=medicines)

# === Analytics ===

@app.route('/analytics')
@login_required
def analytics():
    # Sales by category
    sales_by_category = query_db('''
        SELECT m.category, SUM(s.total_price) as total_sales, SUM(s.quantity) as total_quantity
        FROM sales s
        JOIN medicine m ON s.medicine_id = m.id
        WHERE m.category IS NOT NULL
        GROUP BY m.category
        ORDER BY total_sales DESC
    ''')
    
    # Top selling medicines
    top_medicines = query_db('''
        SELECT m.name, SUM(s.quantity) as total_sold, SUM(s.total_price) as revenue
        FROM sales s
        JOIN medicine m ON s.medicine_id = m.id
        GROUP BY s.medicine_id
        ORDER BY total_sold DESC
        LIMIT 10
    ''')
    
    # Daily sales trend (last 30 days)
    daily_sales = query_db('''
        SELECT DATE(sale_date) as date, SUM(total_price) as total
        FROM sales
        WHERE sale_date >= date('now', '-30 days')
        GROUP BY DATE(sale_date)
        ORDER BY date
    ''')
    
    return render_template('analytics.html',
                         sales_by_category=sales_by_category,
                         top_medicines=top_medicines,
                         daily_sales=daily_sales)

# === Export Functions ===

@app.route('/export_inventory')
@login_required
def export_inventory():
    medicines = query_db("SELECT * FROM medicine")
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Name', 'Generic Name', 'Brand', 'Category', 'Quantity', 
                    'Reorder Level', 'Cost Price', 'Selling Price', 'Expiry Date', 
                    'Barcode', 'Batch Number', 'Rack Location'])
    
    for med in medicines:
        writer.writerow([med['id'], med['name'], med['generic_name'], med['brand'], 
                        med['category'], med['quantity'], med['reorder_level'],
                        med['cost_price'], med['price'], med['expiry_date'],
                        med['barcode'], med['batch_number'], med['rack_location']])
    
    output.seek(0)
    return Response(output, mimetype='text/csv',
                   headers={'Content-Disposition': 'attachment;filename=inventory_export.csv'})

@app.route('/export_sales')
@login_required
def export_sales():
    start_date = request.args.get('start_date', datetime.today().replace(day=1).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', datetime.today().strftime('%Y-%m-%d'))
    
    sales = query_db('''
        SELECT s.*, m.name as medicine_name, c.name as customer_name
        FROM sales s
        JOIN medicine m ON s.medicine_id = m.id
        LEFT JOIN customers c ON s.customer_id = c.id
        WHERE DATE(s.sale_date) BETWEEN ? AND ?
        ORDER BY s.sale_date DESC
    ''', (start_date, end_date))
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Invoice', 'Medicine', 'Customer', 'Quantity', 'Unit Price', 
                    'Discount', 'Tax', 'Total', 'Payment Method', 'Date'])
    
    for sale in sales:
        writer.writerow([sale['invoice_number'], sale['medicine_name'], 
                        sale['customer_name'] or 'Walk-in', sale['quantity'],
                        sale['unit_price'], sale['discount'], sale['tax'],
                        sale['total_price'], sale['payment_method'], sale['sale_date']])
    
    output.seek(0)
    return Response(output, mimetype='text/csv',
                   headers={'Content-Disposition': f'attachment;filename=sales_report_{start_date}_to_{end_date}.csv'})

# === CSV Import Medicine ===

@app.route('/import_medicines', methods=['GET', 'POST'])
@login_required
def import_medicines():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file uploaded!', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected!', 'danger')
            return redirect(request.url)
        
        if not file.filename.endswith('.csv'):
            flash('Please upload a CSV file only!', 'danger')
            return redirect(request.url)
        
        try:
            # Read CSV file
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_reader = csv.DictReader(stream)
            
            success_count = 0
            error_count = 0
            errors = []
            
            conn = get_db()
            c = conn.cursor()
            
            for row_num, row in enumerate(csv_reader, start=2):  # Start from 2 (header is row 1)
                try:
                    # Validate required fields
                    if not row.get('name') or not row.get('brand') or not row.get('price'):
                        errors.append(f"Row {row_num}: Missing required fields (name, brand, price)")
                        error_count += 1
                        continue
                    
                    # Check if barcode already exists (if provided)
                    barcode = row.get('barcode', '').strip()
                    if barcode:
                        c.execute("SELECT id FROM medicine WHERE barcode=?", (barcode,))
                        if c.fetchone():
                            errors.append(f"Row {row_num}: Barcode {barcode} already exists")
                            error_count += 1
                            continue
                    
                    # Insert medicine
                    c.execute('''INSERT INTO medicine 
                                (name, generic_name, brand, category, quantity, reorder_level,
                                 cost_price, price, expiry_date, barcode, batch_number, rack_location, 
                                 description, requires_prescription)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                             (row.get('name', '').strip(),
                              row.get('generic_name', '').strip() or None,
                              row.get('brand', '').strip(),
                              row.get('category', '').strip() or None,
                              int(row.get('quantity', 0) or 0),
                              int(row.get('reorder_level', 10) or 10),
                              float(row.get('cost_price', 0) or 0) or None,
                              float(row.get('price', 0)),
                              row.get('expiry_date', '').strip() or None,
                              barcode or None,
                              row.get('batch_number', '').strip() or None,
                              row.get('rack_location', '').strip() or None,
                              row.get('description', '').strip() or None,
                              1 if str(row.get('requires_prescription', '0')).strip() == '1' else 0))
                    
                    success_count += 1
                    
                except Exception as e:
                    errors.append(f"Row {row_num}: {str(e)}")
                    error_count += 1
            
            conn.commit()
            conn.close()
            
            log_activity('Import Medicines', f"Imported {success_count} medicines, {error_count} errors")
            
            # Show results
            if success_count > 0:
                flash(f'Successfully imported {success_count} medicines!', 'success')
            
            if error_count > 0:
                flash(f'{error_count} rows had errors. Check details below.', 'warning')
                for error in errors[:10]:  # Show first 10 errors
                    flash(error, 'danger')
                if len(errors) > 10:
                    flash(f'... and {len(errors) - 10} more errors', 'danger')
            
            return redirect(url_for('medicines'))
            
        except Exception as e:
            flash(f'Error reading CSV file: {str(e)}', 'danger')
            return redirect(request.url)
    
    return render_template('import_medicines.html')

@app.route('/download_sample_csv')
@login_required
def download_sample_csv():
    """Download a sample CSV template"""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header row
    writer.writerow(['name', 'generic_name', 'brand', 'category', 'quantity', 'reorder_level', 
                    'cost_price', 'price', 'expiry_date', 'barcode', 'batch_number', 
                    'rack_location', 'description', 'requires_prescription'])
    
    # Sample data rows
    writer.writerow(['Paracetamol 500mg', 'Acetaminophen', 'Calpol', 'Painkiller', '100', '20', 
                    '5.50', '10.00', '2026-12-31', '8901234567890', 'BATCH001', 'A-1-5', 
                    'For fever and pain relief', '0'])
    writer.writerow(['Amoxicillin 250mg', 'Amoxicillin', 'Novamox', 'Antibiotic', '50', '15', 
                    '15.00', '25.00', '2026-06-30', '8901234567891', 'BATCH002', 'A-2-3', 
                    'Broad spectrum antibiotic', '1'])
    writer.writerow(['Cetirizine 10mg', 'Cetirizine', 'Zyrtec', 'Antihistamine', '80', '20', 
                    '3.00', '8.00', '2027-03-15', '8901234567892', 'BATCH003', 'B-1-2', 
                    'For allergies', '0'])
    
    output.seek(0)
    return Response(output, mimetype='text/csv',
                   headers={'Content-Disposition': 'attachment;filename=medicine_import_template.csv'})


# === Settings & User Management ===

@app.route('/settings')
@login_required
def settings():
    users = query_db("SELECT * FROM admin ORDER BY created_at DESC")
    return render_template('settings.html', users=users)

@app.route('/add_user', methods=['POST'])
@login_required
def add_user():
    if session.get('role') != 'admin':
        flash('Only admins can add users.', 'danger')
        return redirect(url_for('settings'))
    
    username = request.form['username']
    password = request.form['password']
    full_name = request.form['full_name']
    email = request.form.get('email')
    role = request.form['role']
    
    hashed_pw = generate_password_hash(password)
    
    try:
        query_db('''INSERT INTO admin (username, password, full_name, email, role)
                    VALUES (?, ?, ?, ?, ?)''',
                (username, hashed_pw, full_name, email, role))
        
        log_activity('Add User', f"Added user: {username}")
        flash(f"User '{username}' added successfully!", 'success')
    except sqlite3.IntegrityError:
        flash('Username already exists!', 'danger')
    
    return redirect(url_for('settings'))

# === Activity Log ===

@app.route('/activity_log')
@login_required
def activity_log():
    logs = query_db('''
        SELECT a.*, ad.full_name
        FROM activity_log a
        JOIN admin ad ON a.user_id = ad.id
        ORDER BY a.timestamp DESC
        LIMIT 100
    ''')
    return render_template('activity_log.html', logs=logs)

# === Notifications ===

@app.route('/notifications')
@login_required
def notifications():
    all_notifications = query_db("SELECT * FROM notifications ORDER BY created_at DESC")
    return render_template('notifications.html', notifications=all_notifications)

@app.route('/mark_notification_read/<int:notif_id>')
@login_required
def mark_notification_read(notif_id):
    query_db("UPDATE notifications SET is_read=1 WHERE id=?", (notif_id,))
    return redirect(url_for('notifications'))

# === Logout ===

@app.route('/logout')
def logout():
    log_activity('Logout', f"User {session.get('admin')} logged out")
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=False)