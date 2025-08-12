#!/usr/bin/env python3
"""
Test script for Levenshtein-based evaluation system.
"""

import sys
from pathlib import Path
from src.evaluator import DocumentEvaluator
from src.models import ExtractionResult, ProcessingTime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_levenshtein_evaluation():
    """Test the Levenshtein-based evaluation system."""
    
    print("🧪 Testing Levenshtein-based Evaluation System")
    print("=" * 60)
    
    # Initialize evaluator
    evaluator = DocumentEvaluator()
    
    # Test cases with different levels of similarity
    test_cases = [
        {
            'name': 'Exact Match',
            'ground_truth': 'This is a test document with some content.',
            'extracted': 'This is a test document with some content.'
        },
        {
            'name': 'Minor Character Differences',
            'ground_truth': 'This is a test document with some content.',
            'extracted': 'This is a test document with some contnt.'  # Missing 'e'
        },
        {
            'name': 'Word Order Changes',
            'ground_truth': 'This is a test document with some content.',
            'extracted': 'This is a test document with content some.'  # Swapped words
        },
        {
            'name': 'Missing Words',
            'ground_truth': 'This is a test document with some content.',
            'extracted': 'This is a test document with content.'  # Missing 'some'
        },
        {
            'name': 'Major Differences',
            'ground_truth': 'This is a test document with some content.',
            'extracted': 'This is completely different content here.'
        },
        {
            'name': 'Empty Extraction',
            'ground_truth': 'This is a test document with some content.',
            'extracted': ''
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['name']}")
        print("-" * 40)
        
        # Create extraction result
        extraction_result = ExtractionResult(
            file_path=f"test_file_{i}.md",
            repository_name="test_repo",
            output_path=f"test_output_{i}.md",
            processing_time=ProcessingTime(0.0, 0.0),
            success=True,
            output_content=test_case['extracted']
        )
        
        # Create temporary ground truth file
        gt_file = Path(f"temp_gt_{i}.md")
        with open(gt_file, 'w', encoding='utf-8') as f:
            f.write(test_case['ground_truth'])
        
        try:
            # Evaluate
            evaluation_result = evaluator.evaluate_extraction(extraction_result, str(gt_file))
            
            # Print results
            print(f"Ground Truth: '{test_case['ground_truth']}'")
            print(f"Extracted:    '{test_case['extracted']}'")
            print(f"Overall Score: {evaluation_result.overall_score:.3f}")
            print(f"Character Similarity: {evaluation_result.content_similarity.character_similarity:.3f}")
            print(f"Word Similarity: {evaluation_result.content_similarity.word_similarity:.3f}")
            print(f"Sentence Similarity: {evaluation_result.content_similarity.sentence_similarity:.3f}")
            print(f"Word Overlap (F1): {evaluation_result.content_similarity.word_overlap:.3f}")
            print(f"ROUGE Score: {evaluation_result.content_similarity.rouge_score:.3f}")
            print(f"BLEU Score: {evaluation_result.content_similarity.bleu_score:.3f}")
            
        except Exception as e:
            print(f"❌ Error in test case {i}: {e}")
        finally:
            # Clean up
            if gt_file.exists():
                gt_file.unlink()
    
    print(f"\n✅ Levenshtein evaluation test completed!")

def test_levenshtein_distance_calculation():
    """Test the Levenshtein distance calculation directly."""
    
    print("\n🔍 Testing Levenshtein Distance Calculation")
    print("=" * 50)
    
    evaluator = DocumentEvaluator()
    
    # Test character-level Levenshtein
    test_strings = [
        ("hello", "hello"),      # Same
        ("hello", "helo"),       # Missing character
        ("hello", "hallo"),      # Substitution
        ("hello", "helloo"),     # Extra character
        ("hello", "world"),      # Completely different
        ("", "hello"),           # Empty string
        ("hello", ""),           # Empty string
        ("", ""),                # Both empty
    ]
    
    print("Character-level Levenshtein Distance:")
    for str1, str2 in test_strings:
        distance = evaluator._calculate_levenshtein_distance(str1, str2)
        similarity = evaluator._calculate_character_levenshtein_similarity(str1, str2)
        print(f"  '{str1}' vs '{str2}': Distance={distance}, Similarity={similarity:.3f}")
    
    # Test word-level Levenshtein
    print("\nWord-level Levenshtein Distance:")
    word_tests = [
        (["hello", "world"], ["hello", "world"]),
        (["hello", "world"], ["hello", "earth"]),
        (["hello", "world"], ["hello"]),
        (["hello", "world"], ["world", "hello"]),
        ([], ["hello", "world"]),
    ]
    
    for words1, words2 in word_tests:
        distance = evaluator._calculate_levenshtein_distance_sequences(words1, words2)
        similarity = evaluator._calculate_word_levenshtein_similarity(" ".join(words1), " ".join(words2))
        print(f"  {words1} vs {words2}: Distance={distance}, Similarity={similarity:.3f}")

if __name__ == "__main__":
    test_levenshtein_distance_calculation()
    test_levenshtein_evaluation()
