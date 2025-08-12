#!/usr/bin/env python3
"""
Run evaluate.py benchmark on our data structure
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
import matplotlib.pyplot as plt
from tqdm import tqdm

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

def eval(ex_path, gt_path):
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

def run_benchmark():
    """Run benchmark on all repositories"""
    print("🚀 Running evaluate.py Benchmark")
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
        for gt_file in tqdm(gt_files, desc=f"Evaluating {repo_name}"):
            file_name = gt_file.stem
            extracted_file = repo_folder / f"{file_name}.md"
            
            if not extracted_file.exists():
                print(f"  ⚠️  Warning: No extracted file found for {file_name}")
                continue
            
            try:
                # Evaluate using evaluate.py method
                f1_score, prec, recall, acc = eval(str(extracted_file), str(gt_file))
                
                result = {
                    'filename': file_name,
                    'Precision': prec,
                    'Recall': recall,
                    'F1': f1_score,
                    'Accuracy': acc
                }
                repo_results.append(result)
                
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
    output_dir = Path("evaluate_py_results")
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
    plt.title('evaluate.py Benchmark Results - Performance Comparison')
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
    plt.title('evaluate.py Benchmark - F1 Score Ranking')
    plt.ylim(0, 1.1)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "f1_score_ranking.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Metrics Heatmap
    plt.figure(figsize=(10, 6))
    
    # Prepare data for heatmap
    heatmap_data = summary_df_sorted[['Avg_Precision', 'Avg_Recall', 'Avg_F1', 'Avg_Accuracy']].T
    heatmap_data.columns = summary_df_sorted['Repository']
    
    import seaborn as sns
    sns.heatmap(heatmap_data, annot=True, fmt='.3f', cmap='YlOrRd', 
                cbar_kws={'label': 'Score'}, linewidths=0.5)
    plt.title('evaluate.py Benchmark - Metrics Heatmap')
    plt.tight_layout()
    plt.savefig(output_dir / "metrics_heatmap.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Generate final report
    print(f"\n📋 FINAL REPORT")
    print("=" * 60)
    
    best_f1 = summary_df_sorted.iloc[0]
    best_precision = summary_df.loc[summary_df['Avg_Precision'].idxmax()]
    best_recall = summary_df.loc[summary_df['Avg_Recall'].idxmax()]
    best_accuracy = summary_df.loc[summary_df['Avg_Accuracy'].idxmax()]
    
    print(f"🏆 BEST PERFORMERS:")
    print(f"  • Best F1 Score: {best_f1['Repository']} ({best_f1['Avg_F1']:.3f})")
    print(f"  • Best Precision: {best_precision['Repository']} ({best_precision['Avg_Precision']:.3f})")
    print(f"  • Best Recall: {best_recall['Repository']} ({best_recall['Avg_Recall']:.3f})")
    print(f"  • Best Accuracy: {best_accuracy['Repository']} ({best_accuracy['Avg_Accuracy']:.3f})")
    
    print(f"\n📊 OVERALL RANKING (by F1 Score):")
    for i, (_, repo) in enumerate(summary_df_sorted.iterrows(), 1):
        print(f"  {i}. {repo['Repository']:<15} - F1: {repo['Avg_F1']:.3f}, Files: {repo['Files_Evaluated']}")
    
    print(f"\n📁 Results saved to: {output_dir}")
    print(f"  • Summary: summary_results.csv")
    print(f"  • Detailed: {repo_name}_detailed_results.csv")
    print(f"  • All results: all_results.json")
    print(f"  • Visualizations: performance_comparison.png, f1_score_ranking.png, metrics_heatmap.png")
    
    return summary_df

if __name__ == "__main__":
    try:
        results = run_benchmark()
        print(f"\n✅ Benchmark completed successfully!")
    except Exception as e:
        print(f"\n❌ Benchmark failed: {e}")
        import traceback
        traceback.print_exc()
