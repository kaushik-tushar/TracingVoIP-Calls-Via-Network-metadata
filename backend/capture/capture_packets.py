from scapy.all import IP, UDP, Raw
import threading
import time
import random

# ---------------------- Global Storage ----------------------
active_calls_list = []
call_registry = {}
lock = threading.Lock()

# ---------------------- Packet Processing / Dummy Simulation ----------------------
def process_packet(pkt):
    """Stub for real packets (optional)"""
    return

def simulate_live_calls(num_calls=200, alert_count=35):
    """Simulate multiple active calls for dashboard testing"""
    with lock:
        active_calls_list.clear()
        alert_ips = random.sample(range(num_calls), alert_count)
        for i in range(num_calls):
            src_ip = f"192.168.{random.randint(1,255)}.{random.randint(1,255)}"
            dst_ip = f"10.0.{random.randint(0,20)}.{random.randint(1,255)}"
            alert_flag = i in alert_ips
            active_calls_list.append({
                "call_id": f"{src_ip}-{dst_ip}",
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "protocol": random.choice(["SIP", "RTP"]),
                "timestamp": time.strftime("%H:%M:%S"),
                "size": random.randint(100, 500),
                "sip_count": random.randint(1,5),
                "rtp_count": random.randint(5,20),
                "alert": alert_flag,
                "sip_method": "INVITE",
                "user_agent": random.choice(["Zoiper 5", "Linphone", "X-Lite"]),
                "status": random.choice(["Active","Completed"]),
                "duration": f"00:{random.randint(1,59):02}:{random.randint(1,59):02}"
            })

# ---------------------- Stats for Frontend ----------------------
def get_stats():
    with lock:
        active_calls = len(active_calls_list)
        sip_count = sum(c["sip_count"] for c in active_calls_list)
        rtp_count = sum(c["rtp_count"] for c in active_calls_list)
        alerts = sum(1 for c in active_calls_list if c["alert"])
        logs = [
            {
                "timestamp": c["timestamp"],
                "call_id": c["call_id"],
                "src_ip": c["src_ip"],
                "dst_ip": c["dst_ip"],
                "protocol": c["protocol"],
                "sip_count": c["sip_count"],
                "rtp_count": c["rtp_count"],
                "alert": c["alert"],
                "sip_method": c["sip_method"],
                "user_agent": c["user_agent"],
                "status": c["status"],
                "duration": c["duration"]
            }
            for c in active_calls_list
        ]
    return {
        "active_calls": active_calls,
        "sip_count": sip_count,
        "rtp_count": rtp_count,
        "alerts": alerts,
        "logs": logs
    }

# ---------------------- Live Capture (Optional) ----------------------
def start_capture(interface="Wi-Fi"):
    """Stub function for real capture"""
    t = threading.Thread(target=lambda: None, daemon=True)
    t.start()
