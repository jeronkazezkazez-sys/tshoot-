import sqlite3
from datetime import datetime

DB_NAME = "store.db"

def init_db():
    """إنشاء جدول فحوصات الصيانة إذا لم يكن موجوداً"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diagnostic_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            mode TEXT,
            details TEXT,
            diagnosis TEXT,
            suggested_solution TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_diagnostic(mode, details, diagnosis, solution, status="جديد"):
    """حفظ نتيجة الفحص في قاعدة البيانات"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO diagnostic_records (timestamp, mode, details, diagnosis, suggested_solution, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (now, mode, details, diagnosis, solution, status))
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id

def get_all_records():
    """جلب جميع فحوصات الصيانة السابقة"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM diagnostic_records ORDER BY id DESC')
    records = cursor.fetchall()
    conn.close()
    return records

# تهيئة قاعدة البيانات عند استدعاء الملف
init_db()