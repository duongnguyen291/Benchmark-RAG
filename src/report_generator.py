"""
Report generation module.
Creates comprehensive reports and visualizations for benchmark results.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from .models import (
    BenchmarkSummary, RepositoryBenchmarkResult, EvaluationResult
)

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates comprehensive reports and visualizations."""
    
    def __init__(self, output_dir: str):
        """Initialize report generator.
        
        Args:
            output_dir: Directory to save reports and visualizations.
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set style for plots
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def generate_detailed_report(self, evaluation_results: Dict, 
                               extraction_results: Dict, 
                               ground_truth_results: Dict):
        """Generate detailed evaluation report."""
        logger.info("Generating detailed report...")
        
        report_data = {
            "summary": self._create_summary_section(evaluation_results),
            "repository_performance": self._create_repository_performance_section(evaluation_results),
            "file_analysis": self._create_file_analysis_section(evaluation_results),
            "metric_breakdown": self._create_metric_breakdown_section(evaluation_results),
            "error_analysis": self._create_error_analysis_section(extraction_results)
        }
        
        # Save detailed report
        report_file = self.output_dir / "detailed_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        # Generate HTML report
        self._generate_html_report(report_data)
        
        logger.info(f"Detailed report saved to {report_file}")
    
    def generate_summary_report(self, benchmark_summary: BenchmarkSummary):
        """Generate summary report."""
        logger.info("Generating summary report...")
        
        summary_data = {
            "benchmark_info": {
                "date": benchmark_summary.benchmark_date.isoformat(),
                "total_files": len(benchmark_summary.test_files),
                "repositories_tested": benchmark_summary.repositories_tested,
                "total_processing_time": benchmark_summary.total_processing_time
            },
            "repository_summary": self._create_repository_summary(benchmark_summary),
            "best_performers": {
                "best_overall": benchmark_summary.get_best_repository(),
                "fastest": benchmark_summary.get_fastest_repository()
            }
        }
        
        # Save summary report
        summary_file = self.output_dir / "summary_report.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, default=str)
        
        logger.info(f"Summary report saved to {summary_file}")
    
    def generate_visualizations(self, evaluation_results: Dict):
        """Generate comprehensive visualizations."""
        logger.info("Generating visualizations...")
        
        # Create DataFrame for analysis
        df = self._create_evaluation_dataframe(evaluation_results)
        
        # Generate various plots
        self._generate_performance_comparison_plot(df)
        self._generate_metric_heatmap(df)
        self._generate_processing_time_plot(df)
        self._generate_score_distribution_plot(df)
        self._generate_interactive_dashboard(df)
        
        logger.info("Visualizations generated successfully")
    
    def _create_summary_section(self, evaluation_results: Dict) -> Dict:
        """Create summary section of detailed report."""
        total_evaluations = sum(len(repo_results) for repo_results in evaluation_results.values())
        successful_evaluations = sum(
            sum(1 for eval_result in repo_results.values() 
                if eval_result.overall_score > 0)
            for repo_results in evaluation_results.values()
        )
        
        return {
            "total_evaluations": total_evaluations,
            "successful_evaluations": successful_evaluations,
            "success_rate": successful_evaluations / total_evaluations if total_evaluations > 0 else 0,
            "average_overall_score": self._calculate_average_score(evaluation_results)
        }
    
    def _create_repository_performance_section(self, evaluation_results: Dict) -> Dict:
        """Create repository performance section."""
        repo_performance = {}
        
        for file_results in evaluation_results.values():
            for repo_id, eval_result in file_results.items():
                if repo_id not in repo_performance:
                    repo_performance[repo_id] = {
                        "scores": [],
                        "processing_times": [],
                        "success_count": 0,
                        "total_count": 0
                    }
                
                repo_performance[repo_id]["scores"].append(eval_result.overall_score)
                repo_performance[repo_id]["processing_times"].append(
                    eval_result.extraction_result.processing_time.total_time
                )
                repo_performance[repo_id]["total_count"] += 1
                
                if eval_result.overall_score > 0:
                    repo_performance[repo_id]["success_count"] += 1
        
        # Calculate averages
        for repo_id, data in repo_performance.items():
            data["average_score"] = sum(data["scores"]) / len(data["scores"]) if data["scores"] else 0
            data["average_processing_time"] = sum(data["processing_times"]) / len(data["processing_times"]) if data["processing_times"] else 0
            data["success_rate"] = data["success_count"] / data["total_count"] if data["total_count"] > 0 else 0
        
        return repo_performance
    
    def _create_file_analysis_section(self, evaluation_results: Dict) -> Dict:
        """Create file analysis section."""
        file_analysis = {}
        
        for file_path, repo_results in evaluation_results.items():
            file_name = Path(file_path).name
            file_analysis[file_name] = {
                "repositories": len(repo_results),
                "best_score": max(eval_result.overall_score for eval_result in repo_results.values()),
                "worst_score": min(eval_result.overall_score for eval_result in repo_results.values()),
                "average_score": sum(eval_result.overall_score for eval_result in repo_results.values()) / len(repo_results),
                "best_repository": max(repo_results.items(), key=lambda x: x[1].overall_score)[0]
            }
        
        return file_analysis
    
    def _create_metric_breakdown_section(self, evaluation_results: Dict) -> Dict:
        """Create metric breakdown section."""
        metrics = {
            "content_similarity": [],
            "structure_accuracy": [],
            "formatting_preservation": [],
            "table_quality": []
        }
        
        for file_results in evaluation_results.values():
            for eval_result in file_results.values():
                metrics["content_similarity"].append(eval_result.content_similarity.bert_score)
                metrics["structure_accuracy"].append(eval_result.structure_accuracy.header_accuracy)
                metrics["formatting_preservation"].append(eval_result.formatting_preservation.bold_accuracy)
                metrics["table_quality"].append(eval_result.table_quality.content_accuracy)
        
        # Calculate statistics
        metric_stats = {}
        for metric_name, values in metrics.items():
            if values:
                metric_stats[metric_name] = {
                    "mean": sum(values) / len(values),
                    "median": sorted(values)[len(values) // 2],
                    "min": min(values),
                    "max": max(values),
                    "std": self._calculate_std(values)
                }
        
        return metric_stats
    
    def _create_error_analysis_section(self, extraction_results: Dict) -> Dict:
        """Create error analysis section."""
        errors = {}
        
        for file_results in extraction_results.values():
            for repo_id, extraction_result in file_results.items():
                if not extraction_result.success:
                    error_type = "extraction_failed"
                    error_msg = extraction_result.error_message or "Unknown error"
                    
                    if error_type not in errors:
                        errors[error_type] = {}
                    
                    if repo_id not in errors[error_type]:
                        errors[error_type][repo_id] = []
                    
                    errors[error_type][repo_id].append({
                        "file": Path(extraction_result.file_path).name,
                        "error": error_msg
                    })
        
        return errors
    
    def _create_repository_summary(self, benchmark_summary: BenchmarkSummary) -> Dict:
        """Create repository summary for summary report."""
        repo_summary = {}
        
        for repo_id, repo_result in benchmark_summary.repository_results.items():
            repo_summary[repo_id] = {
                "name": repo_result.repository_name,
                "total_files": repo_result.total_files,
                "successful_extractions": repo_result.successful_extractions,
                "failed_extractions": repo_result.failed_extractions,
                "success_rate": repo_result.success_rate,
                "average_processing_time": repo_result.average_processing_time,
                "average_overall_score": repo_result.average_overall_score
            }
        
        return repo_summary
    
    def _create_evaluation_dataframe(self, evaluation_results: Dict) -> pd.DataFrame:
        """Create DataFrame for visualization."""
        data = []
        
        for file_path, repo_results in evaluation_results.items():
            file_name = Path(file_path).name
            for repo_id, eval_result in repo_results.items():
                data.append({
                    "file": file_name,
                    "repository": repo_id,
                    "overall_score": eval_result.overall_score,
                    "content_similarity": eval_result.content_similarity.bert_score,
                    "structure_accuracy": eval_result.structure_accuracy.header_accuracy,
                    "formatting_preservation": eval_result.formatting_preservation.bold_accuracy,
                    "table_quality": eval_result.table_quality.content_accuracy,
                    "processing_time": eval_result.extraction_result.processing_time.total_time,
                    "success": eval_result.overall_score > 0
                })
        
        return pd.DataFrame(data)
    
    def _generate_performance_comparison_plot(self, df: pd.DataFrame):
        """Generate performance comparison plot."""
        plt.figure(figsize=(12, 8))
        
        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Overall score comparison
        sns.boxplot(data=df, x='repository', y='overall_score', ax=axes[0, 0])
        axes[0, 0].set_title('Overall Score Comparison')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Processing time comparison
        sns.boxplot(data=df, x='repository', y='processing_time', ax=axes[0, 1])
        axes[0, 1].set_title('Processing Time Comparison')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Success rate
        success_rate = df.groupby('repository')['success'].mean()
        success_rate.plot(kind='bar', ax=axes[1, 0])
        axes[1, 0].set_title('Success Rate by Repository')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Metric comparison
        metrics = ['content_similarity', 'structure_accuracy', 'formatting_preservation', 'table_quality']
        metric_means = df.groupby('repository')[metrics].mean()
        metric_means.plot(kind='bar', ax=axes[1, 1])
        axes[1, 1].set_title('Average Metrics by Repository')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "performance_comparison.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    def _generate_metric_heatmap(self, df: pd.DataFrame):
        """Generate metric correlation heatmap."""
        plt.figure(figsize=(10, 8))
        
        # Calculate correlation matrix
        correlation_matrix = df[['overall_score', 'content_similarity', 'structure_accuracy', 
                               'formatting_preservation', 'table_quality']].corr()
        
        # Create heatmap
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, linewidths=0.5)
        plt.title('Metric Correlation Heatmap')
        plt.tight_layout()
        plt.savefig(self.output_dir / "metric_heatmap.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    def _generate_processing_time_plot(self, df: pd.DataFrame):
        """Generate processing time analysis plot."""
        plt.figure(figsize=(12, 6))
        
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Processing time distribution
        sns.histplot(data=df, x='processing_time', hue='repository', bins=20, ax=ax1)
        ax1.set_title('Processing Time Distribution')
        ax1.set_xlabel('Processing Time (seconds)')
        
        # Processing time vs score
        sns.scatterplot(data=df, x='processing_time', y='overall_score', 
                       hue='repository', alpha=0.7, ax=ax2)
        ax2.set_title('Processing Time vs Overall Score')
        ax2.set_xlabel('Processing Time (seconds)')
        ax2.set_ylabel('Overall Score')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "processing_time_analysis.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    def _generate_score_distribution_plot(self, df: pd.DataFrame):
        """Generate score distribution plot."""
        plt.figure(figsize=(12, 8))
        
        # Create subplots for each metric
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        metrics = ['overall_score', 'content_similarity', 'structure_accuracy', 'formatting_preservation']
        titles = ['Overall Score', 'Content Similarity', 'Structure Accuracy', 'Formatting Preservation']
        
        for i, (metric, title) in enumerate(zip(metrics, titles)):
            row, col = i // 2, i % 2
            sns.histplot(data=df, x=metric, bins=20, ax=axes[row, col])
            axes[row, col].set_title(f'{title} Distribution')
            axes[row, col].set_xlabel(title)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "score_distribution.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    def _generate_interactive_dashboard(self, df: pd.DataFrame):
        """Generate interactive dashboard using Plotly."""
        # Create interactive dashboard
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Overall Score by Repository', 'Processing Time by Repository',
                          'Metric Comparison', 'Score Distribution'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "scatter"}, {"type": "histogram"}]]
        )
        
        # Overall score bar chart
        score_by_repo = df.groupby('repository')['overall_score'].mean()
        fig.add_trace(
            go.Bar(x=score_by_repo.index, y=score_by_repo.values, name="Overall Score"),
            row=1, col=1
        )
        
        # Processing time bar chart
        time_by_repo = df.groupby('repository')['processing_time'].mean()
        fig.add_trace(
            go.Bar(x=time_by_repo.index, y=time_by_repo.values, name="Processing Time"),
            row=1, col=2
        )
        
        # Metric comparison scatter
        for metric in ['content_similarity', 'structure_accuracy', 'formatting_preservation']:
            fig.add_trace(
                go.Scatter(x=df['repository'], y=df[metric], mode='markers', name=metric),
                row=2, col=1
            )
        
        # Score distribution histogram
        fig.add_trace(
            go.Histogram(x=df['overall_score'], name="Score Distribution"),
            row=2, col=2
        )
        
        fig.update_layout(height=800, title_text="Benchmark Results Dashboard")
        fig.write_html(self.output_dir / "interactive_dashboard.html")
    
    def _generate_html_report(self, report_data: Dict):
        """Generate HTML report."""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Document Extraction Benchmark Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; }}
                .metric {{ display: inline-block; margin: 10px; padding: 10px; background: #f5f5f5; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>Document Extraction Benchmark Report</h1>
            
            <div class="section">
                <h2>Summary</h2>
                <div class="metric">Total Evaluations: {report_data['summary']['total_evaluations']}</div>
                <div class="metric">Success Rate: {report_data['summary']['success_rate']:.2%}</div>
                <div class="metric">Average Score: {report_data['summary']['average_overall_score']:.3f}</div>
            </div>
            
            <div class="section">
                <h2>Repository Performance</h2>
                <table>
                    <tr><th>Repository</th><th>Average Score</th><th>Success Rate</th><th>Avg Processing Time</th></tr>
        """
        
        for repo_id, perf in report_data['repository_performance'].items():
            html_content += f"""
                    <tr>
                        <td>{repo_id}</td>
                        <td>{perf['average_score']:.3f}</td>
                        <td>{perf['success_rate']:.2%}</td>
                        <td>{perf['average_processing_time']:.2f}s</td>
                    </tr>
            """
        
        html_content += """
                </table>
            </div>
            
            <div class="section">
                <h2>Visualizations</h2>
                <p>Check the generated PNG files and interactive dashboard for detailed visualizations.</p>
            </div>
        </body>
        </html>
        """
        
        with open(self.output_dir / "report.html", 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _calculate_average_score(self, evaluation_results: Dict) -> float:
        """Calculate average overall score."""
        scores = []
        for file_results in evaluation_results.values():
            for eval_result in file_results.values():
                scores.append(eval_result.overall_score)
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _calculate_std(self, values: List[float]) -> float:
        """Calculate standard deviation."""
        if len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return variance ** 0.5
