"""
Data models for benchmark results and evaluation metrics.
Defines the structure for storing and processing benchmark data.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class EvaluationMetric(Enum):
    """Enumeration of evaluation metrics."""
    CONTENT_SIMILARITY = "content_similarity"
    STRUCTURE_ACCURACY = "structure_accuracy"
    FORMATTING_PRESERVATION = "formatting_preservation"
    TABLE_QUALITY = "table_quality"
    PROCESSING_TIME = "processing_time"


@dataclass
class ProcessingTime:
    """Processing time metrics."""
    total_time: float
    extraction_time: float
    preprocessing_time: float = 0.0
    postprocessing_time: float = 0.0


@dataclass
class ContentSimilarityMetrics:
    """Content similarity evaluation metrics."""
    bert_score: float
    rouge_score: float
    bleu_score: float
    exact_match: float
    word_overlap: float


@dataclass
class StructureAccuracyMetrics:
    """Structure accuracy evaluation metrics."""
    header_accuracy: float
    list_accuracy: float
    section_order_accuracy: float
    paragraph_accuracy: float


@dataclass
class FormattingPreservationMetrics:
    """Formatting preservation evaluation metrics."""
    bold_accuracy: float
    italic_accuracy: float
    link_accuracy: float
    image_accuracy: float


@dataclass
class TableQualityMetrics:
    """Table quality evaluation metrics."""
    structure_preservation: float
    content_accuracy: float
    format_consistency: float
    table_format_type: str  # "markdown" or "html"


@dataclass
class ManualEvaluation:
    """Manual evaluation results."""
    overall_quality: int  # 1-5 scale
    table_format_quality: int
    structure_preservation: int
    formatting_accuracy: int
    comments: str = ""
    evaluator_name: str = ""


@dataclass
class ExtractionResult:
    """Result of a single extraction operation."""
    file_path: str
    repository_name: str
    output_path: str
    processing_time: ProcessingTime
    success: bool
    error_message: Optional[str] = None
    output_content: Optional[str] = None


@dataclass
class EvaluationResult:
    """Result of evaluating an extraction against ground truth."""
    extraction_result: ExtractionResult
    ground_truth_path: str
    content_similarity: ContentSimilarityMetrics
    structure_accuracy: StructureAccuracyMetrics
    formatting_preservation: FormattingPreservationMetrics
    table_quality: TableQualityMetrics
    manual_evaluation: Optional[ManualEvaluation] = None
    
    @property
    def overall_score(self) -> float:
        """Calculate overall score as weighted average of metrics."""
        weights = {
            'content': 0.4,
            'structure': 0.25,
            'formatting': 0.2,
            'table': 0.15
        }
        
        content_score = self.content_similarity.bert_score
        structure_score = (
            self.structure_accuracy.header_accuracy +
            self.structure_accuracy.list_accuracy +
            self.structure_accuracy.section_order_accuracy
        ) / 3
        formatting_score = (
            self.formatting_preservation.bold_accuracy +
            self.formatting_preservation.italic_accuracy +
            self.formatting_preservation.link_accuracy
        ) / 3
        table_score = self.table_quality.content_accuracy
        
        return (
            weights['content'] * content_score +
            weights['structure'] * structure_score +
            weights['formatting'] * formatting_score +
            weights['table'] * table_score
        )


@dataclass
class RepositoryBenchmarkResult:
    """Benchmark results for a single repository."""
    repository_name: str
    repository_id: str
    total_files: int
    successful_extractions: int
    failed_extractions: int
    average_processing_time: float
    evaluation_results: List[EvaluationResult] = field(default_factory=list)
    manual_evaluations: List[ManualEvaluation] = field(default_factory=list)
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_files == 0:
            return 0.0
        return self.successful_extractions / self.total_files
    
    @property
    def average_overall_score(self) -> float:
        """Calculate average overall score."""
        if not self.evaluation_results:
            return 0.0
        scores = [result.overall_score for result in self.evaluation_results]
        return sum(scores) / len(scores)


@dataclass
class BenchmarkSummary:
    """Summary of complete benchmark run."""
    benchmark_date: datetime
    test_files: List[str]
    repositories_tested: List[str]
    repository_results: Dict[str, RepositoryBenchmarkResult] = field(default_factory=dict)
    total_processing_time: float = 0.0
    
    def get_best_repository(self) -> Optional[str]:
        """Get the repository with the highest average score."""
        if not self.repository_results:
            return None
        
        best_repo = max(
            self.repository_results.items(),
            key=lambda x: x[1].average_overall_score
        )
        return best_repo[0]
    
    def get_fastest_repository(self) -> Optional[str]:
        """Get the repository with the fastest average processing time."""
        if not self.repository_results:
            return None
        
        fastest_repo = min(
            self.repository_results.items(),
            key=lambda x: x[1].average_processing_time
        )
        return fastest_repo[0]


@dataclass
class BenchmarkConfig:
    """Configuration for a benchmark run."""
    test_files_dir: str
    output_dir: str
    repositories_to_test: List[str]
    enable_manual_evaluation: bool = True
    save_intermediate_results: bool = True
    parallel_processing: bool = False
    max_workers: int = 4
