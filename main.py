#!/usr/bin/env python3
"""
Main CLI interface for Document Extraction Benchmark.
Provides command-line interface for running benchmarks and managing results.
"""

import argparse
import sys
import logging
import json
from pathlib import Path
from typing import List, Dict, Any

from src.models import BenchmarkConfig, EvaluationResult, ExtractionResult, ProcessingTime
from src.benchmark_runner import BenchmarkRunner
from src.manual_evaluation import ManualEvaluationInterface
from src.evaluator import DocumentEvaluator
from src.report_generator import ReportGenerator
from src.config import config_manager

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def list_repositories():
    """List all available repositories."""
    repos = config_manager.get_repositories()
    print("\nAvailable repositories:")
    print("-" * 80)
    
    for repo_id, repo_config in repos.items():
        print(f"ID: {repo_id}")
        print(f"Name: {repo_config.name}")
        print(f"Description: {repo_config.description}")
        print(f"URL: {repo_config.repo_url}")
        print(f"Supported formats: {', '.join(repo_config.supported_formats)}")
        print("-" * 80)


def run_benchmark(args):
    """Run the benchmark with specified configuration."""
    print("🚀 Starting Document Extraction Benchmark...")
    
    # Create benchmark configuration
    config = BenchmarkConfig(
        test_files_dir=args.test_files_dir,
        output_dir=args.output_dir,
        repositories_to_test=args.repositories,
        enable_manual_evaluation=args.enable_manual_eval,
        save_intermediate_results=args.save_intermediate,
        parallel_processing=args.parallel,
        max_workers=args.max_workers
    )
    
    # Run benchmark
    try:
        runner = BenchmarkRunner(config)
        summary = runner.run_benchmark()
        
        # Print results
        print("\n" + "="*60)
        print("📊 BENCHMARK RESULTS")
        print("="*60)
        
        print(f"Total processing time: {summary.total_processing_time:.2f} seconds")
        print(f"Files tested: {len(summary.test_files)}")
        print(f"Repositories tested: {len(summary.repositories_tested)}")
        
        print("\nRepository Performance:")
        print("-" * 60)
        
        for repo_id, repo_result in summary.repository_results.items():
            print(f"\n{repo_result.repository_name} ({repo_id}):")
            print(f"  Success rate: {repo_result.success_rate:.2%}")
            print(f"  Average score: {repo_result.average_overall_score:.3f}")
            print(f"  Average processing time: {repo_result.average_processing_time:.2f}s")
            print(f"  Successful extractions: {repo_result.successful_extractions}/{repo_result.total_files}")
        
        # Show best performers
        best_repo = summary.get_best_repository()
        fastest_repo = summary.get_fastest_repository()
        
        if best_repo:
            print(f"\n🏆 Best overall repository: {best_repo}")
        if fastest_repo:
            print(f"⚡ Fastest repository: {fastest_repo}")
        
        print(f"\n📁 Results saved to: {args.output_dir}")
        
        if args.enable_manual_eval:
            print("\n🔍 Manual evaluation data prepared.")
            print("To start manual evaluation, run:")
            print(f"  python main.py manual-eval {args.output_dir}/manual_evaluation_data.json")
        
        return summary
        
    except Exception as e:
        logger.error(f"Benchmark failed: {e}")
        raise


def start_manual_evaluation(args):
    """Start manual evaluation interface."""
    print("🔍 Starting Manual Evaluation Interface...")
    
    evaluation_data_path = args.evaluation_data
    if not Path(evaluation_data_path).exists():
        print(f"Error: Evaluation data file not found: {evaluation_data_path}")
        sys.exit(1)
    
    try:
        interface = ManualEvaluationInterface(evaluation_data_path)
        interface.start_server(
            host=args.host,
            port=args.port,
            auto_open=args.auto_open
        )
    except Exception as e:
        logger.error(f"Failed to start manual evaluation: {e}")
        raise


