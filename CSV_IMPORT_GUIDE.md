# 📥 Complete Guide to Import Medicines via CSV

## Quick Start

### 3 Simple Steps:
1. **Download Template** - Get the sample CSV file
2. **Fill Your Data** - Add your medicines in Excel/Google Sheets
3. **Upload** - Import all medicines at once

---

## Detailed Instructions

### Step 1: Access Import Feature

1. Login to your Pharmacy POS
2. Go to **Medicines** page
3. Click **Import CSV** button (green button at top)

### Step 2: Download Sample Template

Click "Download Sample CSV Template" button to get a pre-formatted file with:
- Correct column headers
- Sample data rows
- Proper formatting examples

### Step 3: Prepare Your CSV File

#### Using Microsoft Excel:
1. Open the downloaded template in Excel
2. Keep the header row (first row) as is
3. Fill in your medicine data starting from row 2
4. Save as: **File → Save As → CSV (Comma delimited)**

#### Using Google Sheets:
1. Upload template to Google Sheets
2. Fill in your medicine data
3. Download as: **File → Download → Comma Separated Values (.csv)**

---

## CSV Format Details

### Required Columns (Must Have):
- `name` - Medicine name (e.g., "Paracetamol 500mg")
- `brand` - Brand name (e.g., "Calpol")
- `price` - Selling price (e.g., "10.00")

### Optional Columns (Recommended):
- `generic_name` - Generic/scientific name
- `category` - Medicine category
- `quantity` - Current stock quantity
- `reorder_level` - When to reorder
- `cost_price` - Purchase price
- `expiry_date` - Expiry date (YYYY-MM-DD format)
- `barcode` - Barcode number (must be unique)
- `batch_number` - Batch/lot number
- `rack_location` - Physical location
- `description` - Additional details
- `requires_prescription` - 1 for yes, 0 for no

---

## Example CSV File

```csv
name,generic_name,brand,category,quantity,reorder_level,cost_price,price,expiry_date,barcode,batch_number,rack_location,description,requires_prescription
Paracetamol 500mg,Acetaminophen,Calpol,Painkiller,100,20,5.50,10.00,2026-12-31,8901234567890,BATCH001,A-1-5,For fever and pain relief,0
Amoxicillin 250mg,Amoxicillin,Novamox,Antibiotic,50,15,15.00,25.00,2026-06-30,8901234567891,BATCH002,A-2-3,Broad spectrum antibiotic,1
Cetirizine 10mg,Cetirizine,Zyrtec,Antihistamine,80,20,3.00,8.00,2027-03-15,8901234567892,BATCH003,B-1-2,For allergies,0
Omeprazole 20mg,Omeprazole,Omez,Antacid,60,15,8.00,15.00,2026-09-20,8901234567893,BATCH004,A-3-1,For acidity and GERD,0
Metformin 500mg,Metformin,Glycomet,Antidiabetic,90,25,4.50,12.00,2027-01-10,8901234567894,BATCH005,C-1-4,For diabetes type 2,1
```

---

## Field Format Guide

| Field | Type | Format | Example | Notes |
|-------|------|--------|---------|-------|
| name | Text | Any text | Paracetamol 500mg | Required |
| generic_name | Text | Any text | Acetaminophen | Optional |
| brand | Text | Any text | Calpol | Required |
| category | Text | Any text | Painkiller | Optional |
| quantity | Number | Integer | 100 | Default: 0 |
| reorder_level | Number | Integer | 20 | Default: 10 |
| cost_price | Number | Decimal | 5.50 | Optional |
| price | Number | Decimal | 10.00 | Required |
| expiry_date | Date | YYYY-MM-DD | 2026-12-31 | Optional |
| barcode | Text | Any text | 8901234567890 | Must be unique |
| batch_number | Text | Any text | BATCH001 | Optional |
| rack_location | Text | Any text | A-1-5 | Optional |
| description | Text | Any text | For fever | Optional |
| requires_prescription | Number | 0 or 1 | 0 | 0=No, 1=Yes |

---

## Important Rules

