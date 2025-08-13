#!/usr/bin/env python3
"""
Combine and average results from multiple benchmark runs (Fixed version)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import json
from statistics import mean
import seaborn as sns

def load_summary_results(folder_path):
    """Load summary results from a folder"""
    try:
        csv_path = Path(folder_path) / "summary_results.csv"
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            print(f"✅ Loaded {len(df)} results from {folder_path}")
            return df
        else:
            print(f"❌ No summary_results.csv found in {folder_path}")
            return None
    except Exception as e:
        print(f"❌ Error loading {folder_path}: {e}")
        return None

def combine_all_results():
    """Combine results from all benchmark runs"""
    print("🔄 Combining results from all benchmark runs...")
    
    # Define all result folders
    result_folders = [
        "direct_evaluate_results_optimized",
        "direct_evaluate_results_optimized_v1", 
        "direct_evaluate_results_optimized_v2",
        "simple_evaluate_results_optimized"
    ]
    
    # Load all results
    all_dfs = []
    for folder in result_folders:
        df = load_summary_results(folder)
        if df is not None:
            df['Run_Source'] = folder  # Add source identifier
            all_dfs.append(df)
    
    if not all_dfs:
        print("❌ No results found!")
        return None
    
    # Combine all dataframes
    combined_df = pd.concat(all_dfs, ignore_index=True)
    print(f"📊 Combined {len(combined_df)} total results")
    
    return combined_df

def calculate_average_results(combined_df):
    """Calculate average results across all runs"""
    print("📈 Calculating average results...")
    
    # Group by repository and calculate averages
    avg_results = combined_df.groupby('Repository').agg({
        'Files_Evaluated': 'mean',
        'Avg_Precision': 'mean',
        'Avg_Recall': 'mean', 
        'Avg_F1': 'mean',
        'Avg_Accuracy': 'mean',
        'Avg_Processing_Time': 'mean'
    }).round(3)
    
    # Add standard deviation for error analysis
    std_results = combined_df.groupby('Repository').agg({
        'Avg_Precision': 'std',
        'Avg_Recall': 'std',
        'Avg_F1': 'std',
        'Avg_Accuracy': 'std',
        'Avg_Processing_Time': 'std'
    }).round(3)
    
    # Add run count
    run_counts = combined_df.groupby('Repository').size()
    avg_results['Run_Count'] = run_counts
    
    print(f"📊 Calculated averages for {len(avg_results)} repositories")
    return avg_results, std_results

def create_combined_performance_chart(avg_results, std_results):
    """Create combined performance comparison chart"""
    print("📊 Creating combined performance chart...")
    
    # Sort by F1 score
    avg_results_sorted = avg_results.sort_values('Avg_F1', ascending=False)
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))
    
    # Set color palette
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
    
    # Plot 1: Performance Metrics
    x = range(len(avg_results_sorted))
    width = 0.2
    
    # Get standard deviations for error bars
    precision_std = []
    recall_std = []
    f1_std = []
    accuracy_std = []
    
    for repo in avg_results_sorted.index:
        precision_std.append(std_results.loc[repo, 'Avg_Precision'] if repo in std_results.index else 0)
        recall_std.append(std_results.loc[repo, 'Avg_Recall'] if repo in std_results.index else 0)
        f1_std.append(std_results.loc[repo, 'Avg_F1'] if repo in std_results.index else 0)
        accuracy_std.append(std_results.loc[repo, 'Avg_Accuracy'] if repo in std_results.index else 0)
    
    # Plot bars with error bars
    bars1 = ax1.bar([i - width*1.5 for i in x], avg_results_sorted['Avg_Precision'], 
                    width, label='Precision', alpha=0.8, color=colors[0],
                    yerr=precision_std, capsize=5)
    bars2 = ax1.bar([i - width*0.5 for i in x], avg_results_sorted['Avg_Recall'], 
                    width, label='Recall', alpha=0.8, color=colors[1],
                    yerr=recall_std, capsize=5)
    bars3 = ax1.bar([i + width*0.5 for i in x], avg_results_sorted['Avg_F1'], 
                    width, label='F1 Score', alpha=0.8, color=colors[2],
                    yerr=f1_std, capsize=5)
    bars4 = ax1.bar([i + width*1.5 for i in x], avg_results_sorted['Avg_Accuracy'], 
                    width, label='Accuracy', alpha=0.8, color=colors[3],
                    yerr=accuracy_std, capsize=5)
    
    ax1.set_xlabel('Repositories')
    ax1.set_ylabel('Score')
    ax1.set_title('Combined Benchmark Results - Performance Comparison (Averaged)', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(avg_results_sorted.index, rotation=45)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1.1)
    
    # Add value labels on bars
    for bars in [bars1, bars2, bars3, bars4]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{height:.3f}', ha='center', va='bottom', fontsize=8)
    
    # Plot 2: Processing Time
    time_std = []
    for repo in avg_results_sorted.index:
        time_std.append(std_results.loc[repo, 'Avg_Processing_Time'] if repo in std_results.index else 0)
    
    bars5 = ax2.bar(avg_results_sorted.index, avg_results_sorted['Avg_Processing_Time'], 
                    color=colors[4], alpha=0.8, yerr=time_std, capsize=5)
    
    ax2.set_xlabel('Repository')
    ax2.set_ylabel('Average Processing Time (seconds)')
    ax2.set_title('Combined Benchmark Results - Processing Time Comparison (Averaged)', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Add value labels on time bars
    for bar in bars5:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                f'{height:.3f}s', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    # Save the combined chart
    output_path = "performance_comparison_combined.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Combined chart saved as: {output_path}")
    return output_path

def create_statistics_table(avg_results, std_results):
    """Create detailed statistics table"""
    print("📋 Creating statistics table...")
    
    # Create detailed statistics
    stats_data = []
    for repo in avg_results.index:
        precision_str = f"{avg_results.loc[repo, 'Avg_Precision']:.3f}"
        recall_str = f"{avg_results.loc[repo, 'Avg_Recall']:.3f}"
        f1_str = f"{avg_results.loc[repo, 'Avg_F1']:.3f}"
        accuracy_str = f"{avg_results.loc[repo, 'Avg_Accuracy']:.3f}"
        time_str = f"{avg_results.loc[repo, 'Avg_Processing_Time']:.3f}s"
        
        # Add standard deviation if available
        if repo in std_results.index:
            precision_str += f" ± {std_results.loc[repo, 'Avg_Precision']:.3f}"
            recall_str += f" ± {std_results.loc[repo, 'Avg_Recall']:.3f}"
            f1_str += f" ± {std_results.loc[repo, 'Avg_F1']:.3f}"
            accuracy_str += f" ± {std_results.loc[repo, 'Avg_Accuracy']:.3f}"
            time_str += f" ± {std_results.loc[repo, 'Avg_Processing_Time']:.3f}s"
        
        stats_data.append({
            'Repository': repo,
            'Run_Count': int(avg_results.loc[repo, 'Run_Count']),
            'Files_Evaluated': avg_results.loc[repo, 'Files_Evaluated'],
            'Avg_Precision': precision_str,
            'Avg_Recall': recall_str,
            'Avg_F1': f1_str,
            'Avg_Accuracy': accuracy_str,
            'Avg_Processing_Time': time_str
        })
    
    stats_df = pd.DataFrame(stats_data)
    stats_df = stats_df.sort_values('Avg_F1', ascending=False)
    
    # Save statistics
    stats_df.to_csv("combined_statistics.csv", index=False)
    print("✅ Statistics table saved as: combined_statistics.csv")
    
    return stats_df

def generate_final_report(avg_results, std_results):
    """Generate final comprehensive report"""
    print("📋 Generating final report...")
    
    # Find best performers
    best_f1_idx = avg_results['Avg_F1'].idxmax()
    best_precision_idx = avg_results['Avg_Precision'].idxmax()
    best_recall_idx = avg_results['Avg_Recall'].idxmax()
    best_accuracy_idx = avg_results['Avg_Accuracy'].idxmax()
    fastest_idx = avg_results['Avg_Processing_Time'].idxmin()
    
    report = f"""
