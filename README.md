# TracingVoIP-Calls-Via-Network-metadata
VoIPTraceFD – VoIP Call Tracing and Monitoring Tool A comprehensive tool for tracing, monitoring, and analyzing VoIP calls in real-time. Detects suspicious activity, visualizes SIP &amp; RTP packets, provides live call logs, and maps call geolocation. Built using Python, Flask, and web-based dashboards for effective VoIP security monitoring.


# VoIPTraceFD – VoIP Call Tracing and Monitoring Tool

VoIPTraceFD is a Python-based web application designed to monitor, trace, and analyze VoIP calls in real-time. It captures SIP and RTP packets, identifies suspicious activity, and provides live dashboards with graphs and logs. Ideal for cybersecurity enthusiasts and VoIP security monitoring purposes.

## Features

- Real-time SIP & RTP packet tracing
- Live logs of active VoIP calls
- Geolocation mapping of IP addresses
- Detection of suspicious calls and patterns
- Interactive web-based dashboard with charts

## Tools and Technologies

- **Programming Language:** Python 3.13
- **Frameworks:** Flask (backend), HTML/CSS/JavaScript (frontend)
- **Libraries:**
  - Scapy (packet capturing and analysis)
  - Chart.js (interactive charts)
  - Leaflet.js (geolocation mapping)
- **Database:** SQLite (for storing suspicious IPs and call logs)
- **Deployment:** Localhost / Cloud (Vercel or any preferred cloud hosting)
- **Version Control:** Git & GitHub

## Installation

1. Clone the repository:

    git clone https://github.com/your-username/VoIPTraceFD.git
    cd VoIPTraceFD/backend
    Install dependencies:
    pip install -r requirements.txt
    Run the application:
    python app.py
    Open your browser and navigate to:


http://127.0.0.1:5000 or localhost

Test Dataset
  For testing the tool, sample PCAP files are provided in the test_dataset folder. These datasets contain:
  SIP packets for call setup and teardown
  RTP packets for voice data transmission
  Malicious/suspicious VoIP call scenarios for detection testing

Sample files:
  sample_sip.pcap
  sample_rtp.pcap
  suspicious_calls.pcap
  Note: You can also capture live VoIP traffic in a controlled lab environment for real-time testing.

For testing VoIPTraceFD
- Randomly generated SIP packets simulating call setup and teardown
- Random RTP packets representing voice data transmission
- Example suspicious calls for testing alert detection

Usage
  Navigate to the Dashboard to see live SIP & RTP packet graphs.
  Check Live Logs for active call details.
  Suspicious IPs and calls are highlighted in the Alerts section.
  Geolocation of call endpoints can be viewed on the Map.

Contribution
  Contributions are welcome! Feel free to fork the repo, raise issues, or submit pull requests.

License
  This project is licensed under the MIT License. See LICENSE for details.
