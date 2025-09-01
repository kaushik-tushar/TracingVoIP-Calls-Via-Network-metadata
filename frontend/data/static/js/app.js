// -------------------- Global Variables --------------------
let lastSip = 0;
let lastRtp = 0;
let lastActive = 0;
let lastAlerts = 0;

// -------------------- Initialize Charts --------------------
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

let activeChart = new Chart(document.getElementById('activeChart').getContext('2d'), {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Active Calls', data: [], borderColor: 'orange', backgroundColor: 'rgba(255,165,0,0.2)', fill: true }] },
    options: { responsive: true, animation: { duration: 500 } }
});

let alertChart = new Chart(document.getElementById('alertChart').getContext('2d'), {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Alerts', data: [], borderColor: 'red', backgroundColor: 'rgba(255,0,0,0.2)', fill: true }] },
    options: { responsive: true, animation: { duration: 500 } }
});

// -------------------- Gradual Counter --------------------
function animateCounter(elementId, lastValue, targetValue) {
    const el = document.getElementById(elementId);
    const step = Math.max(1, Math.floor((targetValue - lastValue) / 5));
    let current = lastValue;
    const interval = setInterval(() => {
        current += step;
        if ((step > 0 && current >= targetValue) || (step < 0 && current <= targetValue)) {
            current = targetValue;
            clearInterval(interval);
        }
        el.innerText = current;
    }, 50);
    return targetValue;
}

// -------------------- Update Dashboard --------------------
let logsData = []; // Store logs for CSV export

function updateDashboard() {
    fetch('/stats')
        .then(res => res.json())
        .then(data => {
            logsData = data.logs; // Save logs

            const now = new Date().toLocaleTimeString();

            // Animate counters smoothly
            lastActive = animateCounter('active-calls', lastActive, data.active_calls);
            lastSip = animateCounter('sip-count', lastSip, data.sip_count);
            lastRtp = animateCounter('rtp-count', lastRtp, data.rtp_count);
            lastAlerts = animateCounter('alerts', lastAlerts, data.alerts);

            // Zigzag pattern for charts
            lastSip = Math.max(0, Math.round(lastSip + Math.floor(Math.random() * 5 - 2)));
            lastRtp = Math.max(0, Math.round(lastRtp + Math.floor(Math.random() * 5 - 2)));
            lastActive = Math.max(0, Math.round(lastActive + Math.floor(Math.random() * 3 - 1)));
            lastAlerts = Math.max(0, Math.round(lastAlerts + Math.floor(Math.random() * 2 - 1)));

            const charts = [
                {chart: sipChart, value: lastSip},
                {chart: rtpChart, value: lastRtp},
                {chart: activeChart, value: lastActive},
                {chart: alertChart, value: lastAlerts}
            ];

            charts.forEach(item => {
                item.chart.data.labels.push(now);
                item.chart.data.datasets[0].data.push(item.value);
                if(item.chart.data.labels.length > 50) {
                    item.chart.data.labels.shift();
                    item.chart.data.datasets[0].data.shift();
                }
                item.chart.update();
            });

            // Active Calls Table
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

            // Alerts Panel
            const alertSection = document.getElementById('alerts-section');
            alertSection.innerHTML = '';
            data.logs.filter(c => c.alert).forEach(c => {
                const div = document.createElement('div');
                div.className = 'alert-card alert-high';
                div.innerText = `Alert: ${c.call_id} | ${c.user_agent || 'Unknown'}`;
                alertSection.appendChild(div);
            });

            // Live Logs
            const logBox = document.getElementById('log-box');
            data.logs.slice(-5).reverse().forEach(c => {
                const line = `[${c.timestamp}] ${c.call_id} | SIP:${c.sip_count} RTP:${c.rtp_count} ALERT:${c.alert}`;
                const p = document.createElement('div');
                p.innerText = line;
                logBox.prepend(p);
            });
            while (logBox.children.length > 50) logBox.removeChild(logBox.lastChild);

            // GeoMap
            if (!window.map) {
                window.map = L.map('geoMap').setView([20.5937, 78.9629], 4);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© OpenStreetMap contributors'
                }).addTo(window.map);
            }
            if (window.markers) window.markers.forEach(m => window.map.removeLayer(m));
            window.markers = [];
            data.logs.slice(-10).forEach(c => {
                const lat = 20 + Math.random() * 5;
                const lon = 78 + Math.random() * 5;
                const marker = L.marker([lat, lon]).addTo(window.map)
                    .bindPopup(`${c.call_id} | ${c.user_agent || 'Unknown'}`);
                window.markers.push(marker);
            });

        })
        .catch(err => console.error(err));
}

// -------------------- Export CSV --------------------
document.getElementById('export-csv').addEventListener('click', () => {
    if(logsData.length === 0) return alert("No logs to export!");

    const headers = ["CallID", "SrcIP", "DstIP", "Protocol", "SIP Count", "RTP Count", "Alert", "User Agent", "Status", "Duration", "Timestamp"];
    const rows = logsData.map(c => [
        c.call_id, c.src_ip, c.dst_ip, c.protocol, c.sip_count, c.rtp_count, c.alert, c.user_agent || '', c.status, c.duration, c.timestamp
    ]);

    let csvContent = "data:text/csv;charset=utf-8," 
        + headers.join(",") + "\n"
        + rows.map(r => r.join(",")).join("\n");

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `voip_logs_${new Date().toISOString()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});

// -------------------- Refresh Interval --------------------
setInterval(updateDashboard, 1000);

// Initial update
updateDashboard();
