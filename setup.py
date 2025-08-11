#!/usr/bin/env python3
"""
Setup script for Document Extraction Benchmark Framework.
This script helps you set up the environment and test the installation.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install Python dependencies."""
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    )

def test_installation():
    """Test the installation by running the test script."""
    return run_command(
        f"{sys.executable} test_installation.py",
        "Testing installation"
    )

def create_directories():
    """Create necessary directories."""
    print("📁 Creating directories...")
    directories = [
        "test_files",
        "results",
        "repositories",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def show_next_steps():
    """Show next steps for the user."""
    print("\n" + "="*60)
    print("🎉 Setup completed successfully!")
    print("="*60)
    
    print("\n📋 Next Steps:")
    print("1. Prepare your test files:")
    print("   - Create DOCX files and convert them to PDF")
    print("   - Place them in the test_files/ directory")
    print("   - Example: test_files/document1.docx, test_files/document1.pdf")
    
    print("\n2. Run a quick test:")
    print("   python example_evaluation.py")
    
    print("\n3. List available repositories:")
    print("   python main.py list-repos")
    
    print("\n4. Run a full benchmark:")
    print("   python main.py run --test-files ./test_files --output ./results")
    
    print("\n5. Or evaluate pre-extracted files:")
    print("   python main.py evaluate --ground-truth ./ground_truth --extracted ./extracted_files --output ./results")
    
    print("\n📚 For more information, see README.md")

def main():
    """Main setup function."""
    print("🚀 Document Extraction Benchmark Framework - Setup")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation")
        print("Please check the error messages above and try again")
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print("\n❌ Setup failed during installation test")
        print("Please check the error messages above and try again")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    main()