# COMBINED BENCHMARK RESULTS REPORT
{'='*60}

## 🏆 BEST PERFORMERS (Averaged across all runs):

• **Best F1 Score:** {best_f1_idx} ({avg_results.loc[best_f1_idx, 'Avg_F1']:.3f})
• **Best Precision:** {best_precision_idx} ({avg_results.loc[best_precision_idx, 'Avg_Precision']:.3f})
• **Best Recall:** {best_recall_idx} ({avg_results.loc[best_recall_idx, 'Avg_Recall']:.3f})
• **Best Accuracy:** {best_accuracy_idx} ({avg_results.loc[best_accuracy_idx, 'Avg_Accuracy']:.3f})
• **Fastest Processing:** {fastest_idx} ({avg_results.loc[fastest_idx, 'Avg_Processing_Time']:.3f}s)

## 📊 OVERALL RANKING (by F1 Score):

"""
    
    # Sort by F1 score
    avg_results_sorted = avg_results.sort_values('Avg_F1', ascending=False)
    for i, (repo, data) in enumerate(avg_results_sorted.iterrows(), 1):
        f1_std = std_results.loc[repo, 'Avg_F1'] if repo in std_results.index else 0
        report += f"{i}. **{repo}** - F1: {data['Avg_F1']:.3f} ± {f1_std:.3f}, Files: {data['Files_Evaluated']:.1f}, Runs: {int(data['Run_Count'])}\n"
    
    report += f"""