### ✅ DO:
- Keep header row exactly as shown
- Use YYYY-MM-DD for dates (e.g., 2026-12-31)
- Use 0 or 1 for requires_prescription field
- Ensure barcodes are unique
- Double-check required fields
- Save file as CSV format

### ❌ DON'T:
- Don't change column header names
- Don't add extra columns
- Don't use different date formats
- Don't duplicate barcodes
- Don't leave required fields empty
- Don't save as Excel (.xlsx) - must be CSV

---

## Common Categories

Here are some common medicine categories you can use:
- Antibiotic
- Painkiller
- Antacid
- Antihistamine
- Antidiabetic
- Vitamin
- Antiseptic
- Cough & Cold
- Cardiovascular
- Dermatology

---

## Tips for Large Imports

### Importing 100+ Medicines:
1. **Split into batches** - Import 100-200 at a time
2. **Test first** - Import 5-10 medicines to verify format
3. **Backup database** - Copy pharmacy.db before large imports
4. **Check barcodes** - Ensure no duplicates in your CSV

### Excel Tips:
- Use **Freeze Panes** to keep header visible while scrolling
- Use **Data Validation** for categories (consistent naming)
- Use **Find & Replace** to fix formatting issues
- Format date columns as "Text" to prevent auto-formatting

---

## Troubleshooting

### Import Failed - Common Issues:

**"Missing required fields"**
- Solution: Ensure name, brand, and price are filled for every row

**"Barcode already exists"**
- Solution: Check for duplicate barcodes in your CSV or database

**"Error reading CSV file"**
- Solution: Ensure file is saved as CSV, not Excel format

**"Invalid date format"**
- Solution: Use YYYY-MM-DD format (e.g., 2026-12-31)

**Some rows imported, others failed**
- Solution: Check error messages - system will show which rows had issues

### Getting Help:
- Check the first 10 error messages shown after import
- Fix those issues in your CSV
- Try importing again

---

## After Import

### Verify Import:
1. Go to **Medicines** page
2. Check total count increased
3. Search for a few imported medicines
4. Verify all fields are correct

### Next Steps:
1. Review imported medicines
2. Assign suppliers if needed
3. Check low stock items
4. Update rack locations if necessary

---

## Sample Data Included

A sample CSV file with 10 medicines is included:
- `sample_medicines.csv`

You can use this as a reference or starting point for your own data.

---

## Batch Import Best Practices

### For New Pharmacy:
1. Start with top 50 most-used medicines
2. Import in batches of 20-30
3. Verify each batch before next import
4. Add remaining medicines gradually

### For Existing Stock:
1. Export current inventory first (for backup)
2. Prepare comprehensive CSV with all medicines
3. Import during off-hours
4. Verify all data post-import

---

## Advanced Tips

### Using Excel Formulas:
```excel
- Auto-generate batch numbers: ="BATCH"&TEXT(ROW()-1,"000")
- Calculate selling price: =C2*1.3 (where C2 is cost price, 1.3 is 30% markup)
- Set reorder level: =INT(D2*0.2) (where D2 is quantity, 20% of stock)
```

### Data Validation in Excel:
1. Select category column
2. Data → Data Validation → List
3. Enter: Antibiotic,Painkiller,Vitamin,Antacid
4. Now you can select from dropdown

---

## Quick Reference

### Minimum CSV Format:
```csv
name,brand,price
Paracetamol 500mg,Calpol,10.00
Aspirin 75mg,Disprin,5.00
```

### Complete CSV Format:
```csv
name,generic_name,brand,category,quantity,reorder_level,cost_price,price,expiry_date,barcode,batch_number,rack_location,description,requires_prescription
Paracetamol 500mg,Acetaminophen,Calpol,Painkiller,100,20,5.50,10.00,2026-12-31,8901234567890,BATCH001,A-1-5,For fever and pain relief,0
```

---

## Need More Help?

1. Use the **Download Sample CSV Template** button in the import page
2. Check the **Field Reference Table** at the bottom of import page
3. Review error messages after upload for specific issues
4. Start with small batch (5-10 items) to test

---

**Happy Importing! 🎉**

Your medicines will be imported in seconds instead of entering them one by one!
