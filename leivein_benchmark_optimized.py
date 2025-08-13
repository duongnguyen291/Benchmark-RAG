#!/usr/bin/env python3
"""
Optimized version of direct_evaluate_benchmark.py for better performance
"""

import os
import pandas as pd
import numpy as np
import json
from pathlib import Path
import matplotlib.pyplot as plt
from statistics import mean
import re
from scipy.spatial.distance import cdist
import time
from functools import lru_cache
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed

# Optimized functions
def extract_txt(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = ' '.join(line.strip() for line in f)
    return text

def simple_word_tokenize(text):
    """Simple word tokenization to replace underthesea.word_tokenize"""
    # Remove special characters and split by whitespace
    text = re.sub(r'[^\w\s]', ' ', text)
    words = text.split()
    return [word.lower() for word in words if word.strip()]

@lru_cache(maxsize=10000)
def levenshtein_ratio_cached(str1, str2):
    """Cached version of Levenshtein ratio for repeated calculations"""
    return levenshtein_ratio(str1, str2)

def levenshtein_ratio(str1, str2):
    """Calculate Levenshtein similarity ratio (replacement for Levenshtein.ratio)"""
    if len(str1) < len(str2):
        return levenshtein_ratio(str2, str1)
    
    if len(str2) == 0:
        return 0.0
    
    # Early exit for exact matches
    if str1 == str2:
        return 1.0
    
    # Early exit for very different lengths
    if abs(len(str1) - len(str2)) > max(len(str1), len(str2)) * 0.5:
        return 0.0
    
    previous_row = list(range(len(str2) + 1))
    for i, c1 in enumerate(str1):
        current_row = [i + 1]
        for j, c2 in enumerate(str2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    distance = previous_row[-1]
    max_len = max(len(str1), len(str2))
    if max_len == 0:
        return 1.0
    return 1.0 - (distance / max_len)

def compute_sim_matrix_optimized(ex_tokens, gt_tokens):
    """
    Optimized similarity matrix computation with early termination
    """
    # Limit matrix size for very large documents
    max_tokens = 500  # Limit to prevent memory issues
    
    if len(ex_tokens) > max_tokens:
        ex_tokens = ex_tokens[:max_tokens]
    if len(gt_tokens) > max_tokens:
        gt_tokens = gt_tokens[:max_tokens]
    
    # Use numpy for faster computation
    ex_nump = np.array(ex_tokens)
    gt_nump = np.array(gt_tokens)
    
    # Use vectorized operations where possible
    matrix = cdist(ex_nump.reshape(-1, 1), gt_nump.reshape(-1, 1), 
                   lambda x, y: levenshtein_ratio_cached(x[0], y[0]))
    
    return pd.DataFrame(data=matrix, index=ex_tokens, columns=gt_tokens)

def compute_tpfp_optimized(matrix):
    """
    Optimized TP/FP computation using numpy operations
    """
    # Skip first row/column (document-level comparison)
    sub_matrix = matrix.iloc[1:, 1:].values
    
    # Vectorized operations
    max_similarities = np.max(sub_matrix, axis=1)
    tp = np.sum(max_similarities > 0.7)
    fp = len(max_similarities) - tp
    
    return int(tp), int(fp)

def compute_scores(tp, fp, gttoken):
    """
    Function to compute the evaluation metrics.
    """
    if tp + fp == 0:
        return 0, 0, 0
    
    prec = min(tp / (tp + fp), 1.0)
    recall = min(tp / gttoken, 1.0) if gttoken > 0 else 0
    
    if prec == 0 and recall == 0:
        return 0, 0, 0
    else:
        f1_score = (2 * prec * recall) / (prec + recall)
        return f1_score, prec, recall

def eval_optimized(ex_path, gt_path):
    """Optimized evaluation function"""
    ex = extract_txt(ex_path)
    gt = extract_txt(gt_path)

    gt_tokens = simple_word_tokenize(gt)
    ex_tokens = simple_word_tokenize(ex)
    num_gt_tokens = len(gt_tokens)
    
    # Add document-level comparison
    gt = [gt]
    ex = [ex]
    gt_tokens = gt + gt_tokens
    ex_tokens = ex + ex_tokens

    matrix = compute_sim_matrix_optimized(ex_tokens, gt_tokens)
    tp, fp = compute_tpfp_optimized(matrix)
    f1_score, prec, recall = compute_scores(tp, fp, num_gt_tokens)
    acc = float(matrix.iloc[0, 0])

    return f1_score, prec, recall, acc

def process_single_file(args):
    """Process a single file for parallel execution"""
    repo_name, gt_file, extracted_file = args
    
    if not extracted_file.exists():
        return repo_name, None, f"File not found: {extracted_file.name}"
    
    try:
        start_time = time.time()
        f1_score, prec, recall, acc = eval_optimized(str(extracted_file), str(gt_file))
        processing_time = time.time() - start_time
        
        result = {
            'filename': gt_file.stem,
            'Precision': prec,
            'Recall': recall,
            'F1': f1_score,
            'Accuracy': acc,
            'Processing_Time': processing_time
        }
        return repo_name, result, None
        
    except Exception as e:
        return repo_name, None, f"Error: {str(e)}"

def run_benchmark_optimized():
    """Run optimized benchmark"""
    print("🚀 Running Optimized Direct evaluate.py Benchmark")
    print("=" * 60)
    
    start_time = time.time()
    
    # Setup directories
    gt_dir = Path("your_data/ground_truth/v2")
    extracted_dir = Path("your_data/extracted_files")
    
    # Get ground truth files
    gt_files = list(gt_dir.glob("*.md"))
    print(f"Found {len(gt_files)} ground truth files")
    
    # Get repository folders
    repo_folders = [f for f in extracted_dir.iterdir() if f.is_dir()]
    print(f"Found {len(repo_folders)} repositories: {[f.name for f in repo_folders]}")
    
    # Prepare tasks for parallel processing
    tasks = []
    for repo_folder in repo_folders:
        repo_name = repo_folder.name
        for gt_file in gt_files:
            file_name = gt_file.stem
            extracted_file = repo_folder / f"{file_name}.md"
            tasks.append((repo_name, gt_file, extracted_file))
    
    print(f"Total tasks to process: {len(tasks)}")
    
    # Results storage
    all_results = {repo.name: [] for repo in repo_folders}
    errors = []
    
    # Process with multiprocessing
    max_workers = min(mp.cpu_count(), 8)  # Limit to prevent memory issues
    print(f"Using {max_workers} parallel workers")
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_task = {executor.submit(process_single_file, task): task for task in tasks}
        
        # Process completed tasks
        completed = 0
        for future in as_completed(future_to_task):
            repo_name, result, error = future.result()
            completed += 1
            
            if completed % 10 == 0:
                print(f"Progress: {completed}/{len(tasks)} tasks completed")
            
            if error:
                errors.append(error)
                print(f"  ⚠️  {error}")
            elif result:
                all_results[repo_name].append(result)
                print(f"    ✅ {result['filename']}: F1={result['F1']:.3f}, P={result['Precision']:.3f}, R={result['Recall']:.3f}, A={result['Accuracy']:.3f}")
    
    # Generate summary statistics
    print(f"\n📊 GENERATING SUMMARY STATISTICS")
    print("=" * 60)
    
    summary_data = []
    for repo_name, results in all_results.items():
        if not results:
            continue
        
        # Calculate averages
        avg_precision = mean([r['Precision'] for r in results])
        avg_recall = mean([r['Recall'] for r in results])
        avg_f1 = mean([r['F1'] for r in results])
        avg_accuracy = mean([r['Accuracy'] for r in results])
        avg_time = mean([r['Processing_Time'] for r in results])
        
        summary_data.append({
            'Repository': repo_name,
            'Files_Evaluated': len(results),
            'Avg_Precision': avg_precision,
            'Avg_Recall': avg_recall,
            'Avg_F1': avg_f1,
            'Avg_Accuracy': avg_accuracy,
            'Avg_Processing_Time': avg_time
        })
        
        print(f"\n{repo_name}:")
        print(f"  Files evaluated: {len(results)}")
        print(f"  Average Precision: {avg_precision:.3f}")
        print(f"  Average Recall: {avg_recall:.3f}")
        print(f"  Average F1: {avg_f1:.3f}")
        print(f"  Average Accuracy: {avg_accuracy:.3f}")
        print(f"  Average Processing Time: {avg_time:.3f}s")
    
    # Create summary DataFrame
    summary_df = pd.DataFrame(summary_data)
    
    # Save results
    output_dir = Path("direct_evaluate_results_optimized")
    output_dir.mkdir(exist_ok=True)
    
    # Save detailed results
    for repo_name, results in all_results.items():
        if results:
            repo_df = pd.DataFrame(results)
            repo_df.to_csv(output_dir / f"{repo_name}_detailed_results.csv", index=False)
    
    # Save summary
    summary_df.to_csv(output_dir / "summary_results.csv", index=False)
    
    # Save all results as JSON
    with open(output_dir / "all_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=4, default=str)
    
    # Generate visualizations
    print(f"\n📈 GENERATING VISUALIZATIONS")
    print("=" * 60)
    
    try:
        # 1. Overall Performance Comparison
        plt.figure(figsize=(12, 8))
        
        # Sort by F1 score
        summary_df_sorted = summary_df.sort_values('Avg_F1', ascending=False)
        
        x = range(len(summary_df_sorted))
        width = 0.2
        
        plt.bar([i - width*1.5 for i in x], summary_df_sorted['Avg_Precision'], width, label='Precision', alpha=0.8)
        plt.bar([i - width*0.5 for i in x], summary_df_sorted['Avg_Recall'], width, label='Recall', alpha=0.8)
        plt.bar([i + width*0.5 for i in x], summary_df_sorted['Avg_F1'], width, label='F1 Score', alpha=0.8)
        plt.bar([i + width*1.5 for i in x], summary_df_sorted['Avg_Accuracy'], width, label='Accuracy', alpha=0.8)
        
        plt.xlabel('Repositories')
        plt.ylabel('Score')
        plt.title('Optimized Direct evaluate.py Benchmark Results - Performance Comparison')
        plt.xticks(x, summary_df_sorted['Repository'], rotation=45)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_dir / "performance_comparison.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Processing Time Comparison
        plt.figure(figsize=(10, 6))
        bars = plt.bar(summary_df_sorted['Repository'], summary_df_sorted['Avg_Processing_Time'], 
                       color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'])
        
        # Add value labels on bars
        for bar, time_val in zip(bars, summary_df_sorted['Avg_Processing_Time']):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                    f'{time_val:.3f}s', ha='center', va='bottom', fontweight='bold')
        
        plt.xlabel('Repository')
        plt.ylabel('Average Processing Time (seconds)')
        plt.title('Optimized Direct evaluate.py Benchmark - Processing Time Comparison')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_dir / "processing_time_comparison.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print("  ✅ Visualizations generated successfully")
        
    except Exception as e:
        print(f"  ⚠️  Warning: Could not generate visualizations: {e}")
    
    # Generate final report
    total_time = time.time() - start_time
    print(f"\n📋 FINAL REPORT")
    print("=" * 60)
    
    if not summary_df.empty:
        best_f1 = summary_df.loc[summary_df['Avg_F1'].idxmax()]
        best_precision = summary_df.loc[summary_df['Avg_Precision'].idxmax()]
        best_recall = summary_df.loc[summary_df['Avg_Recall'].idxmax()]
        best_accuracy = summary_df.loc[summary_df['Avg_Accuracy'].idxmax()]
        fastest = summary_df.loc[summary_df['Avg_Processing_Time'].idxmin()]
        
        print(f"🏆 BEST PERFORMERS:")
        print(f"  • Best F1 Score: {best_f1['Repository']} ({best_f1['Avg_F1']:.3f})")
        print(f"  • Best Precision: {best_precision['Repository']} ({best_precision['Avg_Precision']:.3f})")
        print(f"  • Best Recall: {best_recall['Repository']} ({best_recall['Avg_Recall']:.3f})")
        print(f"  • Best Accuracy: {best_accuracy['Repository']} ({best_accuracy['Avg_Accuracy']:.3f})")
        print(f"  • Fastest Processing: {fastest['Repository']} ({fastest['Avg_Processing_Time']:.3f}s)")
        
        print(f"\n📊 OVERALL RANKING (by F1 Score):")
        summary_df_sorted = summary_df.sort_values('Avg_F1', ascending=False)
        for i, (_, repo) in enumerate(summary_df_sorted.iterrows(), 1):
            print(f"  {i}. {repo['Repository']:<15} - F1: {repo['Avg_F1']:.3f}, Files: {repo['Files_Evaluated']}, Time: {repo['Avg_Processing_Time']:.3f}s")
    
    print(f"\n⏱️  Total execution time: {total_time:.2f} seconds")
    print(f"📁 Results saved to: {output_dir}")
    print(f"  • Summary: summary_results.csv")
    print(f"  • Detailed: {repo_name}_detailed_results.csv")
    print(f"  • All results: all_results.json")
    print(f"  • Visualizations: performance_comparison.png, processing_time_comparison.png")
    
    return summary_df

if __name__ == "__main__":
    try:
        results = run_benchmark_optimized()
        print(f"\n✅ Optimized benchmark completed successfully!")
    except Exception as e:
        print(f"\n❌ Optimized benchmark failed: {e}")
        import traceback
        traceback.print_exc()
