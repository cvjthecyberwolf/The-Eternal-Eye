#!/usr/bin/env python3
import os
import subprocess
import sys

def setup_eternal_eye():
    print("👁️  Setting up Eternal Eye...")
    
    # Create directory structure
    directories = ["relay", "implant", "controller", "logs", "certificates"]
    for dir in directories:
        os.makedirs(dir, exist_ok=True)
        print(f"✓ Created {dir}/")
    
    print("\n✅ Eternal Eye setup complete!")
    print("Run 'python launcher.py' to launch the system")

if __name__ == "__main__":
    setup_eternal_eye()
