#!/usr/bin/env python3
"""
Test script to verify Vietnamese dependencies work correctly
"""

from Levenshtein import ratio
from underthesea import word_tokenize
import numpy as np
from scipy.spatial.distance import cdist
import pandas as pd

def test_vietnamese_dependencies():
    """Test if Vietnamese dependencies work correctly"""
    print("🧪 Testing Vietnamese dependencies...")
    
    # Test underthesea word_tokenize
    print("\n1. Testing underthesea.word_tokenize:")
    vietnamese_text = "Tôi yêu Việt Nam và tiếng Việt rất đẹp"
    tokens = word_tokenize(vietnamese_text)
    print(f"   Input: {vietnamese_text}")
    print(f"   Tokens: {tokens}")
    
    # Test Levenshtein ratio
    print("\n2. Testing Levenshtein.ratio:")
    str1 = "Việt Nam"
    str2 = "Viet Nam"
    similarity = ratio(str1, str2)
    print(f"   '{str1}' vs '{str2}': {similarity:.3f}")
    
    # Test similarity matrix
    print("\n3. Testing similarity matrix:")
    ex_tokens = ["Tôi", "yêu", "Việt", "Nam"]
    gt_tokens = ["Tôi", "thích", "Việt", "Nam"]
    
    ex_nump = np.array(ex_tokens)
    gt_nump = np.array(gt_tokens)
    
    matrix = cdist(ex_nump.reshape(-1, 1), gt_nump.reshape(-1, 1), 
                   lambda x, y: ratio(x[0], y[0]))
    df = pd.DataFrame(data=matrix, index=ex_tokens, columns=gt_tokens)
    print(f"   Similarity matrix:\n{df}")
    
    print("\n✅ All Vietnamese dependencies working correctly!")

if __name__ == "__main__":
    try:
        test_vietnamese_dependencies()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
