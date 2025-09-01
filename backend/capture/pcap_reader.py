from scapy.all import rdpcap
from .capture_packets import process_packet, active_calls_list, lock
import time

def read_pcap(file_path, delay=0.05):
    """
    Read packets from a PCAP file and process each packet gradually.
    'delay' is the time (in seconds) between packets to simulate live capture.
    """
    try:
        packets = rdpcap(file_path)
        print(f"[INFO] Loaded {len(packets)} packets from {file_path}")

        for pkt in packets:
            process_packet(pkt)  # Updates active_calls_list
            time.sleep(delay)    # gradual increment for live effect

        # Summarize stats after processing
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
                    "user_agent": c["user_agent"]
                }
                for c in active_calls_list
            ]

        print(f"[INFO] Finished processing PCAP with {len(active_calls_list)} active calls")
        return {
            "active_calls": active_calls,
            "sip_count": sip_count,
            "rtp_count": rtp_count,
            "alerts": alerts,
            "logs": logs
        }

    except FileNotFoundError:
        print(f"[ERROR] PCAP file not found: {file_path}")
        return None
    except Exception as e:
        print(f"[ERROR] Failed to read PCAP file {file_path}: {e}")
        return None


# ---------------------- Test Run ----------------------
if __name__ == "__main__":
    import os
    test_file = os.path.join("..", "pcaps", "test.pcap")  # adjust path if needed
    stats = read_pcap(test_file, delay=0.1)  # 0.1s between packets
    if stats:
        print(f"Active Calls: {stats['active_calls']}")
        print(f"SIP Packets: {stats['sip_count']}, RTP Packets: {stats['rtp_count']}, Alerts: {stats['alerts']}")
        for log in stats["logs"]:
            print(log)
