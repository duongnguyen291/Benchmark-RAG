#!/usr/bin/env python3
"""
Optimized Simple evaluate.py benchmark with performance improvements
"""

import os
import pandas as pd
import numpy as np
import json
from pathlib import Path
import matplotlib.pyplot as plt
from statistics import mean
import re
from difflib import SequenceMatcher
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache

def simple_word_tokenize(text):
    """Simple word tokenization without external dependencies"""
    # Remove special characters and split by whitespace
    text = re.sub(r'[^\w\s]', ' ', text)
    words = text.split()
    return [word.lower() for word in words if word.strip()]

def extract_txt(txt_path):
    """Extract text from file"""
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = ' '.join(line.strip() for line in f)
    return text

@lru_cache(maxsize=10000)
def fast_similarity(str1, str2):
    """Fast similarity using SequenceMatcher (much faster than Levenshtein)"""
    if str1 == str2:
        return 1.0
    if not str1 or not str2:
        return 0.0
    return SequenceMatcher(None, str1, str2).ratio()

def compute_sim_matrix_optimized(ex_tokens, gt_tokens, threshold=0.7):
    """Optimized similarity matrix computation with early termination"""
    matrix = np.zeros((len(ex_tokens), len(gt_tokens)))
    
    # Use vectorized operations where possible
    for i, ex_token in enumerate(ex_tokens):
        for j, gt_token in enumerate(gt_tokens):
            # Early termination if tokens are identical
            if ex_token == gt_token:
                matrix[i, j] = 1.0
            else:
                # Only compute similarity if tokens are reasonably similar in length
                len_diff = abs(len(ex_token) - len(gt_token))
                max_len = max(len(ex_token), len(gt_token))
                if max_len > 0 and len_diff / max_len < 0.5:  # Only compare if length difference is reasonable
                    matrix[i, j] = fast_similarity(ex_token, gt_token)
    
    return matrix

def compute_tpfp_optimized(matrix):
    """Optimized True Positive and False Positive computation"""
    tp = 0
    fp = 0
    rows, cols = matrix.shape
    
    # Use numpy operations for better performance
    for x in range(1, rows):  # Skip first row (document level)
        if np.any(matrix[x, 1:] > 0.7):  # Use numpy's any() for faster checking
            tp += 1
        else:
            fp += 1
    return tp, fp

def compute_scores(tp, fp, gt_tokens):
    """Compute Precision, Recall, F1"""
    if tp + fp == 0:
        prec = 0.0
    else:
        prec = min(tp / (tp + fp), 1.0)
    
    if len(gt_tokens) == 0:
        recall = 0.0
    else:
        recall = min(tp / len(gt_tokens), 1.0)
    
    if prec == 0 and recall == 0:
        f1_score = 0.0
    else:
        f1_score = (2 * prec * recall) / (prec + recall)
    
    return f1_score, prec, recall

def eval_optimized(ex_path, gt_path):
    """Optimized evaluation using faster similarity measures"""
    ex = extract_txt(ex_path)
    gt = extract_txt(gt_path)

    gt_tokens = simple_word_tokenize(gt)
    ex_tokens = simple_word_tokenize(ex)
    
    # Limit token count to prevent excessive computation
    max_tokens = 1000  # Limit to prevent memory issues
    if len(gt_tokens) > max_tokens:
        gt_tokens = gt_tokens[:max_tokens]
    if len(ex_tokens) > max_tokens:
        ex_tokens = ex_tokens[:max_tokens]
    
    # Add document-level comparison
    gt_tokens = [gt] + gt_tokens
    ex_tokens = [ex] + ex_tokens
    
    matrix = compute_sim_matrix_optimized(ex_tokens, gt_tokens)
    tp, fp = compute_tpfp_optimized(matrix)
    f1_score, prec, recall = compute_scores(tp, fp, gt_tokens[1:])  # Exclude document level
    acc = float(matrix[0, 0])  # Document-level accuracy

    return f1_score, prec, recall, acc

