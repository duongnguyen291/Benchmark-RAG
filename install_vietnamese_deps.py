#!/usr/bin/env python3
"""
Installation script for Vietnamese dependencies
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")
        return False

def main():
    """Main installation function"""
    print("🚀 Installing Vietnamese dependencies for BenchmarkRAG...")
    print("=" * 60)
    
    # Core dependencies
    core_packages = [
        "pandas",
        "numpy", 
        "matplotlib",
        "scipy",
        "tqdm"
    ]
    
    # Vietnamese-specific dependencies
    vietnamese_packages = [
        "python-Levenshtein",
        "underthesea"
    ]
    
    print("\n📦 Installing core dependencies...")
    core_success = True
    for package in core_packages:
        if not install_package(package):
            core_success = False
    
    print("\n🇻🇳 Installing Vietnamese-specific dependencies...")
    vietnamese_success = True
    for package in vietnamese_packages:
        if not install_package(package):
            vietnamese_success = False
    
    print("\n" + "=" * 60)
    if core_success and vietnamese_success:
        print("🎉 All dependencies installed successfully!")
        print("\nYou can now run:")
        print("  python test_vietnamese.py  # Test dependencies")
        print("  python leivein_benchmark_optimized.py  # Run benchmark")
    else:
        print("⚠️  Some dependencies failed to install.")
        print("Please try installing them manually:")
        print("  pip install python-Levenshtein underthesea")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
