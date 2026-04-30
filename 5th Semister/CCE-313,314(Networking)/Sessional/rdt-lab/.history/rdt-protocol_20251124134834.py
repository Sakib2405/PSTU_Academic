# rdt-protocol.py
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import random
import time
import os

app = Flask(__name__)
CORS(app)

class RDTServer:
    def __init__(self):
        self.sender_seq = 0
        self.receiver_seq = 0
        self.stats = {
            'packets_sent': 0,
            'acks_received': 0,
            'retransmissions': 0
        }
    
    def simulate_transmission(self, data, packet_loss=0.3, ack_loss=0.3, corruption=0.1):
        self.stats['packets_sent'] += 1
        
        # Simulate packet loss
        if random.random() < packet_loss:
            return {'status': 'lost', 'seq': self.sender_seq}
        
        # Simulate corruption
        if random.random() < corruption:
            return {'status': 'corrupted', 'seq': self.sender_seq}
        
        # Check if packet is in order
        if self.sender_seq == self.receiver_seq:
            self.receiver_seq = 1 - self.receiver_seq
            ack_status = 'lost' if random.random() < ack_loss else 'delivered'
            
            if ack_status == 'delivered':
                self.sender_seq = 1 - self.sender_seq
                self.stats['acks_received'] += 1
            
            return {
                'status': 'delivered',
                'seq': self.sender_seq,
                'ack_status': ack_status,
                'data': data
            }
        else:
            return {'status': 'duplicate', 'seq': self.sender_seq}

rdt_server = RDTServer()


@app.route('/')
def index():
    # Serve the local index.html so visiting the server root shows the UI
    return send_from_directory('.', 'index.html')


@app.route('/<path:filename>')
def static_files(filename):
    # Serve static files (script.js, styles.css, etc.) from the same folder
    return send_from_directory('.', filename)

@app.route('/send', methods=['GET', 'POST'])
def send_packet():
    # Allow GET for quick diagnostics and POST for actual simulation requests
    if request.method == 'GET':
        return jsonify({
            'info': 'POST JSON to this endpoint with {"message":"text", "packet_loss":0.3, "ack_loss":0.3, "corruption":0.1}'
        })

    data = request.get_json() or {}
    message = data.get('message', '')
    result = rdt_server.simulate_transmission(
        message,
        data.get('packet_loss', 0.3),
        data.get('ack_loss', 0.3),
        data.get('corruption', 0.1)
    )

    return jsonify({
        'result': result,
        'stats': rdt_server.stats
    })

@app.route('/reset', methods=['POST'])
def reset_simulation():
    rdt_server.__init__()
    return jsonify({'status': 'reset'})

if __name__ == '__main__':
    # Bind to 0.0.0.0 so other devices on the network can reach it if needed
    app.run(host='0.0.0.0', debug=True, port=5000)