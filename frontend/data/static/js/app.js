// -------------------- Global Variables --------------------
let lastSip = 0;
let lastRtp = 0;

// Initialize Charts
let sipChart = new Chart(document.getElementById('sipChart').getContext('2d'), {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'SIP Packets', data: [], borderColor: 'blue', backgroundColor: 'rgba(54,162,235,0.2)', fill: true }] },
    options: { responsive: true, animation: { duration: 500 } }
});

let rtpChart = new Chart(document.getElementById('rtpChart').getContext('2d'), {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'RTP Packets', data: [], borderColor: 'green', backgroundColor: 'rgba(75,192,192,0.2)', fill: true }] },
    options: { responsive: true, animation: { duration: 500 } }
});

// -------------------- Gradual Counter --------------------
function animateCounter(elementId, targetValue) {
    const el = document.getElementById(elementId);
    let current = parseInt(el.innerText) || 0;
    const step = Math.max(1, Math.floor((targetValue - current) / 10));

    const interval = setInterval(() => {
        current += step;
        if ((step > 0 && current >= targetValue) || (step < 0 && current <= targetValue)) {
            current = targetValue;
            clearInterval(interval);
        }
        el.innerText = current;
    }, 50);
}

// -------------------- Update Dashboard --------------------
function updateDashboard() {
    fetch('/stats')
        .then(res => res.json())
        .then(data => {
            // Gradual Counters
            animateCounter('active-calls', data.active_calls);
            animateCounter('sip-count', data.sip_count);
            animateCounter('rtp-count', data.rtp_count);
            animateCounter('alerts', data.alerts);

            const now = new Date().toLocaleTimeString();

            // Gradual Chart Pattern
            lastSip = lastSip + Math.floor(Math.random() * 5 - 2) + data.sip_count * 0.05;
            lastRtp = lastRtp + Math.floor(Math.random() * 5 - 2) + data.rtp_count * 0.05;

            lastSip = Math.max(0, Math.round(lastSip));
            lastRtp = Math.max(0, Math.round(lastRtp));

            sipChart.data.labels.push(now);
            sipChart.data.datasets[0].data.push(lastSip);
            rtpChart.data.labels.push(now);
            rtpChart.data.datasets[0].data.push(lastRtp);

            if (sipChart.data.labels.length > 20) {
                sipChart.data.labels.shift();
                sipChart.data.datasets[0].data.shift();
                rtpChart.data.labels.shift();
                rtpChart.data.datasets[0].data.shift();
            }
            sipChart.update();
            rtpChart.update();

            // ---------------- Active Calls Table ----------------
            const tbody = document.getElementById('active-calls-body');
            tbody.innerHTML = '';
            data.logs.slice(0, 50).forEach((call, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${index + 1}</td>
                    <td>${call.call_id}</td>
                    <td>${call.src_ip} → ${call.dst_ip}</td>
                    <td>${call.user_agent || '-'}</td>
                    <td>${call.timestamp}</td>
                    <td>${call.duration || '-'}</td>
                    <td>${call.status}</td>
                `;
                tbody.appendChild(row);
            });

            // ---------------- Alerts Panel ----------------
            const alertSection = document.getElementById('alerts-section');
            alertSection.innerHTML = '';
            data.logs.filter(c => c.alert).forEach(c => {
                const div = document.createElement('div');
                div.className = 'alert-card alert-high';
                div.innerText = `Alert: ${c.call_id} | ${c.user_agent || 'Unknown'}`;
                alertSection.appendChild(div);
            });

            // ---------------- Live Logs ----------------
            const logBox = document.getElementById('log-box');
            data.logs.slice(-5).reverse().forEach(c => {
                const line = `[${c.timestamp}] ${c.call_id} | SIP:${c.sip_count} RTP:${c.rtp_count} ALERT:${c.alert}`;
                const p = document.createElement('div');
                p.innerText = line;
                logBox.prepend(p);
            });

            // Limit logs to last 50 lines
            while (logBox.children.length > 50) {
                logBox.removeChild(logBox.lastChild);
            }

            // ---------------- GeoMap (Placeholder) ----------------
            if (!window.map) {
                window.map = L.map('geoMap').setView([20.5937, 78.9629], 4); // India view
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© OpenStreetMap contributors'
                }).addTo(window.map);
            }
            // Add markers for active calls (optional, random demo)
            if (window.markers) {
                window.markers.forEach(m => window.map.removeLayer(m));
            }
            window.markers = [];
            data.logs.slice(-10).forEach(c => {
                const lat = 20 + Math.random() * 5; // random demo
                const lon = 78 + Math.random() * 5;
                const marker = L.marker([lat, lon]).addTo(window.map)
                    .bindPopup(`${c.call_id} | ${c.user_agent || 'Unknown'}`);
                window.markers.push(marker);
            });
        })
        .catch(err => console.error(err));
}

// -------------------- Refresh Interval --------------------
setInterval(updateDashboard, 1000);

// Initialize
updateDashboard();
