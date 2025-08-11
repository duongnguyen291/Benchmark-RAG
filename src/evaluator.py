"""
Evaluation module for comprehensive document extraction assessment.
Implements various metrics for evaluating extraction quality.
"""

import re
import json
import logging
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
import numpy as np
from collections import Counter

# Import evaluation libraries
try:
    from bert_score import score as bert_score_func
    BERT_SCORE_AVAILABLE = True
except ImportError:
    BERT_SCORE_AVAILABLE = False
    logging.warning("BERTScore not available. Install with: pip install bert-score")

try:
    from rouge_score import rouge_scorer
    ROUGE_AVAILABLE = True
except ImportError:
    ROUGE_AVAILABLE = False
    logging.warning("ROUGE not available. Install with: pip install rouge-score")

from .models import (
    ContentSimilarityMetrics, StructureAccuracyMetrics, 
    FormattingPreservationMetrics, TableQualityMetrics,
    EvaluationResult, ExtractionResult
)
from .config import config_manager

logger = logging.getLogger(__name__)


class DocumentEvaluator:
    """Comprehensive document extraction evaluator."""
    
    def __init__(self):
        """Initialize evaluator with configuration."""
        self.config = config_manager.get_evaluation_config()
        self.bert_scorer = None
        self.rouge_scorer = None
        
        # Initialize scorers if available
        if BERT_SCORE_AVAILABLE:
            self.bert_scorer = bert_score_func
        if ROUGE_AVAILABLE:
            self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    
    def evaluate_extraction(self, extraction_result: ExtractionResult, 
                          ground_truth_path: str) -> EvaluationResult:
        """Evaluate an extraction result against ground truth.
        
        Args:
            extraction_result: Result from repository extraction.
            ground_truth_path: Path to ground truth markdown file.
            
        Returns:
            EvaluationResult with comprehensive metrics.
        """
        if not extraction_result.success:
            logger.warning(f"Extraction failed for {extraction_result.file_path}")
            return self._create_failed_evaluation(extraction_result, ground_truth_path)
        
        # Load ground truth content
        ground_truth_content = self._load_content(ground_truth_path)
        extracted_content = extraction_result.output_content
        
        if not ground_truth_content or not extracted_content:
            logger.error("Missing content for evaluation")
            return self._create_failed_evaluation(extraction_result, ground_truth_path)
        
        # Normalize content for comparison
        ground_truth_normalized = self._normalize_content(ground_truth_content)
        extracted_normalized = self._normalize_content(extracted_content)
        
        # Calculate metrics
        content_similarity = self._evaluate_content_similarity(
            extracted_normalized, ground_truth_normalized
        )
        structure_accuracy = self._evaluate_structure_accuracy(
            extracted_content, ground_truth_content
        )
        formatting_preservation = self._evaluate_formatting_preservation(
            extracted_content, ground_truth_content
        )
        table_quality = self._evaluate_table_quality(
            extracted_content, ground_truth_content
        )
        
        return EvaluationResult(
            extraction_result=extraction_result,
            ground_truth_path=ground_truth_path,
            content_similarity=content_similarity,
            structure_accuracy=structure_accuracy,
            formatting_preservation=formatting_preservation,
            table_quality=table_quality
        )
    
    def _evaluate_content_similarity(self, extracted: str, ground_truth: str) -> ContentSimilarityMetrics:
        """Evaluate content similarity using multiple metrics."""
        # BERTScore
        bert_score = 0.0
        if self.bert_scorer and BERT_SCORE_AVAILABLE:
            try:
                P, R, F1 = self.bert_scorer([extracted], [ground_truth], 
                                           model_type=self.config.bert_score['model'],
                                           batch_size=self.config.bert_score['batch_size'])
                bert_score = float(F1.mean())
            except Exception as e:
                logger.warning(f"BERTScore calculation failed: {e}")
        
        # ROUGE scores
        rouge_scores = {'rouge1': 0.0, 'rouge2': 0.0, 'rougeL': 0.0}
        if self.rouge_scorer and ROUGE_AVAILABLE:
            try:
                scores = self.rouge_scorer.score(ground_truth, extracted)
                rouge_scores = {
                    'rouge1': scores['rouge1'].fmeasure,
                    'rouge2': scores['rouge2'].fmeasure,
                    'rougeL': scores['rougeL'].fmeasure
                }
            except Exception as e:
                logger.warning(f"ROUGE calculation failed: {e}")
        
        # BLEU score (simplified)
        bleu_score = self._calculate_bleu_score(extracted, ground_truth)
        
        # Exact match
        exact_match = 1.0 if extracted.strip() == ground_truth.strip() else 0.0
        
        # Word overlap
        word_overlap = self._calculate_word_overlap(extracted, ground_truth)
        
        return ContentSimilarityMetrics(
            bert_score=bert_score,
            rouge_score=rouge_scores['rouge1'],  # Use ROUGE-1 as primary
            bleu_score=bleu_score,
            exact_match=exact_match,
            word_overlap=word_overlap
        )
    
    def _evaluate_structure_accuracy(self, extracted: str, ground_truth: str) -> StructureAccuracyMetrics:
        """Evaluate structure preservation accuracy."""
        # Extract headers
        extracted_headers = self._extract_headers(extracted)
        ground_truth_headers = self._extract_headers(ground_truth)
        
        # Header accuracy
        header_accuracy = self._calculate_header_accuracy(extracted_headers, ground_truth_headers)
        
        # List accuracy
        list_accuracy = self._calculate_list_accuracy(extracted, ground_truth)
        
        # Section order accuracy
        section_order_accuracy = self._calculate_section_order_accuracy(
            extracted_headers, ground_truth_headers
        )
        
        # Paragraph accuracy
        paragraph_accuracy = self._calculate_paragraph_accuracy(extracted, ground_truth)
        
        return StructureAccuracyMetrics(
            header_accuracy=header_accuracy,
            list_accuracy=list_accuracy,
            section_order_accuracy=section_order_accuracy,
            paragraph_accuracy=paragraph_accuracy
        )
    
    def _evaluate_formatting_preservation(self, extracted: str, ground_truth: str) -> FormattingPreservationMetrics:
        """Evaluate formatting preservation."""
        # Bold accuracy
        bold_accuracy = self._calculate_formatting_accuracy(extracted, ground_truth, r'\*\*(.*?)\*\*')
        
        # Italic accuracy
        italic_accuracy = self._calculate_formatting_accuracy(extracted, ground_truth, r'\*(.*?)\*')
        
        # Link accuracy
        link_accuracy = self._calculate_link_accuracy(extracted, ground_truth)
        
        # Image accuracy
        image_accuracy = self._calculate_image_accuracy(extracted, ground_truth)
        
        return FormattingPreservationMetrics(
            bold_accuracy=bold_accuracy,
            italic_accuracy=italic_accuracy,
            link_accuracy=link_accuracy,
            image_accuracy=image_accuracy
        )
    
    def _evaluate_table_quality(self, extracted: str, ground_truth: str) -> TableQualityMetrics:
        """Evaluate table quality and format consistency."""
        # Detect table format
        extracted_tables = self._extract_tables(extracted)
        ground_truth_tables = self._extract_tables(ground_truth)
        
        # Structure preservation
        structure_preservation = self._calculate_table_structure_preservation(
            extracted_tables, ground_truth_tables
        )
        
        # Content accuracy
        content_accuracy = self._calculate_table_content_accuracy(
            extracted_tables, ground_truth_tables
        )
        
        # Format consistency
        format_consistency = self._calculate_table_format_consistency(extracted_tables)
        
        # Determine table format type
        table_format_type = self._detect_table_format_type(extracted_tables)
        
        return TableQualityMetrics(
            structure_preservation=structure_preservation,
            content_accuracy=content_accuracy,
            format_consistency=format_consistency,
            table_format_type=table_format_type
        )
    
    def _normalize_content(self, content: str) -> str:
        """Normalize content for comparison."""
        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Remove markdown formatting for content comparison
        content = re.sub(r'[#*_`~\[\]()]', '', content)
        
        # Convert to lowercase
        content = content.lower().strip()
        
        return content
    
    def _load_content(self, file_path: str) -> Optional[str]:
        """Load content from file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to load content from {file_path}: {e}")
            return None
    
    def _calculate_bleu_score(self, candidate: str, reference: str) -> float:
        """Calculate simplified BLEU score."""
        def get_ngrams(text, n):
            words = text.split()
            return Counter([' '.join(words[i:i+n]) for i in range(len(words)-n+1)])
        
        candidate_ngrams = get_ngrams(candidate, 1)  # Unigrams
        reference_ngrams = get_ngrams(reference, 1)
        
        if not candidate_ngrams:
            return 0.0
        
        matches = sum(min(candidate_ngrams[ngram], reference_ngrams[ngram]) 
                     for ngram in candidate_ngrams)
        
        return matches / sum(candidate_ngrams.values())
    
    def _calculate_word_overlap(self, text1: str, text2: str) -> float:
        """Calculate word overlap ratio."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _extract_headers(self, content: str) -> List[str]:
        """Extract headers from markdown content."""
        headers = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
        return [header[1].strip() for header in headers]
    
    def _calculate_header_accuracy(self, extracted_headers: List[str], 
                                 ground_truth_headers: List[str]) -> float:
        """Calculate header accuracy."""
        if not ground_truth_headers:
            return 1.0 if not extracted_headers else 0.0
        
        # Calculate precision and recall
        extracted_set = set(extracted_headers)
        ground_truth_set = set(ground_truth_headers)
        
        if not extracted_set:
            return 0.0
        
        precision = len(extracted_set.intersection(ground_truth_set)) / len(extracted_set)
        recall = len(extracted_set.intersection(ground_truth_set)) / len(ground_truth_set)
        
        if precision + recall == 0:
            return 0.0
        
        return 2 * precision * recall / (precision + recall)
    
    def _calculate_list_accuracy(self, extracted: str, ground_truth: str) -> float:
        """Calculate list accuracy."""
        extracted_lists = re.findall(r'^[-*+]\s+.+$', extracted, re.MULTILINE)
        ground_truth_lists = re.findall(r'^[-*+]\s+.+$', ground_truth, re.MULTILINE)
        
        if not ground_truth_lists:
            return 1.0 if not extracted_lists else 0.0
        
        return len(extracted_lists) / len(ground_truth_lists)
    
    def _calculate_section_order_accuracy(self, extracted_headers: List[str], 
                                        ground_truth_headers: List[str]) -> float:
        """Calculate section order accuracy."""
        if len(extracted_headers) < 2 or len(ground_truth_headers) < 2:
            return 1.0
        
        # Simplified order accuracy based on first few headers
        min_len = min(len(extracted_headers), len(ground_truth_headers))
        matches = sum(1 for i in range(min_len) 
                     if extracted_headers[i] == ground_truth_headers[i])
        
        return matches / min_len
    
    def _calculate_paragraph_accuracy(self, extracted: str, ground_truth: str) -> float:
        """Calculate paragraph accuracy."""
        extracted_paragraphs = len(re.findall(r'\n\s*\n', extracted)) + 1
        ground_truth_paragraphs = len(re.findall(r'\n\s*\n', ground_truth)) + 1
        
        if ground_truth_paragraphs == 0:
            return 1.0
        
        return min(extracted_paragraphs / ground_truth_paragraphs, 1.0)
    
    def _calculate_formatting_accuracy(self, extracted: str, ground_truth: str, pattern: str) -> float:
        """Calculate formatting accuracy for a specific pattern."""
        extracted_formats = re.findall(pattern, extracted)
        ground_truth_formats = re.findall(pattern, ground_truth)
        
        if not ground_truth_formats:
            return 1.0 if not extracted_formats else 0.0
        
        return len(extracted_formats) / len(ground_truth_formats)
    
    def _calculate_link_accuracy(self, extracted: str, ground_truth: str) -> float:
        """Calculate link accuracy."""
        extracted_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', extracted)
        ground_truth_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', ground_truth)
        
        if not ground_truth_links:
            return 1.0 if not extracted_links else 0.0
        
        return len(extracted_links) / len(ground_truth_links)
    
    def _calculate_image_accuracy(self, extracted: str, ground_truth: str) -> float:
        """Calculate image accuracy."""
        extracted_images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', extracted)
        ground_truth_images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', ground_truth)
        
        if not ground_truth_images:
            return 1.0 if not extracted_images else 0.0
        
        return len(extracted_images) / len(ground_truth_images)
    
    def _extract_tables(self, content: str) -> List[str]:
        """Extract tables from content."""
        # Extract markdown tables
        markdown_tables = re.findall(r'\|.*\|.*\n\|[\s\-:|]+\|.*\n(\|.*\|.*\n)*', content)
        
        # Extract HTML tables
        html_tables = re.findall(r'<table>.*?</table>', content, re.DOTALL)
        
        return markdown_tables + html_tables
    
    def _calculate_table_structure_preservation(self, extracted_tables: List[str], 
                                              ground_truth_tables: List[str]) -> float:
        """Calculate table structure preservation."""
        if not ground_truth_tables:
            return 1.0 if not extracted_tables else 0.0
        
        return len(extracted_tables) / len(ground_truth_tables)
    
    def _calculate_table_content_accuracy(self, extracted_tables: List[str], 
                                        ground_truth_tables: List[str]) -> float:
        """Calculate table content accuracy."""
        if not ground_truth_tables:
            return 1.0 if not extracted_tables else 0.0
        
        # Simplified content accuracy
        total_cells = sum(len(table.split('|')) for table in ground_truth_tables)
        if total_cells == 0:
            return 1.0
        
        extracted_cells = sum(len(table.split('|')) for table in extracted_tables)
        return min(extracted_cells / total_cells, 1.0)
    
    def _calculate_table_format_consistency(self, tables: List[str]) -> float:
        """Calculate table format consistency."""
        if not tables:
            return 1.0
        
        markdown_count = len([t for t in tables if '|' in t and '---' in t])
        html_count = len([t for t in tables if '<table>' in t])
        
        total = len(tables)
        if total == 0:
            return 1.0
        
        # Consistency score based on dominant format
        max_format = max(markdown_count, html_count)
        return max_format / total
    
    def _detect_table_format_type(self, tables: List[str]) -> str:
        """Detect the primary table format type."""
        if not tables:
            return "none"
        
        markdown_count = len([t for t in tables if '|' in t and '---' in t])
        html_count = len([t for t in tables if '<table>' in t])
        
        if markdown_count > html_count:
            return "markdown"
        elif html_count > markdown_count:
            return "html"
        else:
            return "mixed"
    
    def _create_failed_evaluation(self, extraction_result: ExtractionResult, 
                                ground_truth_path: str) -> EvaluationResult:
        """Create evaluation result for failed extraction."""
        # Create zero metrics
        zero_metrics = ContentSimilarityMetrics(0.0, 0.0, 0.0, 0.0, 0.0)
        zero_structure = StructureAccuracyMetrics(0.0, 0.0, 0.0, 0.0)
        zero_formatting = FormattingPreservationMetrics(0.0, 0.0, 0.0, 0.0)
        zero_table = TableQualityMetrics(0.0, 0.0, 0.0, "none")
        
        return EvaluationResult(
            extraction_result=extraction_result,
            ground_truth_path=ground_truth_path,
            content_similarity=zero_metrics,
            structure_accuracy=zero_structure,
            formatting_preservation=zero_formatting,
            table_quality=zero_table
        )
