#!/usr/bin/env python3
"""
UV Setup and Management Script for Warhammer Fantasy GSAP Tavern Simulator
Provides UV-based package management, virtual environment setup, and development tools
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import List, Optional

class UVManager:
    """Manages UV package installation and virtual environment setup"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.uv_available = self._check_uv_availability()
        
    def _check_uv_availability(self) -> bool:
        """Check if UV is available on the system"""
        try:
            result = subprocess.run(['uv', '--version'], 
                                  capture_output=True, text=True, check=True)
            print(f"✅ UV found: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️ UV not found. Install with: pip install uv")
            return False
    
    def install_uv(self) -> bool:
        """Install UV if not available"""
        if self.uv_available:
            print("✅ UV already available")
            return True
            
        try:
            print("📦 Installing UV...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'uv'], 
                         check=True)
            self.uv_available = self._check_uv_availability()
            return self.uv_available
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install UV: {e}")
            return False
    
    def create_venv(self, venv_name: str = "tavern-env") -> bool:
        """Create virtual environment using UV"""
        if not self.uv_available:
            print("❌ UV not available for venv creation")
            return False
            
        venv_path = self.project_root / venv_name
        
        try:
            print(f"🏗️ Creating virtual environment: {venv_name}")
            subprocess.run(['uv', 'venv', str(venv_path)], check=True)
            print(f"✅ Virtual environment created at: {venv_path}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create venv: {e}")
            return False
    
    def install_dependencies(self, dev: bool = False, viz: bool = False) -> bool:
        """Install project dependencies using UV"""
        if not self.uv_available:
            print("❌ UV not available for dependency installation")
            return False
        
        try:
            print("📦 Installing dependencies with UV...")
            
            # Base installation
            cmd = ['uv', 'pip', 'install', '-e', '.']
            
            # Add optional dependencies
            extras = []
            if dev:
                extras.append('dev')
            if viz:
                extras.append('viz')
            
            if extras:
                cmd[-1] = f".[{','.join(extras)}]"
            
            subprocess.run(cmd, check=True, cwd=self.project_root)
            print("✅ Dependencies installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    def sync_dependencies(self) -> bool:
        """Sync dependencies using UV"""
        if not self.uv_available:
            return False
            
        try:
            print("🔄 Syncing dependencies...")
            subprocess.run(['uv', 'pip', 'sync', 'requirements.txt'], 
                         check=True, cwd=self.project_root)
            print("✅ Dependencies synced")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to sync dependencies: {e}")
            return False
    
    def run_app(self, app_name: str = "app_enhanced_ui.py") -> bool:
        """Run the application using UV"""
        if not self.uv_available:
            print("❌ UV not available")
            return False
            
        try:
            print(f"🚀 Running {app_name} with UV...")
            subprocess.run(['uv', 'run', 'streamlit', 'run', app_name], 
                         cwd=self.project_root)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to run app: {e}")
            return False
        except KeyboardInterrupt:
            print("\n⏹️ Application stopped by user")
            return True
    
    def run_tests(self) -> bool:
        """Run tests using UV"""
        if not self.uv_available:
            return False
            
        try:
            print("🧪 Running tests with UV...")
            subprocess.run(['uv', 'run', 'python', 'test_complete_integration.py'], 
                         check=True, cwd=self.project_root)
            print("✅ Tests completed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Tests failed: {e}")
            return False
    
    def format_code(self) -> bool:
        """Format code using UV and black"""
        if not self.uv_available:
            return False
            
        try:
            print("🎨 Formatting code with UV + Black...")
            subprocess.run(['uv', 'run', 'black', '.'], 
                         check=True, cwd=self.project_root)
            print("✅ Code formatted")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Code formatting failed: {e}")
            return False
    
    def lint_code(self) -> bool:
        """Lint code using UV and flake8"""
        if not self.uv_available:
            return False
            
        try:
            print("🔍 Linting code with UV + Flake8...")
            subprocess.run(['uv', 'run', 'flake8', '.'], 
                         check=True, cwd=self.project_root)
            print("✅ Code linting passed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Linting issues found: {e}")
            return False
    
    def generate_lockfile(self) -> bool:
        """Generate UV lockfile"""
        if not self.uv_available:
            return False
            
        try:
            print("🔒 Generating UV lockfile...")
            subprocess.run(['uv', 'pip', 'compile', 'pyproject.toml', 
                          '--output-file', 'uv.lock'], 
                         check=True, cwd=self.project_root)
            print("✅ Lockfile generated: uv.lock")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to generate lockfile: {e}")
            return False
    
    def setup_development_environment(self) -> bool:
        """Complete development environment setup"""
        print("🏗️ Setting up development environment with UV...")
        
        steps = [
            ("Install UV", self.install_uv),
            ("Create Virtual Environment", lambda: self.create_venv()),
            ("Install Dependencies", lambda: self.install_dependencies(dev=True, viz=True)),
            ("Generate Lockfile", self.generate_lockfile),
            ("Run Tests", self.run_tests)
        ]
        
        for step_name, step_func in steps:
            print(f"\n📋 {step_name}...")
            if not step_func():
                print(f"❌ {step_name} failed!")
                return False
        
        print("\n🎉 Development environment setup complete!")
        print("\nQuick commands:")
        print("  uv run streamlit run app_enhanced_ui.py  # Run the app")
        print("  uv run python test_complete_integration.py  # Run tests")
        print("  uv run black .  # Format code")
        print("  uv run flake8 .  # Lint code")
        
        return True

def main():
    """Main UV setup execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="UV Setup for Warhammer Tavern Simulator")
    parser.add_argument('command', choices=[
        'setup', 'install', 'run', 'test', 'format', 'lint', 'sync', 'lock'
    ], help='Command to execute')
    parser.add_argument('--dev', action='store_true', help='Include dev dependencies')
    parser.add_argument('--viz', action='store_true', help='Include visualization dependencies')
    parser.add_argument('--app', default='app_enhanced_ui.py', help='App file to run')
    
    args = parser.parse_args()
    
    manager = UVManager()
    
    if args.command == 'setup':
        success = manager.setup_development_environment()
    elif args.command == 'install':
        success = manager.install_dependencies(dev=args.dev, viz=args.viz)
    elif args.command == 'run':
        success = manager.run_app(args.app)
    elif args.command == 'test':
        success = manager.run_tests()
    elif args.command == 'format':
        success = manager.format_code()
    elif args.command == 'lint':
        success = manager.lint_code()
    elif args.command == 'sync':
        success = manager.sync_dependencies()
    elif args.command == 'lock':
        success = manager.generate_lockfile()
    else:
        print(f"❌ Unknown command: {args.command}")
        success = False
    
    if success:
        print(f"\n✅ Command '{args.command}' completed successfully!")
        sys.exit(0)
    else:
        print(f"\n❌ Command '{args.command}' failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
