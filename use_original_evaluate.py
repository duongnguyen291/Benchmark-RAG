#!/usr/bin/env python3
"""
Use original evaluate.py code directly
"""

import os
import sys
import pandas as pd
import numpy as np
import json
from pathlib import Path
import matplotlib.pyplot as plt
from statistics import mean
import re

# Add the vi-ragflow-benchmark directory to path to import evaluate.py
sys.path.append('vi-ragflow-benchmark')

# Import the original evaluate.py functions
from evaluate import extract_txt, compute_sim_matrix, compute_tpfp, compute_scores, eval

def simple_word_tokenize(text):
    """Simple word tokenization to replace underthesea.word_tokenize"""
    # Remove special characters and split by whitespace
    text = re.sub(r'[^\w\s]', ' ', text)
    words = text.split()
    return [word.lower() for word in words if word.strip()]

# Monkey patch the word_tokenize function in evaluate module
import evaluate
evaluate.word_tokenize = simple_word_tokenize

def run_benchmark():
    """Run benchmark using original evaluate.py code"""
    print("🚀 Running Original evaluate.py Benchmark")
    print("=" * 60)
    
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
    
    # Process each repository
    for repo_folder in repo_folders:
        repo_name = repo_folder.name
        print(f"\n📁 Processing repository: {repo_name}")
        
        repo_results = []
        
        # Process each ground truth file
        for gt_file in gt_files:
            file_name = gt_file.stem
            extracted_file = repo_folder / f"{file_name}.md"
            
            if not extracted_file.exists():
                print(f"  ⚠️  Warning: No extracted file found for {file_name}")
                continue
            
            try:
                # Use the original eval function from evaluate.py
                f1_score, prec, recall, acc = eval(str(extracted_file), str(gt_file))
                
                result = {
                    'filename': file_name,
                    'Precision': prec,
                    'Recall': recall,
                    'F1': f1_score,
                    'Accuracy': acc
                }
                repo_results.append(result)
                print(f"    ✅ {file_name}: F1={f1_score:.3f}, P={prec:.3f}, R={recall:.3f}, A={acc:.3f}")
                
            except Exception as e:
                print(f"  ❌ Error evaluating {file_name}: {e}")
                continue
        
        all_results[repo_name] = repo_results
        print(f"  ✅ Evaluated {len(repo_results)} files for {repo_name}")
    
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
        
        summary_data.append({
            'Repository': repo_name,
            'Files_Evaluated': len(results),
            'Avg_Precision': avg_precision,
            'Avg_Recall': avg_recall,
            'Avg_F1': avg_f1,
            'Avg_Accuracy': avg_accuracy
        })
        
        print(f"\n{repo_name}:")
        print(f"  Files evaluated: {len(results)}")
        print(f"  Average Precision: {avg_precision:.3f}")
        print(f"  Average Recall: {avg_recall:.3f}")
        print(f"  Average F1: {avg_f1:.3f}")
        print(f"  Average Accuracy: {avg_accuracy:.3f}")
    
    # Create summary DataFrame
    summary_df = pd.DataFrame(summary_data)
    
    # Save results
    output_dir = Path("original_evaluate_results")
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
        plt.title('Original evaluate.py Benchmark Results - Performance Comparison')
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
        plt.title('Original evaluate.py Benchmark - F1 Score Ranking')
        plt.ylim(0, 1.1)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_dir / "f1_score_ranking.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print("  ✅ Visualizations generated successfully")
        
    except Exception as e:
        print(f"  ⚠️  Warning: Could not generate visualizations: {e}")
    
    # Generate final report
    print(f"\n📋 FINAL REPORT")
    print("=" * 60)
    
    if not summary_df.empty:
        best_f1 = summary_df.loc[summary_df['Avg_F1'].idxmax()]
        best_precision = summary_df.loc[summary_df['Avg_Precision'].idxmax()]
        best_recall = summary_df.loc[summary_df['Avg_Recall'].idxmax()]
        best_accuracy = summary_df.loc[summary_df['Avg_Accuracy'].idxmax()]
        
        print(f"🏆 BEST PERFORMERS:")
        print(f"  • Best F1 Score: {best_f1['Repository']} ({best_f1['Avg_F1']:.3f})")
        print(f"  • Best Precision: {best_precision['Repository']} ({best_precision['Avg_Precision']:.3f})")
        print(f"  • Best Recall: {best_recall['Repository']} ({best_recall['Avg_Recall']:.3f})")
        print(f"  • Best Accuracy: {best_accuracy['Repository']} ({best_accuracy['Avg_Accuracy']:.3f})")
        
        print(f"\n📊 OVERALL RANKING (by F1 Score):")
        summary_df_sorted = summary_df.sort_values('Avg_F1', ascending=False)
        for i, (_, repo) in enumerate(summary_df_sorted.iterrows(), 1):
            print(f"  {i}. {repo['Repository']:<15} - F1: {repo['Avg_F1']:.3f}, Files: {repo['Files_Evaluated']}")
    
    print(f"\n📁 Results saved to: {output_dir}")
    print(f"  • Summary: summary_results.csv")
    print(f"  • Detailed: {repo_name}_detailed_results.csv")
    print(f"  • All results: all_results.json")
    print(f"  • Visualizations: performance_comparison.png, f1_score_ranking.png")
    
    return summary_df

if __name__ == "__main__":
    try:
        results = run_benchmark()
        print(f"\n✅ Benchmark completed successfully!")
    except Exception as e:
        print(f"\n❌ Benchmark failed: {e}")
        import traceback
        traceback.print_exc()
