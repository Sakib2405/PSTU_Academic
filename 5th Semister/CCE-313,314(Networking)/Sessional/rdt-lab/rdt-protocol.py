from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import random
import time
import os

app = Flask(__name__)
CORS(app)

class RDTServer:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.sender_seq = 0
        self.receiver_seq = 0
        self.stats = {
            'packets_sent': 0,
            'acks_received': 0,
            'retransmissions': 0,
            'packets_lost': 0,
            'packets_corrupted': 0,
            'packets_delivered': 0
        }
    
    def simulate_transmission(self, data, packet_loss=0.3, ack_loss=0.3, corruption=0.1):
        self.stats['packets_sent'] += 1
        
        # Simulate packet loss
        if random.random() < packet_loss:
            self.stats['packets_lost'] += 1
            return {'status': 'lost', 'seq': self.sender_seq}
        
        # Simulate corruption
        if random.random() < corruption:
            self.stats['packets_corrupted'] += 1
            return {'status': 'corrupted', 'seq': self.sender_seq}
        
        # Check if packet is in order
        if self.sender_seq == self.receiver_seq:
            self.receiver_seq = 1 - self.receiver_seq
            self.stats['packets_delivered'] += 1
            
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
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

@app.route('/api/send', methods=['POST'])
def send_packet():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        message = data.get('message', '')
        if not message:
            return jsonify({'error': 'No message provided'}), 400
            
        result = rdt_server.simulate_transmission(
            message,
            data.get('packet_loss', 0.3),
            data.get('ack_loss', 0.3),
            data.get('corruption', 0.1)
        )

        return jsonify({
            'result': result,
            'stats': rdt_server.stats,
            'sender_seq': rdt_server.sender_seq,
            'receiver_seq': rdt_server.receiver_seq
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reset', methods=['POST'])
def reset_simulation():
    rdt_server.reset()
    return jsonify({
        'status': 'reset',
        'stats': rdt_server.stats,
        'sender_seq': rdt_server.sender_seq,
        'receiver_seq': rdt_server.receiver_seq
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify({
        'stats': rdt_server.stats,
        'sender_seq': rdt_server.sender_seq,
        'receiver_seq': rdt_server.receiver_seq
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'RDT Protocol Server'})

if __name__ == '__main__':
    print("🔗 RDT Protocol Server Starting...")
    print("📊 Access the simulation at: http://localhost:5000")
    print("⚡ Use Ctrl+C to stop the server")
    app.run(host='0.0.0.0', debug=True, port=5000)