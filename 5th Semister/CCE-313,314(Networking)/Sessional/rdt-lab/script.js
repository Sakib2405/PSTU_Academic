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
        this.autoMode = false;
        this.autoInterval = null;
        this.simulationStartTime = null;
        this.backendAvailable = false;
        
        this.initializeEventListeners();
        this.checkServerStatus();
        this.updateDisplays();
    }

    async checkServerStatus() {
        try {
            const response = await fetch('/api/health');
            if (response.ok) {
                this.backendAvailable = true;
                this.updateServerStatus('✅ Connected to backend server', 'connected');
                this.logEvent('✅ Backend server connected successfully', 'success');
            } else {
                throw new Error('Server not responding properly');
            }
        } catch (error) {
            this.backendAvailable = false;
            this.updateServerStatus('⚠️ Using frontend simulation only', 'disconnected');
            this.logEvent('⚠️ Backend server unavailable, using frontend simulation', 'warning');
        }
    }

    updateServerStatus(message, status) {
        const statusElement = document.getElementById('serverStatus');
        statusElement.textContent = message;
        statusElement.className = `server-status ${status}`;
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
            } else {
                this.logEvent('❌ Please enter a message to send', 'error');
            }
        });

        document.getElementById('sendMultiple').addEventListener('click', () => {
            this.sendTestSequence();
        });

        document.getElementById('autoMode').addEventListener('click', () => {
            this.toggleAutoMode();
        });

        document.getElementById('resetSim').addEventListener('click', () => {
            this.resetSimulation();
        });

        document.getElementById('clearLog').addEventListener('click', () => {
            this.clearLog();
        });

        // Preset buttons
        document.querySelectorAll('.btn-preset').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const preset = e.target.dataset.preset;
                this.applyPreset(preset);
            });
        });

        // Enter key for message input
        document.getElementById('messageInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                document.getElementById('sendSingle').click();
            }
        });

        // Initialize simulation start time
        this.simulationStartTime = Date.now();
    }

    applyPreset(preset) {
        const presets = {
            perfect: { packetLoss: 0, ackLoss: 0, corruption: 0 },
            bad: { packetLoss: 20, ackLoss: 20, corruption: 10 },
            'very-bad': { packetLoss: 40, ackLoss: 40, corruption: 20 }
        };

        const settings = presets[preset];
        if (settings) {
            document.getElementById('packetLoss').value = settings.packetLoss;
            document.getElementById('ackLoss').value = settings.ackLoss;
            document.getElementById('corruption').value = settings.corruption;
            
            document.getElementById('packetLossValue').textContent = settings.packetLoss + '%';
            document.getElementById('ackLossValue').textContent = settings.ackLoss + '%';
            document.getElementById('corruptionValue').textContent = settings.corruption + '%';
            
            this.logEvent(`🎯 Applied ${preset} network preset`, 'success');
        }
    }

    toggleAutoMode() {
        this.autoMode = !this.autoMode;
        const button = document.getElementById('autoMode');
        
        if (this.autoMode) {
            button.textContent = 'Stop Auto Mode';
            button.classList.remove('btn-secondary');
            button.classList.add('btn-danger');
            this.logEvent('🤖 Auto mode started - sending packets continuously', 'info');
            this.startAutoMode();
        } else {
            button.textContent = 'Auto Mode';
            button.classList.remove('btn-danger');
            button.classList.add('btn-secondary');
            this.logEvent('🛑 Auto mode stopped', 'info');
            this.stopAutoMode();
        }
    }

    startAutoMode() {
        let counter = 1;
        this.autoInterval = setInterval(() => {
            if (!this.isWaitingForAck) {
                this.sendPacket(`Auto-${counter}`);
                counter++;
            }
        }, 2000);
    }

    stopAutoMode() {
        if (this.autoInterval) {
            clearInterval(this.autoInterval);
            this.autoInterval = null;
        }
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

            let serverResult = null;
            
            if (this.backendAvailable) {
                try {
                    const response = await fetch('/api/send', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            message: packet.data,
                            packet_loss: params.packetLoss,
                            ack_loss: params.ackLoss,
                            corruption: params.corruption
                        })
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        serverResult = data.result;
                        
                        // Sync with backend state
                        if (data.stats) {
                            this.syncWithBackend(data);
                        }
                    } else {
                        throw new Error('Server error: ' + response.status);
                    }
                } catch (error) {
                    this.logEvent(`⚠️ Backend error: ${error.message}`, 'warning');
                    this.backendAvailable = false;
                    this.updateServerStatus('⚠️ Backend disconnected', 'disconnected');
                }
            }

            // If backend is not available, use frontend simulation
            if (!serverResult) {
                serverResult = this.simulateLocalTransmission(packet, params);
            }

            // Wait for visual travel time then apply outcome
            setTimeout(() => {
                this.processTransmissionResult(packet, packetElement, serverResult);
                resolve(true);
            }, 1000);
        });
    }

    simulateLocalTransmission(packet, params) {
        // Simulate packet loss
        if (Math.random() < params.packetLoss) {
            this.stats.packetsLost++;
            return { status: 'lost', seq: packet.seq };
        }
        
        // Simulate corruption
        if (Math.random() < params.corruption) {
            this.stats.packetsCorrupted++;
            return { status: 'corrupted', seq: packet.seq };
        }
        
        // Check if packet is in order
        if (packet.seq === this.receiverSeq) {
            this.stats.packetsDelivered++;
            this.receiverSeq = 1 - this.receiverSeq;
            
            const ackStatus = Math.random() < params.ackLoss ? 'lost' : 'delivered';
            
            if (ackStatus === 'delivered') {
                this.senderSeq = 1 - this.senderSeq;
                this.stats.acksReceived++;
            }
            
            return {
                status: 'delivered',
                seq: packet.seq,
                ack_status: ackStatus,
                data: packet.data
            };
        } else {
            return { status: 'duplicate', seq: packet.seq };
        }
    }

    processTransmissionResult(packet, packetElement, result) {
        switch (result.status) {
            case 'lost':
                this.logEvent(`📦 Packet ${packet.seq} LOST in transmission!`, 'error');
                packetElement.classList.add('packet-lost');
                packetElement.textContent = `LOST${packet.seq}\n"${packet.data}"`;
                break;
                
            case 'corrupted':
                this.logEvent(`⚠️ Packet ${packet.seq} CORRUPTED!`, 'warning');
                packetElement.classList.add('packet-corrupted');
                packetElement.textContent = `CORRUPT${packet.seq}\n"${packet.data}"`;
                this.animatePacketReceive(packet, true, result.ack_status);
                break;
                
            case 'delivered':
                this.animatePacketReceive(packet, false, result.ack_status);
                break;
                
            case 'duplicate':
                this.logEvent(`🔄 RECEIVER: Duplicate packet ${packet.seq} received`, 'warning');
                packetElement.classList.add('packet-duplicate');
                this.animatePacketReceive(packet, false, 'delivered');
                break;
        }

        packetElement.classList.add('fade-out');
        setTimeout(() => packetElement.remove(), 500);
    }

    syncWithBackend(backendData) {
        if (backendData.stats) {
            const s = backendData.stats;
            this.stats.packetsSent = s.packets_sent || this.stats.packetsSent;
            this.stats.acksReceived = s.acks_received || this.stats.acksReceived;
            this.stats.retransmissions = s.retransmissions || this.stats.retransmissions;
            this.stats.packetsLost = s.packets_lost || this.stats.packetsLost;
            this.stats.packetsCorrupted = s.packets_corrupted || this.stats.packetsCorrupted;
            this.stats.packetsDelivered = s.packets_delivered || this.stats.packetsDelivered;
        }
        
        if (backendData.sender_seq !== undefined) {
            this.senderSeq = backendData.sender_seq;
        }
        if (backendData.receiver_seq !== undefined) {
            this.receiverSeq = backendData.receiver_seq;
        }
        
        this.updateDisplays();
    }

    async animatePacketReceive(packet, isCorrupted, ackStatus = null) {
        if (isCorrupted) {
            this.logEvent(`❌ RECEIVER: Corrupted packet ${packet.seq} received, discarding...`);
            this.updateReceiverStatus(`Received corrupted packet ${packet.seq}`);
        } else if (packet.seq === this.receiverSeq) {
            this.logEvent(`✅ RECEIVER: Correct packet ${packet.seq} received: "${packet.data}"`, 'success');
            this.updateReceiverStatus(`Processing packet ${packet.seq}`);
            this.addToReceiverQueue(packet);
        } else {
            this.logEvent(`🔄 RECEIVER: Duplicate packet ${packet.seq}, expected ${this.receiverSeq}`, 'warning');
            this.updateReceiverStatus(`Duplicate packet ${packet.seq} received`);
        }

        await this.sendAck(packet.seq, isCorrupted, ackStatus);
    }

    async sendAck(seqNum, isCorrupted, forcedAckStatus = null) {
        const params = this.getNetworkParameters();
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
            this.logEvent(`✅ SENDER: Received ACK for packet ${seqNum}`, 'success');
            this.updateSenderStatus(`ACK received for packet ${seqNum}`);
            
            this.isWaitingForAck = false;
            this.clearSenderQueue();
        } else if (isCorrupted) {
            this.logEvent(`❌ SENDER: Corrupted ACK received for packet ${seqNum}`, 'error');
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
        
        const efficiency = this.stats.packetsSent > 0 ?
            Math.round((this.stats.packetsDelivered / this.stats.packetsSent) * 100) : 0;
        document.getElementById('statEfficiency').textContent = efficiency + '%';
        
        const totalTime = this.simulationStartTime ?
            Math.round((Date.now() - this.simulationStartTime) / 1000) : 0;
        document.getElementById('statTime').textContent = totalTime + 's';
        
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
        item.className = 'queue-item success';
        item.textContent = `SEQ${packet.seq}: "${packet.data}"`;
        queue.appendChild(item);
    }

    clearSenderQueue() {
        const queue = document.getElementById('senderQueue');
        while (queue.children.length > 1) {
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
        this.logEvent('Log cleared. Simulation continues...', 'info');
    }

    async resetSimulation() {
        // Stop auto mode if running
        if (this.autoMode) {
            this.toggleAutoMode();
        }

        // Clear any ongoing timeouts
        if (this.timeoutId) {
            clearTimeout(this.timeoutId);
            this.timeoutId = null;
        }

        // Reset backend if available
        if (this.backendAvailable) {
            try {
                const response = await fetch('/api/reset', { method: 'POST' });
                if (response.ok) {
                    const data = await response.json();
                    this.syncWithBackend(data);
                }
            } catch (error) {
                this.logEvent('⚠️ Could not reset backend', 'warning');
            }
        }

        // Reset frontend state
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

        this.simulationStartTime = Date.now();

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
        
        this.logEvent('🔄 Simulation reset. Ready for new transmission.', 'success');
    }
}

// Initialize the simulation when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.rdtSimulation = new RDTSimulation();
});