#!/usr/bin/env python3
"""
Simple comparison script to test performance improvements
"""

import time
import os
from pathlib import Path

def test_original_performance():
    """Test original direct_evaluate_benchmark.py performance"""
    print("🔄 Testing original performance...")
    start_time = time.time()
    
    # Run original script
    os.system("python direct_evaluate_benchmark.py")
    
    original_time = time.time() - start_time
    print(f"⏱️  Original execution time: {original_time:.2f} seconds")
    return original_time

def test_optimized_performance():
    """Test optimized direct_evaluate_benchmark_optimized.py performance"""
    print("🔄 Testing optimized performance...")
    start_time = time.time()
    
    # Run optimized script
    os.system("python direct_evaluate_benchmark_optimized.py")
    
    optimized_time = time.time() - start_time
    print(f"⏱️  Optimized execution time: {optimized_time:.2f} seconds")
    return optimized_time

def main():
    print("🚀 Performance Comparison Test")
    print("=" * 50)
    
    # Check if files exist
    if not Path("direct_evaluate_benchmark.py").exists():
        print("❌ direct_evaluate_benchmark.py not found!")
        return
    
    if not Path("direct_evaluate_benchmark_optimized.py").exists():
        print("❌ direct_evaluate_benchmark_optimized.py not found!")
        return
    
    # Test performance
    try:
        original_time = test_original_performance()
        print("\n" + "="*50)
        optimized_time = test_optimized_performance()
        
        # Calculate improvement
        improvement = ((original_time - optimized_time) / original_time) * 100
        
        print(f"\n📊 PERFORMANCE COMPARISON")
        print("=" * 50)
        print(f"Original time:     {original_time:.2f} seconds")
        print(f"Optimized time:    {optimized_time:.2f} seconds")
        print(f"Improvement:       {improvement:.1f}% faster")
        
        if improvement > 0:
            print(f"✅ Optimized version is {improvement:.1f}% faster!")
        else:
            print(f"⚠️  Optimized version is {abs(improvement):.1f}% slower")
            
    except Exception as e:
        print(f"❌ Error during performance test: {e}")

if __name__ == "__main__":
    main()
