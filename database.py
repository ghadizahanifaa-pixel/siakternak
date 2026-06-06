import sqlite3
import hashlib
from datetime import datetime
import os
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

DB_NAME = 'siakternak.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    c = conn.cursor()

    # Table for users
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT UNIQUE, password TEXT, 
                  nama_lengkap TEXT, created_at TEXT)''')

    # Table for pemasukan (Income)
    # Columns: No (id), jumlah_sapi (Penjualan Sapi (total)), total_harga (Total Penjualan (rp)), tanggal
    c.execute('''CREATE TABLE IF NOT EXISTS pemasukan 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  jumlah_sapi INTEGER, 
                  total_harga INTEGER, 
                  tanggal TEXT)''')

    # Table for pengeluaran (Expense)
    # Columns: No (id), produk (Produk), kategori (Kategori), nominal (Nominal), tanggal
    c.execute('''CREATE TABLE IF NOT EXISTS pengeluaran 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  produk TEXT, 
                  kategori TEXT, 
                  nominal INTEGER, 
                  tanggal TEXT)''')

    # Insert default admin if not exists
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        default_password = hashlib.sha256("admin123".encode()).hexdigest()
        c.execute("INSERT INTO users (username, password, nama_lengkap, created_at) VALUES (?,?,?,?)",
                  ("admin", default_password, "Administrator", datetime.now().strftime("%d/%m/%Y %H:%M")))

    # Check if tables are empty to insert dummy data
    c.execute("SELECT COUNT(*) FROM pemasukan")
    has_pemasukan = c.fetchone()[0] > 0
    c.execute("SELECT COUNT(*) FROM pengeluaran")
    has_pengeluaran = c.fetchone()[0] > 0
    
    if not has_pemasukan and not has_pengeluaran:
        # Insert Pemasukan dummy
        pemasukan_dummies = [
            (5, 75000000, "10/02/2026 10:00"),
            (3, 48000000, "15/03/2026 14:30"),
            (6, 96000000, "02/04/2026 09:15"),
            (4, 64000000, "20/05/2026 16:45"),
            (8, 128000000, "05/06/2026 11:20")
        ]
        c.executemany("INSERT INTO pemasukan (jumlah_sapi, total_harga, tanggal) VALUES (?, ?, ?)", pemasukan_dummies)
        
        # Insert Pengeluaran dummy
        pengeluaran_dummies = [
            ("Pakan Konsentrat", "Pakan", 15000000, "12/02/2026 11:00"),
            ("Vaksin & Obat Sapi", "Kesehatan", 5000000, "18/02/2026 15:30"),
            ("Pakan Hijauan", "Pakan", 12000000, "16/03/2026 10:00"),
            ("Vitamin Organik", "Kesehatan", 4500000, "05/04/2026 14:00"),
            ("Pakan Konsentrat", "Pakan", 18000000, "22/05/2026 11:00"),
            ("Layanan Medis Dokter", "Kesehatan", 8000000, "06/06/2026 12:00")
        ]
        c.executemany("INSERT INTO pengeluaran (produk, kategori, nominal, tanggal) VALUES (?, ?, ?, ?)", pengeluaran_dummies)

    conn.commit()
    conn.close()

# --- AUTHENTICATION ---
def verify_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
    user = c.fetchone()
    conn.close()
    return user

# --- PEMASUKAN CRUD ---
def add_pemasukan(jumlah_sapi, total_harga, tanggal=None):
    if not tanggal:
        tanggal = datetime.now().strftime("%d/%m/%Y %H:%M")
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO pemasukan (jumlah_sapi, total_harga, tanggal) VALUES (?, ?, ?)",
              (int(jumlah_sapi), int(total_harga), tanggal))
    conn.commit()
    conn.close()

def get_all_pemasukan():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, jumlah_sapi, total_harga, tanggal FROM pemasukan ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def update_pemasukan(db_id, jumlah_sapi, total_harga):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE pemasukan SET jumlah_sapi=?, total_harga=? WHERE id=?",
              (int(jumlah_sapi), int(total_harga), int(db_id)))
    conn.commit()
    conn.close()

def delete_pemasukan(db_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM pemasukan WHERE id=?", (int(db_id),))
    conn.commit()
    conn.close()

# --- PENGELUARAN CRUD ---
def add_pengeluaran(produk, kategori, nominal, tanggal=None):
    if not tanggal:
        tanggal = datetime.now().strftime("%d/%m/%Y %H:%M")
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO pengeluaran (produk, kategori, nominal, tanggal) VALUES (?, ?, ?, ?)",
              (produk, kategori, int(nominal), tanggal))
    conn.commit()
    conn.close()

def get_all_pengeluaran():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, produk, kategori, nominal, tanggal FROM pengeluaran ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def update_pengeluaran(db_id, produk, kategori, nominal):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE pengeluaran SET produk=?, kategori=?, nominal=? WHERE id=?",
              (produk, kategori, int(nominal), int(db_id)))
    conn.commit()
    conn.close()

def delete_pengeluaran(db_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM pengeluaran WHERE id=?", (int(db_id),))
    conn.commit()
    conn.close()

# --- SUMMARY & DASHBOARD ---
def get_summary():
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("SELECT SUM(total_harga) FROM pemasukan")
    total_in = c.fetchone()[0] or 0
    
    c.execute("SELECT SUM(nominal) FROM pengeluaran")
    total_out = c.fetchone()[0] or 0
    
    conn.close()
    return {
        'total_in': total_in,
        'total_out': total_out,
        'laba': total_in - total_out
    }

def get_recent_history(limit=20):
    """Get a combined chronological list of recent transactions (pemasukan and pengeluaran)"""
    conn = get_connection()
    c = conn.cursor()
    
    # Select from both tables and union them in a subquery to enable sorting by substring functions on columns
    query = """
    SELECT tipe, id, detail, nominal, tanggal FROM (
        SELECT 'Pemasukan' as tipe, id, jumlah_sapi || ' Sapi' as detail, total_harga as nominal, tanggal 
        FROM pemasukan
        UNION ALL
        SELECT 'Pengeluaran' as tipe, id, produk || ' (' || kategori || ')' as detail, nominal, tanggal
        FROM pengeluaran
    )
    ORDER BY substr(tanggal, 7, 4) DESC, substr(tanggal, 4, 2) DESC, substr(tanggal, 1, 2) DESC, substr(tanggal, 12, 5) DESC
    LIMIT ?
    """
    c.execute(query, (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_monthly_summary(limit=6):
    """
    Returns monthly summary data for chart plotting.
    Groups transactions by month-year.
    """
    conn = get_connection()
    c = conn.cursor()
    
    # We want to group by year-month
    # Since dates are stored as "dd/mm/yyyy hh:mm"
    # Month is substr(tanggal, 4, 2) and Year is substr(tanggal, 7, 4)
    # So YYYY-MM is: substr(tanggal, 7, 4) || '-' || substr(tanggal, 4, 2)
    
    pemasukan_query = """
    SELECT substr(tanggal, 7, 4) || '-' || substr(tanggal, 4, 2) as yyyymm, SUM(total_harga)
    FROM pemasukan
    GROUP BY yyyymm
    """
    c.execute(pemasukan_query)
    in_data = dict(c.fetchall())
    
    pengeluaran_query = """
    SELECT substr(tanggal, 7, 4) || '-' || substr(tanggal, 4, 2) as yyyymm, SUM(nominal)
    FROM pengeluaran
    GROUP BY yyyymm
    """
    c.execute(pengeluaran_query)
    out_data = dict(c.fetchall())
    conn.close()
    
    # Let's get the list of unique months sorted chronologically
    all_months = sorted(list(set(in_data.keys()) | set(out_data.keys())))
    if not all_months:
        # Fallback if empty, return current month
        current_m = datetime.now().strftime("%Y-%m")
        all_months = [current_m]
        
    # Keep only the last `limit` months
    all_months = all_months[-limit:]
    
    # Format labels (e.g., "2026-06" -> "Jun 26" or "Jun")
    month_names = {
        "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "Mei", "06": "Jun",
        "07": "Jul", "08": "Agt", "09": "Sep", "10": "Okt", "11": "Nov", "12": "Des"
    }
    
    labels = []
    pemasukan_vals = []
    pengeluaran_vals = []
    
    for ym in all_months:
        if '-' in ym:
            year, month = ym.split('-')
            lbl = f"{month_names.get(month, month)} {year[2:]}"
        else:
            lbl = ym
        labels.append(lbl)
        pemasukan_vals.append(in_data.get(ym, 0))
        pengeluaran_vals.append(out_data.get(ym, 0))
        
    return labels, pemasukan_vals, pengeluaran_vals

# --- EXCEL EXPORT ---
def export_to_excel(filepath="Laporan_Siakternak.xlsx"):
    wb = openpyxl.Workbook()
    
    # Sheet 1: Pemasukan
    ws_in = wb.active
    ws_in.title = "Pemasukan"
    
    # Headers
    headers_in = ["No", "Jumlah Sapi (Ekor)", "Total Penjualan (Rp)", "Tanggal"]
    ws_in.append(headers_in)
    
    rows_in = get_all_pemasukan()
    # rows_in elements are (id, jumlah_sapi, total_harga, tanggal)
    # let's format it for spreadsheet
    for i, r in enumerate(reversed(rows_in), start=1):
        ws_in.append([i, r[1], r[2], r[3]])
        
    # Styling Sheet 1
    style_sheet(ws_in, "A1:D1", ["#FFD6D6D6", "#FF00FF00"]) # green tint header
    
    # Sheet 2: Pengeluaran
    ws_out = wb.create_sheet(title="Pengeluaran")
    headers_out = ["No", "Produk", "Kategori", "Nominal (Rp)", "Tanggal"]
    ws_out.append(headers_out)
    
    rows_out = get_all_pengeluaran()
    for i, r in enumerate(reversed(rows_out), start=1):
        ws_out.append([i, r[1], r[2], r[3], r[4]])
        
    # Styling Sheet 2
    style_sheet(ws_out, "A1:E1", ["#FFD6D6D6", "#FFFF0000"]) # red tint header
    
    wb.save(filepath)
    return os.path.abspath(filepath)

def style_sheet(ws, header_range, colors):
    # Header Font
    header_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
    # Header Fill (Green for pemasukan, Red for pengeluaran)
    fill_color = "1B5E20" if "00FF00" in colors[1] else "B71C1C"
    header_fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")
    
    # Apply to header
    for cell in ws[1]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    # Add border and align content
    thin_border = Border(
        left=Side(style='thin', color='DDDDDD'),
        right=Side(style='thin', color='DDDDDD'),
        top=Side(style='thin', color='DDDDDD'),
        bottom=Side(style='thin', color='DDDDDD')
    )
    
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
        for cell in row:
            cell.border = thin_border
            if isinstance(cell.value, int):
                cell.number_format = '#,##0'
                cell.alignment = Alignment(horizontal="right")
            elif cell.column == 1:
                cell.alignment = Alignment(horizontal="center")
            else:
                cell.alignment = Alignment(horizontal="left")
                
    # Auto-fit columns
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = openpyxl.utils.get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

# --- ACCOUNTING MODULE HELPERS ---
def get_coa():
    return [
        ("101", "Kas & Bank", "Aset"),
        ("401", "Pendapatan Penjualan Sapi", "Pendapatan"),
        ("501", "Beban Pakan", "Beban"),
        ("502", "Beban Kesehatan Ternak", "Beban"),
        ("503", "Beban Operasional Lainnya", "Beban")
    ]

def get_jurnal_umum():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT jumlah_sapi, total_harga, tanggal FROM pemasukan")
    pemasukan_rows = c.fetchall()
    c.execute("SELECT produk, kategori, nominal, tanggal FROM pengeluaran")
    pengeluaran_rows = c.fetchall()
    conn.close()
    
    all_tx = []
    for row in pemasukan_rows:
        all_tx.append({
            'tipe': 'Pemasukan',
            'val': row[1],
            'tanggal': row[2],
            'desc': f"Penjualan {row[0]} Sapi"
        })
    for row in pengeluaran_rows:
        all_tx.append({
            'tipe': 'Pengeluaran',
            'val': row[2],
            'kategori': row[1],
            'tanggal': row[3],
            'desc': f"Pembelian {row[0]}"
        })
        
    def parse_date(date_str):
        try:
            return datetime.strptime(date_str, "%d/%m/%Y %H:%M")
        except:
            return datetime.min
            
    all_tx.sort(key=lambda x: parse_date(x['tanggal']))
    
    journal_rows = []
    for tx in all_tx:
        tgl = tx['tanggal']
        if tx['tipe'] == 'Pemasukan':
            journal_rows.append((tgl, "101", "Kas & Bank", f"Rp {tx['val']:,}", ""))
            journal_rows.append((tgl, "401", "  Pendapatan Penjualan Sapi", "", f"Rp {tx['val']:,}"))
        else:
            cat = tx['kategori']
            if "Pakan" in cat:
                code, name = "501", "Beban Pakan"
            elif "Kesehatan" in cat:
                code, name = "502", "Beban Kesehatan Ternak"
            else:
                code, name = "503", "Beban Operasional Lainnya"
            
            journal_rows.append((tgl, code, name, f"Rp {tx['val']:,}", ""))
            journal_rows.append((tgl, "101", "  Kas & Bank", "", f"Rp {tx['val']:,}"))
            
    return journal_rows

def get_buku_besar(kode_akun):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT jumlah_sapi, total_harga, tanggal FROM pemasukan")
    pemasukan_rows = c.fetchall()
    c.execute("SELECT produk, kategori, nominal, tanggal FROM pengeluaran")
    pengeluaran_rows = c.fetchall()
    conn.close()
    
    all_tx = []
    for row in pemasukan_rows:
        all_tx.append({
            'tipe': 'Pemasukan',
            'val': row[1],
            'tanggal': row[2],
            'desc': f"Penjualan {row[0]} Sapi"
        })
    for row in pengeluaran_rows:
        all_tx.append({
            'tipe': 'Pengeluaran',
            'val': row[2],
            'kategori': row[1],
            'tanggal': row[3],
            'desc': f"Pembelian {row[0]}"
        })
        
    def parse_date(date_str):
        try:
            return datetime.strptime(date_str, "%d/%m/%Y %H:%M")
        except:
            return datetime.min
            
    all_tx.sort(key=lambda x: parse_date(x['tanggal']))
    
    ledger_rows = []
    balance = 0
    
    for tx in all_tx:
        tgl = tx['tanggal']
        desc = tx['desc']
        debit = 0
        credit = 0
        affected = False
        
        if kode_akun == "101":
            if tx['tipe'] == 'Pemasukan':
                debit = tx['val']
                balance += debit
                affected = True
            else:
                credit = tx['val']
                balance -= credit
                affected = True
        elif kode_akun == "401":
            if tx['tipe'] == 'Pemasukan':
                credit = tx['val']
                balance += credit
                affected = True
        elif kode_akun == "501":
            if tx['tipe'] == 'Pengeluaran' and "Pakan" in tx['kategori']:
                debit = tx['val']
                balance += debit
                affected = True
        elif kode_akun == "502":
            if tx['tipe'] == 'Pengeluaran' and "Kesehatan" in tx['kategori']:
                debit = tx['val']
                balance += debit
                affected = True
        elif kode_akun == "503":
            if tx['tipe'] == 'Pengeluaran' and not ("Pakan" in tx['kategori'] or "Kesehatan" in tx['kategori']):
                debit = tx['val']
                balance += debit
                affected = True
                
        if affected:
            debit_str = f"Rp {debit:,}" if debit > 0 else ""
            credit_str = f"Rp {credit:,}" if credit > 0 else ""
            ledger_rows.append((
                tgl,
                desc,
                debit_str,
                credit_str,
                f"Rp {balance:,}"
            ))
            
    return ledger_rows

def get_neraca_saldo():
    summary = get_summary()
    total_in = summary['total_in']
    total_out = summary['total_out']
    kas_balance = total_in - total_out
    
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT SUM(nominal) FROM pengeluaran WHERE kategori LIKE '%Pakan%'")
    pakan_val = c.fetchone()[0] or 0
    c.execute("SELECT SUM(nominal) FROM pengeluaran WHERE kategori LIKE '%Kesehatan%'")
    kesehatan_val = c.fetchone()[0] or 0
    c.execute("SELECT SUM(nominal) FROM pengeluaran WHERE NOT (kategori LIKE '%Pakan%' OR kategori LIKE '%Kesehatan%')")
    lain_val = c.fetchone()[0] or 0
    conn.close()
    
    rows = []
    rows.append(("101", "Kas & Bank", f"Rp {kas_balance:,}" if kas_balance >= 0 else "", f"Rp {abs(kas_balance):,}" if kas_balance < 0 else ""))
    rows.append(("401", "Pendapatan Penjualan Sapi", "", f"Rp {total_in:,}"))
    rows.append(("501", "Beban Pakan", f"Rp {pakan_val:,}", ""))
    rows.append(("502", "Beban Kesehatan Ternak", f"Rp {kesehatan_val:,}", ""))
    rows.append(("503", "Beban Operasional Lainnya", f"Rp {lain_val:,}", ""))
    
    total_debit = (kas_balance if kas_balance >= 0 else 0) + pakan_val + kesehatan_val + lain_val
    total_kredit = total_in + (abs(kas_balance) if kas_balance < 0 else 0)
    
    return rows, total_debit, total_kredit

def get_laba_rugi():
    summary = get_summary()
    total_in = summary['total_in']
    
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT SUM(nominal) FROM pengeluaran WHERE kategori LIKE '%Pakan%'")
    pakan_val = c.fetchone()[0] or 0
    c.execute("SELECT SUM(nominal) FROM pengeluaran WHERE kategori LIKE '%Kesehatan%'")
    kesehatan_val = c.fetchone()[0] or 0
    c.execute("SELECT SUM(nominal) FROM pengeluaran WHERE NOT (kategori LIKE '%Pakan%' OR kategori LIKE '%Kesehatan%')")
    lain_val = c.fetchone()[0] or 0
    conn.close()
    
    total_beban = pakan_val + kesehatan_val + lain_val
    laba_bersih = total_in - total_beban
    
    return {
        'pendapatan': total_in,
        'beban_pakan': pakan_val,
        'beban_kesehatan': kesehatan_val,
        'beban_lain': lain_val,
        'total_beban': total_beban,
        'laba_bersih': laba_bersih
    }
