from flask import Flask, render_template, jsonify
from capture.capture_packets import get_stats, simulate_live_calls
from threading import Thread

app = Flask(
    __name__,
    template_folder='../frontend/templates',
    static_folder='../frontend/data/static'
)

# -------------- Routes ----------------
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/stats')
def stats():
    """Return current simulated stats as JSON for frontend chart"""
    return jsonify(get_stats())

# ---------------- Main ----------------
if __name__ == '__main__':
    # Start background thread to continuously simulate calls
    t = Thread(target=simulate_live_calls, args=(200, 35, 0.5), daemon=True)
    t.start()

    # Run Flask server
    app.run(debug=True, host="0.0.0.0", port=5000)

