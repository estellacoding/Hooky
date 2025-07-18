"""
Webhook Receiver Server

A Flask application that receives webhook data from various services
and displays it in real-time on a web interface.

Features:
- Accept GET and POST webhook requests
- Real-time updates via Server-Sent Events
- Store webhook data in memory
- Web interface for viewing and copying data
- Support for JSON, form data, and raw text
- Automatic client cleanup for SSE connections
"""

from flask import Flask, request, jsonify, Response
import json
import queue
import os
import logging
import time
from datetime import datetime
from typing import Dict, Any, Optional, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask application
app = Flask(__name__)

# Global storage for webhook data (in-memory, will be lost on restart)
webhook_data: List[Dict[str, Any]] = []

# List of connected SSE clients for real-time updates
clients: List['SSEClient'] = []

# Removed heartbeat functionality - not needed for webhook receiver

# Configuration constants
MAX_WEBHOOK_DATA_SIZE = 1000  # Maximum number of webhook entries to store


class SSEClient:
    """Server-Sent Events client for real-time communication"""
    
    def __init__(self):
        """Initialize client with message queue and add to clients list"""
        self.queue = queue.Queue()
        clients.append(self)
        logger.info(f"New SSE client connected. Total clients: {len(clients)}")
    
    def put(self, data: str) -> None:
        """Add data to client's message queue
        
        Args:
            data: JSON string to send to client
        """
        try:
            self.queue.put(data)
        except Exception as e:
            logger.error(f"Failed to put data in client queue: {e}")
    
    def get(self) -> Optional[str]:
        """Get data from queue (non-blocking)
        
        Returns:
            Data from queue or None if empty
        """
        try:
            return self.queue.get_nowait()
        except queue.Empty:
            return None
    
    def cleanup(self) -> None:
        """Remove client from global clients list"""
        if self in clients:
            clients.remove(self)
            logger.info(f"SSE client disconnected. Total clients: {len(clients)}")


def validate_webhook_data(data: Any) -> bool:
    """Validate webhook data before processing
    
    Args:
        data: Data to validate
        
    Returns:
        True if data is valid, False otherwise
    """
    # Add validation logic here if needed
    # For now, accept all data
    return True


def cleanup_old_data() -> None:
    """Remove old webhook data if exceeding maximum size"""
    global webhook_data
    if len(webhook_data) > MAX_WEBHOOK_DATA_SIZE:
        # Keep only the most recent entries
        webhook_data = webhook_data[-MAX_WEBHOOK_DATA_SIZE:]
        logger.info(f"Cleaned up old webhook data. Current size: {len(webhook_data)}")


def broadcast_to_clients(data: Dict[str, Any]) -> None:
    """Broadcast data to all connected SSE clients
    
    Args:
        data: Data to broadcast
    """
    if not clients:
        return
    
    json_data = json.dumps(data)
    disconnected_clients = []
    
    for client in clients:
        try:
            client.put(json_data)
        except Exception as e:
            logger.error(f"Failed to send data to client: {e}")
            disconnected_clients.append(client)
    
    # Remove disconnected clients
    for client in disconnected_clients:
        client.cleanup()