def evaluate_prepared_files(args):
    """Evaluate pre-extracted Markdown files against ground truth."""
    print("🔍 Starting Evaluation of Prepared Files...")
    
    ground_truth_dir = Path(args.ground_truth)
    extracted_files_dir = Path(args.extracted)
    output_dir = Path(args.output)
    
    # Validate directories
    if not ground_truth_dir.exists():
        print(f"Error: Ground truth directory not found: {ground_truth_dir}")
        sys.exit(1)
    
    if not extracted_files_dir.exists():
        print(f"Error: Extracted files directory not found: {extracted_files_dir}")
        sys.exit(1)
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize evaluator and report generator
    evaluator = DocumentEvaluator(fast_mode=getattr(args, 'fast', False))
    report_generator = ReportGenerator(str(output_dir))
    
    # Find all ground truth files
    ground_truth_files = list(ground_truth_dir.glob("*.md"))
    if not ground_truth_files:
        print(f"Error: No Markdown files found in ground truth directory: {ground_truth_dir}")
        sys.exit(1)
    
    print(f"Found {len(ground_truth_files)} ground truth files")
    
    # Find repository folders
    repo_folders = [f for f in extracted_files_dir.iterdir() if f.is_dir()]
    if not repo_folders:
        print(f"Error: No repository folders found in: {extracted_files_dir}")
        sys.exit(1)
    
    print(f"Found {len(repo_folders)} repository folders")
    
    evaluation_results = {}
    extraction_results = {}
    ground_truth_results = {}
    
    # Process each repository
    for repo_folder in repo_folders:
        repo_name = repo_folder.name
        print(f"\n📁 Processing repository: {repo_name}")
        
        repo_evaluation_results = []
        repo_extraction_results = []
        
        # Process each ground truth file
        for gt_file in ground_truth_files:
            file_name = gt_file.stem
            extracted_file = repo_folder / f"{file_name}.md"
            
            if not extracted_file.exists():
                print(f"  ⚠️  Warning: No extracted file found for {file_name}")
                continue
            
            print(f"  📄 Evaluating: {file_name}")
            
            try:
                # Read files
                with open(gt_file, 'r', encoding='utf-8') as f:
                    ground_truth_content = f.read()
                
                with open(extracted_file, 'r', encoding='utf-8') as f:
                    extracted_content = f.read()
                
                # Create extraction result (simulated)
                extraction_result = ExtractionResult(
                    file_path=str(gt_file),
                    repository_name=repo_name,
                    output_path=str(extracted_file),
                    processing_time=ProcessingTime(
                        total_time=0.0,  # We don't have actual processing time
                        extraction_time=0.0,
                        preprocessing_time=0.0,
                        postprocessing_time=0.0
                    ),
                    success=True,
                    error_message=None,
                    output_content=extracted_content
                )
                
                # Evaluate
                evaluation_result = evaluator.evaluate_extraction(
                    extraction_result, str(gt_file)
                )
                
                repo_evaluation_results.append(evaluation_result)
                repo_extraction_results.append(extraction_result)
                
                # Store ground truth result
                if file_name not in ground_truth_results:
                    ground_truth_results[file_name] = {
                        'content': ground_truth_content,
                        'file_path': str(gt_file)
                    }
                
            except Exception as e:
                print(f"  ❌ Error evaluating {file_name}: {e}")
                continue
        
        evaluation_results[repo_name] = repo_evaluation_results
        extraction_results[repo_name] = repo_extraction_results
    
    # Generate reports
    print("\n📊 Generating reports...")
    report_generator.generate_detailed_report(
        evaluation_results, extraction_results, ground_truth_results
    )
    report_generator.generate_summary_report(
        evaluation_results, extraction_results, ground_truth_results
    )
    report_generator.generate_visualizations(evaluation_results)
    
    # Generate comprehensive analysis
    generate_comprehensive_analysis(evaluation_results, output_dir)
    
    # Save evaluation data for manual evaluation
    manual_eval_data = {
        'evaluation_results': evaluation_results,
        'extraction_results': extraction_results,
        'ground_truth_results': ground_truth_results
    }
    
    manual_eval_file = output_dir / "manual_evaluation_data.json"
    with open(manual_eval_file, 'w', encoding='utf-8') as f:
        json.dump(manual_eval_data, f, indent=2, default=str)
    
    # Print summary
    print("\n" + "="*60)
    print("📊 EVALUATION RESULTS")
    print("="*60)
    
    for repo_name, results in evaluation_results.items():
        if not results:
            continue
        
        # Calculate averages for all metrics
        avg_score = sum(r.overall_score for r in results) / len(results)
        avg_char_sim = sum(r.content_similarity.character_similarity for r in results) / len(results)
        avg_word_sim = sum(r.content_similarity.word_similarity for r in results) / len(results)
        avg_sent_sim = sum(r.content_similarity.sentence_similarity for r in results) / len(results)
        avg_word_overlap = sum(r.content_similarity.word_overlap for r in results) / len(results)
        avg_rouge = sum(r.content_similarity.rouge_score for r in results) / len(results)
        avg_bleu = sum(r.content_similarity.bleu_score for r in results) / len(results)
        avg_header = sum(r.structure_accuracy.header_accuracy for r in results) / len(results)
        avg_list = sum(r.structure_accuracy.list_accuracy for r in results) / len(results)
        avg_section = sum(r.structure_accuracy.section_order_accuracy for r in results) / len(results)
        avg_paragraph = sum(r.structure_accuracy.paragraph_accuracy for r in results) / len(results)
        avg_table_content = sum(r.table_quality.content_accuracy for r in results) / len(results)
        avg_table_structure = sum(r.table_quality.structure_preservation for r in results) / len(results)
        avg_table_format = sum(r.table_quality.format_consistency for r in results) / len(results)
        avg_bold = sum(r.formatting_preservation.bold_accuracy for r in results) / len(results)
        avg_italic = sum(r.formatting_preservation.italic_accuracy for r in results) / len(results)
        avg_link = sum(r.formatting_preservation.link_accuracy for r in results) / len(results)
        avg_image = sum(r.formatting_preservation.image_accuracy for r in results) / len(results)
        
        print(f"\n{repo_name}:")
        print(f"  Files evaluated: {len(results)}")
        print(f"  📈 Overall Score: {avg_score:.3f}")
        print(f"  📝 Content Similarity (Levenshtein-based):")
        print(f"    - Character Similarity: {avg_char_sim:.3f}")
        print(f"    - Word Similarity: {avg_word_sim:.3f}")
        print(f"    - Sentence Similarity: {avg_sent_sim:.3f}")
        print(f"    - Word Overlap (F1): {avg_word_overlap:.3f}")
        print(f"    - ROUGE Score: {avg_rouge:.3f}")
        print(f"    - BLEU Score: {avg_bleu:.3f}")
        print(f"  🏗️  Structure Accuracy:")
        print(f"    - Header Accuracy: {avg_header:.3f}")
        print(f"    - List Accuracy: {avg_list:.3f}")
        print(f"    - Section Order: {avg_section:.3f}")
        print(f"    - Paragraph Accuracy: {avg_paragraph:.3f}")
        print(f"  📊 Table Quality:")
        print(f"    - Content Accuracy: {avg_table_content:.3f}")
        print(f"    - Structure Preservation: {avg_table_structure:.3f}")
        print(f"    - Format Consistency: {avg_table_format:.3f}")
        print(f"  🎨 Formatting Preservation:")
        print(f"    - Bold Accuracy: {avg_bold:.3f}")
        print(f"    - Italic Accuracy: {avg_italic:.3f}")
        print(f"    - Link Accuracy: {avg_link:.3f}")
        print(f"    - Image Accuracy: {avg_image:.3f}")
    
    print(f"\n📁 Results saved to: {output_dir}")
    print(f"🔍 Manual evaluation data: {manual_eval_file}")
    
    if args.enable_manual_eval:
        print("\n🔍 Starting manual evaluation interface...")
        try:
            interface = ManualEvaluationInterface(str(manual_eval_file))
            interface.start_server(
                host=args.host,
                port=args.port,
                auto_open=args.auto_open
            )
        except Exception as e:
            logger.error(f"Failed to start manual evaluation: {e}")
            print(f"Manual evaluation failed: {e}")
    
    return evaluation_results


