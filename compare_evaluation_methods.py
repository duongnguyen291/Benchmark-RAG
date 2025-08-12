#!/usr/bin/env python3
"""
Compare our Levenshtein evaluation method with evaluate.py method
"""

import os
import pandas as pd
from scipy.spatial.distance import cdist
from Levenshtein import ratio
from underthesea import word_tokenize
import numpy as np
import glob
from statistics import mean
import json
from pathlib import Path

def extract_txt(txt_path):
    """Extract text from file (same as evaluate.py)"""
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = ' '.join(line.strip() for line in f)
    return text

def compute_sim_matrix(ex_nump, gt_nump):
    """Compute similarity matrix using Levenshtein ratio (from evaluate.py)"""
    matrix = cdist(ex_nump.reshape(-1, 1), gt_nump.reshape(-1, 1), lambda x, y: ratio(x[0], y[0]))
    df = pd.DataFrame(data=matrix, index=ex_nump, columns=gt_nump)
    return df

def compute_tpfp(matrix):
    """Compute True Positive and False Positive (from evaluate.py)"""
    tp=0
    fp=0
    rows=matrix.shape[0]
    cols=matrix.shape[1]
    for x in range(1,rows):
        flag = False
        for y in range(1,cols):
            if matrix.iloc[x,y] > 0.7:
                flag=True
                break
        if flag:
            tp+=1
        else:
            fp+=1
    return tp,fp

def compute_scores(tp,fp, gttoken):
    """Compute Precision, Recall, F1 (from evaluate.py)"""
    prec=min(tp/(tp+fp), 1.0)
    recall=min(tp/gttoken, 1.0)
    if prec==0 and recall==0:
        return 0,0,0
    else:
        f1_score= (2 * prec * recall)/ (prec + recall)
        return f1_score, prec, recall

def evaluate_py_method(ex_path, gt_path):
    """Evaluate using evaluate.py method"""
    ex = extract_txt(ex_path)
    gt = extract_txt(gt_path)

    gt_tokens = word_tokenize(gt)
    ex_tokens = word_tokenize(ex)
    num_gt_tokens = len(gt_tokens)
    gt = [gt]
    ex = [ex]
    gt_tokens = gt + gt_tokens
    ex_tokens = ex + ex_tokens

    matrix = compute_sim_matrix(np.array(ex_tokens), np.array(gt_tokens))
    tp,fp = compute_tpfp(matrix)
    f1_score, prec, recall = compute_scores(tp, fp, num_gt_tokens)
    acc = float(matrix.iloc[0, 0])

    return f1_score, prec, recall, acc

def our_levenshtein_method(ex_path, gt_path):
    """Evaluate using our custom Levenshtein method"""
    from src.evaluator import DocumentEvaluator
    from src.models import ExtractionResult, ProcessingTime
    
    # Read files
    with open(ex_path, 'r', encoding='utf-8') as f:
        extracted_content = f.read()
    with open(gt_path, 'r', encoding='utf-8') as f:
        ground_truth_content = f.read()
    
    # Create extraction result
    extraction_result = ExtractionResult(
        file_path=ex_path,
        repository_name="test",
        output_path=ex_path,
        processing_time=ProcessingTime(0.0, 0.0, 0.0, 0.0),
        success=True,
        error_message=None,
        output_content=extracted_content
    )
    
    # Evaluate
    evaluator = DocumentEvaluator(fast_mode=True)
    result = evaluator.evaluate_extraction(extraction_result, gt_path)
    
    return {
        'character_similarity': result.content_similarity.character_similarity,
        'word_similarity': result.content_similarity.word_similarity,
        'sentence_similarity': result.content_similarity.sentence_similarity,
        'word_overlap': result.content_similarity.word_overlap,
        'overall_score': result.overall_score
    }

