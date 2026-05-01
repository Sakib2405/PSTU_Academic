# RDT Protocol Lab - Animated Simulation

A web-based animated simulation of Reliable Data Transfer (RDT) protocols.

## Features

- 🎯 **Visual RDT Protocol Simulation**
- 🎨 **Animated Packet Transmissions**
- ⚙️ **Adjustable Network Parameters**
- 📊 **Real-time Statistics**
- 📝 **Detailed Event Logging**
- 📱 **Responsive Design**

## Files

- `index.html` - Main HTML structure
- `styles.css` - Styling and animations
- `script.js` - RDT simulation logic
- `rdt-protocol.py` - Optional Flask backend

## How to Run

### Frontend Only (Recommended):
1. Save all files in a folder
2. Open `index.html` in a web browser
3. Start simulating!

### With Backend:
1. Install Flask: `pip install flask flask-cors`
2. Run: `python rdt-protocol.py`
3. Open `index.html` in browser

## RDT Features Demonstrated

- Sequence Numbers (0,1 alternating)
- Checksum for corruption detection
- ACK mechanism
- Timeout and retransmission
- Stop-and-Wait flow control
- Duplicate detection

## Educational Value

This lab helps understand:
- How reliable data transfer works
- Network reliability challenges
- Protocol design principles
- Flow control mechanisms