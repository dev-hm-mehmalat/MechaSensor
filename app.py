from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime, timezone  # timezone importieren

app = Flask(__name__)
CORS(app)  # CORS für alle Domains (für Entwicklung, später einschränken)

# In-Memory Speicher für Sensordaten und Robot Commands
sensor_data_store = []
command_queue = []

# --- Frontend-Dashboard ---
@app.route('/')
def index():
    """Render das Dashboard HTML."""
    return render_template('index.html')

# --- Sensor-Daten (allgemein) ---
@app.route('/api/sensors/data', methods=['POST'])
def add_sensor_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Keine Daten"}), 400

    temperature = data.get('temperature')
    humidity = data.get('humidity')

    if temperature is None or humidity is None:
        return jsonify({"error": "Temperature und Humidity sind erforderlich"}), 400

    try:
        temperature = float(temperature)
        humidity = float(humidity)
    except ValueError:
        return jsonify({"error": "Temperature und Humidity müssen Zahlen sein"}), 400

    timestamp = data.get('timestamp') or datetime.now(timezone.utc).isoformat()
    sensor_data_store.append({
        "temperature": temperature,
        "humidity": humidity,
        "timestamp": timestamp
    })
    return jsonify({"message": "Gespeichert", "data": sensor_data_store[-1]}), 201

@app.route('/api/sensors/data', methods=['GET'])
def get_sensor_data():
    """Alle Sensordaten zurückgeben."""
    return jsonify({'data': sensor_data_store})

# --- Robotik-spezifische Sensor-Daten ---
@app.route('/api/robot/sensors', methods=['POST'])
def add_robot_sensor_data():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Keine Daten gesendet'}), 400
    data['timestamp'] = data.get('timestamp') or datetime.now(timezone.utc).isoformat()
    sensor_data_store.append(data)
    return jsonify({'message': 'Robot-Sensordaten gespeichert', 'data': data}), 201

@app.route('/api/robot/sensors', methods=['GET'])
def get_robot_sensor_data():
    return jsonify({'data': sensor_data_store})

# --- Robotik-Kommandos ---
@app.route('/api/robot/commands', methods=['POST'])
def add_command():
    command = request.get_json()
    if not command or 'command' not in command:
        return jsonify({'error': 'Ungültiger Befehl'}), 400
    command['timestamp'] = datetime.now(timezone.utc).isoformat()
    command_queue.append(command)
    return jsonify({'message': 'Befehl gespeichert', 'command': command}), 201

@app.route('/api/robot/commands', methods=['GET'])
def get_commands():
    return jsonify({'commands': command_queue})

# --- Fehlerhandler für 404 ---
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Ressource nicht gefunden'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)