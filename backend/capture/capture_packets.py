from scapy.all import IP, UDP, Raw
import threading
import time
import random

# ---------------------- Global Storage ----------------------
active_calls_list = []
lock = threading.Lock()

# ---------------------- Packet Simulation / Live Calls ----------------------
def simulate_live_calls(num_calls=200, alert_count=35, update_interval=0.5):
    """
    Simulate multiple active calls with realistic SIP/RTP/Alert stats
    num_calls: total number of calls to simulate
    alert_count: number of calls with alerts
    update_interval: time between updates (seconds)
    """
    alert_indices = random.sample(range(num_calls), alert_count)
    
    # Initialize empty calls
    with lock:
        active_calls_list.clear()
        for i in range(num_calls):
            src_ip = f"192.168.{random.randint(1,255)}.{random.randint(1,255)}"
            dst_ip = f"10.0.{random.randint(0,20)}.{random.randint(1,255)}"
            active_calls_list.append({
                "call_id": f"{src_ip}-{dst_ip}",
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "protocol": random.choice(["SIP", "RTP"]),
                "timestamp": time.strftime("%H:%M:%S"),
                "sip_count": random.randint(1,5),
                "rtp_count": random.randint(5,20),
                "alert": i in alert_indices,
                "sip_method": "INVITE",
                "user_agent": random.choice(["Zoiper 5", "Linphone", "X-Lite"]),
                "status": random.choice(["Active","Completed"]),
                "duration": f"00:{random.randint(1,59):02}:{random.randint(1,59):02}"
            })
    
    # Gradually update counts to make chart realistic
    for step in range(50):  # 50 steps to simulate gradual updates
        with lock:
            for c in active_calls_list:
                # Zigzag pattern for SIP and RTP counts
                c["sip_count"] = max(0, c["sip_count"] + random.randint(-1, 2))
                c["rtp_count"] = max(0, c["rtp_count"] + random.randint(-2, 5))
                # Occasionally toggle alert status
                if random.random() < 0.02:
                    c["alert"] = not c["alert"]
                # Update timestamp
                c["timestamp"] = time.strftime("%H:%M:%S")
        time.sleep(update_interval)

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

# ---------------------- Live Capture (Background Thread) ----------------------
def start_capture(num_calls=200, alert_count=35, update_interval=0.3):
    """
    Start live capture simulation in background thread
    """
    t = threading.Thread(target=simulate_live_calls, args=(num_calls, alert_count, update_interval), daemon=True)
    t.start()