## 📈 STATISTICAL SUMMARY:

• **Total repositories evaluated:** {len(avg_results)}
• **Average runs per repository:** {avg_results['Run_Count'].mean():.1f}
• **Most consistent performer:** {avg_results['Run_Count'].idxmax()} ({int(avg_results['Run_Count'].max())} runs)

## 📁 OUTPUT FILES:

• **Combined Chart:** performance_comparison_combined.png
• **Statistics Table:** combined_statistics.csv
• **This Report:** combined_report.md

{'='*60}
"""
    
    # Save report
    with open("combined_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("✅ Final report saved as: combined_report.md")
    return report

def main():
    """Main function to combine all results"""
    print("🚀 COMBINING BENCHMARK RESULTS")
    print("=" * 60)
    
    # Step 1: Load and combine all results
    combined_df = combine_all_results()
    if combined_df is None:
        return
    
    # Step 2: Calculate averages
    avg_results, std_results = calculate_average_results(combined_df)
    
    # Step 3: Create combined performance chart
    chart_path = create_combined_performance_chart(avg_results, std_results)
    
    # Step 4: Create statistics table
    stats_df = create_statistics_table(avg_results, std_results)
    
    # Step 5: Generate final report
    report = generate_final_report(avg_results, std_results)
    
    # Print summary
    print(f"\n📊 FINAL SUMMARY")
    print("=" * 60)
    print(f"✅ Combined {len(combined_df)} results from {combined_df['Run_Source'].nunique()} sources")
    print(f"✅ Averaged results for {len(avg_results)} repositories")
    print(f"✅ Generated combined chart: {chart_path}")
    print(f"✅ Created statistics table: combined_statistics.csv")
    print(f"✅ Generated report: combined_report.md")
    
    # Print top performers
    print(f"\n🏆 TOP 3 PERFORMERS (by F1 Score):")
    avg_results_sorted = avg_results.sort_values('Avg_F1', ascending=False)
    for i, (repo, data) in enumerate(avg_results_sorted.head(3).iterrows(), 1):
        print(f"  {i}. {repo}: F1={data['Avg_F1']:.3f}, Precision={data['Avg_Precision']:.3f}, Recall={data['Avg_Recall']:.3f}")

if __name__ == "__main__":
    main()
