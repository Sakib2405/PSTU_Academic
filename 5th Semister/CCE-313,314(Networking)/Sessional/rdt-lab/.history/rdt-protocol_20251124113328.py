# rdt-protocol.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import time

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

@app.route('/send', methods=['POST'])
def send_packet():
    data = request.json
    result = rdt_server.simulate_transmission(
        data['message'],
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
    app.run(debug=True, port=5000)