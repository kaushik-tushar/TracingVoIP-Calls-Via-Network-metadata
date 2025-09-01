from flask import Flask, render_template, jsonify, request
from capture.capture_packets import get_stats, simulate_live_calls
import time

app = Flask(
    __name__,
    template_folder='../frontend/templates',
    static_folder='../frontend/data/static'
)

# ---------------- Routes ----------------
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/stats')
def stats():
    return jsonify(get_stats())

# ---------------- Main ----------------
if __name__ == '__main__':
    # Simulate 200 calls with 35 alerts
    simulate_live_calls(num_calls=200, alert_count=35)

    app.run(debug=True, host="0.0.0.0", port=5000)
