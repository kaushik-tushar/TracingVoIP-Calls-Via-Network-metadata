# backend/manage_ips.py
import sqlite3
from datetime import datetime

DB_PATH = 'backend/suspicious.db'

# ---------------------- Add IP ----------------------
def add_ip(ip, reason="", risk_level="Medium"):
    """
    Add a suspicious IP to database
    - ip: IP address
    - reason: why it is flagged
    - risk_level: High / Medium / Low
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT OR IGNORE INTO suspicious_ips (ip, reason, risk_level, first_seen)
        VALUES (?, ?, ?, ?)
    """, (ip, reason, risk_level, datetime.now()))
    conn.commit()
    conn.close()
    print(f"[INFO] Added IP {ip} with risk {risk_level}")


# ---------------------- Remove IP ----------------------
def remove_ip(ip):
    """Remove an IP from suspicious list"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM suspicious_ips WHERE ip=?", (ip,))
    conn.commit()
    conn.close()
    print(f"[INFO] Removed IP {ip}")


# ---------------------- List IPs ----------------------
def list_ips():
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
    # Sample usage
    add_ip("192.168.20.5", "Test High Risk", "High")
    add_ip("10.0.1.15", "Medium Risk Test", "Medium")
    print("[LIST OF IPs]")
    for ip in list_ips():
        print(ip)
    remove_ip("10.0.1.15")
    print("[AFTER REMOVAL]")
    for ip in list_ips():
        print(ip)
