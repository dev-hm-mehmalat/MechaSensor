from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # CORS für alle Domains (für Entwicklung, später einschränken)

# In-Memory Speicher für Sensordaten
sensor_data_store = []

@app.route('/')
def index():
    """Render das Dashboard HTML."""
    return render_template('index.html')

@app.route('/api/sensors/data', methods=['POST'])
def add_sensor_data():
    """Sensordaten empfangen und speichern."""
    data = request.get_json()

    # Validierung
    try:
        temperature = float(data.get('temperature'))
        humidity = float(data.get('humidity'))
    except (TypeError, ValueError):
        return jsonify({'error': 'Temperature und Humidity müssen gültige Zahlen sein.'}), 400

    timestamp = data.get('timestamp') or datetime.utcnow().isoformat()

    # Datensatz speichern
    sensor_data_store.append({
        'temperature': temperature,
        'humidity': humidity,
        'timestamp': timestamp
    })

    return jsonify({'message': 'Sensordaten gespeichert', 'data': sensor_data_store[-1]}), 201

@app.route('/api/sensors/data', methods=['GET'])
def get_sensor_data():
    """Alle Sensordaten zurückgeben."""
    return jsonify({'data': sensor_data_store})

# Optional: Fehlerhandler für 404
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Ressource nicht gefunden'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)