@app.route('/')
def index():
    """Serve the main HTML page"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logger.error("index.html not found")
        return "Webhook Receiver - Web interface not found", 404
    except Exception as e:
        logger.error(f"Error serving index page: {e}")
        return "Internal Server Error", 500


@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    print("\n====== Webhook Received ======")
    print("Method:", request.method)
    print("Headers:", dict(request.headers))
    print("is_json:", request.is_json)
    print("Raw Body:", request.get_data(as_text=True))

    try:
        # 判斷資料來源與格式
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                source = "json"
            elif request.form:
                data = request.form.to_dict()
                source = "form"
            else:
                raw_text = request.get_data(as_text=True)
                try:
                    data = json.loads(raw_text)
                    source = "raw-json"
                except:
                    data = {"raw": raw_text}
                    source = "raw-text"
        else:
            data = request.args.to_dict()
            source = "get"

        print(f"[Webhook] Data parsed from: {source}")
        print(f"[Webhook] Parsed Data: {data}")

        # 資料驗證（可依需要加強）
        if not validate_webhook_data(data):
            raise ValueError("Invalid webhook data")

        # 儲存
        webhook_entry = {
            'id': f"webhook_{datetime.now().timestamp()}",
            'timestamp': datetime.now().isoformat(),
            'method': request.method,
            'headers': dict(request.headers),
            'data': data,
            'remote_addr': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', 'Unknown'),
            'content_type': request.headers.get('Content-Type', 'Unknown'),
            'source': source
        }

        webhook_data.append(webhook_entry)
        cleanup_old_data()
        broadcast_to_clients(webhook_entry)

        logger.info(f"Webhook received: {request.method} from {request.remote_addr}")

        return jsonify({
            'status': 'success',
            'message': 'Webhook received successfully',
            'timestamp': webhook_entry['timestamp'],
            'id': webhook_entry['id']
        }), 200

    except Exception as e:
        error_entry = {
            'id': f"error_{datetime.now().timestamp()}",
            'timestamp': datetime.now().isoformat(),
            'error': str(e),
            'method': request.method,
            'remote_addr': request.remote_addr,
            'type': 'error'
        }
        webhook_data.append(error_entry)

        logger.error(f"Webhook error: {e} from {request.remote_addr}")

        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': error_entry['timestamp']
        }), 500


@app.route('/events')
def events():
    """Server-Sent Events endpoint for real-time updates
    
    Returns:
        SSE stream response
    """
    def event_stream():
        """Generator function that yields SSE data"""
        client = SSEClient()
        try:
            # Send keepalive immediately to establish connection
            yield f"data: {json.dumps({'type': 'connected', 'timestamp': datetime.now().isoformat()})}\n\n"
            
            while True:
                # Get data from client queue (non-blocking)
                data = client.get()
                if data is not None:
                    # Send actual webhook data to client
                    yield f"data: {data}\n\n"
                else:
                    # Send keepalive every 10 seconds to prevent timeout
                    import time
                    time.sleep(10)
                    yield f"data: {json.dumps({'type': 'keepalive', 'timestamp': datetime.now().isoformat()})}\n\n"
        except GeneratorExit:
            # Clean up client when connection closes
            client.cleanup()
        except Exception as e:
            logger.error(f"Error in SSE stream: {e}")
            client.cleanup()
    
    # Set appropriate headers for SSE
    response = Response(event_stream(), mimetype='text/event-stream')
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Connection'] = 'keep-alive'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/api/data')
def get_data():
    """API endpoint to get all stored webhook data
    
    Returns:
        JSON array of all webhook entries
    """
    return jsonify({
        'data': webhook_data,
        'total': len(webhook_data),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/clear', methods=['POST'])
def clear_data():
    """API endpoint to clear all stored webhook data
    
    Returns:
        JSON response confirming data clearance
    """
    global webhook_data
    old_count = len(webhook_data)
    webhook_data = []
    
    logger.info(f"Webhook data cleared. Removed {old_count} entries.")
    
    return jsonify({
        'status': 'success',
        'message': 'Data cleared successfully',
        'cleared_count': old_count,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/health')
def health_check():
    """Health check endpoint for monitoring
    
    Returns:
        JSON response with server status
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'webhook_count': len(webhook_data),
        'connected_clients': len(clients),
        'version': '1.0.0'
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found',
        'timestamp': datetime.now().isoformat()
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'status': 'error',
        'message': 'Internal server error',
        'timestamp': datetime.now().isoformat()
    }), 500


if __name__ == '__main__':
    # Get configuration from environment variables with defaults
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    host = os.environ.get('HOST', '0.0.0.0')
    
    # Set logging level based on debug mode
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.info("Debug mode enabled")
    else:
        logging.getLogger().setLevel(logging.INFO)
        logger.info("Production mode - debug disabled")
    
    # Print startup information
    logger.info("Starting Webhook Receiver...")
    logger.info(f"Server will run on {host}:{port}")
    logger.info(f"Maximum webhook data size: {MAX_WEBHOOK_DATA_SIZE}")
    
    try:
        # Start Flask application
        # host='0.0.0.0' allows external connections
        # threaded=True enables handling multiple requests simultaneously
        app.run(
            debug=debug,
            host=host,
            port=port,
            threaded=True,
            use_reloader=False  # Disable reloader in production
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        exit(1)