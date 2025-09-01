# backend/suspicious_db.py
import sqlite3

DB_PATH = 'backend/suspicious.db'

def create_db():
    """
    Create suspicious IPs database with enhanced features:
    - id: Primary Key
    - ip: Suspicious IP
    - reason: Reason for being flagged
    - risk_level: High / Medium / Low
    - first_seen: Timestamp
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create table if not exists
    c.execute('''
        CREATE TABLE IF NOT EXISTS suspicious_ips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL UNIQUE,
            reason TEXT,
            risk_level TEXT DEFAULT 'Medium',
            first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Insert sample suspicious IPs (only if not exists)
    sample_ips = [
        ('192.168.10.5', 'Test Alert', 'High'),
        ('10.0.0.99', 'Test Alert', 'Medium'),
        ('172.16.5.20', 'Frequent Short Calls', 'High'),
        ('192.168.1.50', 'Blacklisted Region', 'Medium')
    ]
    for ip, reason, risk in sample_ips:
        c.execute('''
            INSERT OR IGNORE INTO suspicious_ips (ip, reason, risk_level)
            VALUES (?, ?, ?)
        ''', (ip, reason, risk))

    conn.commit()
    conn.close()
    print("[INFO] Database created with sample suspicious IPs and risk levels.")


# ---------------------- Fetch Utility ----------------------
def fetch_suspicious_ips():
    """Return all suspicious IPs with details"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT ip, reason, risk_level, first_seen FROM suspicious_ips")
    rows = c.fetchall()
    conn.close()
    result = []
    for r in rows:
        result.append({
            "ip": r[0],
            "reason": r[1],
            "risk_level": r[2],
            "first_seen": r[3]
        })
    return result


# ---------------------- Test Run ----------------------
if __name__ == "__main__":
    create_db()
    ips = fetch_suspicious_ips()
    for ip in ips:
        print(ip)
