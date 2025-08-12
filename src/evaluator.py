"""
Evaluation module for comprehensive document extraction assessment.
Implements Levenshtein-based metrics for evaluating extraction quality.
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
    """Comprehensive document extraction evaluator using Levenshtein-based metrics."""
    
    def __init__(self, fast_mode=False):
        """Initialize evaluator with configuration."""
        self.config = config_manager.get_evaluation_config()
        self.fast_mode = fast_mode
        self.rouge_scorer = None
        
        # Initialize scorers if available (skip in fast mode)
        if not fast_mode and ROUGE_AVAILABLE:
            self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    
    def evaluate_extraction(self, extraction_result: ExtractionResult, 
                          ground_truth_path: str) -> EvaluationResult:
        """Evaluate an extraction result against ground truth using Levenshtein metrics.
        
        Args:
            extraction_result: Result from repository extraction.
            ground_truth_path: Path to ground truth markdown file.
            
        Returns:
            EvaluationResult with comprehensive Levenshtein-based metrics.
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
        
        # Calculate Levenshtein-based metrics
        content_similarity = self._evaluate_content_similarity_levenshtein(
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
        
        # Debug: Print metrics for analysis
        logger.debug(f"Levenshtein similarity - char: {content_similarity.character_similarity:.3f}, word: {content_similarity.word_similarity:.3f}, sentence: {content_similarity.sentence_similarity:.3f}")
        logger.debug(f"Structure accuracy - header: {structure_accuracy.header_accuracy:.3f}, list: {structure_accuracy.list_accuracy:.3f}")
        logger.debug(f"Table quality - content: {table_quality.content_accuracy:.3f}, structure: {table_quality.structure_preservation:.3f}")
        
        return EvaluationResult(
            extraction_result=extraction_result,
            ground_truth_path=ground_truth_path,
            content_similarity=content_similarity,
            structure_accuracy=structure_accuracy,
            formatting_preservation=formatting_preservation,
            table_quality=table_quality
        )
    
    def _evaluate_content_similarity_levenshtein(self, extracted: str, ground_truth: str) -> ContentSimilarityMetrics:
        """Evaluate content similarity using Levenshtein distance at multiple levels."""
        
        # Character-level Levenshtein similarity
        character_similarity = self._calculate_character_levenshtein_similarity(extracted, ground_truth)
        
        # Word-level Levenshtein similarity
        word_similarity = self._calculate_word_levenshtein_similarity(extracted, ground_truth)
        
        # Sentence-level Levenshtein similarity
        sentence_similarity = self._calculate_sentence_levenshtein_similarity(extracted, ground_truth)
        
        # ROUGE scores (kept for comparison) - skip in fast mode
        rouge_scores = {'rouge1': 0.0, 'rouge2': 0.0, 'rougeL': 0.0}
        if not self.fast_mode and self.rouge_scorer and ROUGE_AVAILABLE:
            try:
                # Limit text length to avoid memory issues
                max_length = 10000  # 10k characters
                gt_limited = ground_truth[:max_length] if len(ground_truth) > max_length else ground_truth
                ext_limited = extracted[:max_length] if len(extracted) > max_length else extracted
                
                # Skip if text is too short
                if len(gt_limited.strip()) < 10 or len(ext_limited.strip()) < 10:
                    logger.warning("Text too short for ROUGE calculation")
                else:
                    scores = self.rouge_scorer.score(gt_limited, ext_limited)
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
        
        # Word overlap (F1-score based)
        word_overlap = self._calculate_word_overlap(extracted, ground_truth)
        
        return ContentSimilarityMetrics(
            bert_score=0.0,  # Disabled
            rouge_score=rouge_scores['rouge1'],  # Use ROUGE-1 as reference
            bleu_score=bleu_score,
            exact_match=exact_match,
            word_overlap=word_overlap,
            character_similarity=character_similarity,
            word_similarity=word_similarity,
            sentence_similarity=sentence_similarity
        )
    
    def _calculate_levenshtein_distance(self, str1: str, str2: str) -> int:
        """Calculate Levenshtein distance between two strings."""
        if len(str1) < len(str2):
            return self._calculate_levenshtein_distance(str2, str1)
        
        if len(str2) == 0:
            return len(str1)
        
        previous_row = list(range(len(str2) + 1))
        for i, c1 in enumerate(str1):
            current_row = [i + 1]
            for j, c2 in enumerate(str2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def _calculate_character_levenshtein_similarity(self, extracted: str, ground_truth: str) -> float:
        """Calculate character-level Levenshtein similarity score."""
        if not ground_truth.strip():
            return 1.0 if not extracted.strip() else 0.0
        
        distance = self._calculate_levenshtein_distance(extracted, ground_truth)
        max_length = max(len(extracted), len(ground_truth))
        
        if max_length == 0:
            return 1.0
        
        # Convert distance to similarity score (0-1)
        similarity = 1.0 - (distance / max_length)
        return max(0.0, min(1.0, similarity))
    
    def _calculate_word_levenshtein_similarity(self, extracted: str, ground_truth: str) -> float:
        """Calculate word-level Levenshtein similarity score."""
        # Split into words
        extracted_words = extracted.split()
        ground_truth_words = ground_truth.split()
        
        if not ground_truth_words:
            return 1.0 if not extracted_words else 0.0
        
        # Calculate Levenshtein distance between word sequences
        distance = self._calculate_levenshtein_distance_sequences(extracted_words, ground_truth_words)
        max_length = max(len(extracted_words), len(ground_truth_words))
        
        if max_length == 0:
            return 1.0
        
        # Convert distance to similarity score (0-1)
        similarity = 1.0 - (distance / max_length)
        return max(0.0, min(1.0, similarity))
    
    def _calculate_levenshtein_distance_sequences(self, seq1: List[str], seq2: List[str]) -> int:
        """Calculate Levenshtein distance between two sequences (e.g., word lists)."""
        if len(seq1) < len(seq2):
            return self._calculate_levenshtein_distance_sequences(seq2, seq1)
        
        if len(seq2) == 0:
            return len(seq1)
        
        previous_row = list(range(len(seq2) + 1))
        for i, item1 in enumerate(seq1):
            current_row = [i + 1]
            for j, item2 in enumerate(seq2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (item1 != item2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def _calculate_sentence_levenshtein_similarity(self, extracted: str, ground_truth: str) -> float:
        """Calculate sentence-level Levenshtein similarity score."""
        # Split into sentences (simple approach)
        extracted_sentences = self._split_into_sentences(extracted)
        ground_truth_sentences = self._split_into_sentences(ground_truth)
        
        if not ground_truth_sentences:
            return 1.0 if not extracted_sentences else 0.0
        
        # Calculate Levenshtein distance between sentence sequences
        distance = self._calculate_levenshtein_distance_sequences(extracted_sentences, ground_truth_sentences)
        max_length = max(len(extracted_sentences), len(ground_truth_sentences))
        
        if max_length == 0:
            return 1.0
        
        # Convert distance to similarity score (0-1)
        similarity = 1.0 - (distance / max_length)
        return max(0.0, min(1.0, similarity))
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences using regex."""
        # Simple sentence splitting - can be improved with more sophisticated NLP
        sentences = re.split(r'[.!?]+', text)
        # Clean up sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences
    
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
        
        # Additional quality check for table formatting
        table_quality_score = self._calculate_table_formatting_quality(extracted, ground_truth)
        
        # Determine table format type
        table_format_type = self._detect_table_format_type(extracted_tables)
        
        return TableQualityMetrics(
            structure_preservation=structure_preservation,
            content_accuracy=content_accuracy,
            format_consistency=format_consistency,
            table_format_type=table_format_type
        )
    
    def _calculate_table_formatting_quality(self, extracted: str, ground_truth: str) -> float:
        """Calculate table formatting quality score."""
        # Check for proper table structure
        extracted_has_proper_table = bool(re.search(r'\|.*\|.*\n\|[\s\-:|]+\|', extracted))
        ground_truth_has_proper_table = bool(re.search(r'\|.*\|.*\n\|[\s\-:|]+\|', ground_truth))
        
        # Check for HTML table structure
        extracted_has_html_table = bool(re.search(r'<table>.*?</table>', extracted, re.DOTALL))
        ground_truth_has_html_table = bool(re.search(r'<table>.*?</table>', ground_truth, re.DOTALL))
        
        # Calculate formatting quality
        if ground_truth_has_proper_table and extracted_has_proper_table:
            return 1.0
        elif ground_truth_has_html_table and extracted_has_html_table:
            return 1.0
        elif ground_truth_has_proper_table or ground_truth_has_html_table:
            # Ground truth has table but extracted doesn't
            return 0.0
        else:
            # Neither has proper table structure
            return 0.5
    
    def _normalize_content(self, content: str) -> str:
        """Normalize content for comparison."""
        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Remove HTML tags but keep content
        content = re.sub(r'<[^>]+>', '', content)
        
        # Remove markdown formatting but keep text content
        content = re.sub(r'#{1,6}\s+', '', content)  # Remove headers but keep text
        content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)  # Remove bold but keep text
        content = re.sub(r'\*(.*?)\*', r'\1', content)  # Remove italic but keep text
        content = re.sub(r'`(.*?)`', r'\1', content)  # Remove code but keep text
        content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)  # Remove links but keep text
        content = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', content)  # Remove images but keep alt text
        
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
        """Calculate word overlap ratio using F1-score."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        
        # Calculate precision and recall
        precision = len(intersection) / len(words1) if words1 else 0.0
        recall = len(intersection) / len(words2) if words2 else 0.0
        
        # Calculate F1-score
        if precision + recall == 0:
            return 0.0
        
        return 2 * precision * recall / (precision + recall)
    
    def _extract_headers(self, content: str) -> List[str]:
        """Extract headers from markdown content."""
        # More flexible header detection
        headers = re.findall(r'^(#{1,6})\s*(.+)$', content, re.MULTILINE)
        return [header[1].strip() for header in headers]
    
    def _calculate_header_accuracy(self, extracted_headers: List[str], 
                                 ground_truth_headers: List[str]) -> float:
        """Calculate header accuracy."""
        if not ground_truth_headers:
            return 1.0 if not extracted_headers else 0.0
        
        # Normalize headers for comparison (remove extra spaces, lowercase)
        extracted_normalized = [h.strip().lower() for h in extracted_headers]
        ground_truth_normalized = [h.strip().lower() for h in ground_truth_headers]
        
        # Calculate precision and recall
        extracted_set = set(extracted_normalized)
        ground_truth_set = set(ground_truth_normalized)
        
        if not extracted_set:
            return 0.0
        
        intersection = extracted_set.intersection(ground_truth_set)
        precision = len(intersection) / len(extracted_set)
        recall = len(intersection) / len(ground_truth_set)
        
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
        tables = []
        
        # Extract markdown tables with better regex
        markdown_pattern = r'\|.*\|.*\n\|[\s\-:|]+\|.*\n(\|.*\|.*\n)*'
        markdown_tables = re.findall(markdown_pattern, content, re.MULTILINE)
        tables.extend(markdown_tables)
        
        # Extract HTML tables
        html_tables = re.findall(r'<table>.*?</table>', content, re.DOTALL)
        tables.extend(html_tables)
        
        # Also look for table-like structures with | characters
        lines = content.split('\n')
        table_lines = []
        for line in lines:
            if '|' in line and len(line.split('|')) > 2:
                table_lines.append(line)
        
        if table_lines:
            # Group consecutive table lines
            current_table = []
            for line in table_lines:
                if current_table and not line.strip().startswith('|'):
                    if current_table:
                        tables.append('\n'.join(current_table))
                    current_table = []
                current_table.append(line)
            if current_table:
                tables.append('\n'.join(current_table))
        
        return tables
    
    def _calculate_table_structure_preservation(self, extracted_tables: List[str], 
                                              ground_truth_tables: List[str]) -> float:
        """Calculate table structure preservation."""
        if not ground_truth_tables:
            return 1.0 if not extracted_tables else 0.0
        
        # Calculate structure preservation based on table count ratio
        table_ratio = len(extracted_tables) / len(ground_truth_tables)
        
        # Ensure the ratio is between 0 and 1
        return max(0.0, min(1.0, table_ratio))
    
    def _calculate_table_content_accuracy(self, extracted_tables: List[str], 
                                        ground_truth_tables: List[str]) -> float:
        """Calculate table content accuracy."""
        if not ground_truth_tables:
            return 1.0 if not extracted_tables else 0.0
        
        # Better content accuracy calculation with table structure consideration
        total_accuracy = 0.0
        total_tables = len(ground_truth_tables)
        
        for gt_table in ground_truth_tables:
            best_match_score = 0.0
            
            for ext_table in extracted_tables:
                # Calculate similarity between tables
                gt_content = re.sub(r'[^\w\s]', '', gt_table.lower())
                ext_content = re.sub(r'[^\w\s]', '', ext_table.lower())
                
                if gt_content and ext_content:
                    # Simple text similarity
                    gt_words = set(gt_content.split())
                    ext_words = set(ext_content.split())
                    
                    if gt_words:
                        intersection = gt_words.intersection(ext_words)
                        similarity = len(intersection) / len(gt_words)
                        
                        # Bonus for proper table structure
                        gt_has_structure = '|' in gt_table and '---' in gt_table
                        ext_has_structure = '|' in ext_table and '---' in ext_table
                        
                        if gt_has_structure and ext_has_structure:
                            similarity *= 1.2  # 20% bonus for proper structure
                        elif gt_has_structure and not ext_has_structure:
                            similarity *= 0.5  # 50% penalty for missing structure
                        
                        best_match_score = max(best_match_score, min(similarity, 1.0))
            
            total_accuracy += best_match_score
        
        return total_accuracy / total_tables if total_tables > 0 else 0.0
    
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
        zero_metrics = ContentSimilarityMetrics(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
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