def process_single_file(args):
    """Process a single file for parallel execution"""
    repo_folder, gt_file, repo_name = args
    file_name = gt_file.stem
    extracted_file = repo_folder / f"{file_name}.md"
    
    if not extracted_file.exists():
        return repo_name, file_name, None, "No extracted file found"
    
    try:
        start_time = time.time()
        f1_score, prec, recall, acc = eval_optimized(str(extracted_file), str(gt_file))
        processing_time = time.time() - start_time
        
        result = {
            'filename': file_name,
            'Precision': prec,
            'Recall': recall,
            'F1': f1_score,
            'Accuracy': acc,
            'processing_time': processing_time
        }
        return repo_name, file_name, result, None
        
    except Exception as e:
        return repo_name, file_name, None, str(e)

def run_benchmark_optimized():
    """Run optimized benchmark on all repositories"""
    print("🚀 Running Optimized Simple evaluate.py Benchmark")
    print("=" * 60)
    
    start_time = time.time()
    
    # Setup directories
    gt_dir = Path("your_data/ground_truth")
    extracted_dir = Path("your_data/extracted_files")
    
    # Get ground truth files
    gt_files = list(gt_dir.glob("*.md"))
    print(f"Found {len(gt_files)} ground truth files")
    
    # Get repository folders
    repo_folders = [f for f in extracted_dir.iterdir() if f.is_dir()]
    print(f"Found {len(repo_folders)} repositories: {[f.name for f in repo_folders]}")
    
    # Results storage
    all_results = {}
    
    # Prepare tasks for parallel processing
    tasks = []
    for repo_folder in repo_folders:
        repo_name = repo_folder.name
        for gt_file in gt_files:
            tasks.append((repo_folder, gt_file, repo_name))
    
    print(f"\n🔄 Processing {len(tasks)} file evaluations...")
    
    # Process files in parallel
    max_workers = min(8, len(tasks))  # Limit to 8 workers to prevent memory issues
    print(f"Using {max_workers} parallel workers")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_task = {executor.submit(process_single_file, task): task for task in tasks}
        
        # Process completed tasks
        completed_count = 0
        for future in as_completed(future_to_task):
            repo_name, file_name, result, error = future.result()
            completed_count += 1
            
            if completed_count % 10 == 0:  # Progress update every 10 files
                print(f"  Progress: {completed_count}/{len(tasks)} files processed")
            
            if error:
                print(f"  ❌ Error evaluating {file_name} in {repo_name}: {error}")
                continue
            
            if result:
                if repo_name not in all_results:
                    all_results[repo_name] = []
                all_results[repo_name].append(result)
                
                # Print result with processing time
                processing_time = result.get('processing_time', 0)
                print(f"    ✅ {file_name}: F1={result['F1']:.3f}, P={result['Precision']:.3f}, R={result['Recall']:.3f}, A={result['Accuracy']:.3f} ({processing_time:.2f}s)")
    
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
        avg_processing_time = mean([r.get('processing_time', 0) for r in results])
        
        summary_data.append({
            'Repository': repo_name,
            'Files_Evaluated': len(results),
            'Avg_Precision': avg_precision,
            'Avg_Recall': avg_recall,
            'Avg_F1': avg_f1,
            'Avg_Accuracy': avg_accuracy,
            'Avg_Processing_Time': avg_processing_time
        })
        
        print(f"\n{repo_name}:")
        print(f"  Files evaluated: {len(results)}")
        print(f"  Average Precision: {avg_precision:.3f}")
        print(f"  Average Recall: {avg_recall:.3f}")
        print(f"  Average F1: {avg_f1:.3f}")
        print(f"  Average Accuracy: {avg_accuracy:.3f}")
        print(f"  Average Processing Time: {avg_processing_time:.2f}s")
    
    # Create summary DataFrame
    summary_df = pd.DataFrame(summary_data)
    
    # Save results
    output_dir = Path("simple_evaluate_results_optimized")
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
        plt.title('Optimized Simple evaluate.py Benchmark Results - Performance Comparison')
        plt.xticks(x, summary_df_sorted['Repository'], rotation=45)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_dir / "performance_comparison.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. F1 Score Ranking
        plt.figure(figsize=(10, 6))
        bars = plt.bar(summary_df_sorted['Repository'], summary_df_sorted['Avg_F1'], 
                       color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'])
        
        # Add value labels on bars
        for bar, score in zip(bars, summary_df_sorted['Avg_F1']):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                    f'{score:.3f}', ha='center', va='bottom', fontweight='bold')
        
        plt.xlabel('Repository')
        plt.ylabel('Average F1 Score')
        plt.title('Optimized Simple evaluate.py Benchmark - F1 Score Ranking')
        plt.ylim(0, 1.1)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_dir / "f1_score_ranking.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Processing Time Comparison
        plt.figure(figsize=(10, 6))
        bars = plt.bar(summary_df_sorted['Repository'], summary_df_sorted['Avg_Processing_Time'], 
                       color=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC', '#99CCFF'])
        
        # Add value labels on bars
        for bar, time_val in zip(bars, summary_df_sorted['Avg_Processing_Time']):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                    f'{time_val:.2f}s', ha='center', va='bottom', fontweight='bold')
        
        plt.xlabel('Repository')
        plt.ylabel('Average Processing Time (seconds)')
        plt.title('Optimized Simple evaluate.py Benchmark - Processing Time Comparison')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_dir / "processing_time_comparison.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print("  ✅ Visualizations generated successfully")
        
    except Exception as e:
        print(f"  ⚠️  Warning: Could not generate visualizations: {e}")
    
    # Generate final report
    print(f"\n📋 FINAL REPORT")
    print("=" * 60)
    
    total_time = time.time() - start_time
    
    if not summary_df.empty:
        best_f1 = summary_df.loc[summary_df['Avg_F1'].idxmax()]
        best_precision = summary_df.loc[summary_df['Avg_Precision'].idxmax()]
        best_recall = summary_df.loc[summary_df['Avg_Recall'].idxmax()]
        best_accuracy = summary_df.loc[summary_df['Avg_Accuracy'].idxmax()]
        fastest_processing = summary_df.loc[summary_df['Avg_Processing_Time'].idxmin()]
        
        print(f"🏆 BEST PERFORMERS:")
        print(f"  • Best F1 Score: {best_f1['Repository']} ({best_f1['Avg_F1']:.3f})")
        print(f"  • Best Precision: {best_precision['Repository']} ({best_precision['Avg_Precision']:.3f})")
        print(f"  • Best Recall: {best_recall['Repository']} ({best_recall['Avg_Recall']:.3f})")
        print(f"  • Best Accuracy: {best_accuracy['Repository']} ({best_accuracy['Avg_Accuracy']:.3f})")
        print(f"  • Fastest Processing: {fastest_processing['Repository']} ({fastest_processing['Avg_Processing_Time']:.2f}s)")
        
        print(f"\n📊 OVERALL RANKING (by F1 Score):")
        summary_df_sorted = summary_df.sort_values('Avg_F1', ascending=False)
        for i, (_, repo) in enumerate(summary_df_sorted.iterrows(), 1):
            print(f"  {i}. {repo['Repository']:<15} - F1: {repo['Avg_F1']:.3f}, Files: {repo['Files_Evaluated']}, Time: {repo['Avg_Processing_Time']:.2f}s")
    
    print(f"\n⏱️  Total benchmark time: {total_time:.2f} seconds")
    print(f"📁 Results saved to: {output_dir}")
    print(f"  • Summary: summary_results.csv")
    print(f"  • Detailed: {repo_name}_detailed_results.csv")
    print(f"  • All results: all_results.json")
    print(f"  • Visualizations: performance_comparison.png, f1_score_ranking.png, processing_time_comparison.png")
    
    return summary_df

if __name__ == "__main__":
    try:
        results = run_benchmark_optimized()
        print(f"\n✅ Optimized benchmark completed successfully!")
    except Exception as e:
        print(f"\n❌ Benchmark failed: {e}")
        import traceback
        traceback.print_exc()
