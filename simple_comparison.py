#!/usr/bin/env python3
"""
Simple comparison between our Levenshtein method and evaluate.py approach
"""

import pandas as pd
from pathlib import Path

def analyze_results():
    """Analyze and compare the evaluation results"""
    print("🔍 COMPARING EVALUATION METHODS")
    print("=" * 60)
    
    # Load our results
    our_results = pd.read_csv('evaluation_results_levenshtein/comprehensive_statistics.csv')
    
    print("\n📊 OUR LEVENSHTEIN METHOD RESULTS:")
    print("-" * 50)
    print(f"{'Repository':<15} {'Overall':<8} {'Content':<8} {'Structure':<10} {'Table':<8} {'Format':<8} {'Consistency':<10}")
    print("-" * 80)
    
    for _, repo in our_results.iterrows():
        print(f"{repo['Repository']:<15} {repo['Overall_Score_Mean']:<8.3f} {repo['Content_Similarity_Mean']:<8.3f} "
              f"{repo['Structure_Accuracy_Mean']:<10.3f} {repo['Table_Quality_Mean']:<8.3f} "
              f"{repo['Formatting_Preservation_Mean']:<8.3f} {repo['Consistency_Score']:<10.3f}")
    
    print(f"\n🎯 KEY FINDINGS:")
    print("-" * 50)
    
    # Find best performers
    best_overall = our_results.loc[our_results['Overall_Score_Mean'].idxmax()]
    best_content = our_results.loc[our_results['Content_Similarity_Mean'].idxmax()]
    best_structure = our_results.loc[our_results['Structure_Accuracy_Mean'].idxmax()]
    most_consistent = our_results.loc[our_results['Consistency_Score'].idxmax()]
    
    print(f"• Best Overall: {best_overall['Repository']} (Score: {best_overall['Overall_Score_Mean']:.3f})")
    print(f"• Best Content: {best_content['Repository']} (Score: {best_content['Content_Similarity_Mean']:.3f})")
    print(f"• Best Structure: {best_structure['Repository']} (Score: {best_structure['Structure_Accuracy_Mean']:.3f})")
    print(f"• Most Consistent: {most_consistent['Repository']} (Score: {most_consistent['Consistency_Score']:.3f})")
    
    print(f"\n📈 METHOD COMPARISON:")
    print("-" * 50)
    
    print(f"OUR LEVENSHTEIN METHOD:")
    print(f"✅ Pros:")
    print(f"  • Multi-level analysis (character, word, sentence)")
    print(f"  • Comprehensive metrics (17+ different scores)")
    print(f"  • No fixed threshold - dynamic similarity calculation")
    print(f"  • Detailed structure and formatting analysis")
    print(f"  • Consistency scoring")
    print(f"  • Rich visualizations and reports")
    
    print(f"❌ Cons:")
    print(f"  • Slower computation (more metrics)")
    print(f"  • Complex scoring system")
    print(f"  • May be overkill for simple tasks")
    
    print(f"\nEVALUATE.PY METHOD:")
    print(f"✅ Pros:")
    print(f"  • Fast and efficient")
    print(f"  • Simple threshold-based approach (0.7)")
    print(f"  • Standard Precision/Recall/F1 metrics")
    print(f"  • Uses underthesea for Vietnamese tokenization")
    print(f"  • Easy to understand and implement")
    
    print(f"❌ Cons:")
    print(f"  • Only word-level analysis")
    print(f"  • Fixed threshold may not work for all cases")
    print(f"  • Limited metrics (only 4 scores)")
    print(f"  • No structure or formatting analysis")
    
    print(f"\n🏆 WHICH IS BETTER?")
    print("-" * 50)
    
    print(f"CHOOSE EVALUATE.PY IF:")
    print(f"  • You need fast evaluation")
    print(f"  • You only care about word-level accuracy")
    print(f"  • You're working with Vietnamese text")
    print(f"  • You want simple Precision/Recall/F1 metrics")
    print(f"  • You have a large dataset to process quickly")
    
    print(f"\nCHOOSE OUR METHOD IF:")
    print(f"  • You need comprehensive analysis")
    print(f"  • You want multi-level similarity scores")
    print(f"  • You care about structure and formatting")
    print(f"  • You need detailed reports and visualizations")
    print(f"  • You want to understand where systems fail")
    print(f"  • You're doing research or detailed benchmarking")
    
    print(f"\n📊 PERFORMANCE RANKING (Our Method):")
    print("-" * 50)
    sorted_results = our_results.sort_values('Overall_Score_Mean', ascending=False)
    for i, (_, repo) in enumerate(sorted_results.iterrows(), 1):
        print(f"{i}. {repo['Repository']:<15} - {repo['Overall_Score_Mean']:.3f} (Consistency: {repo['Consistency_Score']:.3f})")
    
    print(f"\n💡 RECOMMENDATION:")
    print("-" * 50)
    print(f"• For production use: evaluate.py (faster, simpler)")
    print(f"• For research/analysis: Our method (comprehensive)")
    print(f"• For Vietnamese documents: evaluate.py (better tokenization)")
    print(f"• For detailed benchmarking: Our method (more insights)")

if __name__ == "__main__":
    analyze_results()
