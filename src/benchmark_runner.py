"""
Main benchmark runner module.
Orchestrates the entire benchmark process from setup to evaluation.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from .config import config_manager
from .models import (
    BenchmarkConfig, BenchmarkSummary, RepositoryBenchmarkResult,
    EvaluationResult, ManualEvaluation
)
from .ground_truth import GroundTruthGenerator
from .repository_manager import RepositoryManager
from .evaluator import DocumentEvaluator
from .report_generator import ReportGenerator

logger = logging.getLogger(__name__)


class BenchmarkRunner:
    """Main benchmark runner for document extraction evaluation."""
    
    def __init__(self, config: BenchmarkConfig):
        """Initialize benchmark runner.
        
        Args:
            config: Benchmark configuration.
        """
        self.config = config
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.ground_truth_generator = GroundTruthGenerator(
            str(self.output_dir / "ground_truth")
        )
        self.repository_manager = RepositoryManager(
            str(self.output_dir / "repositories")
        )
        self.evaluator = DocumentEvaluator()
        self.report_generator = ReportGenerator(str(self.output_dir))
        
        # Results storage
        self.benchmark_summary = None
        self.ground_truth_results = {}
        self.extraction_results = {}
        self.evaluation_results = {}
        
        # Setup logging
        self._setup_logging()
    
    def run_benchmark(self) -> BenchmarkSummary:
        """Run the complete benchmark process.
        
        Returns:
            BenchmarkSummary with all results.
        """
        logger.info("Starting document extraction benchmark...")
        start_time = time.time()
        
        try:
            # Step 1: Setup repositories
            logger.info("Step 1: Setting up repositories...")
            self._setup_repositories()
            
            # Step 2: Generate ground truth
            logger.info("Step 2: Generating ground truth...")
            self._generate_ground_truth()
            
            # Step 3: Run extractions
            logger.info("Step 3: Running extractions...")
            self._run_extractions()
            
            # Step 4: Evaluate results
            logger.info("Step 4: Evaluating results...")
            self._evaluate_results()
            
            # Step 5: Generate reports
            logger.info("Step 5: Generating reports...")
            self._generate_reports()
            
            # Step 6: Manual evaluation (if enabled)
            if self.config.enable_manual_evaluation:
                logger.info("Step 6: Manual evaluation interface...")
                self._setup_manual_evaluation()
            
            end_time = time.time()
            total_time = end_time - start_time
            
            # Create final summary
            self.benchmark_summary = BenchmarkSummary(
                benchmark_date=datetime.now(),
                test_files=self._get_test_files(),
                repositories_tested=self.config.repositories_to_test,
                repository_results=self._create_repository_results(),
                total_processing_time=total_time
            )
            
            # Save results
            self._save_results()
            
            logger.info(f"Benchmark completed successfully in {total_time:.2f} seconds")
            return self.benchmark_summary
            
        except Exception as e:
            logger.error(f"Benchmark failed: {e}")
            raise
    
    def _setup_logging(self):
        """Setup logging configuration."""
        log_file = self.output_dir / "benchmark.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    
    def _setup_repositories(self):
        """Setup all required repositories."""
        logger.info(f"Setting up {len(self.config.repositories_to_test)} repositories...")
        
        setup_results = self.repository_manager.setup_all_repositories(
            self.config.repositories_to_test
        )
        
        failed_repos = [repo for repo, success in setup_results.items() if not success]
        if failed_repos:
            logger.warning(f"Failed to setup repositories: {failed_repos}")
        
        successful_repos = [repo for repo, success in setup_results.items() if success]
        logger.info(f"Successfully setup {len(successful_repos)} repositories")
    
    def _generate_ground_truth(self):
        """Generate ground truth from DOCX files."""
        docx_files = self._get_docx_files()
        logger.info(f"Generating ground truth for {len(docx_files)} DOCX files...")
        
        self.ground_truth_results = self.ground_truth_generator.batch_generate(docx_files)
        
        successful_gt = sum(1 for result in self.ground_truth_results.values() if result['success'])
        logger.info(f"Generated ground truth for {successful_gt}/{len(docx_files)} files")
    
    def _run_extractions(self):
        """Run extractions with all repositories."""
        pdf_files = self._get_pdf_files()
        logger.info(f"Running extractions for {len(pdf_files)} PDF files...")
        
        self.extraction_results = {}
        
        if self.config.parallel_processing:
            self._run_extractions_parallel(pdf_files)
        else:
            self._run_extractions_sequential(pdf_files)
    
    def _run_extractions_sequential(self, pdf_files: List[str]):
        """Run extractions sequentially."""
        for pdf_file in tqdm(pdf_files, desc="Running extractions"):
            for repo_id in self.config.repositories_to_test:
                try:
                    result = self.repository_manager.extract_with_repository(
                        repo_id, pdf_file, str(self.output_dir / "extractions")
                    )
                    
                    if pdf_file not in self.extraction_results:
                        self.extraction_results[pdf_file] = {}
                    
                    self.extraction_results[pdf_file][repo_id] = result
                    
                except Exception as e:
                    logger.error(f"Extraction failed for {pdf_file} with {repo_id}: {e}")
    
    def _run_extractions_parallel(self, pdf_files: List[str]):
        """Run extractions in parallel."""
        total_tasks = len(pdf_files) * len(self.config.repositories_to_test)
        
        with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            futures = []
            
            for pdf_file in pdf_files:
                for repo_id in self.config.repositories_to_test:
                    future = executor.submit(
                        self._extract_single_file, pdf_file, repo_id
                    )
                    futures.append((pdf_file, repo_id, future))
            
            # Collect results
            for pdf_file, repo_id, future in tqdm(futures, desc="Running extractions"):
                try:
                    result = future.result()
                    if pdf_file not in self.extraction_results:
                        self.extraction_results[pdf_file] = {}
                    self.extraction_results[pdf_file][repo_id] = result
                except Exception as e:
                    logger.error(f"Extraction failed for {pdf_file} with {repo_id}: {e}")
    
    def _extract_single_file(self, pdf_file: str, repo_id: str):
        """Extract a single file with a specific repository."""
        return self.repository_manager.extract_with_repository(
            repo_id, pdf_file, str(self.output_dir / "extractions")
        )
    
    def _evaluate_results(self):
        """Evaluate all extraction results."""
        logger.info("Evaluating extraction results...")
        
        self.evaluation_results = {}
        
        for pdf_file, repo_results in self.extraction_results.items():
            # Find corresponding ground truth
            docx_file = self._get_corresponding_docx(pdf_file)
            if docx_file not in self.ground_truth_results:
                logger.warning(f"No ground truth found for {pdf_file}")
                continue
            
            ground_truth_path = self.ground_truth_results[docx_file]['output_path']
            
            self.evaluation_results[pdf_file] = {}
            
            for repo_id, extraction_result in repo_results.items():
                try:
                    evaluation_result = self.evaluator.evaluate_extraction(
                        extraction_result, ground_truth_path
                    )
                    self.evaluation_results[pdf_file][repo_id] = evaluation_result
                    
                except Exception as e:
                    logger.error(f"Evaluation failed for {pdf_file} with {repo_id}: {e}")
    
    def _generate_reports(self):
        """Generate comprehensive reports."""
        logger.info("Generating reports...")
        
        # Generate detailed report
        self.report_generator.generate_detailed_report(
            self.evaluation_results,
            self.extraction_results,
            self.ground_truth_results
        )
        
        # Generate summary report
        self.report_generator.generate_summary_report(
            self.benchmark_summary
        )
        
        # Generate visualizations
        self.report_generator.generate_visualizations(
            self.evaluation_results
        )
    
    def _setup_manual_evaluation(self):
        """Setup manual evaluation interface."""
        logger.info("Setting up manual evaluation interface...")
        
        # Create manual evaluation data structure
        manual_eval_data = self._prepare_manual_evaluation_data()
        
        # Save manual evaluation data
        manual_eval_file = self.output_dir / "manual_evaluation_data.json"
        with open(manual_eval_file, 'w', encoding='utf-8') as f:
            json.dump(manual_eval_data, f, indent=2, default=str)
        
        logger.info(f"Manual evaluation data saved to {manual_eval_file}")
        logger.info("Start the manual evaluation interface with: python -m src.manual_evaluation")
    
    def _get_test_files(self) -> List[str]:
        """Get list of test files."""
        return self._get_pdf_files()
    
    def _get_pdf_files(self) -> List[str]:
        """Get list of PDF files from test directory."""
        test_dir = Path(self.config.test_files_dir)
        pdf_files = list(test_dir.glob("*.pdf"))
        return [str(f) for f in pdf_files]
    
    def _get_docx_files(self) -> List[str]:
        """Get list of DOCX files from test directory."""
        test_dir = Path(self.config.test_files_dir)
        docx_files = list(test_dir.glob("*.docx"))
        return [str(f) for f in docx_files]
    
    def _get_corresponding_docx(self, pdf_file: str) -> Optional[str]:
        """Get corresponding DOCX file for a PDF file."""
        pdf_path = Path(pdf_file)
        docx_path = pdf_path.with_suffix('.docx')
        
        if docx_path.exists():
            return str(docx_path)
        
        # Try to find by name without extension
        test_dir = Path(self.config.test_files_dir)
        docx_files = list(test_dir.glob(f"{pdf_path.stem}.docx"))
        
        if docx_files:
            return str(docx_files[0])
        
        return None
    
    def _create_repository_results(self) -> Dict[str, RepositoryBenchmarkResult]:
        """Create repository benchmark results."""
        repo_results = {}
        
        for repo_id in self.config.repositories_to_test:
            successful_extractions = 0
            failed_extractions = 0
            total_processing_time = 0.0
            evaluation_results = []
            
            for pdf_file, repo_results_dict in self.extraction_results.items():
                if repo_id in repo_results_dict:
                    extraction_result = repo_results_dict[repo_id]
                    
                    if extraction_result.success:
                        successful_extractions += 1
                        total_processing_time += extraction_result.processing_time.total_time
                        
                        # Add evaluation result if available
                        if (pdf_file in self.evaluation_results and 
                            repo_id in self.evaluation_results[pdf_file]):
                            evaluation_results.append(
                                self.evaluation_results[pdf_file][repo_id]
                            )
                    else:
                        failed_extractions += 1
            
            total_files = successful_extractions + failed_extractions
            avg_processing_time = (total_processing_time / successful_extractions 
                                 if successful_extractions > 0 else 0.0)
            
            repo_config = config_manager.get_repository(repo_id)
            repo_results[repo_id] = RepositoryBenchmarkResult(
                repository_name=repo_config.name if repo_config else repo_id,
                repository_id=repo_id,
                total_files=total_files,
                successful_extractions=successful_extractions,
                failed_extractions=failed_extractions,
                average_processing_time=avg_processing_time,
                evaluation_results=evaluation_results
            )
        
        return repo_results
    
    def _prepare_manual_evaluation_data(self) -> Dict:
        """Prepare data for manual evaluation."""
        manual_eval_data = {
            "benchmark_info": {
                "date": datetime.now().isoformat(),
                "test_files": len(self._get_test_files()),
                "repositories": self.config.repositories_to_test
            },
            "evaluation_items": []
        }
        
        for pdf_file, repo_results in self.evaluation_results.items():
            for repo_id, evaluation_result in repo_results.items():
                item = {
                    "file": pdf_file,
                    "repository": repo_id,
                    "ground_truth_path": evaluation_result.ground_truth_path,
                    "extraction_path": evaluation_result.extraction_result.output_path,
                    "metrics": {
                        "overall_score": evaluation_result.overall_score,
                        "content_similarity": evaluation_result.content_similarity.bert_score,
                        "structure_accuracy": evaluation_result.structure_accuracy.header_accuracy,
                        "formatting_preservation": evaluation_result.formatting_preservation.bold_accuracy,
                        "table_quality": evaluation_result.table_quality.content_accuracy
                    }
                }
                manual_eval_data["evaluation_items"].append(item)
        
        return manual_eval_data
    
    def _save_results(self):
        """Save all benchmark results."""
        # Save extraction results
        extraction_file = self.output_dir / "extraction_results.json"
        with open(extraction_file, 'w', encoding='utf-8') as f:
            json.dump(self.extraction_results, f, indent=2, default=str)
        
        # Save evaluation results
        evaluation_file = self.output_dir / "evaluation_results.json"
        with open(evaluation_file, 'w', encoding='utf-8') as f:
            json.dump(self.evaluation_results, f, indent=2, default=str)
        
        # Save benchmark summary
        summary_file = self.output_dir / "benchmark_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(self.benchmark_summary, f, indent=2, default=str)
        
        logger.info(f"Results saved to {self.output_dir}")
    
    def get_best_repository(self) -> Optional[str]:
        """Get the best performing repository."""
        if not self.benchmark_summary:
            return None
        
        return self.benchmark_summary.get_best_repository()
    
    def get_fastest_repository(self) -> Optional[str]:
        """Get the fastest repository."""
        if not self.benchmark_summary:
            return None
        
        return self.benchmark_summary.get_fastest_repository()
    
    def get_repository_ranking(self) -> List[tuple]:
        """Get repository ranking by overall score."""
        if not self.benchmark_summary:
            return []
        
        rankings = []
        for repo_id, repo_result in self.benchmark_summary.repository_results.items():
            rankings.append((repo_id, repo_result.average_overall_score))
        
        return sorted(rankings, key=lambda x: x[1], reverse=True)
