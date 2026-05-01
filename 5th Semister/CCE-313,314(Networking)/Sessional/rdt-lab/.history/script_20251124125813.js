class RDTSimulation {
    constructor() {
        this.senderSeq = 0;
        this.receiverSeq = 0;
        this.stats = {
            packetsSent: 0,
            acksReceived: 0,
            retransmissions: 0,
            packetsLost: 0,
            packetsCorrupted: 0,
            packetsDelivered: 0
        };
        this.currentPacket = null;
        this.isWaitingForAck = false;
        this.timeoutId = null;
        this.eventLog = [];
        
        this.initializeEventListeners();
        this.updateDisplays();
    }

    initializeEventListeners() {
        // Slider events
        document.getElementById('packetLoss').addEventListener('input', (e) => {
            document.getElementById('packetLossValue').textContent = e.target.value + '%';
        });
        document.getElementById('ackLoss').addEventListener('input', (e) => {
            document.getElementById('ackLossValue').textContent = e.target.value + '%';
        });
        document.getElementById('corruption').addEventListener('input', (e) => {
            document.getElementById('corruptionValue').textContent = e.target.value + '%';
        });
        document.getElementById('timeout').addEventListener('input', (e) => {
            document.getElementById('timeoutValue').textContent = parseFloat(e.target.value).toFixed(1) + 's';
        });

        // Button events
        document.getElementById('sendSingle').addEventListener('click', () => {
            const message = document.getElementById('messageInput').value.trim();
            if (message) {
                this.sendPacket(message);
                document.getElementById('messageInput').value = '';
            }
        });

        document.getElementById('sendMultiple').addEventListener('click', () => {
            this.sendTestSequence();
        });

        document.getElementById('resetSim').addEventListener('click', () => {
            this.resetSimulation();
        });

        document.getElementById('clearLog').addEventListener('click', () => {
            this.clearLog();
        });

        // Enter key for message input
        document.getElementById('messageInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                document.getElementById('sendSingle').click();
            }
        });
    }

    getNetworkParameters() {
        return {
            packetLoss: parseInt(document.getElementById('packetLoss').value) / 100,
            ackLoss: parseInt(document.getElementById('ackLoss').value) / 100,
            corruption: parseInt(document.getElementById('corruption').value) / 100,
            timeout: parseFloat(document.getElementById('timeout').value) * 1000
        };
    }

    async sendPacket(data) {
        if (this.isWaitingForAck) {
            this.logEvent('❌ Cannot send new packet: Waiting for ACK', 'error');
            return;
        }

        const params = this.getNetworkParameters();
        this.currentPacket = {
            seq: this.senderSeq,
            data: data,
            timestamp: Date.now()
        };

        this.stats.packetsSent++;
        this.isWaitingForAck = true;

        this.logEvent(`🚀 SENDER: Sending packet ${this.senderSeq} ("${data}")`);
        this.updateSenderStatus(`Sending packet ${this.senderSeq}...`);
        this.addToSenderQueue(this.currentPacket);

        // Start timeout
        this.startTimeoutTimer(params.timeout);

        // Animate packet sending
        await this.animatePacketSend(this.currentPacket, params);
        
        this.updateDisplays();
    }

    async animatePacketSend(packet, params) {
        // Use backend to decide whether packet is lost/corrupted/delivered
        return new Promise(async (resolve) => {
            const animationArea = document.getElementById('packetAnimation');
            const packetElement = document.createElement('div');
            packetElement.className = 'packet packet-data';
            packetElement.textContent = `DATA${packet.seq}\n"${packet.data}"`;
            packetElement.style.left = '10%';
            packetElement.style.top = '40%';
            animationArea.appendChild(packetElement);

            // Start movement animation
            setTimeout(() => { packetElement.style.left = '90%'; }, 50);

            // Call backend /send to get simulated outcome
            let serverResult = null;
            try {
                const resp = await fetch('/send', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: packet.data,
                        packet_loss: params.packetLoss,
                        ack_loss: params.ackLoss,
                        corruption: params.corruption
                    })
                });
                const json = await resp.json();
                serverResult = json.result || null;

                // If server returned stats, sync them to the UI
                if (json.stats) {
                    const s = json.stats;
                    // Update client-side stats to match server
                    this.stats.packetsSent = s.packets_sent || this.stats.packetsSent;
                    this.stats.acksReceived = s.acks_received || this.stats.acksReceived;
                    this.stats.retransmissions = s.retransmissions || this.stats.retransmissions;

                    // Update visible stat elements
                    document.getElementById('statSent').textContent = this.stats.packetsSent;
                    document.getElementById('statAcks').textContent = this.stats.acksReceived;
                    document.getElementById('statRetrans').textContent = this.stats.retransmissions;
                }
            } catch (err) {
                this.logEvent('⚠️ Backend /send request failed: ' + err.message, 'error');
            }

            // Wait for visual travel time then apply outcome
            setTimeout(() => {
                if (!serverResult) {
                    // If backend failed, fall back to client-side delivered
                    this.logEvent('⚠️ Backend unavailable, defaulting to delivered', 'warning');
                    this.animatePacketReceive(packet, false, 'delivered');
                } else if (serverResult.status === 'lost') {
                    this.stats.packetsLost++;
                    this.logEvent(`📦 Packet ${packet.seq} LOST in transmission!`, 'error');
                    packetElement.classList.add('packet-lost');
                    packetElement.textContent = `LOST${packet.seq}\n"${packet.data}"`;
                    packetElement.classList.add('fade-out');
                    setTimeout(() => packetElement.remove(), 500);
                    resolve(false);
                    return;
                } else if (serverResult.status === 'corrupted') {
                    this.stats.packetsCorrupted++;
                    this.logEvent(`⚠️ Packet ${packet.seq} CORRUPTED!`, 'warning');
                    packetElement.classList.add('packet-corrupted');
                    packetElement.textContent = `CORRUPT${packet.seq}\n"${packet.data}"`;
                    this.animatePacketReceive(packet, true, serverResult.ack_status || 'lost');
                } else if (serverResult.status === 'delivered') {
                    this.stats.packetsDelivered++;
                    this.animatePacketReceive(packet, false, serverResult.ack_status || 'delivered');
                } else {
                    // duplicate or other
                    this.logEvent(`🔄 RECEIVER: Server reported ${serverResult.status} for packet ${packet.seq}`);
                    this.animatePacketReceive(packet, false, serverResult.ack_status || 'delivered');
                }

                packetElement.classList.add('fade-out');
                setTimeout(() => packetElement.remove(), 500);
                resolve(true);
            }, 1000);
        });
    }

    async animatePacketReceive(packet, isCorrupted, ackStatus = null) {
        const params = this.getNetworkParameters();
        
        if (isCorrupted) {
            this.logEvent(`❌ RECEIVER: Corrupted packet ${packet.seq} received, discarding...`);
            this.updateReceiverStatus(`Received corrupted packet ${packet.seq}`);
        } else if (packet.seq === this.receiverSeq) {
            this.stats.packetsDelivered++;
            this.logEvent(`✅ RECEIVER: Correct packet ${packet.seq} received: "${packet.data}"`);
            this.updateReceiverStatus(`Processing packet ${packet.seq}`);
            this.addToReceiverQueue(packet);
            
            // Move expected sequence number
            this.receiverSeq = 1 - this.receiverSeq;
            document.getElementById('expectedSeq').textContent = this.receiverSeq;
        } else {
            this.logEvent(`🔄 RECEIVER: Duplicate packet ${packet.seq}, expected ${this.receiverSeq}`);
            this.updateReceiverStatus(`Duplicate packet ${packet.seq} received`);
        }

        // Send ACK (use ackStatus from server if provided)
        await this.sendAck(packet.seq, isCorrupted, params, ackStatus);
    }

    async sendAck(seqNum, isCorrupted, params, forcedAckStatus = null) {
        // If backend provided an ack status, use it; otherwise simulate locally
        const ackLost = forcedAckStatus ? (forcedAckStatus === 'lost') : (Math.random() < params.ackLoss);

        if (ackLost) {
            this.logEvent(`📨 ACK for packet ${seqNum} LOST!`, 'error');
            return;
        }

        this.logEvent(`📨 RECEIVER: Sending ACK for packet ${seqNum}`);
        
        // Animate ACK
        const animationArea = document.getElementById('packetAnimation');
        const ackElement = document.createElement('div');
        ackElement.className = 'packet packet-ack';
        ackElement.textContent = `ACK${seqNum}`;
        ackElement.style.left = '90%';
        ackElement.style.top = '60%';
        
        animationArea.appendChild(ackElement);

        setTimeout(() => { ackElement.style.left = '10%'; }, 50);

        setTimeout(() => {
            this.handleAckReceived(seqNum, isCorrupted);
            ackElement.classList.add('fade-out');
            setTimeout(() => ackElement.remove(), 500);
        }, 1000);
    }

    handleAckReceived(seqNum, isCorrupted) {
        if (this.timeoutId) {
            clearTimeout(this.timeoutId);
            this.timeoutId = null;
        }

        if (!isCorrupted && seqNum === this.senderSeq) {
            this.stats.acksReceived++;
            this.logEvent(`✅ SENDER: Received ACK for packet ${seqNum}`);
            this.updateSenderStatus(`ACK received for packet ${seqNum}`);
            
            // Move to next sequence number
            this.senderSeq = 1 - this.senderSeq;
            document.getElementById('nextSeq').textContent = this.senderSeq;
            
            this.isWaitingForAck = false;
            this.clearSenderQueue();
        } else if (isCorrupted) {
            this.logEvent(`❌ SENDER: Corrupted ACK received for packet ${seqNum}`);
            this.handleTimeout();
        }
        
        this.updateDisplays();
    }

    startTimeoutTimer(timeoutDuration) {
        this.timeoutId = setTimeout(() => {
            this.handleTimeout();
        }, timeoutDuration);
    }

    handleTimeout() {
        if (!this.isWaitingForAck) return;

        this.stats.retransmissions++;
        this.logEvent(`⏰ SENDER: Timeout for packet ${this.senderSeq}, retransmitting...`, 'warning');
        this.updateSenderStatus(`Timeout - Retransmitting packet ${this.senderSeq}`);

        // Retransmit current packet
        this.isWaitingForAck = false;
        if (this.currentPacket) {
            setTimeout(() => {
                this.sendPacket(this.currentPacket.data);
            }, 1000);
        }
    }

    async sendTestSequence() {
        const testMessages = ['Hello', 'RDT', 'Protocol', 'Lab', 'Test'];
        
        for (const message of testMessages) {
            if (this.isWaitingForAck) {
                // Wait for current transmission to complete
                await new Promise(resolve => {
                    const checkInterval = setInterval(() => {
                        if (!this.isWaitingForAck) {
                            clearInterval(checkInterval);
                            resolve();
                        }
                    }, 100);
                });
            }
            
            await this.sendPacket(message);
            await new Promise(resolve => setTimeout(resolve, 1500));
        }
    }

    // UI Update Methods
    updateDisplays() {
        document.getElementById('nextSeq').textContent = this.senderSeq;
        document.getElementById('expectedSeq').textContent = this.receiverSeq;
        
        document.getElementById('statSent').textContent = this.stats.packetsSent;
        document.getElementById('statAcks').textContent = this.stats.acksReceived;
        document.getElementById('statRetrans').textContent = this.stats.retransmissions;
        
        const successRate = this.stats.packetsSent > 0 ? 
            Math.round((this.stats.acksReceived / this.stats.packetsSent) * 100) : 100;
        document.getElementById('statSuccess').textContent = successRate + '%';
        
        document.getElementById('lostCount').textContent = this.stats.packetsLost;
        document.getElementById('corruptedCount').textContent = this.stats.packetsCorrupted;
        document.getElementById('deliveredCount').textContent = this.stats.packetsDelivered;
    }

    updateSenderStatus(message) {
        document.getElementById('senderStatus').textContent = message;
    }

    updateReceiverStatus(message) {
        document.getElementById('receiverStatus').textContent = message;
    }

    addToSenderQueue(packet) {
        const queue = document.getElementById('senderQueue');
        const item = document.createElement('div');
        item.className = 'queue-item';
        item.textContent = `SEQ${packet.seq}: "${packet.data}"`;
        queue.appendChild(item);
    }

    addToReceiverQueue(packet) {
        const queue = document.getElementById('receiverQueue');
        const item = document.createElement('div');
        item.className = 'queue-item';
        item.textContent = `SEQ${packet.seq}: "${packet.data}"`;
        queue.appendChild(item);
    }

    clearSenderQueue() {
        const queue = document.getElementById('senderQueue');
        while (queue.children.length > 1) { // Keep the label
            queue.removeChild(queue.lastChild);
        }
    }

    logEvent(message, type = 'info') {
        const logEntry = document.createElement('div');
        logEntry.className = `log-entry ${type}`;
        
        const timestamp = new Date().toLocaleTimeString();
        logEntry.textContent = `[${timestamp}] ${message}`;
        
        const logOutput = document.getElementById('eventLog');
        logOutput.appendChild(logEntry);
        logOutput.scrollTop = logOutput.scrollHeight;
        
        this.eventLog.push({ timestamp, message, type });
        document.getElementById('logCount').textContent = this.eventLog.length;
    }

    clearLog() {
        const logOutput = document.getElementById('eventLog');
        while (logOutput.firstChild) {
            logOutput.removeChild(logOutput.firstChild);
        }
        this.eventLog = [];
        document.getElementById('logCount').textContent = '0';
        this.logEvent('Log cleared. Simulation continues...');
    }

    resetSimulation() {
        // Clear any ongoing timeouts
        if (this.timeoutId) {
            clearTimeout(this.timeoutId);
            this.timeoutId = null;
        }

        // Reset state
        this.senderSeq = 0;
        this.receiverSeq = 0;
        this.isWaitingForAck = false;
        this.currentPacket = null;
        
        this.stats = {
            packetsSent: 0,
            acksReceived: 0,
            retransmissions: 0,
            packetsLost: 0,
            packetsCorrupted: 0,
            packetsDelivered: 0
        };

        // Clear UI
        this.clearSenderQueue();
        const receiverQueue = document.getElementById('receiverQueue');
        while (receiverQueue.children.length > 1) {
            receiverQueue.removeChild(receiverQueue.lastChild);
        }

        const animationArea = document.getElementById('packetAnimation');
        while (animationArea.firstChild) {
            animationArea.removeChild(animationArea.firstChild);
        }

        this.updateSenderStatus('Ready to send');
        this.updateReceiverStatus('Waiting for packets');
        
        this.clearLog();
        this.updateDisplays();
        
        this.logEvent('🔄 Simulation reset. Ready for new transmission.');
    }
}

// 4. rdt-protocol.py (Optional Backend)