def compare_methods():
    """Compare both evaluation methods"""
    print("🔍 Comparing Evaluation Methods")
    print("=" * 60)
    
    # Load our results
    our_results = pd.read_csv('evaluation_results_levenshtein/comprehensive_statistics.csv')
    
    print("\n📊 OUR LEVENSHTEIN METHOD RESULTS:")
    print("-" * 40)
    for _, repo in our_results.iterrows():
        print(f"{repo['Repository']}:")
        print(f"  Overall Score: {repo['Overall_Score_Mean']:.3f}")
        print(f"  Content Similarity: {repo['Content_Similarity_Mean']:.3f}")
        print(f"  Consistency: {repo['Consistency_Score']:.3f}")
        print()
    
    # Test evaluate.py method on a few files
    print("\n🧪 TESTING EVALUATE.PY METHOD:")
    print("-" * 40)
    
    # Find some test files
    gt_dir = Path("./your_data/ground_truth")
    extracted_dir = Path("./your_data/extracted_files/parsr")  # Use parsr as example
    
    if gt_dir.exists() and extracted_dir.exists():
        gt_files = list(gt_dir.glob("*.md"))
        ex_files = list(extracted_dir.glob("*.md"))
        
        if gt_files and ex_files:
            # Test first few files
            test_files = list(zip(ex_files[:3], gt_files[:3]))
            
            evaluate_py_scores = []
            our_scores = []
            
            for ex_file, gt_file in test_files:
                print(f"\nTesting: {ex_file.name}")
                
                try:
                    # evaluate.py method
                    f1, prec, recall, acc = evaluate_py_method(str(ex_file), str(gt_file))
                    evaluate_py_scores.append({'f1': f1, 'prec': prec, 'recall': recall, 'acc': acc})
                    print(f"  evaluate.py - F1: {f1:.3f}, Prec: {prec:.3f}, Recall: {recall:.3f}, Acc: {acc:.3f}")
                    
                    # Our method
                    our_result = our_levenshtein_method(str(ex_file), str(gt_file))
                    our_scores.append(our_result)
                    print(f"  Our method - Word Sim: {our_result['word_similarity']:.3f}, Overall: {our_result['overall_score']:.3f}")
                    
                except Exception as e:
                    print(f"  Error: {e}")
            
            # Compare averages
            if evaluate_py_scores and our_scores:
                print(f"\n📈 COMPARISON SUMMARY:")
                print("-" * 40)
                
                avg_evaluate_py = {
                    'f1': mean([s['f1'] for s in evaluate_py_scores]),
                    'prec': mean([s['prec'] for s in evaluate_py_scores]),
                    'recall': mean([s['recall'] for s in evaluate_py_scores]),
                    'acc': mean([s['acc'] for s in evaluate_py_scores])
                }
                
                avg_our = {
                    'word_similarity': mean([s['word_similarity'] for s in our_scores]),
                    'character_similarity': mean([s['character_similarity'] for s in our_scores]),
                    'overall_score': mean([s['overall_score'] for s in our_scores])
                }
                
                print(f"evaluate.py averages:")
                print(f"  F1: {avg_evaluate_py['f1']:.3f}")
                print(f"  Precision: {avg_evaluate_py['prec']:.3f}")
                print(f"  Recall: {avg_evaluate_py['recall']:.3f}")
                print(f"  Accuracy: {avg_evaluate_py['acc']:.3f}")
                
                print(f"\nOur method averages:")
                print(f"  Word Similarity: {avg_our['word_similarity']:.3f}")
                print(f"  Character Similarity: {avg_our['character_similarity']:.3f}")
                print(f"  Overall Score: {avg_our['overall_score']:.3f}")
                
                print(f"\n🎯 ANALYSIS:")
                print("-" * 40)
                print(f"• evaluate.py focuses on word-level precision/recall with 0.7 threshold")
                print(f"• Our method provides multi-level similarity scores")
                print(f"• evaluate.py is more strict (threshold-based)")
                print(f"• Our method is more comprehensive (multiple metrics)")
                
                # Determine which is "better"
                print(f"\n🏆 WHICH IS BETTER?")
                print("-" * 40)
                print(f"• For precision-focused tasks: evaluate.py (more strict)")
                print(f"• For comprehensive analysis: Our method (more metrics)")
                print(f"• For Vietnamese text: evaluate.py (uses underthesea)")
                print(f"• For multi-level analysis: Our method (char/word/sentence)")
                
        else:
            print("No test files found")
    else:
        print("Test directories not found")

if __name__ == "__main__":
    compare_methods()
