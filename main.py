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
    
    ground_truth_dir = Path(args.ground_truth_dir)
    extracted_files_dir = Path(args.extracted_files_dir)
    output_dir = Path(args.output_dir)
    
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
    evaluator = DocumentEvaluator()
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
                    repository_id=repo_name,
                    repository_name=repo_name,
                    input_file=str(gt_file),
                    output_file=str(extracted_file),
                    success=True,
                    processing_time=ProcessingTime(
                        total_time=0.0,  # We don't have actual processing time
                        extraction_time=0.0,
                        preprocessing_time=0.0,
                        postprocessing_time=0.0
                    ),
                    error_message=None,
                    extracted_content=extracted_content
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
        
        avg_score = sum(r.overall_score for r in results) / len(results)
        avg_content_score = sum(r.content_similarity.bert_score for r in results) / len(results)
        avg_structure_score = sum(r.structure_accuracy.header_f1_score for r in results) / len(results)
        
        print(f"\n{repo_name}:")
        print(f"  Files evaluated: {len(results)}")
        print(f"  Average overall score: {avg_score:.3f}")
        print(f"  Average content similarity: {avg_content_score:.3f}")
        print(f"  Average structure accuracy: {avg_structure_score:.3f}")
    
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