def generate_comprehensive_analysis(evaluation_results, output_dir):
    """Generate comprehensive analysis with charts and statistics."""
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    import numpy as np
    from pathlib import Path
    
    # Set style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Prepare data
    data = []
    for repo_name, results in evaluation_results.items():
        for result in results:
            data.append({
                'Repository': repo_name,
                'File': Path(result.extraction_result.file_path).stem,
                'Overall_Score': result.overall_score,
                'Character_Similarity': result.content_similarity.character_similarity,
                'Word_Similarity': result.content_similarity.word_similarity,
                'Sentence_Similarity': result.content_similarity.sentence_similarity,
                'Word_Overlap': result.content_similarity.word_overlap,
                'ROUGE_Score': result.content_similarity.rouge_score,
                'BLEU_Score': result.content_similarity.bleu_score,
                'Header_Accuracy': result.structure_accuracy.header_accuracy,
                'List_Accuracy': result.structure_accuracy.list_accuracy,
                'Section_Order': result.structure_accuracy.section_order_accuracy,
                'Paragraph_Accuracy': result.structure_accuracy.paragraph_accuracy,
                'Table_Content': result.table_quality.content_accuracy,
                'Table_Structure': result.table_quality.structure_preservation,
                'Table_Format': result.table_quality.format_consistency,
                'Bold_Accuracy': result.formatting_preservation.bold_accuracy,
                'Italic_Accuracy': result.formatting_preservation.italic_accuracy,
                'Link_Accuracy': result.formatting_preservation.link_accuracy,
                'Image_Accuracy': result.formatting_preservation.image_accuracy
            })
    
    df = pd.DataFrame(data)
    
    # 1. Overall Score Comparison
    plt.figure(figsize=(12, 8))
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Overall scores
    overall_scores = df.groupby('Repository')['Overall_Score'].mean().sort_values(ascending=False)
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
    bar_colors = [colors[i % len(colors)] for i in range(len(overall_scores))]
    bars1 = ax1.bar(overall_scores.index, overall_scores.values, color=bar_colors)
    ax1.set_title('📈 Overall Score Comparison', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Score')
    ax1.set_ylim(0, 1)
    for bar, score in zip(bars1, overall_scores.values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                f'{score:.3f}', ha='center', va='bottom', fontweight='bold')
    
    # Content similarity metrics (Levenshtein-based)
    content_metrics = ['Character_Similarity', 'Word_Similarity', 'Sentence_Similarity']
    content_data = df.groupby('Repository')[content_metrics].mean()
    content_data.plot(kind='bar', ax=ax2, width=0.8)
    ax2.set_title('📝 Content Similarity (Levenshtein)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Score')
    ax2.legend(title='Metrics')
    ax2.tick_params(axis='x', rotation=45)
    
    # Structure accuracy metrics
    structure_metrics = ['Header_Accuracy', 'List_Accuracy', 'Section_Order', 'Paragraph_Accuracy']
    structure_data = df.groupby('Repository')[structure_metrics].mean()
    structure_data.plot(kind='bar', ax=ax3, width=0.8)
    ax3.set_title('🏗️ Structure Accuracy Metrics', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Score')
    ax3.legend(title='Metrics')
    ax3.tick_params(axis='x', rotation=45)
    
    # Table quality metrics
    table_metrics = ['Table_Content', 'Table_Structure', 'Table_Format']
    table_data = df.groupby('Repository')[table_metrics].mean()
    table_data.plot(kind='bar', ax=ax4, width=0.8)
    ax4.set_title('📊 Table Quality Metrics', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Score')
    ax4.legend(title='Metrics')
    ax4.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'comprehensive_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Detailed Metrics Heatmap
    plt.figure(figsize=(14, 10))
    metrics_for_heatmap = [
        'Character_Similarity', 'Word_Similarity', 'Sentence_Similarity', 'Word_Overlap', 'ROUGE_Score', 'BLEU_Score',
        'Header_Accuracy', 'List_Accuracy', 'Section_Order', 'Paragraph_Accuracy',
        'Table_Content', 'Table_Structure', 'Table_Format',
        'Bold_Accuracy', 'Italic_Accuracy', 'Link_Accuracy', 'Image_Accuracy'
    ]
    
    heatmap_data = df.groupby('Repository')[metrics_for_heatmap].mean()
    
    # Create custom colormap
    colors = ['#FF6B6B', '#FFE66D', '#4ECDC4']
    n_bins = 100
    cmap = sns.blend_palette(colors, n_colors=n_bins, as_cmap=True)
    
    sns.heatmap(heatmap_data.T, annot=True, fmt='.3f', cmap=cmap, 
                cbar_kws={'label': 'Score'}, linewidths=0.5)
    plt.title('🔥 Detailed Metrics Heatmap', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Repository', fontsize=12, fontweight='bold')
    plt.ylabel('Metrics', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_dir / 'metrics_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Score Distribution
    plt.figure(figsize=(15, 10))
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()
    
    metrics_dist = ['Overall_Score', 'Character_Similarity', 'Word_Similarity', 
                   'Header_Accuracy', 'Table_Content', 'Bold_Accuracy']
    
    for i, metric in enumerate(metrics_dist):
        for repo in df['Repository'].unique():
            repo_data = df[df['Repository'] == repo][metric]
            axes[i].hist(repo_data, alpha=0.7, label=repo, bins=10)
        
        axes[i].set_title(f'📊 {metric.replace("_", " ")} Distribution', fontweight='bold')
        axes[i].set_xlabel('Score')
        axes[i].set_ylabel('Frequency')
        axes[i].legend()
        axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'score_distributions.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Performance Ranking
    plt.figure(figsize=(12, 8))
    
    # Calculate average scores for each metric category
    category_scores = {}
    for repo in df['Repository'].unique():
        repo_data = df[df['Repository'] == repo]
        category_scores[repo] = {
            'Content': repo_data[['Character_Similarity', 'Word_Similarity', 'Sentence_Similarity']].mean().mean(),
            'Structure': repo_data[['Header_Accuracy', 'List_Accuracy', 'Section_Order', 'Paragraph_Accuracy']].mean().mean(),
            'Table': repo_data[['Table_Content', 'Table_Structure', 'Table_Format']].mean().mean(),
            'Formatting': repo_data[['Bold_Accuracy', 'Italic_Accuracy', 'Link_Accuracy', 'Image_Accuracy']].mean().mean()
        }
    
    category_df = pd.DataFrame(category_scores).T
    
    # Create radar chart
    categories = list(category_df.columns)
    N = len(categories)
    
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    ax = plt.subplot(111, projection='polar')
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
    for i, repo in enumerate(category_df.index):
        values = category_df.loc[repo].values.flatten().tolist()
        values += values[:1]
        color = colors[i % len(colors)]  # Use modulo to avoid index error
        ax.plot(angles, values, 'o-', linewidth=2, label=repo, color=color)
        ax.fill(angles, values, alpha=0.25, color=color)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_ylim(0, 1)
    ax.set_title('🎯 Performance Radar Chart', size=16, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    plt.tight_layout()
    plt.savefig(output_dir / 'performance_radar.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Generate comprehensive statistics table
    stats_data = []
    for repo in df['Repository'].unique():
        repo_data = df[df['Repository'] == repo]
        
        stats = {
            'Repository': repo,
            'Files_Evaluated': len(repo_data),
            'Overall_Score_Mean': repo_data['Overall_Score'].mean(),
            'Overall_Score_Std': repo_data['Overall_Score'].std(),
            'Overall_Score_Min': repo_data['Overall_Score'].min(),
            'Overall_Score_Max': repo_data['Overall_Score'].max(),
            'Content_Similarity_Mean': repo_data[['Character_Similarity', 'Word_Similarity', 'Sentence_Similarity']].mean().mean(),
            'Structure_Accuracy_Mean': repo_data[['Header_Accuracy', 'List_Accuracy', 'Section_Order', 'Paragraph_Accuracy']].mean().mean(),
            'Table_Quality_Mean': repo_data[['Table_Content', 'Table_Structure', 'Table_Format']].mean().mean(),
            'Formatting_Preservation_Mean': repo_data[['Bold_Accuracy', 'Italic_Accuracy', 'Link_Accuracy', 'Image_Accuracy']].mean().mean(),
            'Best_Performing_Metric': repo_data[metrics_for_heatmap].mean().idxmax(),
            'Worst_Performing_Metric': repo_data[metrics_for_heatmap].mean().idxmin(),
            'Consistency_Score': 1 - repo_data['Overall_Score'].std()  # Lower std = higher consistency
        }
        stats_data.append(stats)
    
    stats_df = pd.DataFrame(stats_data)
    
    # Save statistics to CSV
    stats_df.to_csv(output_dir / 'comprehensive_statistics.csv', index=False)
    
    # Create formatted statistics table
    stats_table = stats_df.round(3)
    stats_table.to_html(output_dir / 'comprehensive_statistics.html', index=False, 
                       classes='table table-striped table-bordered')
    
    # 6. Generate AI Analysis Report
    generate_ai_analysis_report(stats_df, output_dir)
    
    print(f"📊 Comprehensive analysis generated:")
    print(f"  - Charts: comprehensive_analysis.png, metrics_heatmap.png, score_distributions.png, performance_radar.png")
    print(f"  - Statistics: comprehensive_statistics.csv, comprehensive_statistics.html")
    print(f"  - AI Analysis: ai_analysis_report.txt")


def generate_ai_analysis_report(stats_df, output_dir):
    """Generate AI analysis report for easy consumption."""
    
    # Find best and worst performers
    best_overall = stats_df.loc[stats_df['Overall_Score_Mean'].idxmax()]
    worst_overall = stats_df.loc[stats_df['Overall_Score_Mean'].idxmin()]
    
    best_content = stats_df.loc[stats_df['Content_Similarity_Mean'].idxmax()]
    best_structure = stats_df.loc[stats_df['Structure_Accuracy_Mean'].idxmax()]
    best_table = stats_df.loc[stats_df['Table_Quality_Mean'].idxmax()]
    best_formatting = stats_df.loc[stats_df['Formatting_Preservation_Mean'].idxmax()]
    
    report = f"""
🤖 AI ANALYSIS REPORT
{'='*60}

📊 OVERALL PERFORMANCE SUMMARY
{'-'*40}
• Best Overall Repository: {best_overall['Repository']} (Score: {best_overall['Overall_Score_Mean']:.3f})
• Worst Overall Repository: {worst_overall['Repository']} (Score: {worst_overall['Overall_Score_Mean']:.3f})
• Performance Range: {stats_df['Overall_Score_Mean'].min():.3f} - {stats_df['Overall_Score_Mean'].max():.3f}

🏆 CATEGORY LEADERS
{'-'*40}
• Content Similarity: {best_content['Repository']} (Score: {best_content['Content_Similarity_Mean']:.3f})
• Structure Accuracy: {best_structure['Repository']} (Score: {best_structure['Structure_Accuracy_Mean']:.3f})
• Table Quality: {best_table['Repository']} (Score: {best_table['Table_Quality_Mean']:.3f})
• Formatting Preservation: {best_formatting['Repository']} (Score: {best_formatting['Formatting_Preservation_Mean']:.3f})

📈 DETAILED METRICS ANALYSIS
{'-'*40}
"""
    
    for _, repo in stats_df.iterrows():
        report += f"""
{repo['Repository'].upper()}:
• Overall Score: {repo['Overall_Score_Mean']:.3f} (±{repo['Overall_Score_Std']:.3f})
• Content Similarity: {repo['Content_Similarity_Mean']:.3f}
• Structure Accuracy: {repo['Structure_Accuracy_Mean']:.3f}
• Table Quality: {repo['Table_Quality_Mean']:.3f}
• Formatting Preservation: {repo['Formatting_Preservation_Mean']:.3f}
• Best Metric: {repo['Best_Performing_Metric']}
• Worst Metric: {repo['Worst_Performing_Metric']}
• Consistency: {repo['Consistency_Score']:.3f}
"""
    
    report += f"""
🎯 KEY INSIGHTS
{'-'*40}
• Most Consistent: {stats_df.loc[stats_df['Consistency_Score'].idxmax(), 'Repository']}
• Most Variable: {stats_df.loc[stats_df['Consistency_Score'].idxmin(), 'Repository']}
• Average Performance Gap: {stats_df['Overall_Score_Mean'].max() - stats_df['Overall_Score_Mean'].min():.3f}

📋 RECOMMENDATIONS FOR AI ANALYSIS
{'-'*40}
1. Focus on repositories with high consistency scores for reliable performance
2. Consider category-specific strengths for specialized use cases
3. Analyze worst-performing metrics for improvement opportunities
4. Compare performance across different file types and content structures
5. Use radar charts to identify balanced vs. specialized approaches

📊 DATA FORMAT FOR AI PROCESSING
{'-'*40}
The comprehensive_statistics.csv file contains all numerical data for:
• Statistical analysis (mean, std, min, max)
• Performance ranking
• Category comparisons
• Consistency metrics
• Best/worst performing metrics per repository
"""
    
    with open(output_dir / 'ai_analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Document Extraction Benchmark Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List available repositories
  python main.py list-repos
  
  # Run benchmark with all repositories
  python main.py run --test-files ./test_files --output ./results
  
  # Run benchmark with specific repositories
  python main.py run --test-files ./test_files --output ./results --repos marker unstructured
  
  # Evaluate pre-extracted files
  python main.py evaluate --ground-truth ./ground_truth --extracted ./extracted_files --output ./results
  
  # Start manual evaluation
  python main.py manual-eval ./results/manual_evaluation_data.json
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List repositories command
    list_parser = subparsers.add_parser('list-repos', help='List available repositories')
    
    # Run benchmark command
    run_parser = subparsers.add_parser('run', help='Run benchmark')
    run_parser.add_argument('--test-files', '-t', required=True,
                          help='Directory containing test files (DOCX and PDF pairs)')
    run_parser.add_argument('--output', '-o', required=True,
                          help='Output directory for results')
    run_parser.add_argument('--repos', '-r', nargs='+',
                          help='Specific repositories to test (default: all)')
    run_parser.add_argument('--enable-manual-eval', action='store_true',
                          help='Enable manual evaluation interface')
    run_parser.add_argument('--save-intermediate', action='store_true',
                          help='Save intermediate results')
    run_parser.add_argument('--parallel', action='store_true',
                          help='Enable parallel processing')
    run_parser.add_argument('--max-workers', type=int, default=4,
                          help='Maximum number of parallel workers')
    run_parser.add_argument('--verbose', '-v', action='store_true',
                          help='Enable verbose logging')
    
    # Evaluate prepared files command
    evaluate_parser = subparsers.add_parser('evaluate', help='Evaluate pre-extracted Markdown files')
    evaluate_parser.add_argument('--ground-truth', '-g', required=True,
                               help='Directory containing ground truth Markdown files (from DOCX)')
    evaluate_parser.add_argument('--extracted', '-e', required=True,
                               help='Directory containing extracted Markdown files from repositories')
    evaluate_parser.add_argument('--output', '-o', required=True,
                               help='Output directory for results')
    evaluate_parser.add_argument('--enable-manual-eval', action='store_true',
                               help='Enable manual evaluation interface')
    evaluate_parser.add_argument('--fast', action='store_true',
                               help='Fast mode: skip ROUGE and BLEU calculations for speed')
    evaluate_parser.add_argument('--host', default='localhost', help='Server host')
    evaluate_parser.add_argument('--port', type=int, default=5000, help='Server port')
    evaluate_parser.add_argument('--no-auto-open', dest='auto_open', action='store_false',
                               help='Do not automatically open browser')
    evaluate_parser.add_argument('--verbose', '-v', action='store_true',
                               help='Enable verbose logging')
    
    # Manual evaluation command
    manual_parser = subparsers.add_parser('manual-eval', help='Start manual evaluation interface')
    manual_parser.add_argument('evaluation_data', help='Path to evaluation data JSON file')
    manual_parser.add_argument('--host', default='localhost', help='Server host')
    manual_parser.add_argument('--port', type=int, default=5000, help='Server port')
    manual_parser.add_argument('--no-auto-open', dest='auto_open', action='store_false',
                              help='Do not automatically open browser')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Setup logging
    setup_logging(getattr(args, 'verbose', False))
    
    # Execute command
    if args.command == 'list-repos':
        list_repositories()
    
    elif args.command == 'run':
        # Set default repositories if not specified
        if not args.repos:
            args.repos = list(config_manager.list_repositories())
        
        run_benchmark(args)
    
    elif args.command == 'evaluate':
        evaluate_prepared_files(args)
    
    elif args.command == 'manual-eval':
        start_manual_evaluation(args)
    
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()


if __name__ == "__main__":
    main()
